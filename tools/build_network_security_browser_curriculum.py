#!/usr/bin/env python3
"""Author networking, cybersecurity, and browser-platform causal foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "network-security-browser" / "foundations.jsonl"
WORLD = "network-security-browser-v0"

NETWORK_LANES = ["reasoning.causal", "geometry.structural", "thinking.bottom_up", "reasoning.probabilistic"]
SECURITY_LANES = ["reasoning.causal", "reasoning.counterfactual", "reasoning.probabilistic", "thinking.bottom_up"]
BROWSER_LANES = ["thinking.bottom_up", "reasoning.causal", "geometry.structural"]

NETWORK_SOURCES = ["rfc8200", "rfc9293", "rfc9110", "rfc9000", "rfc9499"]
SECURITY_SOURCES = [
    "nist-csf-2", "nist-sp800-218", "nist-sp800-207", "nist-sp800-61r3",
    "owasp-asvs-500", "rfc8446",
]
BROWSER_SOURCES = ["whatwg-html", "whatwg-dom", "whatwg-fetch", "rfc9110", "w3c-wcag-22"]


NETWORK = [
    ("root", "Computer-network causal stack", "A computer network transports encoded information across bounded links and nodes through layered addressing, forwarding, reliability, naming, application semantics, measurement, and congestion mechanisms.", "networking.physical-link"),
    ("signal", "Physical signal", "A physical signal varies an electromagnetic or optical property over time to carry symbols through a medium with finite bandwidth, noise, attenuation, and delay.", "networking.physical-link"),
    ("bit-symbol", "Bits and symbols", "A symbol is a transmitted signal choice that may encode one or more bits; bit rate and symbol rate are related by the modulation and coding scheme.", "networking.physical-link"),
    ("encoding", "Line and channel encoding", "Encoding maps data into transmittable symbols while trading bandwidth, clock recovery, error behavior, and implementation complexity.", "networking.physical-link"),
    ("frame", "Link-layer frame", "A frame delimits link-local data and control fields so neighboring interfaces can identify, validate, and dispatch a transmission.", "networking.physical-link"),
    ("mac-address", "Link-layer address", "A link-layer address identifies an interface within a link technology's delivery scope and is not a globally routable host identity.", "networking.physical-link"),
    ("ethernet-switch", "Ethernet switching", "An Ethernet switch learns source-address locations and forwards frames by destination-address entries while flooding when the destination location is unknown.", "networking.physical-link"),
    ("broadcast-domain", "Broadcast domain", "A broadcast domain is the link scope over which broadcast or equivalent discovery traffic is propagated before a router boundary.", "networking.physical-link"),
    ("vlan", "Virtual LAN", "A VLAN partitions one physical switching fabric into logical broadcast domains whose tags and port configuration must agree across trunks and access edges.", "networking.physical-link"),
    ("mtu", "Maximum transmission unit", "An MTU bounds the network-layer payload a link can carry in one frame and therefore constrains packet size along an end-to-end path.", "networking.physical-link"),
    ("link-error", "Link error detection", "A link checksum or frame check sequence detects many transmission corruptions but does not by itself authenticate the sender or repair loss.", "networking.physical-link"),
    ("neighbor-discovery", "Neighbor discovery", "Neighbor discovery resolves a network-layer next hop to link-layer delivery information and maintains reachability state within a local link.", "networking.physical-link"),
    ("packet", "IP packet", "An IP packet carries a network-layer header and payload across multiple links while routers make hop-local forwarding decisions.", "networking.ip-routing"),
    ("ipv6-address", "IPv6 address", "An IPv6 address is a 128-bit identifier whose prefix and interface-related portions are interpreted by configured routing and addressing rules.", "networking.ip-routing"),
    ("prefix", "Network prefix", "A network prefix represents the leading address bits shared by a set of destinations and is paired with a prefix length.", "networking.ip-routing"),
    ("subnet", "IP subnet", "A subnet is an on-link address prefix under a declared configuration; address similarity alone does not prove direct reachability.", "networking.ip-routing"),
    ("route", "Route", "A route maps a destination prefix to a next hop or local disposition together with attributes used to choose among alternatives.", "networking.ip-routing"),
    ("forwarding-table", "Forwarding table", "A forwarding table is the data-plane structure used to select an action for each packet from destination and policy inputs.", "networking.ip-routing"),
    ("longest-prefix", "Longest-prefix match", "Longest-prefix match selects the matching route with the greatest prefix length before lower-priority tie breakers.", "networking.ip-routing"),
    ("hop-limit", "Hop limit", "A hop limit is decremented by forwarding nodes and discards a packet at zero to bound persistent routing loops.", "networking.ip-routing"),
    ("path-mtu", "Path MTU", "Path MTU is the smallest supported packet size across the selected path and can change when routing changes.", "networking.ip-routing"),
    ("icmp", "Internet Control Message Protocol", "ICMP carries network-layer errors and diagnostics tied to packet processing; filtering all ICMP can break discovery and troubleshooting mechanisms.", "networking.ip-routing"),
    ("nat", "Network address translation", "NAT rewrites address or port bindings across a boundary, creating state and coupling that can disrupt end-to-end identity and inbound reachability.", "networking.ip-routing"),
    ("control-plane", "Routing control plane", "The control plane exchanges or computes reachability information and installs selected routes into the forwarding plane.", "networking.ip-routing"),
    ("routing-loop", "Routing loop", "A routing loop occurs when successive forwarding decisions return traffic to an earlier node, consuming hop budget and capacity.", "networking.ip-routing"),
    ("port", "Transport port", "A transport port identifies an endpoint context within a host so multiple application flows can share network addresses.", "networking.transport"),
    ("socket", "Network socket", "A socket is an operating-system endpoint abstraction bound to protocol, addresses, ports, and lifecycle state.", "networking.transport"),
    ("udp", "UDP datagram", "UDP provides message-oriented multiplexing and checksum protection without promising delivery, order, duplicate suppression, congestion response, or connection state.", "networking.transport"),
    ("tcp-connection", "TCP connection", "A TCP connection is identified by endpoint addresses and ports and maintains synchronized state for a reliable ordered byte stream.", "networking.transport"),
    ("tcp-sequence", "TCP sequence space", "TCP sequence numbers locate bytes in a modulo sequence space so receivers can order data and identify missing or duplicate ranges.", "networking.transport"),
    ("tcp-ack", "TCP acknowledgment", "A TCP acknowledgment communicates received sequence progress and supports loss inference, retransmission, and congestion control.", "networking.transport"),
    ("retransmission", "Retransmission", "Retransmission resends data inferred lost from timers or acknowledgment patterns while avoiding unchecked duplication of application effects.", "networking.transport"),
    ("flow-control", "Flow control", "Flow control prevents a sender from overrunning receiver buffer capacity by advertising an allowable receive window or credit.", "networking.transport"),
    ("congestion-control", "Congestion control", "Congestion control adapts offered load to inferred path capacity so competing flows do not drive queues and loss into collapse.", "networking.transport"),
    ("tcp-handshake", "TCP handshake", "The TCP handshake synchronizes initial sequence state and confirms bidirectional reachability before ordinary data transfer.", "networking.transport"),
    ("tcp-close", "TCP close lifecycle", "TCP close coordinates independent byte-stream directions and retains state long enough to disambiguate delayed segments from later connections.", "networking.transport"),
    ("quic-connection", "QUIC connection", "A QUIC connection carries authenticated packets over UDP, integrates TLS negotiation, and exposes flow-controlled application streams.", "networking.transport"),
    ("quic-stream", "QUIC stream", "A QUIC stream is an ordered byte sequence within a connection whose loss recovery and flow control need not block independent streams.", "networking.transport"),
    ("path-migration", "QUIC path migration", "Connection identifiers allow a QUIC connection to validate and move to a changed network path without equating identity with one address tuple.", "networking.transport"),
    ("dns-name", "Domain name", "A domain name is an ordered sequence of labels interpreted within the DNS namespace, with the root at the rightmost end of the fully qualified form.", "networking.dns"),
    ("dns-zone", "DNS zone", "A DNS zone is an administratively served portion of the namespace bounded by delegation rather than every descendant name string.", "networking.dns"),
    ("dns-delegation", "DNS delegation", "A delegation assigns authority for a child zone through parent records and glue where necessary for resolution.", "networking.dns"),
    ("dns-authoritative", "Authoritative DNS server", "An authoritative server answers from zone data for which it is authoritative rather than resolving arbitrary names on a client's behalf.", "networking.dns"),
    ("dns-recursive", "Recursive resolver", "A recursive resolver pursues referrals or consults caches to answer a client's question and becomes a trust and privacy boundary.", "networking.dns"),
    ("dns-cache", "DNS cache", "A DNS cache reuses a prior answer until its validity interval expires, reducing latency and load while permitting temporarily stale views.", "networking.dns"),
    ("dns-ttl", "DNS time to live", "A DNS TTL bounds how long a resolver may reuse cached data and trades update convergence against query load and latency.", "networking.dns"),
    ("dns-alias", "DNS alias", "An alias record redirects one owner name toward another canonical name and can add dependencies, lookup steps, and loop risks.", "networking.dns"),
    ("dns-negative", "Negative DNS caching", "Negative caching stores authenticated or authoritative evidence that a name or type is absent for a bounded interval.", "networking.dns"),
    ("dnssec", "DNSSEC", "DNSSEC authenticates DNS data origin and integrity through a chain of signed records; it does not encrypt queries or guarantee endpoint safety.", "networking.dns"),
    ("http-resource", "HTTP resource", "An HTTP resource is the conceptual target identified by a URI; a transferred representation is not identical to the resource itself.", "networking.http"),
    ("http-request", "HTTP request", "An HTTP request communicates a method, target, fields, and optional content whose semantics are interpreted by the recipient role.", "networking.http"),
    ("http-response", "HTTP response", "An HTTP response communicates status, fields, and optional content corresponding to a request or protocol event.", "networking.http"),
    ("http-method", "HTTP method", "An HTTP method defines request intent and properties such as safety, idempotency, and cache interaction independently of URL naming conventions.", "networking.http"),
    ("http-safe", "Safe HTTP method", "A safe method requests read-only semantics from the client perspective even though servers may perform incidental logging or accounting.", "networking.http"),
    ("http-idempotent", "Idempotent HTTP method", "An idempotent method has the same intended server effect when repeated, although each response or incidental effect can differ.", "networking.http"),
    ("http-status", "HTTP status code", "An HTTP status code reports the response class and request outcome at the protocol interface, not every downstream business consequence.", "networking.http"),
    ("http-field", "HTTP field", "An HTTP field carries extensible metadata whose meaning depends on field definition, message context, and intermediary behavior.", "networking.http"),
    ("http-representation", "HTTP representation", "A representation combines content with metadata describing the selected state of a resource at a particular interaction.", "networking.http"),
    ("content-negotiation", "Content negotiation", "Content negotiation selects a representation using request preferences, server capabilities, and variation rules that affect caching.", "networking.http"),
    ("http-cache", "HTTP cache", "An HTTP cache reuses stored responses only when method, status, freshness, validation, authorization, and variation rules permit it.", "networking.http"),
    ("cache-validator", "HTTP cache validator", "A validator lets a recipient test whether a stored representation still corresponds to current selected state without retransferring it in full.", "networking.http"),
    ("http-intermediary", "HTTP intermediary", "A proxy, gateway, or tunnel participates between client and origin and can transform, cache, route, or relay messages within protocol constraints.", "networking.http"),
    ("http2", "HTTP/2 multiplexing", "HTTP/2 maps concurrent HTTP messages onto framed streams in one connection while preserving shared transport-level loss behavior.", "networking.http"),
    ("http3", "HTTP/3 over QUIC", "HTTP/3 maps HTTP semantics onto QUIC streams so loss on one stream need not block delivery progress on independent streams.", "networking.http"),
    ("wireless-medium", "Shared wireless medium", "Wireless participants contend for a variable shared medium affected by interference, propagation, coding, mobility, and scheduling.", "networking.wireless"),
    ("wireless-association", "Wireless association", "Association establishes link-layer participation with an access point but does not alone guarantee IP configuration or Internet reachability.", "networking.wireless"),
    ("wireless-roaming", "Wireless roaming", "Roaming changes attachment points and can perturb link, addressing, transport, authentication, and application state on different timescales.", "networking.wireless"),
    ("wireless-interference", "Wireless interference", "Interference lowers usable signal quality and can increase retries, rate adaptation, latency, and loss without appearing as congestion alone.", "networking.wireless"),
    ("sdn", "Software-defined networking", "Software-defined networking separates programmatic control decisions from distributed packet forwarding while retaining failure and consistency boundaries.", "networking.software-defined"),
    ("flow-rule", "Data-plane flow rule", "A flow rule matches packet fields and applies forwarding, modification, measurement, or discard actions with declared priority and lifetime.", "networking.software-defined"),
    ("sdn-controller", "SDN controller", "An SDN controller computes and distributes network policy from a logically centralized view that may be physically replicated and temporarily inconsistent.", "networking.software-defined"),
    ("cloud-vpc", "Virtual private cloud", "A virtual private cloud defines an isolated logical network boundary containing address ranges, routes, interfaces, and policy attachments.", "networking.cloud"),
    ("cloud-load-balancer", "Network load balancer", "A load balancer selects a healthy backend for new traffic according to policy while maintaining protocol and connection-state constraints.", "networking.cloud"),
    ("service-discovery", "Service discovery", "Service discovery maps a logical service identity to currently usable endpoints and therefore couples naming, health, lifecycle, and caching.", "networking.cloud"),
    ("overlay", "Network overlay", "An overlay encapsulates logical traffic across an underlay, adding virtual topology and policy at the cost of header overhead and nested failure modes.", "networking.cloud"),
    ("egress", "Network egress", "Egress is outbound traffic crossing a governed boundary and should be constrained, attributed, measured, and charged according to risk and policy.", "networking.cloud"),
    ("packet-capture", "Packet capture", "A packet capture records traffic visible at one observation point and cannot by itself prove packets elsewhere on the path or decrypted application meaning.", "networking.observability"),
    ("flow-log", "Flow log", "A flow log summarizes selected connection or packet metadata with sampling, aggregation, and visibility limits that must accompany inference.", "networking.observability"),
    ("network-metric", "Network metric", "A network metric is a timestamped measurement with defined vantage point, aggregation, units, and collection loss.", "networking.observability"),
    ("distributed-trace", "Distributed trace", "A distributed trace correlates causally related application operations across processes but requires propagation and sampling that can be incomplete.", "networking.observability"),
    ("clock-boundary", "Measurement clock boundary", "One-way delay and cross-host ordering require synchronized clocks or explicit uncertainty; local timestamps alone do not establish global order.", "networking.observability"),
    ("bandwidth", "Link bandwidth", "Bandwidth is a link's nominal information-carrying capacity under a declared physical and coding context.", "networking.performance"),
    ("throughput", "Network throughput", "Throughput is the rate of transferred data observed over an interval and is bounded by protocol overhead, loss, contention, and bottlenecks.", "networking.performance"),
    ("latency", "Network latency", "Latency includes propagation, serialization, processing, queueing, retransmission, and application delay along the measured path.", "networking.performance"),
    ("jitter", "Network jitter", "Jitter is variation in delay or inter-arrival time and affects real-time playout, buffering, and tail behavior.", "networking.performance"),
    ("loss", "Packet loss", "Packet loss is absence at a later observation point and can result from corruption, congestion, policy discard, route change, or capture limitations.", "networking.performance"),
    ("queue", "Network queue", "A queue absorbs short-term arrival bursts but increases latency and eventually discards or marks traffic when demand exceeds service.", "networking.performance"),
    ("bdp", "Bandwidth-delay product", "Bandwidth-delay product estimates the data required in flight to fill a path at a target rate over its round-trip time.", "networking.performance"),
    ("bottleneck", "Path bottleneck", "A bottleneck is the resource whose available service rate constrains end-to-end throughput under the current traffic mix.", "networking.performance"),
    ("backpressure", "Backpressure", "Backpressure propagates downstream capacity limits toward producers so queues and memory remain bounded.", "networking.performance"),
    ("layered-diagnosis", "Layered network diagnosis", "Layered diagnosis starts from observed scope and tests physical, link, network, transport, naming, security, and application hypotheses without assuming the first visible symptom is the cause.", "networking.troubleshooting"),
    ("baseline", "Network baseline", "A baseline records normal distributions and topology for comparable time, load, and vantage points so deviations can be interpreted.", "networking.troubleshooting"),
    ("path-test", "Path test", "A path test probes reachability or delay from a specific source and protocol context and does not prove reverse-path or application health.", "networking.troubleshooting"),
    ("binary-localization", "Fault-domain localization", "Fault-domain localization changes one boundary at a time to identify the smallest layer, segment, population, or dependency that contains the failure.", "networking.troubleshooting"),
    ("dns-diagnosis", "DNS diagnosis", "DNS diagnosis separates name existence, delegation, authority, recursion, cache state, record type, validation, and final endpoint reachability.", "networking.troubleshooting"),
    ("mtu-diagnosis", "Path-MTU diagnosis", "Path-MTU diagnosis compares payload sizes and control feedback to distinguish size-dependent black holes from general loss.", "networking.troubleshooting"),
]


SECURITY = [
    ("root", "Cybersecurity causal system", "Cybersecurity manages risk to people, information, services, and physical consequences through governance, threat models, secure design, preventive controls, detection, response, recovery, and learning.", "cybersecurity.security-principles"),
    ("asset", "Security asset", "An asset is something of value whose confidentiality, integrity, availability, authenticity, privacy, safety, or accountability may require protection.", "cybersecurity.security-principles"),
    ("stakeholder", "Security stakeholder", "A stakeholder is a person or group that owns, uses, operates, depends on, or bears risk from the system and its controls.", "cybersecurity.security-principles"),
    ("confidentiality", "Confidentiality", "Confidentiality restricts information disclosure to authorized entities and contexts.", "cybersecurity.security-principles"),
    ("integrity", "Integrity", "Integrity protects information and system state from unauthorized or undetected alteration or destruction.", "cybersecurity.security-principles"),
    ("availability", "Availability", "Availability keeps authorized capabilities accessible with required timeliness and capacity despite faults and attacks.", "cybersecurity.security-principles"),
    ("authenticity", "Authenticity", "Authenticity supports confidence that an entity, message, or artifact has the claimed origin or identity.", "cybersecurity.security-principles"),
    ("accountability", "Accountability", "Accountability links security-relevant actions and decisions to responsible identities through policy, evidence, and review.", "cybersecurity.security-principles"),
    ("threat", "Threat", "A threat is a circumstance or actor capability that could exploit a weakness and cause harm to an asset.", "cybersecurity.security-principles"),
    ("threat-actor", "Threat actor", "A threat actor is an entity with motives, capabilities, access, constraints, and opportunities that must be modeled without assuming omnipotence.", "cybersecurity.security-principles"),
    ("vulnerability", "Vulnerability", "A vulnerability is a weakness in design, implementation, configuration, operation, process, or human-system interaction that can enable harm.", "cybersecurity.security-principles"),
    ("exploit", "Exploit", "An exploit is a technique or artifact that exercises a vulnerability under required preconditions to produce an unintended effect.", "cybersecurity.security-principles"),
    ("exposure", "Exposure", "Exposure is the reachable or usable condition that allows a threat to interact with an asset or vulnerable surface.", "cybersecurity.security-principles"),
    ("risk", "Cybersecurity risk", "Cybersecurity risk combines uncertain likelihood, exposure, vulnerability, consequence, and control effectiveness for identified stakeholders.", "cybersecurity.security-principles"),
    ("attack-surface", "Attack surface", "An attack surface is the set of reachable interfaces, data paths, identities, dependencies, privileges, and physical interactions through which harm might be attempted.", "cybersecurity.security-principles"),
    ("trust-boundary", "Trust boundary", "A trust boundary is a transition where identity, authority, data sensitivity, or control assumptions change and therefore require explicit mediation.", "cybersecurity.security-principles"),
    ("threat-model", "Threat model", "A threat model identifies assets, actors, entry points, trust boundaries, capabilities, abuse paths, consequences, controls, assumptions, and residual risk for a versioned system.", "cybersecurity.security-principles"),
    ("misuse-case", "Misuse case", "A misuse case describes how an authorized or unauthorized capability could be abused, including prerequisites, observable steps at an appropriate safety level, and intended mitigations.", "cybersecurity.security-principles"),
    ("defense-depth", "Defense in depth", "Defense in depth uses independent preventive, detective, limiting, and recovery controls so one failure does not expose the full asset.", "cybersecurity.security-principles"),
    ("least-privilege", "Least privilege", "Least privilege grants each subject only the capabilities needed for a bounded purpose and duration, then removes them when no longer required.", "cybersecurity.security-principles"),
    ("fail-safe", "Fail-safe default", "A fail-safe default denies or limits access when policy, identity, validation, or control state is absent or indeterminate.", "cybersecurity.security-principles"),
    ("complete-mediation", "Complete mediation", "Complete mediation checks every security-relevant access at the authoritative decision boundary rather than trusting stale prior approval.", "cybersecurity.security-principles"),
    ("separation-duty", "Separation of duties", "Separation of duties requires independent roles or approvals for high-impact actions so one compromised identity cannot complete the whole chain.", "cybersecurity.security-principles"),
    ("secure-default", "Secure by default", "A secure default minimizes exposed features and privileges before an operator makes an informed, auditable choice to broaden them.", "cybersecurity.security-principles"),
    ("control", "Security control", "A security control is a safeguard designed to prevent, detect, limit, respond to, or recover from specified risk under testable conditions.", "cybersecurity.security-principles"),
    ("residual-risk", "Residual risk", "Residual risk is the uncertainty and consequence remaining after implemented controls and accepted assumptions are considered.", "cybersecurity.security-principles"),
    ("plaintext", "Plaintext", "Plaintext is information in the form presented to a cryptographic transformation and may itself already be encoded or compressed.", "cybersecurity.cryptography"),
    ("ciphertext", "Ciphertext", "Ciphertext is the protected output of encryption and does not hide all metadata such as length, timing, or endpoints.", "cybersecurity.cryptography"),
    ("key", "Cryptographic key", "A cryptographic key is secret or public parameter material whose generation, scope, storage, use, rotation, and destruction determine system security.", "cybersecurity.cryptography"),
    ("entropy", "Cryptographic entropy", "Entropy characterizes uncertainty in a source distribution; a long string is not necessarily unpredictable.", "cybersecurity.cryptography"),
    ("csprng", "Cryptographic random generator", "A cryptographic random generator expands well-seeded state into outputs designed to remain unpredictable under a declared compromise model.", "cybersecurity.cryptography"),
    ("hash", "Cryptographic hash", "A cryptographic hash maps arbitrary input to a fixed-length digest with security properties that depend on the selected construction and use.", "cybersecurity.cryptography"),
    ("mac", "Message authentication code", "A message authentication code uses a shared secret to detect unauthorized alteration and authenticate origin within the key-sharing group.", "cybersecurity.cryptography"),
    ("aead", "Authenticated encryption", "Authenticated encryption protects plaintext confidentiality and integrity together with declared associated data, nonce rules, and key scope.", "cybersecurity.cryptography"),
    ("nonce", "Cryptographic nonce", "A nonce is a value constrained by a construction's uniqueness or unpredictability requirement; reuse can catastrophically break some schemes.", "cybersecurity.cryptography"),
    ("kdf", "Key-derivation function", "A key-derivation function turns keying material and context into purpose-separated keys under declared entropy and salt assumptions.", "cybersecurity.cryptography"),
    ("password-hash", "Password hashing", "Password hashing uses a salted, deliberately costly password-specific function so offline guessing is more expensive and identical passwords do not share stored values.", "cybersecurity.cryptography"),
    ("signature", "Digital signature", "A digital signature lets holders of a public verification key check message integrity and possession of the corresponding private signing key.", "cybersecurity.cryptography"),
    ("certificate", "Public-key certificate", "A certificate binds a public key to named attributes under an issuer's signature and remains dependent on validation policy, time, scope, and trust anchors.", "cybersecurity.cryptography"),
    ("key-lifecycle", "Key lifecycle", "A key lifecycle covers approved generation, provisioning, storage, access, use limits, rotation, revocation, archival where required, and destruction.", "cybersecurity.cryptography"),
    ("forward-secrecy", "Forward secrecy", "Forward secrecy limits later long-term-key compromise from revealing past session keys when ephemeral secrets were correctly generated and erased.", "cybersecurity.cryptography"),
    ("segmentation", "Network segmentation", "Segmentation creates controlled communication boundaries among assets so compromise paths and blast radius can be constrained and observed.", "cybersecurity.network-security"),
    ("firewall", "Firewall policy", "A firewall mediates network traffic using identity, address, protocol, state, content, or application context under ordered allow and deny rules.", "cybersecurity.network-security"),
    ("network-allowlist", "Network allowlist", "A network allowlist admits only explicitly authorized communication and still requires endpoint security and validation of permitted protocols.", "cybersecurity.network-security"),
    ("ids", "Intrusion detection", "Intrusion detection identifies patterns or deviations associated with malicious activity and produces hypotheses that require tuning, context, and investigation.", "cybersecurity.network-security"),
    ("ips", "Intrusion prevention", "Intrusion prevention blocks or alters suspected malicious traffic and must manage false positives, evasion, placement, and fail behavior.", "cybersecurity.network-security"),
    ("ddos", "Denial-of-service resistance", "Denial-of-service resistance combines capacity, rate controls, admission, isolation, degradation modes, upstream coordination, and recovery rather than promising absolute prevention.", "cybersecurity.network-security"),
    ("secure-egress", "Secure egress control", "Secure egress constrains outbound destinations, protocols, identities, data classes, and volume to reduce exfiltration and command paths.", "cybersecurity.network-security"),
    ("vpn", "Virtual private network", "A VPN protects traffic across an untrusted path between authenticated endpoints but does not make either endpoint or permitted application trustworthy.", "cybersecurity.network-security"),
    ("injection", "Injection vulnerability", "Injection occurs when untrusted data is interpreted as commands or syntax by a downstream interpreter because data and control were not kept distinct.", "cybersecurity.application-security"),
    ("xss", "Cross-site scripting", "Cross-site scripting causes attacker-influenced content to execute in a web origin's script context through unsafe generation, parsing, or DOM use.", "cybersecurity.application-security"),
    ("csrf", "Cross-site request forgery", "Cross-site request forgery induces a browser to send an authenticated state-changing request without the user's intended authorization for that action.", "cybersecurity.application-security"),
    ("ssrf", "Server-side request forgery", "Server-side request forgery causes a server-side fetch capability to reach destinations or schemes outside the intended policy boundary.", "cybersecurity.application-security"),
    ("input-validation", "Input validation", "Input validation accepts only values conforming to the application's semantic contract at the authoritative boundary but does not replace context-specific output safety.", "cybersecurity.application-security"),
    ("output-encoding", "Contextual output encoding", "Output encoding represents untrusted data so a particular interpreter context treats it as data rather than executable syntax.", "cybersecurity.application-security"),
    ("parameterization", "Parameterized command", "Parameterization binds data separately from a command or query grammar and prevents data from changing that grammar where the API honors the separation.", "cybersecurity.application-security"),
    ("authorization-check", "Object-level authorization", "Object-level authorization checks that the authenticated subject may perform the requested action on the specific target object and tenant.", "cybersecurity.application-security"),
    ("session-security", "Session security", "Session security binds authenticated state to protected identifiers, expiration, rotation, revocation, transport, and reauthentication rules.", "cybersecurity.application-security"),
    ("secret-management", "Secret management", "Secret management keeps credentials out of source and logs, limits their scope, protects storage and delivery, rotates them, and records access without revealing values.", "cybersecurity.application-security"),
    ("security-log", "Security logging", "Security logging records relevant actor, action, target, result, time, and correlation while protecting sensitive content and tamper evidence.", "cybersecurity.application-security"),
    ("process-isolation", "Process isolation", "Process isolation uses address spaces, privilege boundaries, and kernel mediation to limit one process from reading or modifying another.", "cybersecurity.operating-system-security"),
    ("memory-protection", "Memory protection", "Memory protection enforces access permissions and execution constraints on mapped regions while implementation defects and unsafe code can still violate intent.", "cybersecurity.operating-system-security"),
    ("privilege-boundary", "Operating-system privilege boundary", "A privilege boundary mediates access to kernel, device, file, process, and administrative operations using authenticated security context.", "cybersecurity.operating-system-security"),
    ("sandbox", "Sandbox", "A sandbox constrains a component's capabilities and communication so compromise has a smaller reachable effect, subject to the sandbox's own attack surface.", "cybersecurity.operating-system-security"),
    ("patch", "Security patch", "A security patch changes vulnerable behavior or exposure and requires version tracking, compatibility testing, deployment evidence, and rollback planning.", "cybersecurity.operating-system-security"),
    ("shared-responsibility", "Cloud shared responsibility", "Cloud security responsibilities divide across provider and customer layers and vary by service model, configuration, data, identity, and contract.", "cybersecurity.cloud-security"),
    ("cloud-iam", "Cloud identity policy", "Cloud identity policy grants actions over resources under conditions and must be evaluated across inherited roles, service identities, and organization boundaries.", "cybersecurity.cloud-security"),
    ("metadata-service", "Cloud metadata service", "An instance metadata service exposes workload identity or configuration through a local interface that must resist SSRF, cross-workload access, and credential theft.", "cybersecurity.cloud-security"),
    ("public-storage", "Public cloud storage exposure", "A storage resource becomes publicly exposed when identity, network, object, or inherited policy permits unintended anonymous or broad access.", "cybersecurity.cloud-security"),
    ("subject", "Security subject", "A subject is a user, workload, device, or process that requests an operation under an asserted and verified identity context.", "cybersecurity.identity-access"),
    ("authentication", "Authentication", "Authentication establishes confidence in a claimed identity using one or more authenticators and a protocol resistant to relevant threats.", "cybersecurity.identity-access"),
    ("authorization", "Authorization", "Authorization decides whether an authenticated or otherwise identified subject may perform an action on a resource under current policy and context.", "cybersecurity.identity-access"),
    ("mfa", "Multi-factor authentication", "Multi-factor authentication combines independent factor types so compromise of one factor is insufficient under the modeled attack.", "cybersecurity.identity-access"),
    ("federation", "Identity federation", "Federation lets one administrative domain rely on signed identity assertions from another under explicit issuer, audience, time, and attribute policy.", "cybersecurity.identity-access"),
    ("rbac", "Role-based access control", "Role-based access control assigns permissions to organizational roles and subjects to roles, simplifying policy while risking excessive role accumulation.", "cybersecurity.identity-access"),
    ("abac", "Attribute-based access control", "Attribute-based access control evaluates subject, resource, action, and environment attributes under policy at decision time.", "cybersecurity.identity-access"),
    ("zero-trust", "Zero-trust architecture", "Zero trust removes implicit trust based solely on network location or ownership and continuously mediates access to resources using identity, device, policy, and observed context.", "cybersecurity.identity-access"),
    ("tls-channel", "TLS secure channel", "A correctly validated TLS 1.3 channel protects application data confidentiality and integrity between authenticated endpoints under negotiated parameters.", "cybersecurity.secure-protocols"),
    ("tls-handshake", "TLS handshake", "The TLS handshake negotiates protocol parameters, authenticates the server and optionally the client, and derives traffic keys while binding the transcript.", "cybersecurity.secure-protocols"),
    ("certificate-validation", "Certificate validation", "Certificate validation builds and checks a path to an accepted trust anchor under name, time, usage, algorithm, policy, and revocation constraints.", "cybersecurity.secure-protocols"),
    ("replay", "Replay attack", "A replay attack reuses a previously valid message in a context where freshness or uniqueness was not adequately enforced.", "cybersecurity.secure-protocols"),
    ("downgrade", "Protocol downgrade", "A downgrade attack manipulates negotiation so peers select weaker behavior than their honest mutual capabilities permit.", "cybersecurity.secure-protocols"),
    ("research-authorization", "Vulnerability-research authorization", "Authorized vulnerability research has an explicit owner, scope, targets, methods, data rules, time window, stop conditions, and reporting channel.", "cybersecurity.vulnerability-research"),
    ("repro-case", "Vulnerability reproducer", "A safe reproducer demonstrates the minimum preconditions and effect inside an authorized environment while minimizing destructive payload, persistence, and unrelated data access.", "cybersecurity.vulnerability-research"),
    ("root-cause", "Vulnerability root cause", "Root-cause analysis identifies the design, implementation, process, or assumption failure that permitted the security violation, not only the triggering input.", "cybersecurity.vulnerability-research"),
    ("coordinated-disclosure", "Coordinated disclosure", "Coordinated disclosure communicates enough evidence for remediation through the authorized channel while managing affected users, timelines, and premature exploitation risk.", "cybersecurity.vulnerability-research"),
    ("severity", "Vulnerability severity", "Severity estimates technical consequence and exploit conditions for a declared environment and must not be confused with organization-specific risk or priority.", "cybersecurity.vulnerability-research"),
    ("incident-preparation", "Incident preparation", "Incident preparation establishes roles, authority, contacts, telemetry, playbooks, containment options, evidence handling, backups, and exercises before an event.", "cybersecurity.incident-response"),
    ("incident-detection", "Incident detection", "Incident detection identifies observations that may indicate adverse activity and preserves uncertainty until corroborating evidence supports classification.", "cybersecurity.incident-response"),
    ("incident-analysis", "Incident analysis", "Incident analysis builds and revises a timeline, affected scope, causal hypotheses, indicators, and confidence from preserved evidence.", "cybersecurity.incident-response"),
    ("containment", "Incident containment", "Containment limits ongoing harm and spread while balancing evidence preservation, business impact, adversary adaptation, and recovery options.", "cybersecurity.incident-response"),
    ("eradication", "Incident eradication", "Eradication removes malicious persistence and closes exploited causes across the affected population rather than deleting one visible artifact.", "cybersecurity.incident-response"),
    ("recovery", "Incident recovery", "Recovery restores trusted service in stages, validates control effectiveness, monitors recurrence, and retains a path back if restored state proves unsafe.", "cybersecurity.incident-response"),
    ("lessons", "Incident lessons learned", "Lessons learned convert evidence into control, architecture, process, training, and measurement changes with accountable owners.", "cybersecurity.incident-response"),
    ("chain-custody", "Evidence chain of custody", "Chain of custody records collection, identity, integrity, transfer, access, analysis, and disposition so evidence handling can be evaluated.", "cybersecurity.incident-response"),
    ("data-minimization", "Data minimization", "Data minimization limits collection, processing, sharing, and retention to information necessary for a declared purpose.", "cybersecurity.privacy"),
    ("purpose-limitation", "Purpose limitation", "Purpose limitation prevents data collected for one justified function from silently expanding to unrelated uses.", "cybersecurity.privacy"),
    ("retention", "Data retention", "A retention rule specifies why data is held, for how long, who can access it, and how deletion or legal preservation is verified.", "cybersecurity.privacy"),
    ("pseudonymization", "Pseudonymization", "Pseudonymization replaces direct identifiers while retaining a re-linking path or residual linkage risk, so it is not anonymity.", "cybersecurity.privacy"),
    ("anonymization", "Anonymization", "Anonymization aims to make re-identification infeasible under a declared attacker and auxiliary-data model and therefore requires empirical and contextual assessment.", "cybersecurity.privacy"),
    ("privacy-threat-model", "Privacy threat model", "A privacy threat model identifies people, data flows, inferences, linkability, power, misuse, retention, and harms beyond system compromise alone.", "cybersecurity.privacy"),
    ("provenance", "Software provenance", "Software provenance records who or what produced an artifact, from which inputs and process, under which environment and attestations.", "cybersecurity.supply-chain"),
    ("sbom", "Software bill of materials", "An SBOM enumerates identified software components and relationships for a particular artifact or release but does not prove absence of undeclared code or vulnerability.", "cybersecurity.supply-chain"),
    ("artifact-signing", "Artifact signing", "Artifact signing binds artifact bytes and metadata to a signing identity; verification still requires trusted keys, policy, and secure build context.", "cybersecurity.supply-chain"),
    ("repro-build", "Reproducible build", "A reproducible build yields byte-identical output from declared source and environment, strengthening integrity comparison without proving the source is benign.", "cybersecurity.supply-chain"),
    ("dependency-pin", "Dependency pinning", "Dependency pinning fixes resolved versions and hashes for repeatability while requiring a deliberate process for security updates.", "cybersecurity.supply-chain"),
    ("update-chain", "Secure update chain", "A secure update chain authenticates release metadata and artifacts, handles rollback and key compromise, and verifies installation outcome.", "cybersecurity.supply-chain"),
    ("authorized-scope", "Authorized security scope", "Security work must remain within the systems, identities, data, methods, and time explicitly authorized by the owner.", "cybersecurity.safety-ethics"),
    ("minimum-harm", "Minimum-harm security method", "When several authorized methods can answer the question, choose the one with the least destructive effect, data exposure, persistence, and third-party risk.", "cybersecurity.safety-ethics"),
    ("safe-lab", "Isolated security lab", "An isolated lab uses owned fixtures, synthetic data, constrained connectivity, snapshots, and monitoring so failures do not escape to uninvolved systems.", "cybersecurity.safety-ethics"),
    ("stop-condition", "Security stop condition", "A stop condition ends testing when scope is uncertain, unexpected sensitive data appears, stability degrades, or potential harm exceeds authorization.", "cybersecurity.safety-ethics"),
    ("responsible-report", "Responsible security report", "A responsible report provides affected version, impact, safe reproduction evidence, remediation guidance, and disclosure handling without unnecessary weaponization.", "cybersecurity.safety-ethics"),
]


BROWSER = [
    ("root", "Browser and web-platform pipeline", "A browser coordinates standards-defined parsing, execution, fetching, security, storage, rendering, accessibility, user interaction, and extension boundaries across multiple isolated processes and evolving implementations.", "browser-web-platform.standards"),
    ("html-document", "HTML document", "An HTML document is parsed into a DOM under HTML-specific error-recovery and conformance rules rather than as generic XML.", "browser-web-platform.html"),
    ("html-element", "HTML element", "An HTML element has semantics, content-model constraints, attributes, DOM behavior, accessibility implications, and rendering defaults that are not captured by tag appearance alone.", "browser-web-platform.html"),
    ("semantic-html", "Semantic HTML", "Semantic HTML selects elements for their defined meaning and interaction behavior so multiple user agents can derive structure beyond visual styling.", "browser-web-platform.html"),
    ("html-parser", "HTML parser", "The HTML parser tokenizes input and constructs or mutates a DOM through stateful insertion modes and defined recovery from malformed markup.", "browser-web-platform.html"),
    ("form-control", "Form control", "A form control has name, value, validation, disabled state, focus behavior, successful-submission rules, and accessible semantics.", "browser-web-platform.html"),
    ("custom-element", "Custom element", "A custom element associates a registered definition and lifecycle reactions with matching DOM elements under upgrade timing and construction constraints.", "browser-web-platform.html"),
    ("css-rule", "CSS rule", "A CSS rule associates selectors or conditions with declarations that enter the cascade for matching elements.", "browser-web-platform.css"),
    ("cascade", "CSS cascade", "The cascade resolves competing declarations by origin, importance, context, layer, specificity, scoping proximity, and order before inheritance and value processing.", "browser-web-platform.css"),
    ("specificity", "Selector specificity", "Specificity is one ordered component of cascade precedence and cannot override declarations from stronger origins, importance, or applicable layers by itself.", "browser-web-platform.css"),
    ("inheritance", "CSS inheritance", "Inheritance supplies selected computed values from a parent when the property definition and cascade call for it; most box and layout properties do not inherit by default.", "browser-web-platform.css"),
    ("computed-value", "Computed CSS value", "A computed value is produced after cascade and value resolution but can still differ from used and actual values after layout and device constraints.", "browser-web-platform.css"),
    ("box-model", "CSS box model", "The CSS box model relates content, padding, border, and margin rectangles, with sizing rules determining which edges a declared dimension controls.", "browser-web-platform.css"),
    ("formatting-context", "Formatting context", "A formatting context defines how descendant boxes participate in layout, including flow, flex, grid, table, and independent formatting behavior.", "browser-web-platform.css"),
    ("containing-block", "Containing block", "A containing block supplies the coordinate and percentage-reference rectangle for positioned and sized descendants under layout-specific rules.", "browser-web-platform.css"),
    ("stacking-context", "Stacking context", "A stacking context groups painted descendants into an atomic z-order unit whose internal ordering does not freely interleave with outside content.", "browser-web-platform.css"),
    ("responsive-layout", "Responsive layout", "Responsive layout adapts intrinsic sizing, flow, queries, and constraints to available space and content rather than targeting a fixed device list.", "browser-web-platform.css"),
    ("js-realm", "JavaScript realm", "A JavaScript realm contains its own global object, intrinsic objects, and execution environment, so values crossing realms can have different identity relationships.", "browser-web-platform.javascript-runtime"),
    ("execution-context", "JavaScript execution context", "An execution context tracks the code, lexical and variable environments, realm, and control state for an active evaluation.", "browser-web-platform.javascript-runtime"),
    ("call-stack", "JavaScript call stack", "The call stack orders active execution contexts synchronously until frames return or abrupt completion unwinds them.", "browser-web-platform.javascript-runtime"),
    ("event-loop", "Event loop", "An event loop selects runnable tasks, performs microtask checkpoints, coordinates rendering opportunities, and waits when no work is eligible.", "browser-web-platform.javascript-runtime"),
    ("task", "Browser task", "A task represents queued work from a task source and runs to completion relative to other tasks on the same event loop.", "browser-web-platform.javascript-runtime"),
    ("microtask", "Microtask", "A microtask runs during defined checkpoints after current script or task work and can delay rendering or later tasks if it recursively queues more work.", "browser-web-platform.javascript-runtime"),
    ("promise", "Promise reaction", "A settled promise schedules reactions as microtasks; settlement does not synchronously invoke attached continuation code.", "browser-web-platform.javascript-runtime"),
    ("garbage-collection", "Garbage collection", "Garbage collection reclaims unreachable managed objects according to implementation strategy, and program correctness must not depend on exact collection timing.", "browser-web-platform.javascript-runtime"),
    ("jit", "JavaScript JIT compilation", "A JavaScript engine may compile frequently executed paths using speculative assumptions and must deoptimize when observed values invalidate them.", "browser-web-platform.javascript-runtime"),
    ("dom-node", "DOM node", "A DOM node participates in a rooted or disconnected tree with parent, child, sibling, document, and mutation relationships.", "browser-web-platform.dom-events"),
    ("document-tree", "DOM document tree", "The document tree provides ordered containment used by parsing, selectors, event paths, rendering, and accessibility derivation.", "browser-web-platform.dom-events"),
    ("event-target", "Event target", "An event target can register listeners and participate in dispatch according to the event path and listener options.", "browser-web-platform.dom-events"),
    ("event-dispatch", "DOM event dispatch", "Event dispatch constructs a path and invokes eligible listeners through capture, target, and bubble phases while tracking cancellation and propagation state.", "browser-web-platform.dom-events"),
    ("default-action", "Event default action", "A default action is user-agent behavior associated with an uncanceled event and may occur at a specification-defined point relative to listener invocation.", "browser-web-platform.dom-events"),
    ("abort-signal", "Abort signal", "An abort signal communicates cancellation state and reason to cooperating asynchronous operations without forcibly undoing already completed effects.", "browser-web-platform.dom-events"),
    ("mutation-observer", "Mutation observer", "A mutation observer batches qualifying DOM change records and delivers them at a microtask checkpoint rather than synchronously for each mutation.", "browser-web-platform.dom-events"),
    ("shadow-tree", "Shadow tree", "A shadow tree creates an encapsulated DOM subtree with host, slotting, style, and event-retargeting behavior rather than a security boundary.", "browser-web-platform.dom-events"),
    ("parse-pipeline", "Document parse pipeline", "The browser decodes fetched bytes, tokenizes HTML, constructs DOM nodes, and may pause or schedule around scripts and subresource discovery.", "browser-web-platform.rendering"),
    ("style-calculation", "Style calculation", "Style calculation matches rules and resolves cascade, inheritance, and computed values for elements affected by the current document and environment.", "browser-web-platform.rendering"),
    ("layout", "Browser layout", "Layout computes used box geometry from formatting contexts, intrinsic sizes, constraints, writing mode, viewport, and available space.", "browser-web-platform.rendering"),
    ("paint", "Browser paint", "Paint converts styled layout fragments into ordered drawing commands for backgrounds, text, borders, effects, and replaced content.", "browser-web-platform.rendering"),
    ("compositing", "Browser compositing", "Compositing assembles rasterized layers under transforms, clips, opacity, and effects, often on a separate thread or process.", "browser-web-platform.rendering"),
    ("invalidation", "Rendering invalidation", "Invalidation identifies which style, layout, paint, or composite results are no longer reusable after a state change.", "browser-web-platform.rendering"),
    ("frame-budget", "Frame budget", "A frame budget bounds main-thread, raster, and composite work needed to present an update at a target refresh rate, with tail latency causing visible jank.", "browser-web-platform.rendering"),
    ("fetch-request", "Fetch request", "A Fetch request carries URL, method, headers, mode, credentials, cache, redirect, destination, origin, and body state through the browser networking model.", "browser-web-platform.networking"),
    ("fetch-response", "Fetch response", "A Fetch response has status, headers, body, type, URL list, and tainting or filtering determined by the request and security model.", "browser-web-platform.networking"),
    ("cors", "Cross-origin resource sharing", "CORS is an HTTP-mediated protocol by which a server authorizes selected cross-origin response exposure to script; it is not an authentication mechanism.", "browser-web-platform.networking"),
    ("preflight", "CORS preflight", "A preflight asks whether a server permits a non-simple cross-origin method or header set before the browser exposes the actual scripted request path.", "browser-web-platform.networking"),
    ("credential-mode", "Fetch credential mode", "Credential mode controls whether cookies and HTTP authentication participate in fetching and interacts with origin and CORS policy.", "browser-web-platform.networking"),
    ("redirect", "Fetch redirect", "Redirect processing creates a bounded URL chain while applying method rewriting, credential, origin, referrer, and exposure rules.", "browser-web-platform.networking"),
    ("browser-cache", "Browser HTTP cache", "The browser HTTP cache applies HTTP freshness and validation semantics within an implementation's partition and privacy policy.", "browser-web-platform.networking"),
    ("navigation", "Browser navigation", "Navigation selects or creates a history entry and navigable document through URL, fetch, response, origin, policy, and lifecycle processing.", "browser-web-platform.networking"),
    ("cookie", "HTTP cookie", "A cookie is scoped state attached to qualifying HTTP requests under domain, path, security, same-site, partition, expiration, and user-agent policy.", "browser-web-platform.storage"),
    ("web-storage", "Web storage", "Web storage exposes origin-scoped string key-value state with synchronous access and implementation-defined quota and lifecycle limits.", "browser-web-platform.storage"),
    ("indexeddb", "IndexedDB", "IndexedDB provides asynchronous transactional object storage scoped by origin and database, with version-change coordination across connections.", "browser-web-platform.storage"),
    ("cache-storage", "Cache Storage", "Cache Storage persists request-response pairs for script-managed lookup under origin and quota boundaries without replacing HTTP cache semantics.", "browser-web-platform.storage"),
    ("service-worker", "Service worker", "A service worker is an origin-and-scope-bound event-driven worker that can intercept fetches and support offline, update, messaging, and background behavior.", "browser-web-platform.storage"),
    ("sw-lifecycle", "Service-worker lifecycle", "Service-worker registration progresses through install, waiting, activation, control, update, and redundancy states so new code does not silently split one client transaction.", "browser-web-platform.storage"),
    ("origin", "Web origin", "An origin is a scheme-host-port security principal used to isolate script access and network disclosure, with opaque origins for contexts lacking tuple identity.", "browser-web-platform.security"),
    ("site", "Web site boundary", "A site is a registrable-domain-based relation used by selected cookie and process policies and is broader than an origin.", "browser-web-platform.security"),
    ("same-origin", "Same-origin policy", "The same-origin policy restricts one origin's scripted access to another origin's data and objects while allowing narrowly specified cross-origin interactions.", "browser-web-platform.security"),
    ("csp", "Content Security Policy", "Content Security Policy constrains permitted resource loads and script execution as defense in depth; it does not repair an underlying injection flaw.", "browser-web-platform.security"),
    ("iframe-sandbox", "Iframe sandbox", "An iframe sandbox removes selected capabilities from embedded content unless explicitly restored and can assign an opaque origin.", "browser-web-platform.security"),
    ("mixed-content", "Mixed content", "Mixed-content policy blocks or upgrades insecure subresources in a secure context because an active network attacker could otherwise alter them.", "browser-web-platform.security"),
    ("sri", "Subresource integrity", "Subresource Integrity lets a document require fetched bytes to match a declared digest before executing or applying an eligible external resource.", "browser-web-platform.security"),
    ("permissions", "Web permission", "A web permission mediates a powerful capability using origin, top-level context, user choice, policy, activation, device, and revocation state.", "browser-web-platform.security"),
    ("trusted-types", "Trusted Types", "Trusted Types can require typed values at selected DOM injection sinks so string construction is separated from reviewed sanitization policy.", "browser-web-platform.security"),
    ("storage-partition", "Storage partitioning", "Storage partitioning keys selected state by top-level site or related context to reduce cross-site tracking and hidden communication.", "browser-web-platform.privacy"),
    ("fingerprinting", "Browser fingerprinting", "Fingerprinting combines observable device, software, behavior, and timing features into a probabilistic identifier without requiring a stored cookie.", "browser-web-platform.privacy"),
    ("tracking", "Cross-context tracking", "Tracking links a person's activity across contexts through identifiers, shared state, network observations, or probabilistic inference.", "browser-web-platform.privacy"),
    ("referrer", "Referrer policy", "Referrer policy limits which source URL information a browser includes when navigating or fetching across trust boundaries.", "browser-web-platform.privacy"),
    ("privacy-budget", "Privacy surface budgeting", "A privacy budget is a design approach that limits cumulative high-entropy observations; it is not a universal deployed browser invariant.", "browser-web-platform.privacy"),
    ("a11y-tree", "Accessibility tree", "An accessibility tree exposes semantic roles, names, values, states, relationships, and actions derived from the DOM, styling, and accessibility APIs.", "browser-web-platform.accessibility"),
    ("accessible-name", "Accessible name", "An accessible name identifies a control or region to assistive technology through a specification-defined precedence of visible and referenced text.", "browser-web-platform.accessibility"),
    ("focus", "Keyboard focus", "Focus identifies the element receiving keyboard interaction and must remain visible, logical, and restorable across dynamic updates.", "browser-web-platform.accessibility"),
    ("keyboard", "Keyboard operability", "Keyboard operability ensures interactive functionality can be reached and used without requiring pointer-specific gestures.", "browser-web-platform.accessibility"),
    ("aria", "ARIA semantics", "ARIA can supply or refine accessibility semantics when native HTML is insufficient, but it does not add missing keyboard behavior or visual state automatically.", "browser-web-platform.accessibility"),
    ("reduced-motion", "Reduced-motion preference", "A reduced-motion preference lets content limit nonessential animation and vestibular triggers while preserving meaning and operability.", "browser-web-platform.accessibility"),
    ("extension-manifest", "Browser-extension manifest", "An extension manifest declares identity, entry points, permissions, resources, content-script matches, and platform version under a browser-specific schema.", "browser-web-platform.extensions"),
    ("extension-permission", "Extension permission", "An extension permission grants access to browser capabilities or host data and should be minimized, explained, and requested at the latest useful time.", "browser-web-platform.extensions"),
    ("content-script", "Extension content script", "A content script runs in a web page context with an isolated JavaScript world but shares and can modify the page's DOM under granted host scope.", "browser-web-platform.extensions"),
    ("extension-worker", "Extension background worker", "A background service worker handles extension events without a persistent page and must preserve needed state outside ephemeral globals.", "browser-web-platform.extensions"),
    ("extension-message", "Extension messaging", "Extension messaging crosses component and trust boundaries and therefore requires sender, schema, capability, and data validation at the receiver.", "browser-web-platform.extensions"),
    ("living-standard", "Living standard", "A living web standard is continuously maintained; a claim must identify the retrieval snapshot and interoperability status rather than assume a timeless edition.", "browser-web-platform.standards"),
    ("conformance", "Web conformance", "Conformance is defined against normative specification requirements for a particular role and does not follow from one browser accepting the input.", "browser-web-platform.standards"),
    ("interoperability", "Browser interoperability", "Interoperability requires independently implemented user agents to produce compatible observable behavior for shared tests and real content.", "browser-web-platform.standards"),
    ("wpt", "Web-platform test", "A web-platform test encodes an observable cross-browser requirement with controlled setup and expected result, while test gaps do not imply unspecified behavior.", "browser-web-platform.standards"),
    ("progressive-enhancement", "Progressive enhancement", "Progressive enhancement starts with robust semantic content and layers optional behavior so core use survives unsupported or failed enhancements.", "browser-web-platform.standards"),
]


RELATIONS = [
    ("net-signal-symbol", "net.signal", "net.bit-symbol", "implements", "Physical signal states implement transmitted symbols under a coding scheme."),
    ("net-encoding-signal", "net.encoding", "net.signal", "transforms_to", "Encoding transforms data into a physical signal sequence."),
    ("net-frame-encoding", "net.encoding", "net.frame", "enables", "A shared encoding and delimiter scheme enables receivers to recover frames."),
    ("net-mac-frame", "net.mac-address", "net.frame", "qualifies", "Link-layer addressing qualifies frame delivery on a shared link."),
    ("net-switch-frame", "net.ethernet-switch", "net.frame", "implements", "An Ethernet switch implements selective frame forwarding."),
    ("net-vlan-broadcast", "net.vlan", "net.broadcast-domain", "transforms_to", "VLAN configuration transforms one switching fabric into multiple logical broadcast domains."),
    ("net-mtu-frame", "net.mtu", "net.frame", "qualifies", "The link MTU qualifies the largest network payload carried by a frame."),
    ("net-error-frame", "net.link-error", "net.frame", "measures", "A frame check measures consistency of received bits with the transmitted checksum relation."),
    ("net-neighbor-mac", "net.neighbor-discovery", "net.mac-address", "clarifies", "Neighbor discovery clarifies the link-layer delivery target for a network-layer next hop."),
    ("net-packet-frame", "net.packet", "net.frame", "part_of", "An IP packet is carried as the payload of a link-layer frame on each hop."),
    ("net-address-prefix", "net.ipv6-address", "net.prefix", "part_of", "Leading IPv6 address bits participate in a configured network prefix."),
    ("net-prefix-subnet", "net.prefix", "net.subnet", "grounds", "A configured prefix grounds the address scope of an IP subnet."),
    ("net-route-prefix", "net.prefix", "net.route", "part_of", "A destination prefix is part of a route."),
    ("net-route-fib", "net.route", "net.forwarding-table", "part_of", "Selected routes populate the forwarding table."),
    ("net-lpm-fib", "net.longest-prefix", "net.forwarding-table", "implements", "Longest-prefix match implements destination-route selection in the forwarding table."),
    ("net-fib-packet", "net.forwarding-table", "net.packet", "causes", "A matching forwarding entry causes a hop-local packet action."),
    ("net-hop-loop", "net.hop-limit", "net.routing-loop", "prevents", "A hop limit prevents a routing loop from circulating a packet indefinitely."),
    ("net-mtu-path", "net.mtu", "net.path-mtu", "measures", "The smallest link MTU on the selected route determines path MTU."),
    ("net-icmp-mtu", "net.icmp", "net.path-mtu", "supports", "Relevant ICMP feedback supports path-MTU discovery."),
    ("net-nat-address", "net.nat", "net.ipv6-address", "transforms_to", "Address translation transforms packet address or port bindings across a boundary."),
    ("net-control-route", "net.control-plane", "net.route", "causes", "Control-plane computation causes selected routes to be installed or withdrawn."),
    ("net-loop-route", "net.route", "net.routing-loop", "enables", "Inconsistent next-hop routes can enable a forwarding loop."),
    ("net-port-socket", "net.port", "net.socket", "part_of", "A transport port forms part of a bound socket endpoint."),
    ("net-udp-packet", "net.udp", "net.packet", "part_of", "A UDP datagram is carried in an IP packet."),
    ("net-tcp-socket", "net.socket", "net.tcp-connection", "implements", "Sockets expose local endpoints of a TCP connection."),
    ("net-handshake-tcp", "net.tcp-handshake", "net.tcp-connection", "causes", "A valid handshake causes TCP endpoints to enter synchronized established state."),
    ("net-sequence-ack", "net.tcp-sequence", "net.tcp-ack", "enables", "Sequence positions enable acknowledgments to describe receive progress."),
    ("net-ack-retransmit", "net.tcp-ack", "net.retransmission", "enables", "Acknowledgment gaps or timeout evidence enable loss inference and retransmission."),
    ("net-flow-window", "net.flow-control", "net.tcp-connection", "qualifies", "Receiver flow control qualifies how much TCP data may remain in flight."),
    ("net-congestion-throughput", "net.congestion-control", "net.throughput", "qualifies", "Congestion control qualifies offered load and achieved throughput."),
    ("net-close-state", "net.tcp-close", "net.tcp-connection", "transforms_to", "Close events transform TCP through half-closed and terminal states."),
    ("net-quic-udp", "net.quic-connection", "net.udp", "part_of", "QUIC packets are carried in UDP datagrams."),
    ("net-quic-stream", "net.quic-stream", "net.quic-connection", "part_of", "Application streams are multiplexed within a QUIC connection."),
    ("net-migrate-quic", "net.path-migration", "net.quic-connection", "transforms_to", "Validated path migration transforms a QUIC connection's active network path."),
    ("net-name-zone", "net.dns-name", "net.dns-zone", "part_of", "Names at or below an authority boundary can be served from a DNS zone subject to delegation."),
    ("net-delegation-zone", "net.dns-delegation", "net.dns-zone", "transforms_to", "Delegation transfers authority for a child namespace to a distinct zone."),
    ("net-auth-zone", "net.dns-authoritative", "net.dns-zone", "supports", "An authoritative server supports answers from the served zone."),
    ("net-recursive-auth", "net.dns-recursive", "net.dns-authoritative", "supports", "A recursive resolver follows delegation to authoritative servers."),
    ("net-cache-resolver", "net.dns-cache", "net.dns-recursive", "supports", "A cache supports recursive resolution by reusing bounded prior answers."),
    ("net-ttl-cache", "net.dns-ttl", "net.dns-cache", "qualifies", "TTL qualifies how long cached DNS data can be reused."),
    ("net-alias-resolution", "net.dns-alias", "net.dns-recursive", "causes", "An alias causes an additional canonical-name resolution dependency."),
    ("net-negative-cache", "net.dns-negative", "net.dns-cache", "part_of", "Negative answers form a bounded class of cached DNS data."),
    ("net-dnssec-auth", "net.dnssec", "net.dns-authoritative", "supports", "DNSSEC supports validation of authoritative data origin and integrity."),
    ("net-resource-representation", "net.http-representation", "net.http-resource", "qualifies", "A representation describes selected resource state without becoming the resource identity."),
    ("net-request-method", "net.http-method", "net.http-request", "part_of", "A method supplies the request's primary protocol intent."),
    ("net-request-response", "net.http-request", "net.http-response", "causes", "Processing a request causes one or more response messages under HTTP semantics."),
    ("net-safe-method", "net.http-safe", "net.http-method", "qualifies", "Safety qualifies a method's intended client-requested effect."),
    ("net-idempotent-method", "net.http-idempotent", "net.http-method", "qualifies", "Idempotency qualifies repeated intended server effects."),
    ("net-status-response", "net.http-status", "net.http-response", "part_of", "A status code forms part of an HTTP response."),
    ("net-field-message", "net.http-field", "net.http-request", "part_of", "Request fields carry request metadata."),
    ("net-negotiation-representation", "net.content-negotiation", "net.http-representation", "causes", "Content negotiation causes selection among available representations."),
    ("net-validator-cache", "net.cache-validator", "net.http-cache", "supports", "Validators support revalidation of cached responses."),
    ("net-intermediary-cache", "net.http-intermediary", "net.http-cache", "enables", "An intermediary can enable shared caching under authorization and variation rules."),
    ("net-http2-tcp", "net.http2", "net.tcp-connection", "part_of", "HTTP/2 commonly multiplexes streams over a TCP connection."),
    ("net-http3-quic", "net.http3", "net.quic-connection", "part_of", "HTTP/3 maps HTTP messages onto QUIC streams."),
    ("net-interference-loss", "net.wireless-interference", "net.loss", "causes", "Severe interference can cause frame errors, retries, and observed packet loss."),
    ("net-association-subnet", "net.wireless-association", "net.subnet", "enables", "Wireless association enables link participation but only later configuration establishes subnet reachability."),
    ("net-roaming-path", "net.wireless-roaming", "net.path-migration", "enables", "A changed wireless attachment can enable or require transport path migration."),
    ("net-sdn-control", "net.sdn-controller", "net.control-plane", "implements", "An SDN controller implements a programmatic routing and policy control plane."),
    ("net-rule-forward", "net.flow-rule", "net.forwarding-table", "implements", "Flow rules implement packet actions in a programmable forwarding plane."),
    ("net-vpc-subnet", "net.subnet", "net.cloud-vpc", "part_of", "Cloud subnets compose a virtual private cloud's address and routing space."),
    ("net-discovery-load", "net.service-discovery", "net.cloud-load-balancer", "supports", "Service discovery supports selection of current load-balancer or backend endpoints."),
    ("net-overlay-mtu", "net.overlay", "net.path-mtu", "qualifies", "Encapsulation overhead qualifies usable path MTU for overlay payloads."),
    ("net-egress-flow", "net.egress", "net.flow-log", "measures", "Flow logs can measure selected metadata about network egress."),
    ("net-capture-packet", "net.packet-capture", "net.packet", "measures", "A packet capture measures packets visible at one interface and time."),
    ("net-trace-latency", "net.distributed-trace", "net.latency", "measures", "Trace spans measure selected application and network latency components."),
    ("net-clock-trace", "net.clock-boundary", "net.distributed-trace", "qualifies", "Clock uncertainty qualifies cross-host trace ordering and one-way duration."),
    ("net-bandwidth-throughput", "net.bandwidth", "net.throughput", "qualifies", "Available bandwidth upper-bounds throughput before overhead and competing demand."),
    ("net-queue-latency", "net.queue", "net.latency", "causes", "Queue occupancy causes additional waiting latency."),
    ("net-queue-loss", "net.queue", "net.loss", "causes", "A full queue can cause packet discard or marking."),
    ("net-jitter-latency", "net.jitter", "net.latency", "measures", "Jitter measures variation across latency or inter-arrival observations."),
    ("net-bdp-flow", "net.bdp", "net.flow-control", "qualifies", "Bandwidth-delay product qualifies the receive and send windows needed to fill a path."),
    ("net-bottleneck-throughput", "net.bottleneck", "net.throughput", "causes", "The current bottleneck constrains end-to-end throughput."),
    ("net-backpressure-queue", "net.backpressure", "net.queue", "prevents", "Effective backpressure prevents unbounded queue growth by slowing producers."),
    ("net-baseline-metric", "net.baseline", "net.network-metric", "qualifies", "A comparable baseline qualifies whether a metric is anomalous."),
    ("net-layer-localize", "net.layered-diagnosis", "net.binary-localization", "supports", "Layer boundaries support systematic fault-domain localization."),
    ("net-dns-trouble", "net.dns-diagnosis", "net.layered-diagnosis", "part_of", "DNS diagnosis is one branch of layered network troubleshooting."),
    ("net-mtu-trouble", "net.mtu-diagnosis", "net.layered-diagnosis", "part_of", "Path-MTU diagnosis is one branch of layered network troubleshooting."),
    ("sec-asset-risk", "sec.asset", "sec.risk", "prerequisite", "Identifying the affected asset is prerequisite to meaningful risk analysis."),
    ("sec-stakeholder-risk", "sec.stakeholder", "sec.risk", "qualifies", "Stakeholder consequence qualifies cybersecurity risk."),
    ("sec-threat-vulnerability", "sec.threat", "sec.vulnerability", "enables", "A threat with relevant capability can exploit a reachable vulnerability."),
    ("sec-vulnerability-exploit", "sec.vulnerability", "sec.exploit", "enables", "A vulnerability enables an exploit under its preconditions."),
    ("sec-exposure-exploit", "sec.exposure", "sec.exploit", "prerequisite", "Reachable exposure is prerequisite to a remote exploit path."),
    ("sec-exploit-risk", "sec.exploit", "sec.risk", "causes", "Successful exploitation can cause stakeholder harm represented in risk."),
    ("sec-surface-exposure", "sec.attack-surface", "sec.exposure", "part_of", "Exposed interfaces and dependencies compose an attack surface."),
    ("sec-boundary-model", "sec.trust-boundary", "sec.threat-model", "part_of", "Trust boundaries form part of a threat model."),
    ("sec-misuse-model", "sec.misuse-case", "sec.threat-model", "supports", "Misuse cases support explicit adversarial paths in a threat model."),
    ("sec-defense-control", "sec.defense-depth", "sec.control", "qualifies", "Defense in depth qualifies controls by independence and failure coverage."),
    ("sec-least-risk", "sec.least-privilege", "sec.risk", "inhibits", "Least privilege inhibits exploit impact and lateral movement."),
    ("sec-failsafe-control", "sec.fail-safe", "sec.control", "qualifies", "Fail-safe behavior qualifies a control's response to missing or indeterminate state."),
    ("sec-mediation-authz", "sec.complete-mediation", "sec.authorization", "implements", "Complete mediation implements repeated authorization at the governing boundary."),
    ("sec-separation-impact", "sec.separation-duty", "sec.risk", "inhibits", "Separation of duties inhibits one identity from completing a high-impact chain."),
    ("sec-default-surface", "sec.secure-default", "sec.attack-surface", "inhibits", "Secure defaults inhibit unnecessary attack-surface exposure."),
    ("sec-control-residual", "sec.control", "sec.residual-risk", "qualifies", "Control effectiveness qualifies the residual risk that remains."),
    ("sec-key-aead", "sec.key", "sec.aead", "prerequisite", "Correctly scoped key material is prerequisite to authenticated encryption."),
    ("sec-entropy-csprng", "sec.entropy", "sec.csprng", "prerequisite", "Adequate seed entropy is prerequisite to unpredictable generator output."),
    ("sec-nonce-aead", "sec.nonce", "sec.aead", "qualifies", "The construction's nonce rule qualifies safe authenticated-encryption use."),
    ("sec-hash-mac", "sec.hash", "sec.mac", "part_of", "A secure hash construction can form part of a message authentication code."),
    ("sec-kdf-key", "sec.kdf", "sec.key", "transforms_to", "A KDF transforms source keying material into context-separated keys."),
    ("sec-password-hash", "sec.password-hash", "sec.authentication", "supports", "Password hashing supports safer verifier storage for password authentication."),
    ("sec-sign-authenticity", "sec.signature", "sec.authenticity", "supports", "A valid signature under trusted key binding supports artifact authenticity."),
    ("sec-cert-sign", "sec.certificate", "sec.signature", "supports", "A validated certificate supports binding a verification key to named identity attributes."),
    ("sec-lifecycle-key", "sec.key-lifecycle", "sec.key", "qualifies", "Lifecycle controls qualify when and where a key remains trustworthy."),
    ("sec-forward-tls", "sec.forward-secrecy", "sec.tls-channel", "qualifies", "Forward secrecy qualifies the consequences of later long-term-key compromise for past TLS sessions."),
    ("sec-segment-surface", "sec.segmentation", "sec.attack-surface", "inhibits", "Segmentation inhibits reachable compromise paths across zones."),
    ("sec-firewall-boundary", "sec.firewall", "sec.trust-boundary", "implements", "A firewall implements network mediation at a trust boundary."),
    ("sec-allow-firewall", "sec.network-allowlist", "sec.firewall", "qualifies", "An allowlist qualifies firewall policy toward explicit permitted flows."),
    ("sec-detect-incident", "sec.ids", "sec.incident-detection", "supports", "Intrusion-detection signals support incident detection hypotheses."),
    ("sec-ips-control", "sec.ips", "sec.control", "implements", "Intrusion prevention implements a blocking security control."),
    ("sec-ddos-availability", "sec.ddos", "sec.availability", "supports", "Layered denial-of-service resistance supports service availability."),
    ("sec-egress-exfil", "sec.secure-egress", "sec.data-minimization", "supports", "Secure egress supports limiting unauthorized data transfer."),
    ("sec-vpn-tls", "sec.vpn", "sec.tls-channel", "analogous_to", "VPN and TLS channels both protect traffic across untrusted paths at different scopes."),
    ("sec-injection-control", "sec.parameterization", "sec.injection", "prevents", "Correct parameterization prevents data from changing supported command grammar."),
    ("sec-output-xss", "sec.output-encoding", "sec.xss", "prevents", "Contextual output encoding prevents attacker data from becoming executable markup or script in the encoded context."),
    ("sec-csrf-session", "sec.session-security", "sec.csrf", "qualifies", "Session and same-site controls qualify cross-site request-forgery exposure."),
    ("sec-ssrf-metadata", "sec.ssrf", "sec.metadata-service", "enables", "An unrestricted server-side fetch can enable access to cloud metadata services."),
    ("sec-validation-boundary", "sec.input-validation", "sec.trust-boundary", "implements", "Input validation implements semantic mediation at a trust boundary."),
    ("sec-authz-object", "sec.authorization-check", "sec.authorization", "implements", "Object-level checks implement authorization for a specific resource and tenant."),
    ("sec-secret-auth", "sec.secret-management", "sec.authentication", "supports", "Secret management supports credential integrity throughout authentication lifecycles."),
    ("sec-log-account", "sec.security-log", "sec.accountability", "supports", "Protected security logs support attribution and review."),
    ("sec-process-sandbox", "sec.process-isolation", "sec.sandbox", "supports", "Process isolation supports a sandbox boundary."),
    ("sec-memory-process", "sec.memory-protection", "sec.process-isolation", "implements", "Page permissions implement one mechanism of process isolation."),
    ("sec-priv-sandbox", "sec.least-privilege", "sec.sandbox", "supports", "Least privilege supports limiting sandbox-reachable effects."),
    ("sec-patch-vuln", "sec.patch", "sec.vulnerability", "prevents", "A correctly deployed security patch prevents exploitation of the repaired vulnerable behavior."),
    ("sec-shared-cloud", "sec.shared-responsibility", "sec.cloud-iam", "qualifies", "The cloud service model qualifies who owns each identity control."),
    ("sec-public-policy", "sec.cloud-iam", "sec.public-storage", "prevents", "Least-privilege storage policy prevents unintended public access."),
    ("sec-subject-authn", "sec.subject", "sec.authentication", "prerequisite", "A claimed subject identity is prerequisite to authentication."),
    ("sec-authn-authz", "sec.authentication", "sec.authorization", "prerequisite", "Many authorization decisions require authenticated subject context."),
    ("sec-mfa-authn", "sec.mfa", "sec.authentication", "supports", "Independent factors support stronger authentication under the modeled attacks."),
    ("sec-federation-authn", "sec.federation", "sec.authentication", "supports", "Validated federated assertions support authentication across administrative domains."),
    ("sec-rbac-authz", "sec.rbac", "sec.authorization", "implements", "Role assignments implement one form of authorization policy."),
    ("sec-abac-authz", "sec.abac", "sec.authorization", "implements", "Attribute policy implements context-sensitive authorization."),
    ("sec-zero-mediation", "sec.zero-trust", "sec.complete-mediation", "supports", "Zero-trust architecture supports continuous resource-centered mediation."),
    ("sec-handshake-channel", "sec.tls-handshake", "sec.tls-channel", "causes", "A successfully validated TLS handshake causes establishment of traffic keys and channel state."),
    ("sec-cert-handshake", "sec.certificate-validation", "sec.tls-handshake", "part_of", "Certificate validation forms part of authenticated TLS handshakes using certificates."),
    ("sec-replay-nonce", "sec.nonce", "sec.replay", "prevents", "Freshness or uniqueness mechanisms can prevent acceptance of replayed messages."),
    ("sec-downgrade-handshake", "sec.tls-handshake", "sec.downgrade", "prevents", "Transcript-bound negotiation prevents supported TLS parameters from being silently downgraded."),
    ("sec-auth-repro", "sec.research-authorization", "sec.repro-case", "qualifies", "Authorization qualifies the target, method, and data permitted in a vulnerability reproducer."),
    ("sec-repro-root", "sec.repro-case", "sec.root-cause", "supports", "A minimal reproducer supports isolation of a vulnerability root cause."),
    ("sec-root-patch", "sec.root-cause", "sec.patch", "supports", "Root-cause analysis supports a repair that addresses the enabling weakness."),
    ("sec-report-disclosure", "sec.responsible-report", "sec.coordinated-disclosure", "implements", "A responsible report implements the evidence transfer needed for coordinated disclosure."),
    ("sec-prepare-detect", "sec.incident-preparation", "sec.incident-detection", "enables", "Prepared telemetry and roles enable effective incident detection."),
    ("sec-detect-analysis", "sec.incident-detection", "sec.incident-analysis", "causes", "A credible detection triggers incident analysis."),
    ("sec-analysis-contain", "sec.incident-analysis", "sec.containment", "qualifies", "Analysis qualifies which containment action limits harm without destroying needed evidence."),
    ("sec-contain-eradicate", "sec.containment", "sec.eradication", "prerequisite", "Containment is often prerequisite to safely eradicating persistent causes."),
    ("sec-eradicate-recover", "sec.eradication", "sec.recovery", "prerequisite", "Removing known persistence is prerequisite to trusted recovery."),
    ("sec-recover-lessons", "sec.recovery", "sec.lessons", "causes", "Recovery evidence and residual gaps cause concrete lessons-learned actions."),
    ("sec-custody-analysis", "sec.chain-custody", "sec.incident-analysis", "supports", "Chain-of-custody records support confidence in incident evidence handling."),
    ("sec-min-purpose", "sec.data-minimization", "sec.purpose-limitation", "supports", "Data minimization supports enforcement of declared purpose."),
    ("sec-retention-min", "sec.retention", "sec.data-minimization", "implements", "Bounded retention implements temporal data minimization."),
    ("sec-pseudo-anon", "sec.pseudonymization", "sec.anonymization", "undercuts", "Residual re-linking in pseudonymized data undercuts a claim of anonymity."),
    ("sec-privacy-model", "sec.privacy-threat-model", "sec.threat-model", "analogous_to", "Privacy and security threat models share causal analysis while protecting partly different interests."),
    ("sec-provenance-sign", "sec.provenance", "sec.artifact-signing", "supports", "Recorded provenance supports interpreting what an artifact signature attests."),
    ("sec-sbom-provenance", "sec.sbom", "sec.provenance", "part_of", "Component relationships form part of software provenance."),
    ("sec-repro-sign", "sec.repro-build", "sec.artifact-signing", "supports", "Reproducibility supports comparison between signed artifacts and declared source builds."),
    ("sec-pin-update", "sec.dependency-pin", "sec.update-chain", "qualifies", "Pinned dependencies qualify which updates must be deliberately resolved and verified."),
    ("sec-auth-scope", "sec.authorized-scope", "sec.research-authorization", "grounds", "Owner authorization grounds the permitted security-research scope."),
    ("sec-minimum-lab", "sec.minimum-harm", "sec.safe-lab", "supports", "An isolated lab supports minimum-harm testing."),
    ("sec-stop-scope", "sec.stop-condition", "sec.authorized-scope", "prevents", "Stop conditions prevent continued testing when authorization becomes uncertain."),
    ("web-html-parser", "web.html-parser", "web.html-document", "transforms_to", "The HTML parser transforms input bytes and tokens into a document tree."),
    ("web-element-semantic", "web.semantic-html", "web.html-element", "qualifies", "Semantic intent qualifies element selection."),
    ("web-form-element", "web.form-control", "web.html-element", "part_of", "Form controls are interactive HTML elements with submission behavior."),
    ("web-custom-dom", "web.custom-element", "web.dom-node", "transforms_to", "Registration upgrades matching DOM elements into custom elements."),
    ("web-rule-cascade", "web.css-rule", "web.cascade", "part_of", "Matching declarations from CSS rules enter the cascade."),
    ("web-specific-cascade", "web.specificity", "web.cascade", "qualifies", "Specificity qualifies precedence within the relevant cascade tier."),
    ("web-cascade-computed", "web.cascade", "web.computed-value", "causes", "The winning declaration contributes to computed-value resolution."),
    ("web-inherit-computed", "web.inheritance", "web.computed-value", "causes", "Inheritance can supply a computed value from the parent."),
    ("web-box-layout", "web.box-model", "web.layout", "part_of", "Box edges and sizing participate in layout geometry."),
    ("web-context-layout", "web.formatting-context", "web.layout", "qualifies", "The formatting context qualifies box placement and sizing rules."),
    ("web-block-layout", "web.containing-block", "web.layout", "qualifies", "Containing blocks qualify coordinate and percentage resolution."),
    ("web-stack-paint", "web.stacking-context", "web.paint", "qualifies", "Stacking contexts qualify paint order."),
    ("web-responsive-layout", "web.responsive-layout", "web.layout", "transforms_to", "Responsive constraints transform layout as available space changes."),
    ("web-context-stack", "web.execution-context", "web.call-stack", "part_of", "Active execution contexts compose the JavaScript call stack."),
    ("web-realm-context", "web.js-realm", "web.execution-context", "qualifies", "A realm qualifies globals and intrinsics used by an execution context."),
    ("web-loop-task", "web.task", "web.event-loop", "part_of", "Tasks are selected by an event loop."),
    ("web-microtask-loop", "web.microtask", "web.event-loop", "part_of", "Microtasks drain at event-loop checkpoints."),
    ("web-promise-micro", "web.promise", "web.microtask", "causes", "Promise settlement queues eligible reaction microtasks."),
    ("web-jit-context", "web.jit", "web.execution-context", "implements", "JIT-compiled code implements execution under guarded assumptions."),
    ("web-node-tree", "web.dom-node", "web.document-tree", "part_of", "DOM nodes compose the document tree."),
    ("web-target-dispatch", "web.event-target", "web.event-dispatch", "prerequisite", "An event target is prerequisite to listener dispatch."),
    ("web-dispatch-default", "web.event-dispatch", "web.default-action", "qualifies", "Cancellation during dispatch qualifies whether a default action proceeds."),
    ("web-abort-fetch", "web.abort-signal", "web.fetch-request", "inhibits", "An abort signal inhibits further cooperative fetch processing without undoing completed external effects."),
    ("web-mutation-micro", "web.mutation-observer", "web.microtask", "part_of", "Mutation-observer callbacks are delivered during microtask processing."),
    ("web-shadow-event", "web.shadow-tree", "web.event-dispatch", "qualifies", "Shadow boundaries qualify event paths and retargeting."),
    ("web-parse-tree", "web.parse-pipeline", "web.document-tree", "causes", "Parsing causes incremental document-tree construction."),
    ("web-tree-style", "web.document-tree", "web.style-calculation", "prerequisite", "Document structure is prerequisite to selector matching and style calculation."),
    ("web-style-layout", "web.style-calculation", "web.layout", "prerequisite", "Resolved style is prerequisite to most layout calculations."),
    ("web-layout-paint", "web.layout", "web.paint", "prerequisite", "Layout geometry is prerequisite to painting positioned fragments."),
    ("web-paint-compose", "web.paint", "web.compositing", "prerequisite", "Painted or rasterized layer content is prerequisite to final compositing."),
    ("web-invalidate-style", "web.invalidation", "web.style-calculation", "causes", "Relevant mutations cause style invalidation and recalculation."),
    ("web-frame-pipeline", "web.frame-budget", "web.compositing", "qualifies", "The display frame budget qualifies when pipeline work becomes visible jank."),
    ("web-request-response", "web.fetch-request", "web.fetch-response", "causes", "Fetch processing produces a response or network error."),
    ("web-cors-response", "web.cors", "web.fetch-response", "qualifies", "CORS qualifies which cross-origin response data script can observe."),
    ("web-preflight-cors", "web.preflight", "web.cors", "part_of", "Preflight is one authorization exchange in CORS processing."),
    ("web-credential-request", "web.credential-mode", "web.fetch-request", "qualifies", "Credential mode qualifies whether credentials accompany a fetch."),
    ("web-redirect-request", "web.redirect", "web.fetch-request", "transforms_to", "Redirect processing transforms a request into a bounded follow-up request."),
    ("web-cache-fetch", "web.browser-cache", "web.fetch-response", "supports", "A reusable cached response can satisfy fetch processing."),
    ("web-navigation-fetch", "web.navigation", "web.fetch-request", "causes", "Navigation causes document-fetch and policy processing."),
    ("web-cookie-fetch", "web.cookie", "web.credential-mode", "qualifies", "Cookie eligibility is qualified by fetch credentials and cookie scope."),
    ("web-idb-storage", "web.indexeddb", "web.storage-partition", "qualifies", "Storage partition keys qualify IndexedDB availability across contexts."),
    ("web-cache-storage", "web.cache-storage", "web.service-worker", "supports", "Cache Storage supports service-worker offline response strategies."),
    ("web-worker-fetch", "web.service-worker", "web.fetch-request", "qualifies", "A controlling service worker can qualify a request by intercepting fetch processing."),
    ("web-lifecycle-worker", "web.sw-lifecycle", "web.service-worker", "transforms_to", "Lifecycle events transform a registration among installing, waiting, active, and redundant workers."),
    ("web-origin-same", "web.origin", "web.same-origin", "grounds", "Origin identity grounds same-origin access decisions."),
    ("web-site-origin", "web.origin", "web.site", "part_of", "Multiple origins can belong to one site."),
    ("web-csp-xss", "web.csp", "sec.xss", "inhibits", "A restrictive CSP inhibits classes of script execution after an injection flaw."),
    ("web-sandbox-origin", "web.iframe-sandbox", "web.origin", "transforms_to", "Sandboxing can transform an embedded document into an opaque origin."),
    ("web-mixed-tls", "sec.tls-channel", "web.mixed-content", "prevents", "Secure subresource transport prevents active mixed-content exposure."),
    ("web-sri-auth", "web.sri", "sec.authenticity", "supports", "A matching integrity digest supports byte identity for a fetched subresource."),
    ("web-permission-authz", "web.permissions", "sec.authorization", "implements", "Browser permission state implements authorization for selected powerful capabilities."),
    ("web-trusted-xss", "web.trusted-types", "sec.xss", "inhibits", "Trusted Types inhibits string flow into selected script-capable DOM sinks."),
    ("web-partition-tracking", "web.storage-partition", "web.tracking", "inhibits", "Partitioned state inhibits passive cross-site identifier reuse."),
    ("web-fingerprint-track", "web.fingerprinting", "web.tracking", "enables", "A sufficiently stable fingerprint enables probabilistic cross-context linkage."),
    ("web-referrer-privacy", "web.referrer", "web.tracking", "inhibits", "A restrictive referrer policy inhibits source-URL disclosure across contexts."),
    ("web-semantics-a11y", "web.semantic-html", "web.a11y-tree", "supports", "Native element semantics support construction of the accessibility tree."),
    ("web-name-tree", "web.accessible-name", "web.a11y-tree", "part_of", "Accessible names form part of exposed accessibility semantics."),
    ("web-focus-keyboard", "web.focus", "web.keyboard", "supports", "Managed visible focus supports keyboard operability."),
    ("web-aria-tree", "web.aria", "web.a11y-tree", "qualifies", "ARIA attributes qualify exposed roles, states, and relationships."),
    ("web-motion-access", "web.reduced-motion", "web.frame-budget", "qualifies", "Reduced-motion preference qualifies animation and transition design."),
    ("web-manifest-permission", "web.extension-permission", "web.extension-manifest", "part_of", "Declared extension permissions form part of the manifest contract."),
    ("web-content-dom", "web.content-script", "web.document-tree", "qualifies", "A content script can read or mutate the shared DOM under host permission."),
    ("web-worker-message", "web.extension-worker", "web.extension-message", "supports", "Extension messaging supports coordination with an ephemeral background worker."),
    ("web-message-boundary", "web.extension-message", "sec.trust-boundary", "implements", "Extension message receivers implement a trust boundary requiring validation."),
    ("web-standard-conformance", "web.living-standard", "web.conformance", "qualifies", "A living-standard snapshot qualifies the exact conformance target."),
    ("web-test-interoperability", "web.wpt", "web.interoperability", "measures", "Shared web-platform tests measure selected observable interoperability."),
    ("web-progressive-conformance", "web.progressive-enhancement", "web.semantic-html", "supports", "Semantic HTML supports progressive enhancement when optional behavior fails."),
    ("bridge-dns-browser", "net.dns-recursive", "web.fetch-request", "prerequisite", "Name resolution is often prerequisite to establishing the network endpoint for a browser fetch."),
    ("bridge-http-fetch", "net.http-request", "web.fetch-request", "analogous_to", "Fetch request state maps onto HTTP request semantics but includes additional browser policy."),
    ("bridge-tls-fetch", "sec.tls-channel", "web.fetch-response", "qualifies", "Validated transport security qualifies whether a response is delivered in a secure context."),
    ("bridge-origin-http", "web.origin", "net.http-resource", "qualifies", "Origin partitions authority over HTTP resources by scheme, host, and port."),
    ("bridge-cors-same", "web.cors", "web.same-origin", "qualifies", "CORS creates narrow response-sharing exceptions without removing the same-origin policy."),
    ("bridge-mtu-browser", "net.path-mtu", "web.fetch-request", "qualifies", "Path-MTU failure can qualify a size-dependent browser fetch symptom."),
    ("bridge-observe-incident", "net.flow-log", "sec.incident-analysis", "supports", "Versioned flow metadata can support incident timeline and scope analysis."),
    ("bridge-extension-least", "sec.least-privilege", "web.extension-permission", "qualifies", "Least privilege qualifies which extension permissions are justified."),
    ("bridge-cache-privacy", "net.http-cache", "web.storage-partition", "qualifies", "Privacy partitioning qualifies which HTTP cache state can be reused across top-level contexts."),
]


CONTROLS = [
    ("net-layer-name", "networking", "networking.troubleshooting", NETWORK_LANES, "Layer-name diagnosis", "Naming a network layer without discriminating evidence must not count as locating the failure."),
    ("net-ping-proof", "networking", "networking.troubleshooting", NETWORK_LANES, "Ping proves service health", "An ICMP echo reply must not be treated as proof that DNS, transport, TLS, HTTP, or application behavior is healthy."),
    ("net-no-ping-down", "networking", "networking.troubleshooting", NETWORK_LANES, "No ping means host down", "Missing echo replies must not prove a host is down when policy, path, or protocol support can suppress them."),
    ("net-private-secure", "networking", "networking.cloud", NETWORK_LANES, "Private address means secure", "A private or internal address must not be treated as authorization, encryption, or endpoint trust."),
    ("net-association-internet", "networking", "networking.wireless", NETWORK_LANES, "Association means Internet", "Wireless association alone must not be reported as end-to-end Internet reachability."),
    ("net-bandwidth-throughput", "networking", "networking.performance", NETWORK_LANES, "Bandwidth equals throughput", "Nominal link bandwidth must not be substituted for measured application throughput."),
    ("net-loss-congestion", "networking", "networking.performance", NETWORK_LANES, "All loss is congestion", "Packet loss must not be attributed to congestion without excluding corruption, policy, path change, and measurement gaps."),
    ("net-capture-global", "networking", "networking.observability", NETWORK_LANES, "Capture proves global path", "A packet capture at one interface must not establish what every other path node received or emitted."),
    ("net-dns-endpoint", "networking", "networking.dns", NETWORK_LANES, "DNS success proves endpoint", "A DNS answer must not be treated as proof that the returned endpoint is reachable, authorized, or healthy."),
    ("net-cache-current", "networking", "networking.dns", NETWORK_LANES, "Cached data is current", "A cached answer within TTL must not be assumed to reflect an immediately changed authority state."),
    ("net-tcp-message", "networking", "networking.transport", NETWORK_LANES, "TCP preserves messages", "TCP byte-stream delivery must not be described as preserving application write boundaries."),
    ("net-udp-unusable", "networking", "networking.transport", NETWORK_LANES, "UDP means unreliable application", "UDP's lack of built-in reliability must not imply an application cannot implement appropriate reliability and congestion behavior."),
    ("net-http-status-business", "networking", "networking.http", NETWORK_LANES, "HTTP status proves business effect", "A success status must not alone prove that every asynchronous or external business consequence completed."),
    ("net-nat-firewall", "networking", "networking.ip-routing", NETWORK_LANES, "NAT is a firewall", "Address translation must not be treated as a security policy or complete traffic mediation."),
    ("sec-tool-authority", "cybersecurity", "cybersecurity.safety-ethics", SECURITY_LANES, "Tool availability grants authority", "Possession of a scanner, exploit, credential, or administrative tool must never be treated as authorization to use it on a target."),
    ("sec-scope-expand", "cybersecurity", "cybersecurity.safety-ethics", SECURITY_LANES, "Silent scope expansion", "Unexpected access or a neighboring vulnerable system must not broaden the authorized security-testing scope."),
    ("sec-persistence", "cybersecurity", "cybersecurity.safety-ethics", SECURITY_LANES, "Unneeded persistence", "Security validation must not install persistence when a reversible, nonpersistent reproducer can establish the finding."),
    ("sec-exfil-proof", "cybersecurity", "cybersecurity.safety-ethics", SECURITY_LANES, "Sensitive-data exfiltration as proof", "A finding must not be proven by copying unrelated sensitive data when synthetic markers or metadata evidence suffice."),
    ("sec-scan-safe", "cybersecurity", "cybersecurity.vulnerability-research", SECURITY_LANES, "Scanner is harmless", "Automated scanning must not be assumed safe without rate, state-change, target, and authorization analysis."),
    ("sec-cve-risk", "cybersecurity", "cybersecurity.vulnerability-research", SECURITY_LANES, "Severity equals local risk", "A vulnerability severity score must not replace environment-specific exposure, asset, control, and consequence analysis."),
    ("sec-encryption-authz", "cybersecurity", "cybersecurity.cryptography", SECURITY_LANES, "Encryption grants authorization", "An encrypted channel must not be treated as proof that an authenticated party is authorized for a requested action."),
    ("sec-hash-encryption", "cybersecurity", "cybersecurity.cryptography", SECURITY_LANES, "Hashing is encryption", "A one-way digest must not be described as reversible confidentiality protection."),
    ("sec-encoding-safety", "cybersecurity", "cybersecurity.application-security", SECURITY_LANES, "One encoding fits every sink", "Encoding safe for one interpreter context must not be reused as universal output sanitization."),
    ("sec-client-validation", "cybersecurity", "cybersecurity.application-security", SECURITY_LANES, "Client validation is authoritative", "Client-side validation must not substitute for server-side validation and authorization at the trusted boundary."),
    ("sec-authn-authz", "cybersecurity", "cybersecurity.identity-access", SECURITY_LANES, "Authentication implies authorization", "A verified identity must not be treated as permission to access every resource or action."),
    ("sec-mfa-perfect", "cybersecurity", "cybersecurity.identity-access", SECURITY_LANES, "MFA eliminates account risk", "Multi-factor authentication must not be treated as eliminating phishing, session theft, recovery abuse, malware, or authorization errors."),
    ("sec-zero-product", "cybersecurity", "cybersecurity.identity-access", SECURITY_LANES, "Zero trust as a product", "Buying one product or removing one perimeter must not be reported as implementing a complete zero-trust architecture."),
    ("sec-tls-safe-app", "cybersecurity", "cybersecurity.secure-protocols", SECURITY_LANES, "TLS makes application safe", "A valid TLS channel must not be treated as repairing injection, authorization, endpoint compromise, or malicious content."),
    ("sec-cert-trust-all", "cybersecurity", "cybersecurity.secure-protocols", SECURITY_LANES, "Certificate means universally trusted", "A syntactically valid certificate must not establish identity outside name, chain, time, usage, and policy validation."),
    ("sec-log-truth", "cybersecurity", "cybersecurity.incident-response", SECURITY_LANES, "Log entry is complete truth", "A log record must not be treated as complete or untampered evidence without provenance, clock, collection, and integrity analysis."),
    ("sec-delete-eradicate", "cybersecurity", "cybersecurity.incident-response", SECURITY_LANES, "Deleting indicator equals eradication", "Removing one visible file or account must not count as eradication without closing persistence and root cause across scope."),
    ("sec-pseudo-anon", "cybersecurity", "cybersecurity.privacy", SECURITY_LANES, "Pseudonymous means anonymous", "Replacing direct identifiers must not be reported as anonymization while linkage or re-identification remains feasible."),
    ("sec-sbom-safe", "cybersecurity", "cybersecurity.supply-chain", SECURITY_LANES, "SBOM proves secure", "An SBOM must not be treated as proof that components are complete, uncompromised, vulnerability-free, or safely configured."),
    ("sec-sign-benign", "cybersecurity", "cybersecurity.supply-chain", SECURITY_LANES, "Signature proves benign", "A valid signature proves a key assertion about bytes, not that those bytes are safe or correctly built."),
    ("web-div-button", "browser-web-platform", "browser-web-platform.accessibility", BROWSER_LANES, "Styled div equals button", "A visually styled generic element must not be treated as a button without semantic role, keyboard behavior, focus, state, and activation semantics."),
    ("web-aria-fix", "browser-web-platform", "browser-web-platform.accessibility", BROWSER_LANES, "ARIA fixes all accessibility", "ARIA attributes must not be treated as adding missing keyboard interaction, focus management, contrast, or usable language."),
    ("web-cors-firewall", "browser-web-platform", "browser-web-platform.security", BROWSER_LANES, "CORS is server firewall", "CORS must not be treated as preventing non-browser clients from sending requests or as server authentication."),
    ("web-csp-fix", "browser-web-platform", "browser-web-platform.security", BROWSER_LANES, "CSP fixes injection", "Content Security Policy must not substitute for eliminating unsafe data-to-code flows."),
    ("web-shadow-security", "browser-web-platform", "browser-web-platform.dom-events", BROWSER_LANES, "Shadow DOM is security isolation", "Shadow DOM encapsulation must not be treated as a confidentiality or authorization boundary."),
    ("web-local-secret", "browser-web-platform", "browser-web-platform.storage", BROWSER_LANES, "Browser storage is secret storage", "Origin-scoped browser storage must not be treated as safe storage for long-lived secrets against same-origin script compromise."),
    ("web-service-permanent", "browser-web-platform", "browser-web-platform.storage", BROWSER_LANES, "Service worker is permanent process", "A service worker must not depend on in-memory globals surviving between events."),
    ("web-microtask-parallel", "browser-web-platform", "browser-web-platform.javascript-runtime", BROWSER_LANES, "Microtasks run in parallel", "Promise reactions and microtasks on one event loop must not be described as parallel execution."),
    ("web-timeout-exact", "browser-web-platform", "browser-web-platform.javascript-runtime", BROWSER_LANES, "Timer delay is exact schedule", "A timer delay must not be interpreted as an exact execution time under task queues, throttling, and suspension."),
    ("web-css-specificity", "browser-web-platform", "browser-web-platform.css", BROWSER_LANES, "Specificity beats everything", "Specificity must not be treated as stronger than origin, importance, cascade layer, or relevant scoping order."),
    ("web-dom-pixels", "browser-web-platform", "browser-web-platform.rendering", BROWSER_LANES, "DOM mutation immediately changes pixels", "A DOM mutation must not be treated as synchronous display; style, layout, paint, compositing, and presentation intervene."),
    ("web-origin-site", "browser-web-platform", "browser-web-platform.security", BROWSER_LANES, "Origin equals site", "An origin and a site must not be treated as identical security principals."),
    ("web-https-trust", "browser-web-platform", "browser-web-platform.security", BROWSER_LANES, "HTTPS means trustworthy content", "A secure transport and validated host identity must not be treated as proof that page content or operator intent is benign."),
    ("web-one-browser", "browser-web-platform", "browser-web-platform.standards", BROWSER_LANES, "One browser defines standard", "Observed behavior in one browser version must not be reported as the normative web-platform requirement."),
]


WORKED_EXAMPLES = [
    ("net", "layered-outage", "Layered outage diagnosis", "A host resolves a name and completes TCP but receives a TLS name error, so the diagnosis retains link, IP, DNS, and TCP as working observations and localizes the failed identity check.", "networking.troubleshooting", NETWORK_LANES, NETWORK_SOURCES),
    ("net", "mtu-black-hole", "Path-MTU black-hole diagnosis", "Small requests succeed while larger protected records stall; a bounded size sweep plus missing size feedback supports a path-MTU hypothesis without declaring all loss to be MTU-related.", "networking.troubleshooting", NETWORK_LANES, NETWORK_SOURCES),
    ("net", "queue-delay", "Queue-delay composition", "A worked path adds propagation, serialization, processing, and measured queue delay, then predicts increased tail latency when arrival rate approaches the bottleneck service rate.", "networking.performance", NETWORK_LANES, NETWORK_SOURCES),
    ("sec", "threat-model", "Bounded threat model", "A worked model identifies a signing key as the asset, CI and release boundaries as entry points, a compromised dependency as one actor path, and independent build attestation as a limiting control.", "cybersecurity.security-principles", SECURITY_LANES, SECURITY_SOURCES),
    ("sec", "authz-counterexample", "Authentication-authority counterexample", "A valid user session requests another tenant's object; identity is established but the object-level policy denies access, demonstrating that authentication is not authorization.", "cybersecurity.identity-access", SECURITY_LANES, SECURITY_SOURCES),
    ("sec", "incident-timeline", "Incident evidence timeline", "A worked timeline records clock uncertainty, immutable source hashes, competing initial-access hypotheses, containment decisions, and evidence that later rules out one hypothesis.", "cybersecurity.incident-response", SECURITY_LANES, SECURITY_SOURCES),
    ("sec", "safe-reproducer", "Safe vulnerability reproducer", "A worked reproducer uses an owned fixture and synthetic marker, proves unauthorized read scope, stops before unrelated data access, and records the root-cause boundary for repair.", "cybersecurity.vulnerability-research", SECURITY_LANES, SECURITY_SOURCES),
    ("web", "event-order", "Event-loop ordering", "A worked trace runs synchronous script, drains queued promise reactions, reaches the rendering opportunity, and only then selects the next timer task.", "browser-web-platform.javascript-runtime", BROWSER_LANES, BROWSER_SOURCES),
    ("web", "render-invalidation", "Rendering invalidation", "A class change invalidates matching style, changes intrinsic width, triggers layout and paint, and reuses an unaffected composited layer.", "browser-web-platform.rendering", BROWSER_LANES, BROWSER_SOURCES),
    ("web", "cors-boundary", "CORS boundary example", "A cross-origin request reaches the server but the response lacks the authorizing CORS field, so browser script cannot read it; the example distinguishes network delivery from response exposure.", "browser-web-platform.networking", BROWSER_LANES, BROWSER_SOURCES),
    ("web", "accessible-control", "Accessible custom control", "A worked control supplies native button semantics where possible, visible focus, keyboard activation, an accessible name, and synchronized disabled state.", "browser-web-platform.accessibility", BROWSER_LANES, BROWSER_SOURCES),
    ("web", "service-worker-update", "Service-worker update lifecycle", "A new worker installs and waits while existing clients remain controlled by the prior active worker, then activates after the lifecycle permits a coherent transition.", "browser-web-platform.storage", BROWSER_LANES, BROWSER_SOURCES),
]


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 37 == 0:
        return "cross_domain_holdout"
    if index % 29 == 0:
        return "sealed_test"
    if index % 19 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 31 == 0:
        return "cross_domain_holdout"
    if index and index % 23 == 0:
        return "sealed_test"
    if index and index % 17 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    domain: str,
    subject: str,
    lanes: list[str],
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": sorted(set(lanes)),
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "networking, cybersecurity, and browser-platform foundation tranche",
        "limitations": [
            "Versioned protocol and platform behavior must be refreshed against current standards and verified implementations.",
            "Security content is defensive and authorization-bound; operational attack detail remains limited to owned or explicitly authorized fixtures.",
            "Specialist protocols, vendor behavior, and the open discovery frontier remain incomplete.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "network-security-browser-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def relation_owner(identifier: str) -> tuple[str, str, str, list[str], list[str]]:
    if identifier.startswith("net-"):
        return "networking", "networking.troubleshooting", "established", NETWORK_LANES, NETWORK_SOURCES
    if identifier.startswith("sec-"):
        return "cybersecurity", "cybersecurity.security-principles", "established", SECURITY_LANES, SECURITY_SOURCES
    if identifier.startswith("web-"):
        return "browser-web-platform", "browser-web-platform.standards", "established", BROWSER_LANES, BROWSER_SOURCES
    return (
        "browser-web-platform",
        "browser-web-platform.networking",
        "established",
        sorted(set(NETWORK_LANES + SECURITY_LANES + BROWSER_LANES)),
        sorted(set(NETWORK_SOURCES + SECURITY_SOURCES + BROWSER_SOURCES)),
    )


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    groups = [
        ("net", "networking", NETWORK, NETWORK_LANES, NETWORK_SOURCES),
        ("sec", "cybersecurity", SECURITY, SECURITY_LANES, SECURITY_SOURCES),
        ("web", "browser-web-platform", BROWSER, BROWSER_LANES, BROWSER_SOURCES),
    ]
    roots = {"net": "net.root", "sec": "sec.root", "web": "web.root"}
    domains = {"net": "networking", "sec": "cybersecurity", "web": "browser-web-platform"}

    for prefix, domain, entries, lanes, sources in groups:
        for index, (identifier, label, statement, subject) in enumerate(entries):
            node_id = f"{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        node_id, domain, subject, lanes, sources,
                        split_for(index, root=identifier == "root"), "concept", "established",
                    ),
                    "label": label,
                    "statement": statement,
                    "aliases": [label.lower()],
                }
            )
            if identifier == "root":
                continue
            membership_id = f"nsb.membership.{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        membership_id, domain, subject, lanes, sources,
                        edge_split_for(index), "relation", "established",
                    ),
                    "label": f"{label} world membership",
                    "statement": f"{label} is a distinct component of the {domain} causal world with versioned scope and explicit failure conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": roots[prefix],
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared foundation-world scope and version apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in RELATIONS])
    for identifier, source, target, kind, statement in RELATIONS:
        domain, subject, epistemic, lanes, sources = relation_owner(identifier)
        split = splitter.split(kind, cross_requested=identifier.startswith("bridge-"))
        records.append(
            {
                **make_base(
                    f"nsb.relation.{identifier}", domain, subject, lanes, sources,
                    split, "relation", epistemic,
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source,
                    "target_node": target,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["the stated topology, identity, protocol version, and threat assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, domain, subject, lanes, label, statement) in enumerate(CONTROLS):
        record_id = f"nsb.control.{identifier}"
        records.append(
            {
                **make_base(
                    record_id, domain, subject, lanes, [], control_splits[index % 4],
                    "synthetic_control", "synthetic_control",
                ),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", domain],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    source_by_prefix = {"net": NETWORK_SOURCES, "sec": SECURITY_SOURCES, "web": BROWSER_SOURCES}
    for index, (prefix, identifier, label, statement, subject, lanes, sources) in enumerate(WORKED_EXAMPLES):
        split = example_splits[index % 4]
        domain = domains[prefix]
        node_id = f"{prefix}.example.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, lanes, sources, split, "worked_example", "established"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", domain],
            }
        )
        membership_id = f"nsb.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(
                    membership_id, domain, subject, lanes, source_by_prefix[prefix],
                    split, "relation", "established",
                ),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded mechanism composition in the {domain} world.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": roots[prefix],
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains bounded and versioned"],
                    "exceptions": [],
                },
                "coverage_axes": ["applications_toolchains", "within_domain_composition"],
            }
        )

    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    counts: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
        kinds[record["record_kind"]] = kinds.get(record["record_kind"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records")
    print(f"splits: {dict(sorted(counts.items()))}")
    print(f"kinds: {dict(sorted(kinds.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
