#!/usr/bin/env python3
"""Author software-engineering, frontend, and mobile-app causal foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "software-app-development" / "foundations.jsonl"
WORLD = "software-app-development-v0"

SOFTWARE_LANES = ["thinking.bottom_up", "reasoning.causal", "reasoning.counterfactual", "creativity.constraint_based"]
FRONTEND_LANES = ["creativity.constraint_based", "geometry.structural", "thinking.bottom_up"]
MOBILE_LANES = ["thinking.bottom_up", "creativity.constraint_based", "geometry.structural"]

SOFTWARE_SOURCES = ["swebok-v4", "git-reference", "semver-200", "nist-sp800-218"]
FRONTEND_SOURCES = ["whatwg-html", "whatwg-dom", "whatwg-fetch", "w3c-wcag-22", "w3c-css-color-4"]
MOBILE_SOURCES = [
    "android-app-architecture", "android-studio", "android-compose", "android-build",
    "kotlin-documentation", "swift-language-guide", "apple-swiftui", "apple-xcode", "apple-accessibility",
]


SOFTWARE = [
    ("root", "Software-engineering system", "Software engineering turns stakeholder needs into maintained executable systems through explicit requirements, architecture, implementation, testing, release evidence, operation, security, and feedback.", "software-engineering.requirements"),
    ("stakeholder-need", "Stakeholder need", "A stakeholder need describes a valued outcome or avoided harm in the stakeholder's context before committing to a software mechanism.", "software-engineering.requirements"),
    ("requirement", "Software requirement", "A software requirement states a necessary observable capability, quality, interface, or constraint with scope and a testable satisfaction condition.", "software-engineering.requirements"),
    ("functional", "Functional requirement", "A functional requirement specifies behavior or state transformation the system must provide for a defined actor and condition.", "software-engineering.requirements"),
    ("quality", "Quality requirement", "A quality requirement makes performance, reliability, security, usability, accessibility, maintainability, or other properties measurable under a workload and environment.", "software-engineering.requirements"),
    ("constraint", "Engineering constraint", "A constraint limits technologies, interfaces, resources, laws, deadlines, or compatibility and should include its source and change authority.", "software-engineering.requirements"),
    ("acceptance", "Acceptance criterion", "An acceptance criterion defines setup, action, observable outcome, and tolerance sufficient to decide whether a requirement is met.", "software-engineering.requirements"),
    ("traceability", "Requirement traceability", "Traceability links need, requirement, design, code, test, result, and release so changes and proof can be followed in both directions.", "software-engineering.requirements"),
    ("architecture", "Software architecture", "Software architecture is the set of consequential structures, responsibilities, interfaces, dependencies, constraints, and decisions that shape system qualities and evolution.", "software-engineering.architecture"),
    ("component", "Software component", "A component owns a coherent responsibility behind an explicit interface and lifecycle boundary.", "software-engineering.architecture"),
    ("dependency", "Software dependency", "A dependency is a required service, library, platform, data contract, or build input whose availability and change can affect the consumer.", "software-engineering.architecture"),
    ("boundary", "System boundary", "A system boundary defines ownership, trust, deployment, failure, data, and compatibility transitions that require explicit contracts.", "software-engineering.architecture"),
    ("coupling", "Coupling", "Coupling is the degree to which one unit depends on another's identity, behavior, timing, data shape, or change pattern.", "software-engineering.architecture"),
    ("cohesion", "Cohesion", "Cohesion is the degree to which a unit's responsibilities and data serve one stable reason to change.", "software-engineering.architecture"),
    ("architecture-decision", "Architecture decision record", "An architecture decision record preserves context, decision, alternatives, consequences, status, and supersession rather than only the chosen mechanism.", "software-engineering.architecture"),
    ("modularity", "Modularity", "Modularity partitions behavior and knowledge into units whose interfaces constrain propagation of change.", "software-engineering.architecture"),
    ("layer", "Architectural layer", "A layer groups responsibilities at one abstraction level and constrains dependency direction; visual stacking alone does not create a layer.", "software-engineering.architecture"),
    ("event-driven", "Event-driven architecture", "Event-driven architecture communicates state-change facts or commands through asynchronous delivery and therefore must define identity, ordering, duplication, failure, and replay.", "software-engineering.architecture"),
    ("pattern", "Design pattern", "A design pattern names a recurring problem, forces, structure, consequences, and applicability rather than a universally superior code template.", "software-engineering.design-patterns"),
    ("strategy", "Strategy pattern", "Strategy encapsulates interchangeable algorithms behind one contract so selection can vary independently of callers.", "software-engineering.design-patterns"),
    ("adapter", "Adapter pattern", "An adapter translates one interface and semantic contract into another while making lossy mappings and failures explicit.", "software-engineering.design-patterns"),
    ("observer", "Observer pattern", "Observer propagates change notifications from a subject to subscribers and must define subscription lifecycle, ordering, failure, and reentrancy.", "software-engineering.design-patterns"),
    ("state-machine", "State-machine pattern", "A state machine makes allowed states, events, guards, transitions, effects, and invalid inputs explicit.", "software-engineering.design-patterns"),
    ("dependency-injection", "Dependency injection", "Dependency injection supplies a component's collaborators from outside its construction logic, making ownership and test substitution explicit.", "software-engineering.design-patterns"),
    ("pattern-tradeoff", "Pattern tradeoff", "A pattern is justified only when its forces and consequences fit the current context better than simpler alternatives.", "software-engineering.design-patterns"),
    ("test-oracle", "Test oracle", "A test oracle independently determines the expected observable result and must not merely duplicate the implementation under test.", "software-engineering.testing"),
    ("unit-test", "Unit test", "A unit test isolates a small behavior and its contract using controlled collaborators and fast deterministic execution.", "software-engineering.testing"),
    ("integration-test", "Integration test", "An integration test verifies contracts and behavior across real component boundaries under a controlled environment.", "software-engineering.testing"),
    ("system-test", "System test", "A system test exercises an assembled product through externally meaningful boundaries and representative configuration.", "software-engineering.testing"),
    ("property-test", "Property-based test", "A property-based test generates many inputs and shrinks failures against an invariant rather than enumerating only selected examples.", "software-engineering.testing"),
    ("metamorphic-test", "Metamorphic test", "A metamorphic test checks a relation among multiple executions when a direct expected output is unavailable.", "software-engineering.testing"),
    ("fuzz-test", "Fuzz test", "A fuzz test drives generated or mutated inputs through a bounded interface while detecting crashes, invariant violations, hangs, and sanitizer findings.", "software-engineering.testing"),
    ("regression-test", "Regression test", "A regression test reproduces a prior boundary failure and remains tied to the owning contract after the fix.", "software-engineering.testing"),
    ("test-pyramid", "Test portfolio", "A test portfolio balances fast local checks, boundary integration, end-to-end realism, negative cases, and production observations according to risk.", "software-engineering.testing"),
    ("formal-verification", "Formal verification", "Formal verification proves a stated property of a mathematical model under assumptions that must be connected to the implemented system.", "software-engineering.testing"),
    ("symptom", "Software symptom", "A symptom is an observable deviation and should be recorded separately from candidate causes and attempted fixes.", "software-engineering.debugging"),
    ("minimal-reproducer", "Minimal reproducer", "A minimal reproducer retains the smallest inputs, state, environment, and actions that still trigger the failure.", "software-engineering.debugging"),
    ("hypothesis", "Debugging hypothesis", "A debugging hypothesis predicts what evidence should change if a proposed cause is true and what observation would refute it.", "software-engineering.debugging"),
    ("bisect", "Change bisection", "Change bisection uses a reproducible oracle to divide an ordered revision interval and locate the first behavior-changing revision.", "software-engineering.debugging"),
    ("instrumentation", "Diagnostic instrumentation", "Instrumentation exposes state, timing, identity, causality, and errors with enough context to discriminate hypotheses while controlling overhead and sensitive data.", "software-engineering.debugging"),
    ("root-cause", "Software root cause", "A root cause is the enabling design, implementation, process, or assumption failure whose correction prevents the observed class, not merely the last visible error.", "software-engineering.debugging"),
    ("benchmark", "Software benchmark", "A benchmark measures a versioned workload, input distribution, environment, setup, warmup, repetitions, and statistic rather than a context-free speed number.", "software-engineering.performance"),
    ("latency", "Software latency", "Latency is elapsed time for a defined operation and should report distribution and tail behavior, not only a mean.", "software-engineering.performance"),
    ("throughput", "Software throughput", "Throughput is completed useful work per interval under a declared concurrency and workload.", "software-engineering.performance"),
    ("resource", "Resource utilization", "Resource utilization measures demand on CPU, memory, storage, network, accelerator, handles, or other bounded capacity at a defined vantage point.", "software-engineering.performance"),
    ("profile", "Performance profile", "A profile attributes sampled or instrumented cost to execution contexts and must be interpreted with sampling, optimization, and observer effects.", "software-engineering.performance"),
    ("complexity", "Algorithmic complexity", "Complexity characterizes resource growth with input size under a model and complements rather than replaces measured constants and system effects.", "software-engineering.performance"),
    ("capacity", "Capacity model", "A capacity model relates arrival rate, concurrency, service demand, queues, limits, and failure behavior to a target workload and margin.", "software-engineering.performance"),
    ("reliability", "Software reliability", "Reliability is the probability of correct service over a declared interval and operating conditions.", "software-engineering.reliability"),
    ("availability", "Service availability", "Availability is the fraction of relevant time or requests for which service meets a declared success criterion.", "software-engineering.reliability"),
    ("fault", "Fault", "A fault is an underlying defect or adverse condition that can activate into an erroneous internal state and later an observable failure.", "software-engineering.reliability"),
    ("failure", "Failure", "A failure is externally observable service behavior outside its specified contract.", "software-engineering.reliability"),
    ("redundancy", "Redundancy", "Redundancy supplies alternate resources or paths and improves reliability only when common-mode failures and coordination are controlled.", "software-engineering.reliability"),
    ("timeout", "Timeout", "A timeout bounds waiting but does not prove the remote action failed; the outcome may be unknown and require idempotency or reconciliation.", "software-engineering.reliability"),
    ("retry", "Retry policy", "A retry policy defines eligible errors, idempotency, attempt limit, backoff, jitter, budget, and final handling.", "software-engineering.reliability"),
    ("circuit-breaker", "Circuit breaker", "A circuit breaker temporarily rejects calls after evidence of dependency failure, then probes recovery under a defined state machine.", "software-engineering.reliability"),
    ("bulkhead", "Bulkhead isolation", "A bulkhead partitions capacity so exhaustion or failure in one workload does not consume every shared resource.", "software-engineering.reliability"),
    ("graceful-degradation", "Graceful degradation", "Graceful degradation preserves the highest-value safe behavior when dependencies or resources are impaired and clearly exposes reduced capability.", "software-engineering.reliability"),
    ("api-contract", "API contract", "An API contract defines operations, types, states, errors, compatibility, security, and side effects at a maintained boundary.", "software-engineering.api-design"),
    ("resource-model", "API resource model", "A resource model gives domain entities stable identities, relationships, lifecycle, and operations rather than mirroring database tables blindly.", "software-engineering.api-design"),
    ("idempotency", "API idempotency", "Idempotency ensures repeated equivalent requests do not compound the intended effect under a declared identity and retention window.", "software-engineering.api-design"),
    ("pagination", "API pagination", "Pagination defines ordering, cursor stability, page size, continuation, mutation interaction, and completion behavior.", "software-engineering.api-design"),
    ("error-contract", "API error contract", "An error contract supplies stable machine identity, human context, retryability, cause boundary, and remediation without leaking secrets.", "software-engineering.api-design"),
    ("compatibility", "Compatibility contract", "Compatibility defines which old clients, data, plugins, and behaviors continue to work across a change and which migration is required.", "software-engineering.api-design"),
    ("protocol-state", "Protocol state", "A protocol defines message grammar together with participant roles, state transitions, ordering, duplication, timing, and error handling.", "software-engineering.api-design"),
    ("commit", "Version-control commit", "A commit records a content tree, parents, authorship metadata, and message as an immutable object identity within the repository model.", "software-engineering.version-control"),
    ("branch", "Version-control branch", "A branch is a movable reference to a commit lineage rather than an independent copy of every file.", "software-engineering.version-control"),
    ("merge", "Three-way merge", "A three-way merge combines changes relative to a common base and requires semantic review even when text conflict markers are absent.", "software-engineering.version-control"),
    ("review", "Code review", "Code review evaluates correctness, security, clarity, tests, maintainability, and fit using a concrete diff and evidence while preserving accountable authorship.", "software-engineering.version-control"),
    ("build", "Software build", "A build transforms declared source, dependencies, configuration, and toolchains into artifacts with captured inputs and diagnostics.", "software-engineering.build-release"),
    ("artifact", "Release artifact", "A release artifact is an immutable, identified output whose bytes, provenance, platform, and compatibility are verified before promotion.", "software-engineering.build-release"),
    ("ci", "Continuous integration", "Continuous integration validates each change in a clean automated environment and reports reproducible evidence before merge or promotion.", "software-engineering.build-release"),
    ("release", "Software release", "A release promotes identified artifacts and metadata through approvals, distribution, migration, observation, and rollback readiness.", "software-engineering.build-release"),
    ("semantic-version", "Semantic version", "Semantic Versioning communicates compatibility changes to a declared public API through major, minor, patch, prerelease, and build metadata rules.", "software-engineering.build-release"),
    ("deployment", "Deployment", "Deployment places a release into an environment; it is distinct from exposing traffic, completing data migration, and verifying user-visible behavior.", "software-engineering.build-release"),
    ("canary", "Canary release", "A canary exposes an identified artifact to a bounded population and compares predefined health and outcome metrics before expanding.", "software-engineering.build-release"),
    ("rollback", "Release rollback", "Rollback restores a prior compatible application and data state or disables the new path, with limits declared for irreversible effects.", "software-engineering.build-release"),
    ("technical-debt", "Technical debt", "Technical debt is a deliberate or accidental design compromise that creates future cost, risk, or constrained options and should be tracked with consequence and owner.", "software-engineering.maintenance"),
    ("refactor", "Refactoring", "Refactoring changes internal structure while preserving declared externally observable behavior, verified by appropriate tests.", "software-engineering.maintenance"),
    ("migration", "Software migration", "A migration changes data, interface, platform, or architecture through staged compatibility, backfill, cutover, verification, and retirement.", "software-engineering.maintenance"),
    ("deprecation", "Deprecation", "Deprecation announces a supported path away from an interface with rationale, replacement, dates, telemetry, and eventual removal conditions.", "software-engineering.maintenance"),
    ("observability", "Software observability", "Observability provides evidence about internal state from metrics, logs, traces, profiles, and domain events designed around diagnostic questions.", "software-engineering.maintenance"),
    ("secure-lifecycle", "Secure development lifecycle", "A secure lifecycle integrates security requirements, threat modeling, protected environments, review, testing, provenance, response, and feedback across development.", "software-engineering.secure-development"),
    ("secure-review", "Security-focused review", "Security-focused review examines trust boundaries, identity, input, state, concurrency, secrets, dependencies, failure, and abuse cases in the actual change.", "software-engineering.secure-development"),
    ("dependency-governance", "Dependency governance", "Dependency governance records source, license, version, provenance, vulnerability status, update policy, transitive reach, and removal ownership.", "software-engineering.secure-development"),
    ("release-provenance", "Release provenance", "Release provenance binds an artifact to reviewed source, build identity, dependencies, environment, signer, and promotion evidence.", "software-engineering.secure-development"),
]


FRONTEND = [
    ("root", "Frontend application system", "Frontend engineering composes semantic documents, responsive visual layout, typed interaction logic, state, data, accessibility, performance, testing, design systems, build tools, and offline behavior at the browser boundary.", "frontend-web-development.semantic-html"),
    ("document-outline", "Semantic document outline", "A semantic document outline uses headings, landmarks, sections, and relationships to expose content structure independently of its visual arrangement.", "frontend-web-development.semantic-html"),
    ("native-control", "Native interactive control", "A native control supplies established semantics, focus, keyboard behavior, state, and form integration before custom enhancement.", "frontend-web-development.semantic-html"),
    ("form-model", "Frontend form model", "A form model connects labels, controls, help, validation, errors, submission, pending state, and server response without relying on color alone.", "frontend-web-development.semantic-html"),
    ("content-first", "Content-first structure", "Content-first structure establishes meaningful reading and task order before arranging presentation for particular viewports.", "frontend-web-development.semantic-html"),
    ("intrinsic-layout", "Intrinsic web layout", "Intrinsic layout lets content, available space, min-max constraints, and wrapping determine geometry before adding device-specific breakpoints.", "frontend-web-development.css-layout"),
    ("flex-layout", "Flexible box layout", "Flex layout distributes free space and aligns items primarily along one axis while allowing wrapping and intrinsic constraints.", "frontend-web-development.css-layout"),
    ("grid-layout", "Grid layout", "Grid layout defines two-dimensional tracks and placement relationships while content and available space resolve final track sizes.", "frontend-web-development.css-layout"),
    ("container-query", "Container query", "A container query adapts a component to the size or style of its containing context rather than the viewport alone.", "frontend-web-development.css-layout"),
    ("responsive-image", "Responsive image", "A responsive image supplies source candidates and selection hints so the browser can choose appropriate intrinsic dimensions, format, and density.", "frontend-web-development.css-layout"),
    ("logical-property", "CSS logical property", "Logical properties express layout relative to writing mode and text direction instead of assuming physical left-to-right geometry.", "frontend-web-development.css-layout"),
    ("progressive-css", "Progressive CSS enhancement", "Progressive CSS uses feature queries, fallbacks, and robust flow so unsupported decoration does not remove core content or tasks.", "frontend-web-development.css-layout"),
    ("module", "JavaScript module", "A JavaScript module has explicit imports, exports, evaluation ordering, and module identity under a loader and URL graph.", "frontend-web-development.javascript-typescript"),
    ("type-contract", "TypeScript type contract", "A TypeScript type describes checked source-level possibilities but is erased at runtime and cannot validate untrusted external data by itself.", "frontend-web-development.javascript-typescript"),
    ("runtime-validation", "Runtime data validation", "Runtime validation checks unknown boundary data against a versioned schema before it enters trusted application state.", "frontend-web-development.javascript-typescript"),
    ("async-effect", "Asynchronous frontend effect", "An asynchronous effect has identity, cancellation, ordering, stale-result, retry, and error-display behavior beyond the awaited value.", "frontend-web-development.javascript-typescript"),
    ("event-handler", "UI event handler", "An event handler translates a user or platform event into a state transition or effect while respecting propagation and default action.", "frontend-web-development.javascript-typescript"),
    ("component", "UI component", "A UI component owns a coherent semantic responsibility with inputs, outputs, state, slots, accessibility, layout, and lifecycle boundaries.", "frontend-web-development.component-systems"),
    ("component-contract", "Component contract", "A component contract defines supported properties, events, content slots, states, accessibility semantics, styling hooks, and compatibility.", "frontend-web-development.component-systems"),
    ("composition", "Component composition", "Component composition builds larger behavior by nesting and coordinating small contracts rather than inheriting hidden global behavior.", "frontend-web-development.component-systems"),
    ("controlled-component", "Controlled component", "A controlled component receives authoritative state and emits requested changes, keeping ownership outside the component.", "frontend-web-development.component-systems"),
    ("uncontrolled-component", "Uncontrolled component", "An uncontrolled component owns selected transient state and exposes initialization, observation, and reset boundaries.", "frontend-web-development.component-systems"),
    ("lifecycle", "Component lifecycle", "A component lifecycle covers creation, attachment, update, visibility, suspension, detachment, and cleanup according to the framework and platform.", "frontend-web-development.component-systems"),
    ("application-state", "Application state", "Application state is the minimal information needed to derive current behavior and presentation under a defined ownership boundary.", "frontend-web-development.state-data"),
    ("single-source-truth", "Single source of truth", "A single source of truth gives one owner authority for a datum while other representations are derived, cached, or synchronized explicitly.", "frontend-web-development.state-data"),
    ("unidirectional-flow", "Unidirectional data flow", "Unidirectional data flow sends state downward and events upward through explicit transitions, making causality and replay easier to inspect.", "frontend-web-development.state-data"),
    ("derived-state", "Derived UI state", "Derived state is computed from authoritative inputs and should not be independently mutated or duplicated without an invalidation strategy.", "frontend-web-development.state-data"),
    ("server-state", "Server state", "Server state is remote, shared, asynchronous, and potentially stale, so clients need identity, freshness, invalidation, optimistic-update, and reconciliation rules.", "frontend-web-development.state-data"),
    ("optimistic-update", "Optimistic update", "An optimistic update presents the expected result before server confirmation and must reconcile success, conflict, retry, and rollback.", "frontend-web-development.state-data"),
    ("loading-state", "Loading state", "Loading state distinguishes initial, background, incremental, empty, stale, partial, and failed data so the interface communicates what is actually known.", "frontend-web-development.state-data"),
    ("critical-path", "Frontend critical path", "The critical path is the dependency chain that determines when meaningful content and interaction can become available.", "frontend-web-development.performance"),
    ("resource-priority", "Resource priority", "Resource priority influences scheduling among critical, deferred, lazy, and speculative resources but cannot create bandwidth or eliminate dependencies.", "frontend-web-development.performance"),
    ("code-splitting", "Code splitting", "Code splitting creates loadable program chunks around routes or capabilities and trades initial transfer against request overhead and interaction delays.", "frontend-web-development.performance"),
    ("lazy-render", "Lazy rendering", "Lazy rendering defers offscreen or low-priority work while preserving discoverability, layout stability, accessibility, and later responsiveness.", "frontend-web-development.performance"),
    ("layout-shift", "Layout shift", "Layout shift occurs when rendered geometry changes unexpectedly after presentation and is reduced by reserving space and controlling late content.", "frontend-web-development.performance"),
    ("main-thread", "Main-thread budget", "A main-thread budget limits long tasks, script, style, layout, and rendering work so input and presentation deadlines remain responsive.", "frontend-web-development.performance"),
    ("performance-measure", "Real-user performance measurement", "Real-user measurement records distributions by device, network, route, version, and user state rather than relying only on laboratory averages.", "frontend-web-development.performance"),
    ("dom-test", "DOM behavior test", "A DOM behavior test exercises user-observable semantics and state transitions without overfitting to private component implementation.", "frontend-web-development.testing"),
    ("visual-test", "Visual regression test", "A visual regression test compares controlled rendered output and requires tolerance, environment, font, animation, and intentional-change review.", "frontend-web-development.testing"),
    ("accessibility-test", "Frontend accessibility test", "Accessibility testing combines automated rules, semantic inspection, keyboard operation, assistive technology, and representative users because no one method is complete.", "frontend-web-development.testing"),
    ("e2e-test", "Frontend end-to-end test", "An end-to-end test verifies a critical user journey through real browser, application, network, and backend boundaries with controlled state.", "frontend-web-development.testing"),
    ("contract-test", "Frontend contract test", "A contract test verifies that frontend assumptions about API schemas, states, and errors match the provider contract.", "frontend-web-development.testing"),
    ("keyboard-flow", "Keyboard interaction flow", "A keyboard flow preserves logical focus order, visible focus, expected activation, escape, arrow, and tab behavior for the widget pattern.", "frontend-web-development.accessibility"),
    ("name-role-value", "Accessible name, role, and value", "Interactive elements expose a coherent name, role, value or state, and supported actions to accessibility APIs.", "frontend-web-development.accessibility"),
    ("focus-management", "Focus management", "Focus management moves focus only when context changes require it, announces meaningful transitions, and returns it to a sensible owner on close.", "frontend-web-development.accessibility"),
    ("error-access", "Accessible error recovery", "Accessible error recovery identifies the affected field, explains the problem and correction, preserves input, and moves or links attention appropriately.", "frontend-web-development.accessibility"),
    ("contrast-motion", "Contrast and motion adaptation", "Accessible presentation maintains perceptual contrast and respects reduced-motion preferences without removing essential state information.", "frontend-web-development.accessibility"),
    ("design-token", "Design token", "A design token gives a named role to a reusable visual or motion decision and maps it to platform-specific values under version control.", "frontend-web-development.design-systems"),
    ("component-library", "Component library", "A component library packages reviewed semantic, visual, interaction, accessibility, and testing contracts for reuse.", "frontend-web-development.design-systems"),
    ("variant", "Component variant", "A variant represents a supported semantic or behavioral configuration rather than every local styling difference.", "frontend-web-development.design-systems"),
    ("theme", "Design-system theme", "A theme maps semantic tokens across brand, color scheme, density, motion, and platform while preserving component meaning and contrast.", "frontend-web-development.design-systems"),
    ("design-governance", "Design-system governance", "Governance defines ownership, contribution, review, release, migration, deprecation, and adoption evidence for system components.", "frontend-web-development.design-systems"),
    ("module-graph", "Frontend module graph", "A module graph links source and dependencies into build, split, preload, and execution relationships.", "frontend-web-development.build-tooling"),
    ("transpile", "Frontend transpilation", "Transpilation converts supported source syntax and types into a target language version while preserving declared semantics and source mapping.", "frontend-web-development.build-tooling"),
    ("bundle", "Frontend bundle", "Bundling resolves a module graph into deployable chunks while applying transformations, asset handling, and runtime loading metadata.", "frontend-web-development.build-tooling"),
    ("tree-shaking", "Tree shaking", "Tree shaking removes statically proven unused exports under module and side-effect assumptions that package metadata must state correctly.", "frontend-web-development.build-tooling"),
    ("source-map", "Source map", "A source map maps transformed code locations back to authored sources and must be distributed under an explicit debugging and disclosure policy.", "frontend-web-development.build-tooling"),
    ("dev-server", "Frontend development server", "A development server provides rapid rebuilding and module updates but is not a production security, caching, or performance boundary.", "frontend-web-development.build-tooling"),
    ("pwa", "Progressive web application", "A progressive web application combines secure delivery, installability where supported, responsive UI, service-worker behavior, and progressive enhancement.", "frontend-web-development.progressive-web-apps"),
    ("offline-model", "Offline data model", "An offline model defines which reads and writes work without network, how operations queue, and how conflicts reconcile after connectivity returns.", "frontend-web-development.progressive-web-apps"),
    ("update-model", "Web-app update model", "An update model coordinates cached assets, active clients, schema compatibility, activation, reload prompts, and rollback so one session stays coherent.", "frontend-web-development.progressive-web-apps"),
    ("installability", "Web-app installability", "Installability packages manifest identity, icons, display behavior, navigation scope, and platform criteria without guaranteeing app-store-like privileges.", "frontend-web-development.progressive-web-apps"),
]


MOBILE = [
    ("root", "Mobile application system", "Mobile application engineering composes platform lifecycles, constrained resources, declarative UI, persistent state, permissions, tooling, testing, distribution, accessibility, and form-factor adaptation under versioned Android and Apple contracts.", "mobile-android-apple.android-platform"),
    ("android-app", "Android application", "An Android application is a signed package whose components run under an application identity and platform-managed process lifecycle.", "mobile-android-apple.android-platform"),
    ("android-component", "Android app component", "An activity, service, broadcast receiver, or content provider is a platform entry point with declared lifecycle, exposure, permission, and process behavior.", "mobile-android-apple.android-platform"),
    ("manifest", "Android manifest", "The Android manifest declares package-level components, permissions, features, intent filters, process settings, and platform compatibility metadata.", "mobile-android-apple.android-platform"),
    ("intent", "Android intent", "An intent describes an action and optional data, categories, extras, package, or component for platform-mediated dispatch.", "mobile-android-apple.android-platform"),
    ("process-death", "Android process death", "The Android system may terminate an app process while retaining reconstructable navigation or component state, so in-memory objects are not durable application state.", "mobile-android-apple.android-platform"),
    ("resource", "Android resource", "An Android resource separates localized, density, size, theme, and configuration variants from code and is selected by device configuration.", "mobile-android-apple.android-platform"),
    ("permission", "Android permission", "An Android permission gates a protected platform capability according to declaration, grant, runtime request, role, policy, and OS version.", "mobile-android-apple.android-platform"),
    ("app-sandbox", "Android application sandbox", "The Android application sandbox isolates app identities, processes, and private storage while controlled IPC and shared services cross the boundary.", "mobile-android-apple.android-platform"),
    ("android-studio", "Android Studio", "Android Studio integrates project editing, Gradle coordination, device management, inspection, profiling, debugging, testing, and packaging for Android development.", "mobile-android-apple.android-studio"),
    ("emulator", "Android emulator", "The Android emulator runs a configured virtual device image for repeatable platform testing but does not replace real-device sensors, performance, vendor behavior, or distribution tests.", "mobile-android-apple.android-studio"),
    ("adb", "Android Debug Bridge", "ADB provides an authorized host-device channel for app installation, shell access, files, logs, debugging, and port forwarding under device trust controls.", "mobile-android-apple.android-studio"),
    ("logcat", "Logcat", "Logcat exposes timestamped system and application log buffers whose filters, retention, privacy, and process context qualify diagnosis.", "mobile-android-apple.android-studio"),
    ("profiler", "Android profiler", "Android profiling measures CPU, memory, network, energy, and rendering behavior for a specific device, build, and workload.", "mobile-android-apple.android-studio"),
    ("layout-inspector", "Android layout inspector", "The layout inspector shows a running app's view or composition hierarchy, properties, recomposition, and geometry at an observed state.", "mobile-android-apple.android-studio"),
    ("kotlin-null", "Kotlin null safety", "Kotlin's nullable and non-null types make many nullability conditions explicit, while platform types and unsafe assertions retain runtime risk.", "mobile-android-apple.kotlin-android"),
    ("coroutine", "Kotlin coroutine", "A coroutine is a suspendable computation whose dispatcher, structured scope, cancellation, exception, and lifecycle ownership determine safe Android use.", "mobile-android-apple.kotlin-android"),
    ("flow", "Kotlin Flow", "A Flow represents an asynchronous stream whose cold or hot behavior, collection lifecycle, cancellation, buffering, and errors must be declared.", "mobile-android-apple.kotlin-android"),
    ("structured-concurrency", "Structured concurrency", "Structured concurrency binds child tasks to an owning scope so completion, cancellation, and failure cannot outlive their intended lifecycle silently.", "mobile-android-apple.kotlin-android"),
    ("sealed-state", "Kotlin sealed UI state", "A sealed hierarchy can enumerate known UI-state variants so rendering and transitions handle loading, content, empty, and failure explicitly.", "mobile-android-apple.kotlin-android"),
    ("composable", "Composable function", "A composable function describes UI from inputs and composition state and may be re-executed, skipped, or reordered by the Compose runtime.", "mobile-android-apple.compose"),
    ("composition", "Compose composition", "A composition is the retained description produced by executing composables, keyed by call structure and identity.", "mobile-android-apple.compose"),
    ("recomposition", "Compose recomposition", "Recomposition re-executes invalidated composable scopes after observed state changes and applies the resulting differences.", "mobile-android-apple.compose"),
    ("compose-state", "Compose state", "Observable Compose state records values whose reads establish invalidation dependencies and whose writes schedule relevant recomposition.", "mobile-android-apple.compose"),
    ("remember", "Compose remember", "Remember stores a value at a composition position across recompositions but loses it when that position leaves composition unless separate saveable or durable state is used.", "mobile-android-apple.compose"),
    ("state-hoisting", "Compose state hoisting", "State hoisting moves state to the lowest common owner and gives a component value inputs plus event outputs, improving reuse and single ownership.", "mobile-android-apple.compose"),
    ("modifier", "Compose modifier", "A modifier composes layout, drawing, input, semantics, and parent-data behavior in an order where sequence can change results.", "mobile-android-apple.compose"),
    ("compose-effect", "Compose side effect", "A Compose effect connects composition to lifecycle-bound external work and must declare stable keys, cleanup, and cancellation.", "mobile-android-apple.compose"),
    ("adaptive-compose", "Adaptive Compose layout", "Adaptive layouts derive panes, navigation, and content arrangement from available window size and posture rather than device labels alone.", "mobile-android-apple.compose"),
    ("gradle", "Gradle build", "Gradle constructs a task and dependency graph from configuration, variants, plugins, and inputs, then executes required tasks with caching and incremental rules.", "mobile-android-apple.android-build"),
    ("android-plugin", "Android Gradle Plugin", "The Android Gradle Plugin adds Android source sets, variants, resource processing, manifests, packaging, testing, lint, and device tasks to the build.", "mobile-android-apple.android-build"),
    ("build-variant", "Android build variant", "A build variant combines build type, product flavors, signing, source sets, and generated configuration into one buildable application form.", "mobile-android-apple.android-build"),
    ("sdk-level", "Android SDK level", "Compile, target, and minimum SDK levels govern available APIs, compatibility behavior, declarations, and install eligibility in distinct ways.", "mobile-android-apple.android-build"),
    ("resource-merge", "Android resource and manifest merge", "Build tooling merges resources and manifest contributions by priority and declared directives, producing one packaged application contract.", "mobile-android-apple.android-build"),
    ("signing", "Android app signing", "Android signing binds package updates to accepted signer identity and distribution policy; key loss or compromise affects the app's update chain.", "mobile-android-apple.android-build"),
    ("activity-lifecycle", "Activity lifecycle", "An activity moves through created, started, resumed, paused, stopped, and destroyed callbacks as visibility and interaction change; callbacks do not guarantee process survival.", "mobile-android-apple.android-lifecycle"),
    ("viewmodel", "Android ViewModel", "A ViewModel owns screen-level state and work across configuration recreation but does not survive process death or replace durable persistence.", "mobile-android-apple.android-lifecycle"),
    ("saved-state", "Android saved state", "Saved state preserves small reconstructive values across recreation or process death and should not duplicate large durable data.", "mobile-android-apple.android-lifecycle"),
    ("repository", "Android repository layer", "A repository owns access and synchronization policy for one data area across local, remote, cache, and error sources.", "mobile-android-apple.android-lifecycle"),
    ("udf", "Android unidirectional data flow", "Unidirectional data flow exposes immutable UI state and sends user events to an owner that performs transitions and effects.", "mobile-android-apple.android-lifecycle"),
    ("navigation", "Android navigation state", "Navigation state records destinations, arguments, deep links, back-stack transitions, and restored state rather than only visible widgets.", "mobile-android-apple.android-lifecycle"),
    ("ios-app", "Apple-platform application", "An Apple-platform application is a signed bundle executed under platform lifecycle, entitlement, sandbox, resource, and distribution rules.", "mobile-android-apple.ios-platform"),
    ("app-lifecycle", "Apple app lifecycle", "The app and scene lifecycle coordinates launch, activation, backgrounding, suspension, restoration, and termination across platform-managed scenes.", "mobile-android-apple.ios-platform"),
    ("entitlement", "Apple entitlement", "An entitlement is a signed capability assertion granted through provisioning and platform policy for protected services or sandbox access.", "mobile-android-apple.ios-platform"),
    ("ios-sandbox", "Apple application sandbox", "The application sandbox restricts filesystem, process, device, and service access according to identity, container, entitlement, and user permission.", "mobile-android-apple.ios-platform"),
    ("background-mode", "Mobile background execution", "Background execution is platform-scheduled and capability-specific; apps must persist work state and tolerate suspension or termination.", "mobile-android-apple.ios-platform"),
    ("swift-value", "Swift value semantics", "Swift structures and enumerations ordinarily copy value meaning across assignment while implementation may optimize storage without changing observable semantics.", "mobile-android-apple.swift"),
    ("swift-protocol", "Swift protocol", "A Swift protocol declares required capabilities that conforming types provide and can participate in generic or existential use with different tradeoffs.", "mobile-android-apple.swift"),
    ("swift-option", "Swift optional", "A Swift optional represents either a wrapped value or absence and requires explicit binding, transformation, defaulting, or justified force unwrapping.", "mobile-android-apple.swift"),
    ("swift-error", "Swift error handling", "Swift error handling propagates typed values through throwing calls and separates recoverable failure from option absence and process traps.", "mobile-android-apple.swift"),
    ("swift-concurrency", "Swift structured concurrency", "Swift tasks, async functions, task groups, actors, and cancellation form a structured concurrency model whose isolation must cross legacy callbacks deliberately.", "mobile-android-apple.swift"),
    ("swift-actor", "Swift actor", "A Swift actor serializes access to isolated mutable state while awaited suspension can permit reentrancy and intervening state changes.", "mobile-android-apple.swift"),
    ("swiftui-view", "SwiftUI View", "A SwiftUI View is a value describing part of the interface; the framework reconciles changing descriptions into retained platform presentation.", "mobile-android-apple.swiftui"),
    ("swiftui-state", "SwiftUI state ownership", "SwiftUI state wrappers communicate ownership, observation, binding, persistence, and environment relationships that determine update behavior.", "mobile-android-apple.swiftui"),
    ("swiftui-binding", "SwiftUI Binding", "A binding provides read-write access to state owned elsewhere and should not be mistaken for independent storage.", "mobile-android-apple.swiftui"),
    ("swiftui-environment", "SwiftUI environment", "The environment propagates contextual values down a view hierarchy and creates implicit dependencies that should remain documented and scoped.", "mobile-android-apple.swiftui"),
    ("swiftui-identity", "SwiftUI view identity", "View identity determines whether framework-managed state is preserved or replaced as the declared hierarchy changes.", "mobile-android-apple.swiftui"),
    ("swiftui-navigation", "SwiftUI navigation state", "Navigation APIs derive presented destinations and paths from bound state and must preserve type, restoration, and deep-link semantics.", "mobile-android-apple.swiftui"),
    ("swiftui-preview", "SwiftUI preview", "A preview renders a view under selected data, device, locale, color, size, and accessibility configurations but does not replace tests on shipped runtime paths.", "mobile-android-apple.swiftui"),
    ("xcode-project", "Xcode project and workspace", "An Xcode project declares targets, build settings, files, schemes, and dependencies, while a workspace coordinates multiple projects and packages.", "mobile-android-apple.xcode"),
    ("xcode-target", "Xcode target", "An Xcode target defines one product together with source membership, build phases, configuration, platform, signing, and dependencies.", "mobile-android-apple.xcode"),
    ("xcode-scheme", "Xcode scheme", "A scheme selects targets, configuration, executable, arguments, environment, diagnostics, and actions for build, test, run, profile, archive, and analysis.", "mobile-android-apple.xcode"),
    ("simulator", "Apple simulator", "A simulator executes platform frameworks for configured virtual devices while differing from device CPU, sensors, security hardware, thermal limits, and distribution.", "mobile-android-apple.xcode"),
    ("instruments", "Instruments profiling", "Instruments records time-correlated CPU, memory, allocations, energy, I/O, rendering, signposts, and subsystem traces for a chosen build and device.", "mobile-android-apple.xcode"),
    ("package-manager", "Swift Package Manager", "Swift Package Manager resolves declared package identities, versions, products, targets, and build settings into a dependency graph.", "mobile-android-apple.xcode"),
    ("cross-platform-core", "Cross-platform domain core", "A cross-platform core isolates business rules, data contracts, and state transitions that can be shared without erasing native lifecycle and interaction boundaries.", "mobile-android-apple.cross-platform"),
    ("platform-adapter", "Mobile platform adapter", "A platform adapter maps shared capability requests into native APIs while preserving platform-specific errors, permissions, lifecycle, and semantics.", "mobile-android-apple.cross-platform"),
    ("shared-ui-tradeoff", "Shared UI tradeoff", "Shared UI increases code reuse but must be evaluated against native accessibility, performance, interaction, tooling, and platform evolution.", "mobile-android-apple.cross-platform"),
    ("offline-sync", "Mobile offline synchronization", "Offline synchronization records operation identity, causal version, conflict policy, retry, deletion, and user-visible reconciliation across intermittent connectivity.", "mobile-android-apple.cross-platform"),
    ("secure-storage", "Mobile secure storage", "Secure storage uses platform key services and access controls for small secrets while declaring backup, device-lock, migration, and compromised-device limits.", "mobile-android-apple.mobile-security"),
    ("deep-link-security", "Deep-link security", "Deep links cross an external input boundary and require verified association where possible, strict parsing, authorization, and safe fallback.", "mobile-android-apple.mobile-security"),
    ("ipc-security", "Mobile IPC security", "Interprocess endpoints require minimal exposure, caller identity checks, permission enforcement, schema validation, and bounded returned data.", "mobile-android-apple.mobile-security"),
    ("mobile-secret", "Mobile client secret boundary", "A distributed mobile binary cannot keep an embedded universal secret from a device owner; high-value authority belongs on a controlled service or hardware-backed per-device key.", "mobile-android-apple.mobile-security"),
    ("network-security", "Mobile network security", "Mobile clients validate secure transport and server identity, protect credentials, handle hostile networks, and avoid weakening policy for debugging convenience.", "mobile-android-apple.mobile-security"),
    ("update-security", "Mobile update security", "Signed store or enterprise update channels bind package identity and version while rollout, compatibility, key protection, and rollback still require design.", "mobile-android-apple.mobile-security"),
    ("dynamic-type", "Dynamic text sizing", "Mobile interfaces adapt layout and content to user-selected text size without clipping, overlap, hidden actions, or forced horizontal reading.", "mobile-android-apple.mobile-accessibility"),
    ("screen-reader", "Mobile screen-reader semantics", "Controls expose name, role, value, state, order, grouping, and actions compatible with TalkBack, VoiceOver, and platform accessibility APIs.", "mobile-android-apple.mobile-accessibility"),
    ("touch-target", "Touch target", "A touch target provides sufficient interactive area and spacing without requiring precise motor control, while its semantic bounds match expected action.", "mobile-android-apple.mobile-accessibility"),
    ("switch-control", "Alternative input support", "Mobile interaction supports keyboard, switch, voice, pointer, and assistive actions without assuming a single touch gesture.", "mobile-android-apple.mobile-accessibility"),
    ("mobile-contrast", "Mobile contrast and non-color cues", "Text, controls, focus, and status remain perceivable across appearance, brightness, contrast, and color-vision conditions without color-only meaning.", "mobile-android-apple.mobile-accessibility"),
]


RELATIONS = [
    ("sw-need-requirement", "sw.stakeholder-need", "sw.requirement", "grounds", "Stakeholder needs ground the purpose and priority of software requirements."),
    ("sw-functional-requirement", "sw.functional", "sw.requirement", "part_of", "Functional behavior forms one class of software requirement."),
    ("sw-quality-requirement", "sw.quality", "sw.requirement", "part_of", "Measurable quality properties form one class of software requirement."),
    ("sw-constraint-requirement", "sw.constraint", "sw.requirement", "qualifies", "External and engineering constraints qualify acceptable requirement solutions."),
    ("sw-accept-requirement", "sw.acceptance", "sw.requirement", "supports", "Acceptance criteria support deciding whether a requirement is satisfied."),
    ("sw-trace-requirement", "sw.traceability", "sw.requirement", "supports", "Traceability supports impact analysis and evidence linkage."),
    ("sw-requirement-architecture", "sw.requirement", "sw.architecture", "qualifies", "Requirements and constraints qualify architecture decisions."),
    ("sw-component-architecture", "sw.component", "sw.architecture", "part_of", "Components form part of an architecture's structural view."),
    ("sw-dependency-component", "sw.dependency", "sw.component", "qualifies", "Dependencies qualify a component's failure and change surface."),
    ("sw-boundary-architecture", "sw.boundary", "sw.architecture", "part_of", "Ownership and trust boundaries form part of architecture."),
    ("sw-coupling-change", "sw.coupling", "sw.dependency", "measures", "Coupling measures how dependency detail propagates change."),
    ("sw-cohesion-component", "sw.cohesion", "sw.component", "qualifies", "Cohesion qualifies whether responsibilities belong in one component."),
    ("sw-decision-architecture", "sw.architecture-decision", "sw.architecture", "supports", "Decision records support architecture evolution and review."),
    ("sw-module-coupling", "sw.modularity", "sw.coupling", "inhibits", "Well-chosen modules inhibit propagation of change through private detail."),
    ("sw-layer-dependency", "sw.layer", "sw.dependency", "qualifies", "Layering qualifies allowed dependency direction."),
    ("sw-event-state", "sw.event-driven", "sw.state-machine", "qualifies", "Asynchronous events qualify state transitions through delivery semantics."),
    ("sw-strategy-pattern", "sw.strategy", "sw.pattern", "part_of", "Strategy is one design-pattern family."),
    ("sw-adapter-pattern", "sw.adapter", "sw.pattern", "part_of", "Adapter is one boundary-translation pattern."),
    ("sw-observer-pattern", "sw.observer", "sw.pattern", "part_of", "Observer is one notification pattern."),
    ("sw-state-pattern", "sw.state-machine", "sw.pattern", "part_of", "State machines form an explicit behavioral pattern."),
    ("sw-di-component", "sw.dependency-injection", "sw.component", "supports", "Dependency injection supports explicit component collaboration."),
    ("sw-tradeoff-pattern", "sw.pattern-tradeoff", "sw.pattern", "qualifies", "Forces and consequences qualify whether a pattern applies."),
    ("sw-oracle-test", "sw.test-oracle", "sw.unit-test", "prerequisite", "An independent oracle is prerequisite to a decisive unit test."),
    ("sw-unit-integration", "sw.unit-test", "sw.integration-test", "prerequisite", "Unit checks support but do not replace integration-boundary tests."),
    ("sw-integration-system", "sw.integration-test", "sw.system-test", "prerequisite", "Integration evidence supports assembled-system testing."),
    ("sw-property-invariant", "sw.property-test", "sw.formal-verification", "analogous_to", "Property tests and proofs both target invariants with empirical and formal evidence respectively."),
    ("sw-fuzz-regression", "sw.fuzz-test", "sw.regression-test", "causes", "A minimized fuzz finding causes creation of a durable regression test."),
    ("sw-metamorphic-oracle", "sw.metamorphic-test", "sw.test-oracle", "implements", "A metamorphic relation implements an oracle when exact output is unavailable."),
    ("sw-portfolio-system", "sw.test-pyramid", "sw.system-test", "qualifies", "Risk and cost qualify the role of system tests in the portfolio."),
    ("sw-formal-contract", "sw.formal-verification", "sw.api-contract", "supports", "A proof can support selected contract properties under explicit assumptions."),
    ("sw-symptom-hypothesis", "sw.symptom", "sw.hypothesis", "causes", "A reproducible symptom causes formation of competing debugging hypotheses."),
    ("sw-repro-hypothesis", "sw.minimal-reproducer", "sw.hypothesis", "supports", "A minimal reproducer supports discriminating causal hypotheses."),
    ("sw-hypothesis-instrument", "sw.hypothesis", "sw.instrumentation", "qualifies", "A hypothesis qualifies which instrumentation can discriminate it."),
    ("sw-bisect-repro", "sw.minimal-reproducer", "sw.bisect", "prerequisite", "A stable reproducer and oracle are prerequisite to revision bisection."),
    ("sw-evidence-root", "sw.instrumentation", "sw.root-cause", "supports", "Versioned diagnostic evidence supports root-cause analysis."),
    ("sw-benchmark-latency", "sw.benchmark", "sw.latency", "measures", "A benchmark can measure a latency distribution."),
    ("sw-benchmark-throughput", "sw.benchmark", "sw.throughput", "measures", "A benchmark can measure throughput under declared load."),
    ("sw-profile-resource", "sw.profile", "sw.resource", "measures", "A profile measures attributed resource cost."),
    ("sw-complexity-capacity", "sw.complexity", "sw.capacity", "qualifies", "Algorithmic growth qualifies capacity behavior as input size changes."),
    ("sw-resource-capacity", "sw.resource", "sw.capacity", "part_of", "Resource limits form part of a capacity model."),
    ("sw-fault-failure", "sw.fault", "sw.failure", "causes", "An activated fault can cause an externally observable failure."),
    ("sw-reliability-failure", "sw.failure", "sw.reliability", "measures", "Observed failures contribute to reliability estimation."),
    ("sw-availability-failure", "sw.failure", "sw.availability", "inhibits", "Service failures inhibit availability under the declared success criterion."),
    ("sw-redundancy-fault", "sw.redundancy", "sw.fault", "inhibits", "Independent redundancy inhibits one fault from becoming a service failure."),
    ("sw-timeout-unknown", "sw.timeout", "sw.retry", "qualifies", "An unknown timed-out outcome qualifies whether retry is safe."),
    ("sw-retry-idempotency", "sw.idempotency", "sw.retry", "supports", "Idempotency supports safe retry after ambiguous outcomes."),
    ("sw-breaker-failure", "sw.circuit-breaker", "sw.failure", "inhibits", "A circuit breaker inhibits repeated pressure on a failing dependency."),
    ("sw-bulkhead-resource", "sw.bulkhead", "sw.resource", "qualifies", "Bulkheads qualify which workloads can consume each resource pool."),
    ("sw-degrade-availability", "sw.graceful-degradation", "sw.availability", "supports", "Graceful degradation supports partial availability under impairment."),
    ("sw-resource-api", "sw.resource-model", "sw.api-contract", "part_of", "The resource model forms part of an API contract."),
    ("sw-error-api", "sw.error-contract", "sw.api-contract", "part_of", "Error semantics form part of an API contract."),
    ("sw-page-api", "sw.pagination", "sw.api-contract", "qualifies", "Pagination qualifies collection retrieval behavior."),
    ("sw-compat-api", "sw.compatibility", "sw.api-contract", "qualifies", "Compatibility policy qualifies safe contract evolution."),
    ("sw-protocol-state", "sw.protocol-state", "sw.state-machine", "implements", "Protocol roles and messages implement a distributed state machine."),
    ("sw-commit-branch", "sw.commit", "sw.branch", "part_of", "A branch reference identifies a commit lineage tip."),
    ("sw-branch-merge", "sw.branch", "sw.merge", "prerequisite", "Divergent branch histories are inputs to a three-way merge."),
    ("sw-review-merge", "sw.review", "sw.merge", "qualifies", "Semantic review qualifies whether a clean textual merge is acceptable."),
    ("sw-build-artifact", "sw.build", "sw.artifact", "causes", "A build transforms declared inputs into identified artifacts."),
    ("sw-ci-build", "sw.ci", "sw.build", "implements", "Continuous integration implements clean automated builds and checks."),
    ("sw-artifact-release", "sw.artifact", "sw.release", "prerequisite", "An identified verified artifact is prerequisite to release promotion."),
    ("sw-semver-compat", "sw.semantic-version", "sw.compatibility", "clarifies", "Semantic versions clarify declared public-API compatibility changes."),
    ("sw-release-deploy", "sw.release", "sw.deployment", "causes", "Release promotion causes deployment into selected environments."),
    ("sw-canary-release", "sw.canary", "sw.release", "qualifies", "Canary population and gates qualify release expansion."),
    ("sw-rollback-deploy", "sw.rollback", "sw.deployment", "transforms_to", "Rollback transforms an environment back to a compatible prior path."),
    ("sw-debt-maintain", "sw.technical-debt", "sw.migration", "qualifies", "Accumulated debt qualifies migration cost and urgency."),
    ("sw-refactor-test", "sw.regression-test", "sw.refactor", "supports", "Regression tests support behavior-preserving refactoring."),
    ("sw-migrate-compat", "sw.compatibility", "sw.migration", "prerequisite", "Compatibility staging is prerequisite to a reversible migration."),
    ("sw-deprecation-migrate", "sw.deprecation", "sw.migration", "supports", "Deprecation supports an observable migration path before removal."),
    ("sw-observe-maintain", "sw.observability", "sw.root-cause", "supports", "Operational observability supports diagnosis of maintained systems."),
    ("sw-secure-requirement", "sw.secure-lifecycle", "sw.requirement", "qualifies", "Secure development qualifies requirements with threat and control needs."),
    ("sw-review-secure", "sw.secure-review", "sw.review", "part_of", "Security-focused review forms one dimension of code review."),
    ("sw-dependency-provenance", "sw.dependency-governance", "sw.release-provenance", "supports", "Dependency governance supports complete release provenance."),
    ("sw-provenance-artifact", "sw.release-provenance", "sw.artifact", "supports", "Provenance supports confidence in an artifact's origin and process."),
    ("fe-outline-content", "fe.content-first", "fe.document-outline", "supports", "Content-first ordering supports a meaningful semantic outline."),
    ("fe-native-form", "fe.native-control", "fe.form-model", "supports", "Native controls support accessible form behavior."),
    ("fe-intrinsic-responsive", "fe.intrinsic-layout", "fe.responsive-image", "qualifies", "Intrinsic layout qualifies image slot sizing for responsive selection."),
    ("fe-flex-intrinsic", "fe.flex-layout", "fe.intrinsic-layout", "implements", "Flex sizing implements one intrinsic one-dimensional layout model."),
    ("fe-grid-intrinsic", "fe.grid-layout", "fe.intrinsic-layout", "implements", "Grid tracks implement two-dimensional intrinsic layout."),
    ("fe-container-component", "fe.container-query", "fe.component", "qualifies", "Container queries qualify component layout by local available space."),
    ("fe-logical-global", "fe.logical-property", "fe.intrinsic-layout", "supports", "Logical properties support writing-mode-independent layout."),
    ("fe-css-progressive", "fe.progressive-css", "fe.content-first", "supports", "Progressive styling supports robust content when features fail."),
    ("fe-module-graph", "fe.module", "fe.module-graph", "part_of", "JavaScript modules compose the frontend module graph."),
    ("fe-type-runtime", "fe.type-contract", "fe.runtime-validation", "qualifies", "Type erasure qualifies why external data still needs runtime validation."),
    ("fe-effect-cancel", "fe.async-effect", "fe.application-state", "transforms_to", "Async effect outcomes transform application state under cancellation and stale-result rules."),
    ("fe-handler-state", "fe.event-handler", "fe.application-state", "causes", "A UI event handler causes a declared state transition or effect."),
    ("fe-contract-component", "fe.component-contract", "fe.component", "qualifies", "The contract qualifies supported component behavior and evolution."),
    ("fe-composition-component", "fe.component", "fe.composition", "part_of", "Components compose larger interface structures."),
    ("fe-controlled-owner", "fe.controlled-component", "fe.single-source-truth", "supports", "Controlled state supports one authoritative owner."),
    ("fe-uncontrolled-lifecycle", "fe.uncontrolled-component", "fe.lifecycle", "qualifies", "Lifecycle qualifies the persistence of internally owned state."),
    ("fe-single-state", "fe.single-source-truth", "fe.application-state", "qualifies", "Single ownership qualifies mutation authority over application state."),
    ("fe-flow-state", "fe.unidirectional-flow", "fe.application-state", "transforms_to", "Events transform authoritative state in unidirectional flow."),
    ("fe-derived-state", "fe.application-state", "fe.derived-state", "causes", "Authoritative inputs cause derived UI state."),
    ("fe-server-loading", "fe.server-state", "fe.loading-state", "qualifies", "Remote freshness and request state qualify loading presentation."),
    ("fe-optimistic-server", "fe.optimistic-update", "fe.server-state", "transforms_to", "Optimistic mutation tentatively transforms cached server state before reconciliation."),
    ("fe-critical-priority", "fe.critical-path", "fe.resource-priority", "qualifies", "Critical dependencies qualify resource scheduling priority."),
    ("fe-split-module", "fe.code-splitting", "fe.module-graph", "transforms_to", "Code splitting transforms a module graph into separately loaded chunks."),
    ("fe-lazy-main", "fe.lazy-render", "fe.main-thread", "inhibits", "Lazy rendering inhibits low-priority main-thread work before it is needed."),
    ("fe-shift-layout", "fe.layout-shift", "fe.intrinsic-layout", "undercuts", "Unexpected shifts undercut stable responsive layout."),
    ("fe-measure-budget", "fe.performance-measure", "fe.main-thread", "measures", "Real-user telemetry measures main-thread responsiveness across populations."),
    ("fe-dom-e2e", "fe.dom-test", "fe.e2e-test", "analogous_to", "DOM behavior and end-to-end tests observe user behavior at different system scopes."),
    ("fe-contract-api", "fe.contract-test", "sw.api-contract", "supports", "Frontend contract tests support compatibility with provider APIs."),
    ("fe-a11y-test", "fe.accessibility-test", "fe.keyboard-flow", "measures", "Accessibility tests measure selected keyboard and semantic behavior."),
    ("fe-name-control", "fe.name-role-value", "fe.native-control", "supports", "Native controls support correct exposed name, role, and value."),
    ("fe-focus-flow", "fe.focus-management", "fe.keyboard-flow", "supports", "Focus management supports coherent keyboard interaction."),
    ("fe-error-form", "fe.error-access", "fe.form-model", "qualifies", "Accessible recovery qualifies form error presentation."),
    ("fe-token-theme", "fe.design-token", "fe.theme", "part_of", "Semantic tokens compose a theme."),
    ("fe-library-contract", "fe.component-library", "fe.component-contract", "supports", "A component library packages reviewed contracts."),
    ("fe-variant-component", "fe.variant", "fe.component", "qualifies", "Supported variants qualify component semantics and behavior."),
    ("fe-govern-library", "fe.design-governance", "fe.component-library", "supports", "Governance supports coherent library evolution."),
    ("fe-transpile-bundle", "fe.transpile", "fe.bundle", "prerequisite", "Targeted source transformation is prerequisite to bundling some source graphs."),
    ("fe-tree-bundle", "fe.tree-shaking", "fe.bundle", "transforms_to", "Tree shaking transforms a bundle graph by removing proven unused exports."),
    ("fe-map-transpile", "fe.source-map", "fe.transpile", "supports", "Source maps support debugging transformed code."),
    ("fe-dev-build", "fe.dev-server", "fe.module-graph", "supports", "A development server supports rapid module-graph iteration."),
    ("fe-pwa-progressive", "fe.progressive-css", "fe.pwa", "supports", "Progressive enhancement supports resilient PWA behavior."),
    ("fe-offline-server", "fe.offline-model", "fe.server-state", "qualifies", "Offline operation qualifies synchronization of server state."),
    ("fe-update-worker", "fe.update-model", "fe.offline-model", "qualifies", "Application update policy qualifies cached code and offline schema compatibility."),
    ("mo-manifest-component", "mo.android-component", "mo.manifest", "part_of", "Manifest declarations expose Android components to platform dispatch."),
    ("mo-intent-component", "mo.intent", "mo.android-component", "causes", "A resolved intent can cause platform dispatch to an app component."),
    ("mo-process-state", "mo.process-death", "mo.saved-state", "qualifies", "Process death qualifies which reconstructive state must be persisted."),
    ("mo-resource-config", "mo.resource", "mo.adaptive-compose", "supports", "Configuration-specific resources support adaptive presentation."),
    ("mo-permission-sandbox", "mo.permission", "mo.app-sandbox", "qualifies", "Granted permissions qualify which protected platform operations cross the sandbox."),
    ("mo-studio-emulator", "mo.android-studio", "mo.emulator", "supports", "Android Studio supports virtual-device management and testing."),
    ("mo-adb-log", "mo.adb", "mo.logcat", "supports", "Authorized ADB access supports log collection and device diagnosis."),
    ("mo-profiler-benchmark", "mo.profiler", "sw.benchmark", "measures", "Android profiling measures resource behavior for a benchmark workload."),
    ("mo-layout-compose", "mo.layout-inspector", "mo.composition", "measures", "Layout inspection measures a running composition hierarchy and recomposition state."),
    ("mo-null-state", "mo.kotlin-null", "mo.sealed-state", "supports", "Explicit nullable and sealed states support exhaustive UI-state handling."),
    ("mo-coroutine-scope", "mo.structured-concurrency", "mo.coroutine", "qualifies", "Structured scope qualifies coroutine ownership and cancellation."),
    ("mo-flow-state", "mo.flow", "mo.compose-state", "causes", "Collected flow values can cause observable Compose state updates."),
    ("mo-composable-composition", "mo.composable", "mo.composition", "causes", "Executing composables causes creation or update of a composition."),
    ("mo-state-recompose", "mo.compose-state", "mo.recomposition", "causes", "Writing observed Compose state schedules relevant recomposition."),
    ("mo-remember-composition", "mo.remember", "mo.composition", "part_of", "Remembered slots form part of retained composition state."),
    ("mo-hoist-udf", "mo.state-hoisting", "mo.udf", "supports", "State hoisting supports unidirectional data flow and reusable UI."),
    ("mo-modifier-view", "mo.modifier", "mo.composable", "qualifies", "Modifier order qualifies layout, input, drawing, and semantics."),
    ("mo-effect-lifecycle", "mo.compose-effect", "mo.activity-lifecycle", "qualifies", "Lifecycle ownership qualifies when a Compose effect starts and cancels."),
    ("mo-gradle-plugin", "mo.android-plugin", "mo.gradle", "part_of", "The Android plugin extends Gradle with Android build models and tasks."),
    ("mo-variant-build", "mo.build-variant", "mo.gradle", "qualifies", "A selected variant qualifies source, settings, signing, and output tasks."),
    ("mo-sdk-variant", "mo.sdk-level", "mo.build-variant", "qualifies", "SDK levels qualify compilation, install, and compatibility behavior."),
    ("mo-merge-package", "mo.resource-merge", "mo.android-app", "transforms_to", "Resource and manifest merging transforms contributions into one package input."),
    ("mo-sign-update", "mo.signing", "mo.android-app", "supports", "Signer continuity supports authorized Android package updates."),
    ("mo-activity-viewmodel", "mo.viewmodel", "mo.activity-lifecycle", "qualifies", "ViewModel lifetime spans configuration recreation but not process death."),
    ("mo-state-viewmodel", "mo.saved-state", "mo.viewmodel", "supports", "Saved reconstructive values support ViewModel state restoration."),
    ("mo-repository-udf", "mo.repository", "mo.udf", "supports", "Repository data flows support UI-state transitions."),
    ("mo-nav-state", "mo.navigation", "mo.saved-state", "supports", "Saved navigation state supports restoration after recreation."),
    ("mo-entitlement-sandbox", "mo.entitlement", "mo.ios-sandbox", "qualifies", "Entitlements qualify protected capabilities crossing the Apple sandbox."),
    ("mo-background-lifecycle", "mo.background-mode", "mo.app-lifecycle", "qualifies", "Platform background modes qualify work allowed outside active scenes."),
    ("mo-swift-value", "mo.swift-value", "mo.swiftui-view", "supports", "Swift value semantics support declarative view descriptions."),
    ("mo-protocol-adapter", "mo.swift-protocol", "mo.platform-adapter", "supports", "Protocols support replaceable platform adapter contracts."),
    ("mo-option-error", "mo.swift-option", "mo.swift-error", "qualifies", "Optional absence and thrown failure represent distinct conditions."),
    ("mo-concurrency-actor", "mo.swift-concurrency", "mo.swift-actor", "part_of", "Actors form one isolation mechanism in Swift concurrency."),
    ("mo-view-state", "mo.swiftui-state", "mo.swiftui-view", "qualifies", "State ownership qualifies SwiftUI view updates."),
    ("mo-binding-state", "mo.swiftui-binding", "mo.swiftui-state", "supports", "A binding supports mutation of externally owned SwiftUI state."),
    ("mo-environment-view", "mo.swiftui-environment", "mo.swiftui-view", "qualifies", "Environment values qualify descendant view behavior."),
    ("mo-identity-state", "mo.swiftui-identity", "mo.swiftui-state", "qualifies", "View identity qualifies persistence of framework-managed state."),
    ("mo-nav-swiftui", "mo.swiftui-navigation", "mo.swiftui-state", "transforms_to", "Navigation actions transform bound SwiftUI navigation state."),
    ("mo-preview-test", "mo.swiftui-preview", "sw.system-test", "undercuts", "A preview cannot replace system tests on shipped runtime paths."),
    ("mo-project-target", "mo.xcode-target", "mo.xcode-project", "part_of", "Targets form buildable products within Xcode projects."),
    ("mo-scheme-target", "mo.xcode-scheme", "mo.xcode-target", "qualifies", "A scheme qualifies target actions and build configurations."),
    ("mo-simulator-test", "mo.simulator", "sw.system-test", "supports", "Simulator execution supports repeatable platform system tests with declared limits."),
    ("mo-instruments-profile", "mo.instruments", "sw.profile", "implements", "Instruments implements Apple-platform performance profiling."),
    ("mo-package-project", "mo.package-manager", "mo.xcode-project", "supports", "Swift package resolution supports project dependency graphs."),
    ("mo-core-adapter", "mo.cross-platform-core", "mo.platform-adapter", "prerequisite", "A shared domain core is connected to native capabilities through platform adapters."),
    ("mo-ui-tradeoff", "mo.shared-ui-tradeoff", "mo.cross-platform-core", "qualifies", "Native quality requirements qualify how much UI can be shared."),
    ("mo-offline-sync", "mo.offline-sync", "fe.offline-model", "analogous_to", "Mobile and web offline models share queued-operation and reconciliation mechanisms."),
    ("mo-secure-secret", "mo.secure-storage", "mo.mobile-secret", "qualifies", "Platform secure storage qualifies per-device secret protection but cannot conceal embedded universal secrets."),
    ("mo-link-intent", "mo.deep-link-security", "mo.intent", "qualifies", "Deep-link validation qualifies external intent handling."),
    ("mo-ipc-sandbox", "mo.ipc-security", "mo.app-sandbox", "qualifies", "IPC authorization qualifies controlled crossings of the app sandbox."),
    ("mo-network-tls", "mo.network-security", "sw.secure-lifecycle", "part_of", "Mobile transport validation forms part of secure development."),
    ("mo-update-sign", "mo.update-security", "mo.signing", "supports", "Package signer identity supports secure mobile updates."),
    ("mo-text-layout", "mo.dynamic-type", "mo.adaptive-compose", "qualifies", "Dynamic text size qualifies adaptive layout geometry."),
    ("mo-reader-semantics", "mo.screen-reader", "fe.name-role-value", "analogous_to", "Mobile and web accessibility expose analogous name, role, value, state, and action semantics."),
    ("mo-touch-input", "mo.touch-target", "mo.switch-control", "qualifies", "Motor-access needs qualify target size and alternative input support."),
    ("bridge-requirement-ui", "sw.requirement", "fe.component-contract", "qualifies", "Product requirements qualify component states, behavior, and accessibility."),
    ("bridge-frontend-mobile-state", "fe.unidirectional-flow", "mo.udf", "analogous_to", "Frontend and mobile unidirectional data flow share explicit state ownership and event transitions."),
    ("bridge-design-mobile", "fe.design-token", "mo.resource", "transforms_to", "Semantic design tokens transform into Android and Apple resource values under platform constraints."),
    ("bridge-release-mobile", "sw.release", "mo.update-security", "qualifies", "Mobile signing and store rollout qualify the general release process."),
    ("bridge-test-mobile", "sw.test-pyramid", "mo.emulator", "qualifies", "A test portfolio qualifies which mobile behaviors require emulator and real-device evidence."),
]


CONTROLS = [
    ("sw-feature-need", "software-engineering", "software-engineering.requirements", SOFTWARE_LANES, "Feature substituted for need", "A requested feature must not be treated as the underlying stakeholder outcome without validating the need and alternatives."),
    ("sw-vague-quality", "software-engineering", "software-engineering.requirements", SOFTWARE_LANES, "Unmeasurable quality", "Words such as fast, scalable, intuitive, or secure must not count as acceptance criteria without workload, population, threshold, and context."),
    ("sw-diagram-architecture", "software-engineering", "software-engineering.architecture", SOFTWARE_LANES, "Diagram equals architecture", "A box diagram must not be treated as architecture without responsibilities, interfaces, dependencies, decisions, and quality consequences."),
    ("sw-pattern-default", "software-engineering", "software-engineering.design-patterns", SOFTWARE_LANES, "Pattern by fashion", "A familiar design pattern must not be selected without matching its forces and tradeoffs to the actual problem."),
    ("sw-mock-integration", "software-engineering", "software-engineering.testing", SOFTWARE_LANES, "Mocks prove integration", "Tests against mocked collaborators must not be reported as proof that real boundary contracts interoperate."),
    ("sw-coverage-quality", "software-engineering", "software-engineering.testing", SOFTWARE_LANES, "Coverage proves correctness", "High code coverage must not substitute for assertions, oracles, boundary cases, and requirement coverage."),
    ("sw-fix-before-cause", "software-engineering", "software-engineering.debugging", SOFTWARE_LANES, "Patch before diagnosis", "A plausible code change must not be called a root-cause fix until the reproducer and causal evidence explain why it works."),
    ("sw-benchmark-no-context", "software-engineering", "software-engineering.performance", SOFTWARE_LANES, "Context-free benchmark", "A speed number without workload, environment, version, warmup, repetitions, and distribution must not support a performance claim."),
    ("sw-average-tail", "software-engineering", "software-engineering.performance", SOFTWARE_LANES, "Mean hides tail", "Mean latency must not represent user experience when tail behavior or multiple populations materially differ."),
    ("sw-retry-loop", "software-engineering", "software-engineering.reliability", SOFTWARE_LANES, "Unbounded retry", "Retries must not be added without idempotency, budget, backoff, jitter, and overload analysis."),
    ("sw-timeout-failed", "software-engineering", "software-engineering.reliability", SOFTWARE_LANES, "Timeout proves failure", "A local timeout must not be treated as proof that a remote side effect did not occur."),
    ("sw-breaking-patch", "software-engineering", "software-engineering.build-release", SOFTWARE_LANES, "Breaking patch version", "A release with a public compatibility break must not be labeled a semantic patch update."),
    ("sw-deploy-release", "software-engineering", "software-engineering.build-release", SOFTWARE_LANES, "Deployment equals verified release", "Artifact deployment must not be reported as successful release before traffic, migration, and user-visible verification."),
    ("sw-destructive-migration", "software-engineering", "software-engineering.maintenance", SOFTWARE_LANES, "Unstaged destructive migration", "A destructive schema or platform change must not precede compatibility, backup, verification, and rollback evidence."),
    ("sw-sign-safe", "software-engineering", "software-engineering.secure-development", SOFTWARE_LANES, "Signed means safe", "A signed artifact must not be treated as benign without trusted source, build, dependency, and review evidence."),
    ("fe-div-button", "frontend-web-development", "frontend-web-development.semantic-html", FRONTEND_LANES, "Generic element as control", "A generic element with a click listener must not be treated as a complete accessible button."),
    ("fe-desktop-breakpoints", "frontend-web-development", "frontend-web-development.css-layout", FRONTEND_LANES, "Device-list responsiveness", "Responsive design must not assume fixed phone, tablet, and desktop widths while ignoring content and container constraints."),
    ("fe-type-untrusted", "frontend-web-development", "frontend-web-development.javascript-typescript", FRONTEND_LANES, "TypeScript validates network data", "A compile-time TypeScript annotation must not be treated as runtime validation of untrusted input."),
    ("fe-component-global", "frontend-web-development", "frontend-web-development.component-systems", FRONTEND_LANES, "Hidden global component contract", "A component must not silently depend on global state, styling, locale, or providers absent from its declared contract."),
    ("fe-duplicate-state", "frontend-web-development", "frontend-web-development.state-data", FRONTEND_LANES, "Duplicated derived state", "A derived value must not be independently mutated without an explicit synchronization and invalidation mechanism."),
    ("fe-stale-response", "frontend-web-development", "frontend-web-development.state-data", FRONTEND_LANES, "Stale response wins", "An older asynchronous response must not overwrite state owned by a newer request without correlation and policy."),
    ("fe-lazy-hidden", "frontend-web-development", "frontend-web-development.performance", FRONTEND_LANES, "Lazy loading hides content", "Deferral must not make core content undiscoverable to keyboard, assistive technology, search, or failed-script contexts."),
    ("fe-lab-only", "frontend-web-development", "frontend-web-development.performance", FRONTEND_LANES, "Laboratory average proves users", "One lab run must not replace real-user distributions across devices, routes, networks, and versions."),
    ("fe-snapshot-behavior", "frontend-web-development", "frontend-web-development.testing", FRONTEND_LANES, "Snapshot proves behavior", "A rendered snapshot must not substitute for interaction, state transition, accessibility, and boundary assertions."),
    ("fe-automated-a11y", "frontend-web-development", "frontend-web-development.accessibility", FRONTEND_LANES, "Automated scan proves accessible", "A passing automated accessibility scan must not be treated as complete keyboard, screen-reader, cognitive, or user evidence."),
    ("fe-aria-native", "frontend-web-development", "frontend-web-development.accessibility", FRONTEND_LANES, "ARIA replaces native behavior", "ARIA must not be used to imitate semantics when a native element already supplies correct interaction and platform behavior."),
    ("fe-token-hex", "frontend-web-development", "frontend-web-development.design-systems", FRONTEND_LANES, "Token as raw value", "A token named only by a hex value or size must not be treated as a stable semantic design decision."),
    ("fe-library-frozen", "frontend-web-development", "frontend-web-development.design-systems", FRONTEND_LANES, "Component library is finished", "A component library must not be treated as complete without ownership, versioning, adoption feedback, migration, and deprecation."),
    ("fe-dev-production", "frontend-web-development", "frontend-web-development.build-tooling", FRONTEND_LANES, "Development server as production", "A development server must not be exposed as a production security, caching, or reliability boundary."),
    ("fe-tree-sideeffect", "frontend-web-development", "frontend-web-development.build-tooling", FRONTEND_LANES, "Unsafe tree shaking", "Code must not be removed as unused when undeclared side effects or dynamic access invalidate the analysis."),
    ("fe-offline-current", "frontend-web-development", "frontend-web-development.progressive-web-apps", FRONTEND_LANES, "Offline cache is current", "Cached offline content must not be presented as current without freshness and reconciliation state."),
    ("mo-memory-durable", "mobile-android-apple", "mobile-android-apple.android-lifecycle", MOBILE_LANES, "Memory survives process death", "Activity, ViewModel, composition, or singleton memory must not be treated as durable Android application state."),
    ("mo-callback-order", "mobile-android-apple", "mobile-android-apple.android-lifecycle", MOBILE_LANES, "One lifecycle path", "A mobile component must not assume one ideal callback sequence while ignoring recreation, background, deep-link, and process-death entry paths."),
    ("mo-permission-trust", "mobile-android-apple", "mobile-android-apple.android-platform", MOBILE_LANES, "Permission makes input trusted", "A granted platform permission must not remove validation, authorization, privacy, or compromised-peer concerns."),
    ("mo-emulator-device", "mobile-android-apple", "mobile-android-apple.android-studio", MOBILE_LANES, "Emulator proves device behavior", "Emulator success must not establish real-device performance, sensors, vendor integrations, security hardware, or store delivery."),
    ("mo-global-scope", "mobile-android-apple", "mobile-android-apple.kotlin-android", MOBILE_LANES, "Unowned global coroutine", "Lifecycle work must not be launched into an unbounded global scope when cancellation and failure ownership are required."),
    ("mo-remember-save", "mobile-android-apple", "mobile-android-apple.compose", MOBILE_LANES, "Remember is durable", "A remembered Compose value must not be treated as surviving removal from composition or process death."),
    ("mo-sideeffect-body", "mobile-android-apple", "mobile-android-apple.compose", MOBILE_LANES, "Side effect in composable body", "A composable body must not perform uncontrolled external effects because recomposition can repeat, skip, or reorder execution."),
    ("mo-min-target", "mobile-android-apple", "mobile-android-apple.android-build", MOBILE_LANES, "SDK levels are interchangeable", "Minimum, target, and compile SDK values must not be treated as one version setting with identical effects."),
    ("mo-preview-test", "mobile-android-apple", "mobile-android-apple.swiftui", MOBILE_LANES, "Preview proves app behavior", "A SwiftUI preview must not replace device, lifecycle, navigation, persistence, performance, and accessibility testing."),
    ("mo-binding-owner", "mobile-android-apple", "mobile-android-apple.swiftui", MOBILE_LANES, "Binding owns state", "A SwiftUI Binding must not be treated as independent state ownership."),
    ("mo-actor-no-race", "mobile-android-apple", "mobile-android-apple.swift", MOBILE_LANES, "Actor eliminates logic races", "Actor isolation must not be treated as preventing reentrancy, stale assumptions across await, or multi-actor protocol races."),
    ("mo-sim-production", "mobile-android-apple", "mobile-android-apple.xcode", MOBILE_LANES, "Simulator equals production", "Simulator evidence must not establish device hardware, signing, entitlement, energy, thermal, or distribution behavior."),
    ("mo-shared-best", "mobile-android-apple", "mobile-android-apple.cross-platform", MOBILE_LANES, "Maximum reuse is optimal", "Cross-platform code reuse must not outrank native accessibility, lifecycle, performance, interaction, and maintainability requirements automatically."),
    ("mo-embedded-secret", "mobile-android-apple", "mobile-android-apple.mobile-security", MOBILE_LANES, "Embedded app secret", "A universal credential embedded in a distributed mobile binary must not be treated as secret from device owners."),
    ("mo-deeplink-auth", "mobile-android-apple", "mobile-android-apple.mobile-security", MOBILE_LANES, "Deep link implies authorization", "Possession of a deep-link URL must not authorize the referenced account, object, or action."),
    ("mo-color-only", "mobile-android-apple", "mobile-android-apple.mobile-accessibility", MOBILE_LANES, "Color-only mobile state", "A mobile interface must not communicate essential status or action only by color."),
]


WORKED_EXAMPLES = [
    ("sw", "requirement-trace", "Requirement trace", "A worked trace links a measurable offline-start requirement to an architecture decision, an integration test, its result, the shipped artifact, and production latency evidence.", "software-engineering.requirements", SOFTWARE_LANES, SOFTWARE_SOURCES),
    ("sw", "timeout-reconcile", "Ambiguous timeout reconciliation", "A payment request times out after transmission; the client uses its idempotency key to query outcome before retrying instead of assuming failure.", "software-engineering.reliability", SOFTWARE_LANES, SOFTWARE_SOURCES),
    ("sw", "canary-gate", "Canary release gate", "A canary compares error and tail-latency distributions against the control population, halts expansion on a predeclared threshold, and preserves the exact artifact identity.", "software-engineering.build-release", SOFTWARE_LANES, SOFTWARE_SOURCES),
    ("fe", "stale-search", "Stale search response", "A search UI assigns each query an identity and discards an older response that arrives after the newest query, preserving the current input-result relation.", "frontend-web-development.state-data", FRONTEND_LANES, FRONTEND_SOURCES),
    ("fe", "responsive-card", "Intrinsic responsive card", "A card uses semantic markup, grid min-max tracks, a container query, logical spacing, and a responsive image without device-name breakpoints.", "frontend-web-development.css-layout", FRONTEND_LANES, FRONTEND_SOURCES),
    ("fe", "accessible-dialog", "Accessible modal dialog", "A dialog names itself, moves focus on open, traps only while modal, supports Escape, hides background interaction, and restores focus to the opener.", "frontend-web-development.accessibility", FRONTEND_LANES, FRONTEND_SOURCES),
    ("fe", "offline-conflict", "Offline conflict reconciliation", "Two offline edits carry base versions; reconnect detects divergence, preserves both values, applies the domain merge rule, and surfaces unresolved conflict to the user.", "frontend-web-development.progressive-web-apps", FRONTEND_LANES, FRONTEND_SOURCES),
    ("mo", "android-restore", "Android process restoration", "A screen stores durable records in a repository and only a small record identifier in saved state, then reconstructs its ViewModel after process death.", "mobile-android-apple.android-lifecycle", MOBILE_LANES, MOBILE_SOURCES),
    ("mo", "compose-hoist", "Compose state hoisting", "A reusable filter composable receives an immutable selection and emits selection events while the screen ViewModel owns validation and persistence.", "mobile-android-apple.compose", MOBILE_LANES, MOBILE_SOURCES),
    ("mo", "swift-actor", "Swift actor reentrancy check", "An actor method reads a version, awaits remote work, then rechecks the version before committing because another message could mutate actor state during suspension.", "mobile-android-apple.swift", MOBILE_LANES, MOBILE_SOURCES),
    ("mo", "cross-platform-boundary", "Cross-platform capability boundary", "A shared sync engine emits typed storage requests while Android and Apple adapters map platform permissions, lifecycle, errors, and secure key services separately.", "mobile-android-apple.cross-platform", MOBILE_LANES, MOBILE_SOURCES),
    ("mo", "mobile-access", "Mobile accessibility matrix", "A worked screen is tested with large text, screen readers, keyboard, switch input, dark mode, increased contrast, reduced motion, and narrow landscape geometry.", "mobile-android-apple.mobile-accessibility", MOBILE_LANES, MOBILE_SOURCES),
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
    epistemic: str = "established",
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
        "scope": "software-engineering, frontend, and mobile-application foundation tranche",
        "limitations": [
            "Framework, SDK, browser, operating-system, store, and tool behavior is version-sensitive and must be refreshed.",
            "The world defines transferable mechanisms and representative platform boundaries; specialist APIs and ecosystems remain open.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "software-app-development-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def relation_owner(identifier: str) -> tuple[str, str, list[str], list[str]]:
    if identifier.startswith("sw-"):
        return "software-engineering", "software-engineering.architecture", SOFTWARE_LANES, SOFTWARE_SOURCES
    if identifier.startswith("fe-"):
        return "frontend-web-development", "frontend-web-development.component-systems", FRONTEND_LANES, FRONTEND_SOURCES
    if identifier.startswith("mo-"):
        return "mobile-android-apple", "mobile-android-apple.cross-platform", MOBILE_LANES, MOBILE_SOURCES
    return (
        "software-engineering",
        "software-engineering.architecture",
        sorted(set(SOFTWARE_LANES + FRONTEND_LANES + MOBILE_LANES)),
        sorted(set(SOFTWARE_SOURCES + FRONTEND_SOURCES + MOBILE_SOURCES)),
    )


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    groups = [
        ("sw", "software-engineering", SOFTWARE, SOFTWARE_LANES, SOFTWARE_SOURCES),
        ("fe", "frontend-web-development", FRONTEND, FRONTEND_LANES, FRONTEND_SOURCES),
        ("mo", "mobile-android-apple", MOBILE, MOBILE_LANES, MOBILE_SOURCES),
    ]
    roots = {"sw": "sw.root", "fe": "fe.root", "mo": "mo.root"}
    domains = {"sw": "software-engineering", "fe": "frontend-web-development", "mo": "mobile-android-apple"}

    for prefix, domain, entries, lanes, sources in groups:
        for index, (identifier, label, statement, subject) in enumerate(entries):
            node_id = f"{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        node_id, domain, subject, lanes, sources,
                        split_for(index, root=identifier == "root"), "concept",
                    ),
                    "label": label,
                    "statement": statement,
                    "aliases": [label.lower()],
                }
            )
            if identifier == "root":
                continue
            membership_id = f"sad.membership.{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        membership_id, domain, subject, lanes, sources,
                        edge_split_for(index), "relation",
                    ),
                    "label": f"{label} world membership",
                    "statement": f"{label} is a distinct component of the {domain} causal world with versioned applicability and failure conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": roots[prefix],
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared platform and foundation-world version apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in RELATIONS])
    for identifier, source, target, kind, statement in RELATIONS:
        domain, subject, lanes, sources = relation_owner(identifier)
        records.append(
            {
                **make_base(
                    f"sad.relation.{identifier}", domain, subject, lanes, sources,
                    splitter.split(kind, cross_requested=identifier.startswith("bridge-")), "relation",
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
                    "conditions": ["the stated contract, state, workload, lifecycle, and version assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, domain, subject, lanes, label, statement) in enumerate(CONTROLS):
        record_id = f"sad.control.{identifier}"
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
    for index, (prefix, identifier, label, statement, subject, lanes, sources) in enumerate(WORKED_EXAMPLES):
        split = example_splits[index % 4]
        domain = domains[prefix]
        node_id = f"{prefix}.example.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, lanes, sources, split, "worked_example"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", domain],
            }
        )
        membership_id = f"sad.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(membership_id, domain, subject, lanes, sources, split, "relation"),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded mechanism composition in the {domain} world.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": roots[prefix],
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains versioned and bounded"],
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
