use lightcone_core::{AdmissionPolicy, ConeDirection, PackError, WorldPack};
use serde_json::json;
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

static NONCE: AtomicU64 = AtomicU64::new(0);

struct Fixture {
    root: PathBuf,
}

impl Fixture {
    fn create() -> Self {
        let nonce = NONCE.fetch_add(1, Ordering::Relaxed);
        let root =
            std::env::temp_dir().join(format!("new-lightcone-test-{}-{nonce}", std::process::id()));
        fs::create_dir_all(&root).expect("create fixture root");

        let sources = json!({
            "schema_version": 1,
            "sources": [{
                "source_id": "source.physics",
                "title": "Fixture mechanics source",
                "locator": "fixture://physics",
                "publisher": "fixture",
                "version": "1",
                "retrieved_at": "2026-09-03",
                "rights": "green",
                "trust_role": "test"
            }]
        });
        write_json(root.join("sources.json"), &sources);

        let nodes = [
            json!({
                "schema_version": 1, "node_id": "mechanics.fall", "domain_id": "physics",
                "subject_id": "physics.classical-mechanics", "lanes": ["reasoning.causal"],
                "label": "falling object", "statement": "A released object accelerates under the modeled gravitational field.",
                "aliases": ["falling body"], "epistemic_class": "established", "source_ids": ["source.physics"],
                "scope": "fixture mechanics", "limitations": [], "as_of": null, "version_boundary": "fixture-v1"
            }),
            json!({
                "schema_version": 1, "node_id": "mechanics.acceleration", "domain_id": "physics",
                "subject_id": "physics.classical-mechanics", "lanes": ["reasoning.causal"],
                "label": "acceleration", "statement": "Net force changes velocity according to the model.",
                "aliases": [], "epistemic_class": "formal", "source_ids": ["source.physics"],
                "scope": "fixture mechanics", "limitations": [], "as_of": null, "version_boundary": "fixture-v1"
            }),
            json!({
                "schema_version": 1, "node_id": "mechanics.impact", "domain_id": "physics",
                "subject_id": "physics.classical-mechanics", "lanes": ["reasoning.causal"],
                "label": "impact", "statement": "Contact changes the motion boundary conditions.",
                "aliases": [], "epistemic_class": "established", "source_ids": ["source.physics"],
                "scope": "fixture mechanics", "limitations": [], "as_of": null, "version_boundary": "fixture-v1"
            }),
            json!({
                "schema_version": 1, "node_id": "optics.refraction", "domain_id": "physics",
                "subject_id": "physics.optics", "lanes": ["reasoning.causal"],
                "label": "refraction", "statement": "A wave changes direction across media under the fixture law.",
                "aliases": [], "epistemic_class": "established", "source_ids": ["source.physics"],
                "scope": "fixture optics", "limitations": [], "as_of": null, "version_boundary": "fixture-v1"
            }),
        ];
        write_jsonl(root.join("nodes.jsonl"), &nodes);

        let edges = [
            json!({
                "schema_version": 1, "edge_id": "edge.fall-acceleration", "source_node": "mechanics.fall",
                "target_node": "mechanics.acceleration", "kind": "causes", "polarity": 1,
                "direction": "forward", "conditions": ["object is released"], "exceptions": [],
                "source_ids": ["source.physics"]
            }),
            json!({
                "schema_version": 1, "edge_id": "edge.acceleration-impact", "source_node": "mechanics.acceleration",
                "target_node": "mechanics.impact", "kind": "enables", "polarity": 1,
                "direction": "forward", "conditions": ["a surface intersects the trajectory"], "exceptions": [],
                "source_ids": ["source.physics"]
            }),
        ];
        write_jsonl(root.join("edges.jsonl"), &edges);
        write_json(
            root.join("lexicon.json"),
            &json!({
                "schema_version": 1,
                "entries": {
                    "acceleration": ["mechanics.acceleration"],
                    "falling body": ["mechanics.fall"],
                    "falling object": ["mechanics.fall"],
                    "impact": ["mechanics.impact"],
                    "refraction": ["optics.refraction"]
                }
            }),
        );
        write_json(
            root.join("receipts-training.json"),
            &json!({"fixture": true}),
        );
        write_json(
            root.join("receipts-validation.json"),
            &json!({"fixture": true, "passed": true}),
        );

        let names = [
            "nodes.jsonl",
            "edges.jsonl",
            "sources.json",
            "lexicon.json",
            "receipts-training.json",
            "receipts-validation.json",
        ];
        let files = names
            .into_iter()
            .map(|name| (name.to_string(), hash_file(&root.join(name))))
            .collect::<BTreeMap<_, _>>();
        write_json(
            root.join("manifest.json"),
            &json!({
                "schema_version": 1,
                "world_id": "fixture-mechanics",
                "version": "1.0.0",
                "created_at": "2026-09-03T00:00:00Z",
                "adapter_independent": true,
                "ontology_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "domains": ["physics"],
                "lanes": ["reasoning.causal"],
                "node_count": 4,
                "edge_count": 2,
                "coordinate_dimensions": null,
                "files": files,
                "training_receipt": "receipts-training.json",
                "validation_receipts": ["receipts-validation.json"],
                "limitations": ["test fixture"]
            }),
        );
        Self { root }
    }
}

impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}

#[test]
fn verifies_every_hash_before_loading() {
    let fixture = Fixture::create();
    fs::write(fixture.root.join("lexicon.json"), "{}\n").expect("tamper fixture");
    let error = WorldPack::load(&fixture.root).expect_err("tampering must fail");
    assert!(matches!(error, PackError::HashMismatch { .. }));
}

#[test]
fn admits_exact_future_cone_without_unrelated_nodes() {
    let fixture = Fixture::create();
    let pack = WorldPack::load(&fixture.root).expect("valid pack");
    let policy = AdmissionPolicy {
        policy_id: "future-two".into(),
        max_hops: 2,
        max_nodes: 16,
        direction: ConeDirection::CausalFuture,
        allowed_relations: Default::default(),
    };
    let admission = pack
        .admit("Explain a falling object", policy)
        .expect("admission");
    assert_eq!(
        admission.receipt.admitted_nodes,
        [
            "mechanics.acceleration",
            "mechanics.fall",
            "mechanics.impact"
        ]
    );
    assert!(
        !admission
            .receipt
            .admitted_nodes
            .contains(&"optics.refraction".to_string())
    );
    assert_eq!(admission.receipt.traversed_edges.len(), 2);
    assert!(admission.receipt.passive);
    assert!(!admission.receipt.holds_verdict);
}

#[test]
fn direction_and_hop_limit_are_exact() {
    let fixture = Fixture::create();
    let pack = WorldPack::load(&fixture.root).expect("valid pack");
    let admission = pack
        .admit(
            "impact",
            AdmissionPolicy {
                policy_id: "past-one".into(),
                max_hops: 1,
                max_nodes: 16,
                direction: ConeDirection::CausalPast,
                allowed_relations: Default::default(),
            },
        )
        .expect("admission");
    assert_eq!(
        admission.receipt.admitted_nodes,
        ["mechanics.acceleration", "mechanics.impact"]
    );
}

#[test]
fn unknown_query_is_empty_and_deterministic() {
    let fixture = Fixture::create();
    let pack = WorldPack::load(&fixture.root).expect("valid pack");
    let first = pack
        .admit("unrepresented subject", AdmissionPolicy::default())
        .expect("first");
    let second = pack
        .admit("unrepresented subject", AdmissionPolicy::default())
        .expect("second");
    assert!(first.nodes.is_empty());
    assert!(first.edges.is_empty());
    assert_eq!(first.receipt, second.receipt);
}

#[test]
fn bounded_cone_reports_truncation() {
    let fixture = Fixture::create();
    let pack = WorldPack::load(&fixture.root).expect("valid pack");
    let admission = pack
        .admit(
            "falling object",
            AdmissionPolicy {
                policy_id: "bounded".into(),
                max_hops: 2,
                max_nodes: 2,
                direction: ConeDirection::CausalFuture,
                allowed_relations: Default::default(),
            },
        )
        .expect("admission");
    assert!(admission.receipt.truncated);
    assert_eq!(admission.receipt.excluded_frontier_count, 1);
    assert_eq!(admission.receipt.admitted_nodes.len(), 2);
}

fn write_json(path: PathBuf, value: &serde_json::Value) {
    fs::write(path, serde_json::to_vec_pretty(value).expect("serialize")).expect("write JSON");
}

fn write_jsonl(path: PathBuf, values: &[serde_json::Value]) {
    let mut text = values
        .iter()
        .map(|value| serde_json::to_string(value).expect("serialize row"))
        .collect::<Vec<_>>()
        .join("\n");
    text.push('\n');
    fs::write(path, text).expect("write JSONL");
}

fn hash_file(path: &Path) -> String {
    format!(
        "{:x}",
        Sha256::digest(fs::read(path).expect("read for hash"))
    )
}
