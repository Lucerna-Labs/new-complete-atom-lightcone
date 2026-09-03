use lightcone_core::{AdmissionPolicy, ConeDirection, WorldPack};
use serde_json::json;
use std::path::PathBuf;

fn main() {
    if let Err(error) = run() {
        eprintln!("lightcone-cli: {error}");
        std::process::exit(1);
    }
}

fn run() -> Result<(), String> {
    let mut args = std::env::args().skip(1);
    let command = args.next().ok_or_else(usage)?;
    match command.as_str() {
        "verify" => {
            let pack_path = required(&mut args, "world-pack path")?;
            no_more(&mut args)?;
            let pack = WorldPack::load(&pack_path).map_err(|error| error.to_string())?;
            println!(
                "{}",
                serde_json::to_string_pretty(&json!({
                    "verified": true,
                    "world_id": pack.manifest.world_id,
                    "version": pack.manifest.version,
                    "manifest_hash": pack.manifest_hash,
                    "nodes": pack.nodes.len(),
                    "edges": pack.edges.len(),
                    "sources": pack.sources.sources.len(),
                    "lexicon_terms": pack.lexicon.len(),
                    "coordinate_dimensions": pack.manifest.coordinate_dimensions,
                    "adapter_independent": pack.manifest.adapter_independent
                }))
                .map_err(|error| error.to_string())?
            );
        }
        "inspect" => {
            let pack_path = required(&mut args, "world-pack path")?;
            no_more(&mut args)?;
            let pack = WorldPack::load(&pack_path).map_err(|error| error.to_string())?;
            println!(
                "{}",
                serde_json::to_string_pretty(&pack.manifest).map_err(|error| error.to_string())?
            );
        }
        "admit" => {
            let pack_path = required(&mut args, "world-pack path")?;
            let query = required(&mut args, "query")?;
            let mut policy = AdmissionPolicy::default();
            while let Some(flag) = args.next() {
                match flag.as_str() {
                    "--hops" => {
                        policy.max_hops = required(&mut args, "hop count")?
                            .parse()
                            .map_err(|_| "--hops requires a non-negative integer".to_string())?;
                    }
                    "--max-nodes" => {
                        policy.max_nodes = required(&mut args, "node limit")?
                            .parse()
                            .map_err(|_| "--max-nodes requires a positive integer".to_string())?;
                    }
                    "--direction" => {
                        policy.direction = match required(&mut args, "direction")?.as_str() {
                            "past" => ConeDirection::CausalPast,
                            "future" => ConeDirection::CausalFuture,
                            "both" => ConeDirection::Both,
                            other => {
                                return Err(format!(
                                    "unknown direction {other:?}; use past, future, or both"
                                ));
                            }
                        };
                    }
                    other => return Err(format!("unknown option {other:?}\n{}", usage())),
                }
            }
            policy.policy_id = format!(
                "cli-{}-h{}-n{}",
                match policy.direction {
                    ConeDirection::CausalPast => "past",
                    ConeDirection::CausalFuture => "future",
                    ConeDirection::Both => "both",
                },
                policy.max_hops,
                policy.max_nodes
            );
            let pack =
                WorldPack::load(PathBuf::from(pack_path)).map_err(|error| error.to_string())?;
            let admission = pack
                .admit(&query, policy)
                .map_err(|error| error.to_string())?;
            println!(
                "{}",
                serde_json::to_string_pretty(&json!({
                    "receipt": admission.receipt,
                    "nodes": admission.nodes,
                    "edges": admission.edges
                }))
                .map_err(|error| error.to_string())?
            );
        }
        "formal" => {
            let encoded = required(&mut args, "formal request JSON")?;
            no_more(&mut args)?;
            let request = serde_json::from_str::<lightcone_formal::Request>(&encoded)
                .map_err(|error| format!("invalid formal request: {error}"))?;
            let receipt = lightcone_formal::execute_checked(&request)
                .map_err(|error| format!("formal execution failed closed: {error}"))?;
            println!(
                "{}",
                serde_json::to_string_pretty(&receipt).map_err(|error| error.to_string())?
            );
        }
        "help" | "--help" | "-h" => println!("{}", usage()),
        other => return Err(format!("unknown command {other:?}\n{}", usage())),
    }
    Ok(())
}

fn required(args: &mut impl Iterator<Item = String>, label: &str) -> Result<String, String> {
    args.next()
        .ok_or_else(|| format!("missing {label}\n{}", usage()))
}

fn no_more(args: &mut impl Iterator<Item = String>) -> Result<(), String> {
    if let Some(extra) = args.next() {
        Err(format!("unexpected argument {extra:?}\n{}", usage()))
    } else {
        Ok(())
    }
}

fn usage() -> String {
    "usage:\n  lightcone-cli verify <world-pack>\n  lightcone-cli inspect <world-pack>\n  lightcone-cli admit <world-pack> <query> [--hops N] [--max-nodes N] [--direction past|future|both]\n  lightcone-cli formal '<request-json>'".into()
}
