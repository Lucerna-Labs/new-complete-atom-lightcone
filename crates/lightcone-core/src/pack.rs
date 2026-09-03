use crate::model::{
    Coordinates, EdgeDirection, Lexicon, SourceRegistry, WorldEdge, WorldManifest, WorldNode,
};
use crate::normalize::normalize_text;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Component, Path, PathBuf};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PackError {
    #[error("cannot read {path}: {source}")]
    Read {
        path: PathBuf,
        source: std::io::Error,
    },
    #[error("invalid JSON in {path}: {source}")]
    Json {
        path: PathBuf,
        source: serde_json::Error,
    },
    #[error("invalid world pack: {0}")]
    Invalid(String),
    #[error("hash mismatch for {path}: expected {expected}, observed {observed}")]
    HashMismatch {
        path: String,
        expected: String,
        observed: String,
    },
}

#[derive(Clone, Debug)]
pub struct WorldPack {
    pub root: PathBuf,
    pub manifest: WorldManifest,
    pub manifest_hash: String,
    pub nodes: BTreeMap<String, WorldNode>,
    pub edges: BTreeMap<String, WorldEdge>,
    pub sources: SourceRegistry,
    pub lexicon: BTreeMap<String, Vec<String>>,
    pub coordinates: Option<Coordinates>,
    pub(crate) outgoing: BTreeMap<String, Vec<String>>,
    pub(crate) incoming: BTreeMap<String, Vec<String>>,
}

impl WorldPack {
    pub fn load(root: impl AsRef<Path>) -> Result<Self, PackError> {
        let root = root.as_ref().to_path_buf();
        let manifest_path = root.join("manifest.json");
        let manifest_bytes = read_bytes(&manifest_path)?;
        let manifest_hash = sha256(&manifest_bytes);
        let manifest: WorldManifest = parse_json(&manifest_path, &manifest_bytes)?;
        validate_manifest(&manifest)?;

        for (relative, expected) in &manifest.files {
            let path = safe_join(&root, relative)?;
            let observed = sha256(&read_bytes(&path)?);
            if observed != *expected {
                return Err(PackError::HashMismatch {
                    path: relative.clone(),
                    expected: expected.clone(),
                    observed,
                });
            }
        }
        for required in ["nodes.jsonl", "edges.jsonl", "sources.json", "lexicon.json"] {
            if !manifest.files.contains_key(required) {
                return Err(PackError::Invalid(format!(
                    "manifest does not hash required file {required}"
                )));
            }
        }
        if !manifest.files.contains_key(&manifest.training_receipt) {
            return Err(PackError::Invalid(
                "training receipt is not hash-bound by the manifest".into(),
            ));
        }
        for receipt in &manifest.validation_receipts {
            if !manifest.files.contains_key(receipt) {
                return Err(PackError::Invalid(format!(
                    "validation receipt {receipt} is not hash-bound by the manifest"
                )));
            }
        }

        let nodes = parse_jsonl::<WorldNode, _>(&root.join("nodes.jsonl"), "node_id", |node| {
            &node.node_id
        })?;
        let edges = parse_jsonl::<WorldEdge, _>(&root.join("edges.jsonl"), "edge_id", |edge| {
            &edge.edge_id
        })?;
        let sources: SourceRegistry = parse_file(&root.join("sources.json"))?;
        let lexicon: Lexicon = parse_file(&root.join("lexicon.json"))?;
        let coordinates = if manifest.files.contains_key("coordinates.json") {
            Some(parse_file::<Coordinates>(&root.join("coordinates.json"))?)
        } else {
            None
        };
        validate_contents(
            &manifest,
            &nodes,
            &edges,
            &sources,
            &lexicon,
            coordinates.as_ref(),
        )?;

        let mut outgoing: BTreeMap<String, Vec<String>> = BTreeMap::new();
        let mut incoming: BTreeMap<String, Vec<String>> = BTreeMap::new();
        for edge in edges.values() {
            outgoing
                .entry(edge.source_node.clone())
                .or_default()
                .push(edge.edge_id.clone());
            incoming
                .entry(edge.target_node.clone())
                .or_default()
                .push(edge.edge_id.clone());
            if edge.direction == EdgeDirection::Bidirectional {
                outgoing
                    .entry(edge.target_node.clone())
                    .or_default()
                    .push(edge.edge_id.clone());
                incoming
                    .entry(edge.source_node.clone())
                    .or_default()
                    .push(edge.edge_id.clone());
            }
        }
        for ids in outgoing.values_mut().chain(incoming.values_mut()) {
            ids.sort();
            ids.dedup();
        }

        Ok(Self {
            root,
            manifest,
            manifest_hash,
            nodes,
            edges,
            sources,
            lexicon: lexicon.entries,
            coordinates,
            outgoing,
            incoming,
        })
    }
}

fn validate_manifest(manifest: &WorldManifest) -> Result<(), PackError> {
    if manifest.schema_version != 1 {
        return Err(PackError::Invalid(format!(
            "unsupported manifest schema {}",
            manifest.schema_version
        )));
    }
    if !manifest.adapter_independent {
        return Err(PackError::Invalid("world pack is model-specific".into()));
    }
    if manifest.world_id.trim().is_empty() || manifest.version.trim().is_empty() {
        return Err(PackError::Invalid(
            "world_id and version must be non-empty".into(),
        ));
    }
    if manifest.domains.is_empty() || manifest.lanes.is_empty() {
        return Err(PackError::Invalid(
            "world pack must declare domains and lanes".into(),
        ));
    }
    if manifest.validation_receipts.is_empty() {
        return Err(PackError::Invalid(
            "world pack has no validation receipt".into(),
        ));
    }
    for (path, digest) in &manifest.files {
        validate_relative(path)?;
        if digest.len() != 64
            || !digest
                .bytes()
                .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        {
            return Err(PackError::Invalid(format!("invalid SHA-256 for {path}")));
        }
    }
    Ok(())
}

fn validate_contents(
    manifest: &WorldManifest,
    nodes: &BTreeMap<String, WorldNode>,
    edges: &BTreeMap<String, WorldEdge>,
    sources: &SourceRegistry,
    lexicon: &Lexicon,
    coordinates: Option<&Coordinates>,
) -> Result<(), PackError> {
    if nodes.len() != manifest.node_count || edges.len() != manifest.edge_count {
        return Err(PackError::Invalid(format!(
            "manifest counts differ: nodes {} != {}, edges {} != {}",
            manifest.node_count,
            nodes.len(),
            manifest.edge_count,
            edges.len()
        )));
    }
    if nodes.is_empty() {
        return Err(PackError::Invalid("world pack contains no nodes".into()));
    }
    let source_ids = sources
        .sources
        .iter()
        .map(|source| source.source_id.as_str())
        .collect::<BTreeSet<_>>();
    if source_ids.len() != sources.sources.len() {
        return Err(PackError::Invalid(
            "source registry contains duplicate IDs".into(),
        ));
    }
    for node in nodes.values() {
        if node.schema_version != 1 {
            return Err(PackError::Invalid(format!(
                "node {} has unsupported schema",
                node.node_id
            )));
        }
        if !manifest.domains.contains(&node.domain_id) {
            return Err(PackError::Invalid(format!(
                "node {} uses undeclared domain {}",
                node.node_id, node.domain_id
            )));
        }
        if node.lanes.is_empty() || node.lanes.iter().any(|lane| !manifest.lanes.contains(lane)) {
            return Err(PackError::Invalid(format!(
                "node {} uses an empty or undeclared lane set",
                node.node_id
            )));
        }
        if node
            .source_ids
            .iter()
            .any(|source| !source_ids.contains(source.as_str()))
        {
            return Err(PackError::Invalid(format!(
                "node {} references an unknown source",
                node.node_id
            )));
        }
        if node.epistemic_class != crate::model::EpistemicClass::SyntheticControl
            && node.source_ids.is_empty()
        {
            return Err(PackError::Invalid(format!(
                "non-synthetic node {} has no evidence",
                node.node_id
            )));
        }
    }
    for edge in edges.values() {
        if edge.schema_version != 1 || !(-1..=1).contains(&edge.polarity) {
            return Err(PackError::Invalid(format!(
                "edge {} has an invalid schema or polarity",
                edge.edge_id
            )));
        }
        if !nodes.contains_key(&edge.source_node) || !nodes.contains_key(&edge.target_node) {
            return Err(PackError::Invalid(format!(
                "edge {} references an unknown node",
                edge.edge_id
            )));
        }
        if edge.source_ids.is_empty()
            || edge
                .source_ids
                .iter()
                .any(|source| !source_ids.contains(source.as_str()))
        {
            return Err(PackError::Invalid(format!(
                "edge {} has missing or unknown evidence",
                edge.edge_id
            )));
        }
    }
    for (raw_term, node_ids) in &lexicon.entries {
        if normalize_text(raw_term) != *raw_term || raw_term.is_empty() {
            return Err(PackError::Invalid(format!(
                "lexicon term is not canonical: {raw_term:?}"
            )));
        }
        if node_ids.is_empty() || node_ids.iter().any(|node| !nodes.contains_key(node)) {
            return Err(PackError::Invalid(format!(
                "lexicon term {raw_term:?} has no valid targets"
            )));
        }
    }
    if let Some(coordinates) = coordinates {
        if coordinates.schema_version != 1
            || Some(coordinates.dimensions) != manifest.coordinate_dimensions
        {
            return Err(PackError::Invalid(
                "coordinate metadata differs from manifest".into(),
            ));
        }
        let vector_ids = coordinates
            .vectors
            .iter()
            .map(|vector| vector.node_id.as_str())
            .collect::<BTreeSet<_>>();
        if vector_ids.len() != nodes.len()
            || !nodes.keys().all(|node| vector_ids.contains(node.as_str()))
        {
            return Err(PackError::Invalid(
                "coordinates do not cover every node exactly once".into(),
            ));
        }
        for vector in &coordinates.vectors {
            if vector.values.len() != coordinates.dimensions
                || vector.values.iter().any(|value| !value.is_finite())
            {
                return Err(PackError::Invalid(format!(
                    "node {} has an invalid coordinate vector",
                    vector.node_id
                )));
            }
        }
    } else if manifest.coordinate_dimensions.is_some() {
        return Err(PackError::Invalid(
            "manifest declares coordinates but coordinates.json is absent".into(),
        ));
    }
    Ok(())
}

fn parse_jsonl<T, F>(path: &Path, label: &str, id_of: F) -> Result<BTreeMap<String, T>, PackError>
where
    T: serde::de::DeserializeOwned,
    F: Fn(&T) -> &str,
{
    let text = String::from_utf8(read_bytes(path)?)
        .map_err(|_| PackError::Invalid(format!("{} is not UTF-8", path.display())))?;
    let mut output = BTreeMap::new();
    for (line_index, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        let value: T = serde_json::from_str(line).map_err(|source| PackError::Json {
            path: path.to_path_buf(),
            source,
        })?;
        let id = id_of(&value).to_string();
        if id.is_empty() || output.insert(id.clone(), value).is_some() {
            return Err(PackError::Invalid(format!(
                "duplicate or empty {label} {id:?} at line {}",
                line_index + 1
            )));
        }
    }
    Ok(output)
}

fn parse_file<T: serde::de::DeserializeOwned>(path: &Path) -> Result<T, PackError> {
    let bytes = read_bytes(path)?;
    parse_json(path, &bytes)
}

fn parse_json<T: serde::de::DeserializeOwned>(path: &Path, bytes: &[u8]) -> Result<T, PackError> {
    serde_json::from_slice(bytes).map_err(|source| PackError::Json {
        path: path.to_path_buf(),
        source,
    })
}

fn read_bytes(path: &Path) -> Result<Vec<u8>, PackError> {
    fs::read(path).map_err(|source| PackError::Read {
        path: path.to_path_buf(),
        source,
    })
}

fn validate_relative(relative: &str) -> Result<(), PackError> {
    let path = Path::new(relative);
    if path.is_absolute()
        || path
            .components()
            .any(|part| !matches!(part, Component::Normal(_)))
    {
        return Err(PackError::Invalid(format!(
            "manifest path is not a safe relative path: {relative}"
        )));
    }
    Ok(())
}

fn safe_join(root: &Path, relative: &str) -> Result<PathBuf, PackError> {
    validate_relative(relative)?;
    Ok(root.join(relative))
}

pub(crate) fn sha256(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
