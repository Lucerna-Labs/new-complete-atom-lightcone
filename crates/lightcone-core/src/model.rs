use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct WorldManifest {
    pub schema_version: u32,
    pub world_id: String,
    pub version: String,
    pub created_at: String,
    pub adapter_independent: bool,
    pub ontology_hash: String,
    pub domains: Vec<String>,
    pub lanes: Vec<String>,
    pub node_count: usize,
    pub edge_count: usize,
    pub coordinate_dimensions: Option<usize>,
    pub files: BTreeMap<String, String>,
    pub training_receipt: String,
    pub validation_receipts: Vec<String>,
    #[serde(default)]
    pub limitations: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum EpistemicClass {
    Formal,
    Established,
    Provisional,
    Hypothesis,
    Contested,
    Interpretive,
    Creative,
    SyntheticControl,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct WorldNode {
    pub schema_version: u32,
    pub node_id: String,
    pub domain_id: String,
    pub subject_id: String,
    pub lanes: Vec<String>,
    pub label: String,
    pub statement: String,
    #[serde(default)]
    pub aliases: Vec<String>,
    pub epistemic_class: EpistemicClass,
    #[serde(default)]
    pub source_ids: Vec<String>,
    #[serde(default)]
    pub scope: String,
    #[serde(default)]
    pub limitations: Vec<String>,
    pub as_of: Option<String>,
    pub version_boundary: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum RelationKind {
    Causes,
    Enables,
    Supports,
    Grounds,
    Clarifies,
    Qualifies,
    Inhibits,
    Prevents,
    Contradicts,
    Undercuts,
    Counterexample,
    Prerequisite,
    PartOf,
    TransformsTo,
    AnalogousTo,
    Predicts,
    Measures,
    Implements,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum EdgeDirection {
    Forward,
    Bidirectional,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct WorldEdge {
    pub schema_version: u32,
    pub edge_id: String,
    pub source_node: String,
    pub target_node: String,
    pub kind: RelationKind,
    pub polarity: i8,
    pub direction: EdgeDirection,
    #[serde(default)]
    pub conditions: Vec<String>,
    #[serde(default)]
    pub exceptions: Vec<String>,
    #[serde(default)]
    pub source_ids: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct SourceRegistry {
    pub schema_version: u32,
    pub sources: Vec<SourceRecord>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct SourceRecord {
    pub source_id: String,
    pub title: String,
    pub locator: String,
    pub publisher: String,
    pub version: Option<String>,
    pub retrieved_at: String,
    pub rights: String,
    pub trust_role: String,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Lexicon {
    pub schema_version: u32,
    pub entries: BTreeMap<String, Vec<String>>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Coordinates {
    pub schema_version: u32,
    pub dimensions: usize,
    pub vectors: Vec<NodeVector>,
}

#[derive(Clone, Debug, Deserialize, Serialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct NodeVector {
    pub node_id: String,
    pub values: Vec<f32>,
}
