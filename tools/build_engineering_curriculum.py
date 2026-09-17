#!/usr/bin/env python3
"""Author systems, mechanical, civil, aerospace, electrical, materials, and robotics engineering."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "engineering" / "foundations.jsonl"
WORLD = "engineering-v0"
LANES = ["thinking.bottom_up", "reasoning.causal", "reasoning.deductive", "geometry.structural", "creativity.constraint_based"]
GENERAL_SOURCES = ["nasa-systems-engineering-handbook", "nist-engineering-laboratory", "nist-measurement-uncertainty", "nist-sp800-218"]
MECH_SOURCES = ["nasa-systems-engineering-handbook", "faa-airworthiness-certification", "nist-engineering-laboratory", "nist-codata-2022"]
ELECTRICAL_SOURCES = ["nist-engineering-laboratory", "nist-codata-2022", "nist-measurement-uncertainty"]
MATERIALS_SOURCES = ["nist-engineering-laboratory", "nist-chemistry-webbook", "iupac-goldbook-500", "nist-measurement-uncertainty"]
ROBOTICS_SOURCES = ["nist-manufacturing-robotics", "nasa-systems-engineering-handbook", "nist-ai-rmf-10", "nist-measurement-uncertainty"]


ENGINEERING = [
    ("engineering.requirements", "requirements", "Requirements engineering", "Requirements engineering elicits stakeholder needs and transforms them into traceable, feasible, verifiable, versioned system obligations and constraints.", "Requirement statement", "A requirement names subject, required outcome, conditions, threshold, tolerance, interface, and verification method without embedding unnecessary design.", "Traceability chain", "Need, requirement, architecture, implementation, verification, validation, risk, and change records form an evidence chain.", "Preference is requirement", "A stakeholder preference must not become a mandatory requirement without authority, rationale, priority, and conflict resolution."),
    ("engineering.systems", "systems", "Systems engineering", "Systems engineering coordinates interacting people, hardware, software, data, operations, environment, interfaces, lifecycle, risk, and assurance around mission outcomes.", "System boundary", "A system boundary declares included elements, external actors, interfaces, environments, lifecycle stages, and responsibility.", "Technical baseline", "Requirements, architecture, interfaces, budgets, risks, and verification evidence are frozen into controlled baselines that evolve through change authority.", "Component success proves system success", "Passing component tests must not establish emergent system behavior, integration, mission validation, or lifecycle readiness."),
    ("engineering.design", "design", "Engineering design", "Engineering design generates and selects realizable solutions against functions, constraints, interfaces, uncertainty, safety, cost, and lifecycle tradeoffs.", "Design variable", "A design variable is a controllable choice with bounds, resolution, coupling, and manufacturing or operational feasibility.", "Trade study", "A trade study compares alternatives with common criteria, uncertainty, sensitivity, risk, and stakeholder weighting rather than one hidden score.", "Novel design is automatically better", "Novelty must not outrank requirement fit, evidence, manufacturability, safety, maintainability, and total lifecycle consequence."),
    ("engineering.modeling-simulation", "modeling-simulation", "Engineering modeling and simulation", "Engineering models represent selected structure and behavior for analysis, prediction, design, test planning, and decision under declared assumptions.", "Model abstraction", "A model abstraction preserves task-relevant variables and relations while omitting detail whose impact must be bounded.", "Simulation experiment", "Initial state, parameters, boundary conditions, solver, discretization, scenarios, and outputs form a reproducible simulation experiment.", "Simulation is physical test", "A simulation result must not be labeled observed hardware performance without model validation and uncertainty."),
    ("engineering.verification-validation", "verification-validation", "Engineering verification and validation", "Verification asks whether the implementation meets specified requirements, while validation asks whether the built system fulfills stakeholder needs in its intended context.", "Verification method", "Inspection, analysis, demonstration, or test is selected with acceptance criteria and configuration identity for each requirement.", "Validation evidence", "Representative users, missions, environments, hazards, operations, and outcomes provide validation evidence beyond specification conformance.", "Verification equals validation", "Meeting written requirements must not prove the requirements capture the right mission or stakeholder need."),
    ("engineering.reliability", "reliability", "Reliability and fault analysis", "Reliability engineering models failure modes, rates, dependencies, detection, tolerance, repair, common causes, and mission success over time.", "Failure mode", "A failure mode is a specific way an item loses or degrades required function under conditions and effects.", "Fault propagation", "Component faults propagate through interfaces and redundancy according to architecture, coverage, timing, and common-cause dependencies.", "Redundancy doubles reliability", "Adding a duplicate must not be assumed to improve reliability without independence, switching, detection, maintenance, and common-cause analysis."),
    ("engineering.safety", "safety", "Safety engineering", "Safety engineering identifies hazards and controls risk through design, barriers, procedures, assurance, operations, incident learning, and lifecycle governance.", "Hazard", "A hazard is a system state or condition with potential to cause harm, described independently from its probability.", "Hazard control", "Elimination, substitution, passive or active engineered barriers, warnings, procedures, training, and recovery reduce risk with differing reliability.", "No prior accident means safe", "Absence of observed accidents must not establish safety when exposure, reporting, sample size, latent hazards, or changed conditions are unresolved."),
    ("engineering.optimization", "optimization", "Engineering optimization", "Engineering optimization selects design or operating variables to improve objectives subject to physical, safety, discrete, robust, and lifecycle constraints.", "Design objective", "An objective quantifies one desired outcome with direction, units, aggregation, and stakeholder interpretation.", "Robust optimization", "Uncertain parameters and scenarios qualify feasible choices so performance remains acceptable across a declared uncertainty set or distribution.", "Optimal model solution is buildable", "A mathematical optimum must not be accepted without feasibility, tolerance, discrete, manufacturing, safety, and model-validity checks."),
    ("engineering.manufacturing", "manufacturing", "Manufacturing engineering", "Manufacturing engineering transforms designs into repeatable products through processes, tooling, metrology, variation control, quality, automation, supply, and feedback.", "Process capability", "Process capability compares stable manufacturing variation with specification limits under measurement and distribution assumptions.", "Process plan", "Material, operations, tooling, parameters, inspections, handling, traceability, and nonconformance rules transform design definition into product.", "Inspection creates quality", "End inspection must not substitute for capable processes, prevention, measurement validity, and root-cause control."),
    ("engineering.maintenance", "maintenance", "Maintenance and lifecycle engineering", "Lifecycle engineering manages condition, inspection, repair, spares, upgrades, obsolescence, configuration, disposal, and feedback from operation.", "Degradation state", "A degradation state records damage, wear, corrosion, drift, software aging, contamination, or remaining margin relative to function.", "Maintenance policy", "Condition evidence, failure consequence, access, resources, interval, repair quality, and uncertainty determine preventive, predictive, or corrective action.", "Scheduled replacement guarantees health", "A calendar interval must not prove current condition or remove infant mortality, installation, hidden, and common-cause failures."),
]


MECHANICAL = [
    ("mechanical-civil-aerospace.mechanics", "mechanics", "Solid and structural mechanics", "Structural mechanics relates loads, supports, stress, strain, stiffness, stability, fatigue, fracture, geometry, and material response.", "Free-body model", "A free-body model isolates a body and represents every external force, moment, constraint, and coordinate convention.", "Load-path response", "Equilibrium, compatibility, constitutive laws, geometry, and boundary conditions transform loads into deformation and internal stress.", "Safety factor replaces failure analysis", "A scalar factor of safety must not replace mode, uncertainty, fatigue, fracture, instability, and consequence analysis."),
    ("mechanical-civil-aerospace.thermofluids", "thermofluids", "Thermofluids", "Thermofluids integrates fluid mechanics, heat transfer, thermodynamics, combustion, phase change, and energy systems.", "Control volume", "A control volume defines mass, momentum, species, and energy crossing a boundary and accumulating inside.", "Transport balance", "Advection, diffusion, pressure work, viscous stress, heat transfer, reaction, and storage determine thermofluid evolution.", "Steady means no flow", "Steady state must not be confused with zero flow or zero energy transfer; it means time-invariant modeled fields."),
    ("mechanical-civil-aerospace.machines", "machines", "Machines and mechanisms", "Machine design relates motion, force, power, geometry, materials, joints, bearings, gears, actuators, tolerances, lubrication, and failure.", "Kinematic pair", "A kinematic pair constrains relative motion between linked bodies through joints, contacts, or compliant elements.", "Power transmission", "Torque, speed, forces, efficiency, contact, dynamics, and losses transmit power through a machine chain.", "Kinematics proves strength", "A mechanism moving as intended must not establish load capacity, fatigue life, stability, or safe guarding."),
    ("mechanical-civil-aerospace.civil-structures", "civil-structures", "Civil structures", "Civil structural engineering designs buildings, bridges, foundations, and infrastructure for load, serviceability, durability, hazards, construction, and public safety.", "Load combination", "A load combination applies code-defined concurrent permanent, occupancy, wind, seismic, thermal, and other effects with factors and limits.", "Structural system response", "Members, connections, diaphragms, foundations, nonlinear behavior, and load paths distribute demands and deformations.", "Code minimum proves zero risk", "Meeting a prescriptive code minimum must not be presented as eliminating residual risk, deterioration, misuse, or out-of-scope hazards."),
    ("mechanical-civil-aerospace.geotechnical", "geotechnical", "Geotechnical engineering", "Geotechnical engineering models soil and rock strength, stiffness, water, consolidation, foundations, slopes, excavation, and site variability.", "Site model", "A site model integrates stratigraphy, groundwater, material properties, spatial variability, investigation limits, and design scenarios.", "Effective-stress response", "Total stress, pore pressure, drainage, loading rate, constitutive behavior, and history determine effective stress and deformation.", "One borehole defines site", "A single investigation point must not be generalized to a heterogeneous site without spatial and geological evidence."),
    ("mechanical-civil-aerospace.transportation", "transportation", "Transportation engineering", "Transportation engineering designs and operates movement systems using demand, capacity, safety, geometry, control, human behavior, equity, maintenance, and environmental evidence.", "Traffic flow state", "Flow, density, speed, vehicle mix, arrivals, queues, and control describe a transportation stream under location and time.", "Network assignment", "Traveler choices, capacities, controls, incidents, schedules, and feedback distribute demand across a network.", "More lanes always reduce congestion", "Added capacity must not be assumed to reduce long-term congestion without induced demand, bottleneck, land-use, safety, and mode analysis."),
    ("mechanical-civil-aerospace.aerodynamics", "aerodynamics", "Aerodynamics", "Aerodynamics studies forces, moments, flow, boundary layers, compressibility, turbulence, shocks, and aeroelastic coupling around moving bodies.", "Flow condition", "Mach number, Reynolds number, geometry, angle, roughness, turbulence, and atmosphere define an aerodynamic condition.", "Pressure-shear loading", "Flow solution and surface stresses integrate into lift, drag, moment, heating, and unsteady loads.", "Wind-tunnel result transfers directly", "A model test must not transfer to full scale without similarity, wall, support, transition, Reynolds, Mach, and uncertainty corrections."),
    ("mechanical-civil-aerospace.flight-dynamics", "flight-dynamics", "Flight dynamics", "Flight dynamics models aircraft translation, rotation, stability, control, navigation, atmosphere, propulsion, configuration, and pilot or autonomy interaction.", "Aircraft state", "Position, velocity, attitude, angular rate, mass, configuration, atmosphere, and control inputs define a flight-dynamics state.", "Stability and control response", "Aerodynamic, inertial, propulsive, gravity, control, delay, and disturbance effects determine modes and trajectories.", "Stable aircraft is controllable everywhere", "Passive stability must not establish control authority, handling quality, envelope safety, or recovery from every state."),
    ("mechanical-civil-aerospace.propulsion", "propulsion", "Propulsion", "Propulsion engineering converts stored, chemical, electrical, nuclear, or environmental energy into thrust under mass, thermal, structural, acoustic, and emissions constraints.", "Propulsive control volume", "Mass flow, momentum, pressure, energy, composition, and area across an engine control volume determine ideal thrust and efficiency.", "Energy-to-thrust chain", "Energy release, working-fluid acceleration, nozzle or propulsor interaction, and losses produce thrust across an operating map.", "Peak thrust defines mission performance", "One maximum thrust value must not establish efficiency, endurance, transient, thermal, reliability, altitude, noise, or integration performance."),
]


ELECTRICAL = [
    ("electrical-electronics-control.circuits", "circuits", "Circuit theory", "Circuit theory models voltage, current, charge, power, energy, components, topology, transients, frequency response, and network constraints.", "Circuit graph", "Nodes, branches, sources, impedances, references, and orientation define the circuit topology and variables.", "Kirchhoff-constrained response", "Charge and energy conservation plus component constitutive laws determine circuit voltages and currents.", "Schematic proves physical behavior", "An ideal schematic must not establish parasitic, thermal, tolerance, layout, saturation, and safety behavior."),
    ("electrical-electronics-control.electronics", "electronics", "Analog and digital electronics", "Electronics engineers devices and circuits for amplification, switching, conversion, logic, memory, timing, and interfaces under nonideal constraints.", "Operating point", "An operating point sets device voltages, currents, modes, temperature, and margins around which small-signal or switching behavior is analyzed.", "Signal transformation", "Device characteristics, feedback, bias, loading, noise, bandwidth, and power transform input signals into outputs.", "Digital signal has only zero and one voltage", "Logic levels must not be treated as exact voltages without thresholds, noise margins, timing, and transition behavior."),
    ("electrical-electronics-control.signal-processing", "signal-processing", "Signal processing", "Signal processing represents, filters, transforms, estimates, compresses, detects, and reconstructs signals under sampling and noise models.", "Signal representation", "A signal representation declares domain, sampling, units, bandwidth, channels, phase, quantization, and time reference.", "Filter response", "Impulse or state response, coefficients, initial conditions, numerical precision, and boundary handling determine filtered output.", "FFT changes information content automatically", "A Fourier transform must not be described as creating frequency information or improving SNR without processing and model context."),
    ("electrical-electronics-control.control", "control", "Control theory", "Control engineering shapes dynamical-system behavior through sensing, estimation, feedback, feedforward, actuation, stability, robustness, and constraints.", "Plant model", "A plant model maps state and input to evolution and output under disturbances, uncertainty, delay, and operating regime.", "Closed-loop feedback", "Measured error and controller state alter actuation, changing poles, sensitivity, disturbance rejection, and stability margins.", "Feedback always stabilizes", "Closing a feedback loop must not be assumed stable without sign, delay, gain, dynamics, saturation, and uncertainty analysis."),
    ("electrical-electronics-control.power", "power", "Power systems", "Power engineering coordinates generation, conversion, transmission, distribution, storage, protection, stability, markets, loads, and safety.", "Power-flow state", "Bus voltage magnitudes and angles, injections, network impedances, limits, and topology define a steady power-flow model.", "Grid balance", "Generation, load, storage, losses, reserves, frequency control, voltage support, and network limits jointly maintain service.", "Energy capacity equals power capability", "Stored energy must not be substituted for instantaneous power, ramp, thermal, voltage, and duration capability."),
    ("electrical-electronics-control.embedded", "embedded", "Embedded systems", "Embedded engineering integrates processors, memory, peripherals, firmware, timing, power, sensors, actuators, communication, safety, and hardware constraints.", "Hardware-software interface", "Registers, buses, interrupts, DMA, clocks, pins, memory maps, and protocol timing form the hardware-software contract.", "Real-time task chain", "Interrupts, scheduling, computation, communication, actuation, deadlines, and watchdogs determine end-to-end embedded response.", "Fast average proves deadline", "Average execution speed must not establish worst-case real-time deadline satisfaction."),
    ("electrical-electronics-control.semiconductors", "semiconductors", "Semiconductor devices", "Semiconductor engineering relates band structure, carriers, doping, junctions, fields, transport, fabrication, variability, and device circuits.", "Carrier distribution", "Electron and hole populations depend on energy bands, doping, temperature, injection, fields, and nonequilibrium processes.", "Junction control", "Built-in potentials and applied bias alter depletion, carrier injection, recombination, and current in semiconductor junctions.", "Ideal diode equation covers all operation", "An ideal compact equation must not be extended beyond breakdown, high injection, series resistance, temperature, frequency, and geometry limits."),
    ("electrical-electronics-control.instrumentation", "instrumentation", "Instrumentation", "Instrumentation engineering converts physical quantities into calibrated signals and decisions through sensors, conditioning, acquisition, timing, processing, uncertainty, and interfaces.", "Sensor transfer function", "A sensor transfer function maps a measurand and influence quantities to output with sensitivity, offset, noise, hysteresis, range, and dynamics.", "Measurement chain", "Sensing, conditioning, conversion, synchronization, calibration, processing, and display transform a measurand into a reported value.", "Resolution equals accuracy", "Fine display resolution must not be treated as low measurement uncertainty or traceable accuracy."),
    ("electrical-electronics-control.rf", "rf", "Radio-frequency engineering", "RF engineering designs distributed circuits, antennas, propagation, matching, oscillators, amplifiers, mixers, noise, modulation, and electromagnetic compatibility.", "Scattering parameter", "A scattering parameter relates incident and reflected traveling waves at network ports under reference impedance and frequency.", "Impedance matching", "Matching networks transform impedance to control reflection and power transfer over a frequency, power, tolerance, and stability range.", "Matched port means all power delivered usefully", "A low reflection coefficient must not prove efficiency, radiation, linearity, stability, or useful load absorption."),
]


MATERIALS = [
    ("materials-chemical-engineering.structure-property", "structure-property", "Structure-property relationships", "Materials engineering connects composition and structure across electronic, atomic, microstructural, mesoscopic, and component scales to processing and properties.", "Material microstructure", "Phases, grains, defects, interfaces, texture, porosity, residual stress, and spatial distributions define microstructure.", "Process-structure-property chain", "Processing history transforms structure, which mediates mechanical, thermal, electrical, optical, chemical, and degradation behavior.", "Composition alone determines property", "Nominal composition must not establish material performance without process, microstructure, condition, geometry, and test evidence."),
    ("materials-chemical-engineering.metallurgy", "metallurgy", "Metallurgy", "Metallurgy studies metallic phases, solidification, thermomechanical processing, heat treatment, deformation, fracture, corrosion, joining, and recycling.", "Phase diagram", "A phase diagram maps equilibrium phases against composition, temperature, pressure, or other variables under a defined system.", "Heat-treatment transformation", "Time-temperature history, diffusion, nucleation, growth, deformation, and cooling transform metallic microstructure and properties.", "Equilibrium diagram predicts every process", "An equilibrium phase diagram must not be used as a kinetic transformation path without time and nonequilibrium evidence."),
    ("materials-chemical-engineering.ceramics", "ceramics", "Ceramics", "Ceramic engineering studies inorganic nonmetallic powders, forming, sintering, phases, grain boundaries, defects, brittle fracture, thermal behavior, and functional properties.", "Ceramic green body", "A green body is a formed but unsintered particle compact with binder, density, pores, gradients, and handling strength.", "Sintering", "Diffusion and interfacial-energy reduction densify and coarsen a ceramic while atmosphere, temperature, time, and additives control phases and pores.", "Hard ceramic cannot fail", "High hardness must not be treated as toughness, flaw tolerance, thermal-shock resistance, or damage immunity."),
    ("materials-chemical-engineering.polymers", "polymers", "Polymer materials", "Polymer materials engineering relates chain chemistry, molecular weight, architecture, crystallinity, crosslinks, additives, processing, viscoelasticity, and aging.", "Polymer morphology", "Amorphous, crystalline, phase-separated, oriented, filled, and crosslinked structures define polymer morphology across scales.", "Time-temperature response", "Segmental mobility and relaxation make polymer stiffness, creep, damping, and failure depend strongly on time and temperature.", "One elastic modulus describes polymer", "A single modulus must not represent viscoelastic response across time, temperature, strain, frequency, and history."),
    ("materials-chemical-engineering.composites", "composites", "Composite materials", "Composite engineering combines constituents and interfaces to tailor anisotropic stiffness, strength, toughness, weight, transport, and damage.", "Composite architecture", "Fiber, particle, matrix, interface, orientation, stacking, volume fraction, defects, and geometry define composite architecture.", "Load transfer", "Interfacial shear and constituent deformation transfer load, while matrix cracking, debonding, delamination, and fiber failure interact.", "Rule of mixtures proves strength", "A simple constituent average must not establish composite strength, failure mode, defects, interface, or multiaxial behavior."),
    ("materials-chemical-engineering.process-design", "process-design", "Chemical process design", "Process design converts feeds into products through unit operations, reactions, recycles, utilities, controls, economics, environmental constraints, and safety.", "Process flowsheet", "A flowsheet represents streams, compositions, conditions, equipment, recycles, controls, and boundaries for mass and energy balances.", "Process integration", "Material and energy balances, thermodynamics, kinetics, transport, separation, heat recovery, and control determine process performance.", "Steady simulation proves operability", "A converged steady flowsheet must not establish startup, shutdown, control, upset, fouling, safety, and maintainability."),
    ("materials-chemical-engineering.transport", "transport", "Transport phenomena", "Transport phenomena studies momentum, heat, and mass transfer through conservation laws, constitutive fluxes, geometry, boundary layers, and dimensionless scaling.", "Flux", "A flux measures a transported extensive quantity per area and time with direction and constitutive dependence.", "Gradient-driven transport", "Velocity, temperature, chemical-potential, concentration, and pressure gradients drive transport under regime-specific laws.", "Transport coefficient is universal constant", "A viscosity, diffusivity, or conductivity must not be moved across composition, temperature, pressure, phase, and microstructure without evidence."),
    ("materials-chemical-engineering.reactors", "reactors", "Reaction engineering", "Reaction engineering couples kinetics, transport, residence time, mixing, heat, pressure, catalysis, deactivation, and safety to reactor performance.", "Residence-time distribution", "A residence-time distribution describes how long flowing material spends inside a reactor and exposes mixing departures from ideal models.", "Reaction-transport coupling", "Intrinsic kinetics, mass transfer, heat transfer, mixing, phase contact, and catalyst state jointly determine observed conversion and selectivity.", "Higher temperature always improves reactor", "Temperature increase must not be assumed beneficial when equilibrium, side reactions, deactivation, heat removal, pressure, and safety change."),
    ("materials-chemical-engineering.process-safety", "process-safety", "Process safety", "Process safety prevents catastrophic releases, fires, explosions, runaway reactions, toxic exposure, and cascading loss through inherently safer design and independent protection.", "Hazard scenario", "A scenario links initiating event, failed or successful barriers, process dynamics, release, escalation, exposure, and consequence.", "Layer of protection", "Independent preventive and mitigative layers reduce scenario frequency or consequence only when effectiveness, independence, testing, and common causes hold.", "Personal protective equipment is primary process safety", "PPE must not replace inventory reduction, substitution, containment, control, relief, detection, shutdown, and siting for major hazards."),
]


ROBOTICS = [
    ("robotics-autonomy.kinematics", "kinematics", "Robot kinematics", "Robot kinematics maps joint or actuator coordinates to body pose, velocity, and geometric constraints without considering forces.", "Configuration space", "Configuration space represents all robot configurations with joint limits, topology, collision regions, and constraints.", "Forward and inverse kinematics", "Forward kinematics composes transforms from joints to pose, while inverse kinematics solves configurations for a desired pose with multiplicity and reachability.", "Inverse kinematics always unique", "A requested pose must not be assigned one joint solution without reachability, singularity, joint limit, redundancy, and collision analysis."),
    ("robotics-autonomy.dynamics", "dynamics", "Robot dynamics", "Robot dynamics relates mass, inertia, forces, torques, contacts, actuators, constraints, and motion through equations of motion.", "Robot state", "A dynamics state includes configuration and velocity plus actuator, contact, and environment state needed by the model.", "Force-motion propagation", "Actuator forces, gravity, inertia, Coriolis terms, friction, contact, and constraints determine acceleration and impact response.", "Kinematic plan is dynamically feasible", "A collision-free geometric path must not be treated as executable without velocity, acceleration, torque, contact, and stability limits."),
    ("robotics-autonomy.control", "control", "Robot control", "Robot control converts desired task behavior and estimated state into bounded actuator commands under dynamics, uncertainty, delay, contact, and safety constraints.", "Feedback policy", "A feedback policy maps estimated state and reference to control actions with gains, limits, and internal state.", "Closed-loop tracking", "Estimation, controller dynamics, actuation, plant response, disturbances, and sensing form a closed causal loop.", "Simulation tuning proves hardware stability", "Controller performance in one simulation must not establish real hardware stability, saturation, delay, contact, or fault behavior."),
    ("robotics-autonomy.perception", "perception", "Robot perception", "Robot perception transforms time-synchronized sensor data into uncertain estimates of objects, geometry, motion, material, and affordances.", "Sensor observation", "A sensor observation has calibration, frame, timestamp, field of view, resolution, noise, occlusion, and environmental conditions.", "Perceptual inference", "Measurement models, priors, features, learned representations, fusion, tracking, and uncertainty transform observations into state hypotheses.", "Classifier confidence is physical certainty", "A perception score must not be treated as calibrated physical truth outside its sensor, population, and environmental validation."),
    ("robotics-autonomy.localization-mapping", "localization-mapping", "Localization and mapping", "Localization and mapping estimate robot pose and environment structure from motion and observations under frame, association, drift, and uncertainty.", "Pose graph", "A pose graph represents robot states as nodes and relative-motion or observation constraints as uncertain edges.", "Loop closure", "Recognizing a previously observed place adds a long-range constraint that can correct accumulated drift if data association is valid.", "Map is exact territory", "A robot map must not be treated as complete, current, frame-free, resolution-free, or uncertainty-free physical reality."),
    ("robotics-autonomy.planning", "planning", "Motion and task planning", "Planning searches action, configuration, trajectory, or task spaces for feasible goal-reaching behavior under dynamics, uncertainty, resources, and costs.", "Planning state", "A planning state abstracts robot, environment, task, resources, beliefs, and time needed to predict action feasibility and consequence.", "Search and optimization", "Successor generation, constraints, heuristics, sampling, optimization, collision checks, and replanning produce candidate actions or trajectories.", "Shortest path is safest plan", "Minimum geometric length must not replace clearance, dynamics, uncertainty, interaction, energy, rules, and failure recovery."),
    ("robotics-autonomy.human-robot", "human-robot", "Human-robot interaction", "Human-robot interaction studies shared tasks, communication, trust, intent, ergonomics, accessibility, authority, workload, and social and physical effects.", "Interaction role", "A role defines what human and robot can observe, decide, command, override, explain, and remain responsible for.", "Shared-control loop", "Human intent, robot inference, interface feedback, automation, environment, and correction form a coupled control and decision loop.", "Human presence guarantees oversight", "A human in the loop must not be treated as effective oversight without attention, time, understanding, authority, and usable intervention."),
    ("robotics-autonomy.safety", "safety", "Autonomy safety", "Autonomy safety limits harm from sensing, learning, planning, control, actuation, interaction, misuse, faults, and distribution shift through layered assurance.", "Operational design domain", "An operational design domain declares environments, actors, speeds, weather, maps, sensors, rules, and conditions in which an autonomous function is intended to operate.", "Safety envelope", "Independent monitors, constraints, redundancy, fallback, safe stop, geofencing, validation, and incident response bound autonomous actions.", "Passed demo proves safe autonomy", "A successful demonstration must not establish safety across rare events, distribution shifts, faults, adversarial behavior, and lifetime operation."),
]


CROSS_RELATIONS = [
    ("eng-need-requirement", "eng.requirements.primitive", "eng.requirements.mechanism", "supports", "Verifiable requirement statements support traceability from needs through evidence."),
    ("eng-requirement-system", "eng.requirements.mechanism", "eng.systems.primitive", "qualifies", "Traceable requirements qualify the controlled system boundary and baseline."),
    ("eng-system-design", "eng.systems.mechanism", "eng.design.mechanism", "qualifies", "Technical baselines qualify the alternatives compared in design trade studies."),
    ("eng-model-design", "eng.modeling-simulation.mechanism", "eng.design.mechanism", "supports", "Validated simulation experiments support quantitative design trade studies."),
    ("eng-verify-requirement", "eng.verification-validation.primitive", "eng.requirements.primitive", "measures", "Verification methods measure satisfaction of allocated requirements."),
    ("eng-fault-reliability", "eng.reliability.mechanism", "eng.systems.primitive", "qualifies", "Fault propagation qualifies system boundaries and redundancy architecture."),
    ("eng-hazard-design", "eng.safety.mechanism", "eng.design.mechanism", "qualifies", "Hazard controls qualify acceptable design alternatives."),
    ("eng-opt-design", "eng.optimization.mechanism", "eng.design.primitive", "supports", "Robust optimization supports selection of design variables under uncertainty."),
    ("eng-design-manufacture", "eng.design.primitive", "eng.manufacturing.mechanism", "qualifies", "Design tolerances and variables qualify the manufacturing process plan."),
    ("eng-manufacture-maintain", "eng.manufacturing.mechanism", "eng.maintenance.primitive", "causes", "Manufacturing variation and records cause initial condition differences tracked through lifecycle maintenance."),
    ("mech-load-structure", "mech.mechanics.primitive", "mech.mechanics.mechanism", "causes", "External loads cause internal structural response through the load path."),
    ("mech-thermal-structure", "mech.thermofluids.mechanism", "mech.mechanics.mechanism", "qualifies", "Temperature and fluid loads qualify structural stress and deformation."),
    ("mech-machine-power", "mech.machines.mechanism", "mech.thermofluids.primitive", "supports", "Machine power transmission supports thermofluid energy conversion and pumping."),
    ("mech-geotech-civil", "mech.geotechnical.primitive", "mech.civil-structures.mechanism", "qualifies", "Site and foundation response qualify civil structural load paths."),
    ("mech-transport-civil", "mech.transportation.mechanism", "mech.civil-structures.primitive", "qualifies", "Transportation demand and vehicle loads qualify infrastructure design combinations."),
    ("mech-aero-flight", "mech.aerodynamics.mechanism", "mech.flight-dynamics.mechanism", "causes", "Integrated aerodynamic forces and moments cause aircraft state evolution."),
    ("mech-prop-flight", "mech.propulsion.mechanism", "mech.flight-dynamics.primitive", "causes", "Propulsive thrust and moments cause changes in aircraft state."),
    ("mech-cert-flight", "eng.verification-validation.mechanism", "mech.flight-dynamics.root", "supports", "Representative ground and flight evidence supports validation and airworthiness findings."),
    ("elec-circuit-electronic", "elec.circuits.mechanism", "elec.electronics.mechanism", "supports", "Circuit constraints support electronic signal transformation analysis."),
    ("elec-signal-control", "elec.signal-processing.mechanism", "elec.control.primitive", "supports", "Filtering and estimation support control-state feedback."),
    ("elec-control-power", "elec.control.mechanism", "elec.power.mechanism", "supports", "Closed-loop control supports frequency, voltage, converter, and resource balance."),
    ("elec-embedded-control", "elec.embedded.mechanism", "elec.control.mechanism", "implements", "Real-time embedded task chains implement digital control loops."),
    ("elec-semiconductor-electronic", "elec.semiconductors.mechanism", "elec.electronics.primitive", "grounds", "Semiconductor junction behavior grounds electronic device models."),
    ("elec-instrument-control", "elec.instrumentation.mechanism", "elec.control.primitive", "supports", "Calibrated measurement chains support feedback control."),
    ("elec-rf-circuit", "elec.rf.mechanism", "elec.circuits.primitive", "qualifies", "Distributed matching qualifies circuit behavior at radio frequencies."),
    ("mat-process-structure", "mat.structure-property.mechanism", "eng.manufacturing.mechanism", "supports", "Processing-to-structure relations support manufacturing parameter selection."),
    ("mat-metal-structure", "mat.metallurgy.mechanism", "mat.structure-property.primitive", "causes", "Heat treatment causes metallic microstructure changes."),
    ("mat-ceramic-structure", "mat.ceramics.mechanism", "mat.structure-property.primitive", "causes", "Sintering causes ceramic density, grain, pore, and phase changes."),
    ("mat-polymer-structure", "mat.polymers.mechanism", "mat.structure-property.primitive", "qualifies", "Polymer morphology qualifies time-temperature material response."),
    ("mat-composite-load", "mat.composites.mechanism", "mech.mechanics.mechanism", "qualifies", "Constituent load transfer qualifies composite structural response."),
    ("mat-flowsheet-reactor", "mat.process-design.primitive", "mat.reactors.mechanism", "qualifies", "Flowsheet balances qualify reactor feeds, recycles, and heat integration."),
    ("mat-transport-reactor", "mat.transport.mechanism", "mat.reactors.mechanism", "qualifies", "Transport gradients qualify observed reactor conversion and selectivity."),
    ("mat-safety-process", "mat.process-safety.mechanism", "mat.process-design.mechanism", "qualifies", "Independent protection layers qualify acceptable process integration."),
    ("rob-kin-dyn", "rob.kinematics.mechanism", "rob.dynamics.primitive", "prerequisite", "Kinematic transforms and Jacobians are prerequisites to robot dynamic models."),
    ("rob-dyn-control", "rob.dynamics.mechanism", "rob.control.primitive", "qualifies", "Robot dynamics qualify feasible controller commands and stability."),
    ("rob-perception-local", "rob.perception.mechanism", "rob.localization-mapping.mechanism", "supports", "Perceptual observations support pose-graph constraints and loop closure."),
    ("rob-map-plan", "rob.localization-mapping.primitive", "rob.planning.primitive", "qualifies", "Map frame, geometry, and uncertainty qualify planning state."),
    ("rob-plan-control", "rob.planning.mechanism", "rob.control.mechanism", "qualifies", "Planned trajectories qualify controller references."),
    ("rob-human-plan", "rob.human-robot.mechanism", "rob.planning.primitive", "qualifies", "Shared-control roles qualify robot task planning and authority."),
    ("rob-safety-all", "rob.safety.mechanism", "rob.control.mechanism", "inhibits", "A safety envelope inhibits unsafe control commands and triggers fallback."),
    ("bridge-req-robot", "eng.requirements.primitive", "rob.safety.primitive", "qualifies", "Safety requirements qualify the autonomous operational design domain."),
    ("bridge-model-aero", "eng.modeling-simulation.mechanism", "mech.aerodynamics.mechanism", "supports", "Validated simulations support aerodynamic load prediction within similarity limits."),
    ("bridge-reliability-power", "eng.reliability.mechanism", "elec.power.mechanism", "qualifies", "Fault propagation and common causes qualify power-system redundancy and reserves."),
    ("bridge-manufacturing-material", "eng.manufacturing.mechanism", "mat.structure-property.mechanism", "causes", "Manufacturing process history causes material structure and property variation."),
]


WORKED_EXAMPLES = [
    ("eng", "trace", "Requirement evidence trace", "A braking-distance need becomes a bounded requirement, is allocated to sensing and actuation, verified by component and integration tests, then validated on representative surfaces and users.", "engineering.requirements"),
    ("eng", "fault-tree", "Fault propagation example", "A top loss requires either independent channel failures plus failed detection or a shared power cause; common-cause terms prevent multiplying independent rates blindly.", "engineering.reliability"),
    ("mech", "free-body", "Structural free-body model", "A beam model includes distributed load, support reactions, connection release, self-weight, coordinate signs, and equilibrium before stress is calculated.", "mechanical-civil-aerospace.mechanics"),
    ("mech", "scale-test", "Aerodynamic scale test", "A model test matches Mach number and key geometry, quantifies Reynolds mismatch and wall corrections, and carries those uncertainties into full-scale loads.", "mechanical-civil-aerospace.aerodynamics"),
    ("elec", "feedback-delay", "Delayed feedback example", "A controller stable in a no-delay model becomes oscillatory after sensor, computation, communication, and actuator delay shift loop phase across the gain crossover.", "electrical-electronics-control.control"),
    ("elec", "measurement-chain", "Instrumentation chain", "A temperature report preserves sensor calibration, self-heating, lead resistance, ADC reference, sampling, filtering, mounting, and uncertainty.", "electrical-electronics-control.instrumentation"),
    ("mat", "heat-treatment", "Metallurgical process chain", "Alloy composition plus heating, hold, quench, and temper history produces a measured phase and hardness profile with geometry-dependent cooling uncertainty.", "materials-chemical-engineering.metallurgy"),
    ("mat", "reactor-hotspot", "Reactor hotspot example", "Exothermic kinetics accelerate with temperature while heat removal saturates, creating positive feedback that requires relief, shutdown, and validated runaway scenarios.", "materials-chemical-engineering.process-safety"),
    ("rob", "pose-graph", "Robot loop closure", "Odometry accumulates drift until a validated place match adds a loop constraint; robust optimization shifts the pose graph while preserving an outlier alternative.", "robotics-autonomy.localization-mapping"),
    ("rob", "safe-stop", "Autonomy safe stop", "Sensor disagreement leaves the operational domain; an independent monitor bounds speed, selects a verified stopping corridor, alerts the operator, and records the trigger.", "robotics-autonomy.safety"),
    ("rob", "dynamic-path", "Dynamically feasible robot path", "A geometric path is time-parameterized only after joint limits, torque, acceleration, contact, payload, collision margin, and emergency stopping are satisfied.", "robotics-autonomy.dynamics"),
    ("eng", "canary-manufacture", "Manufacturing process qualification", "A process window is qualified with measurement-system analysis, capability, destructive tests, traceable lots, nonconformance rules, and a limited production ramp.", "engineering.manufacturing"),
]


GROUPS = [
    ("eng", "engineering", ENGINEERING, GENERAL_SOURCES, "Engineering foundations", "Engineering converts needs into verified and maintainable systems through requirements, architecture, design, models, evidence, reliability, safety, optimization, manufacturing, and lifecycle feedback."),
    ("mech", "mechanical-civil-aerospace", MECHANICAL, MECH_SOURCES, "Mechanical, civil, and aerospace engineering", "Mechanical, civil, and aerospace engineering coordinate loads, motion, fluids, heat, structures, soils, transport, flight, propulsion, materials, construction, and certification."),
    ("elec", "electrical-electronics-control", ELECTRICAL, ELECTRICAL_SOURCES, "Electrical, electronics, and control engineering", "Electrical engineering coordinates circuits, devices, signals, feedback, power, embedded computation, semiconductors, instruments, and electromagnetic systems."),
    ("mat", "materials-chemical-engineering", MATERIALS, MATERIALS_SOURCES, "Materials and chemical engineering", "Materials and chemical engineering connect composition, structure, processing, transport, reaction, equipment, safety, and lifecycle performance."),
    ("rob", "robotics-autonomy", ROBOTICS, ROBOTICS_SOURCES, "Robotics and autonomy", "Robotics and autonomy integrate geometry, dynamics, sensing, estimation, mapping, planning, control, human interaction, computing, and safety under uncertainty."),
]


def split_for(index: int) -> str:
    if index and index % 23 == 0:
        return "cross_domain_holdout"
    if index and index % 17 == 0:
        return "sealed_test"
    if index and index % 13 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    domain: str,
    subject: str,
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
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "engineering design, implementation, assurance, and lifecycle foundation tranche",
        "limitations": [
            "Every design conclusion is conditional on requirements, loads, environment, model validity, material and manufacturing variation, and lifecycle state.",
            "Simulation and analysis complement but do not silently replace required physical, integration, human, operational, or certification evidence.",
            "Codes, standards, platforms, and specialist engineering methods remain versioned and open to continued expansion.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "engineering-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def context_for_prefix(prefix: str) -> tuple[str, list[str], str]:
    for group_prefix, domain, profiles, sources, _label, _statement in GROUPS:
        if group_prefix == prefix:
            return domain, sources, profiles[0][0]
    raise ValueError(f"unknown engineering prefix {prefix}")


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    global_index = 0
    for prefix, domain, profiles, sources, domain_label, domain_statement in GROUPS:
        records.append(
            {
                **make_base(f"{prefix}.root", domain, profiles[0][0], sources, "train", "concept"),
                "label": domain_label,
                "statement": domain_statement,
                "aliases": [domain_label.lower()],
            }
        )
        for subject, slug, label, definition, primitive_label, primitive_statement, mechanism_label, mechanism_statement, control_label, control_statement in profiles:
            for offset, (suffix, node_label, statement) in enumerate(
                [
                    ("root", label, definition),
                    ("primitive", primitive_label, primitive_statement),
                    ("mechanism", mechanism_label, mechanism_statement),
                ]
            ):
                node_id = f"{prefix}.{slug}.{suffix}"
                records.append(
                    {
                        **make_base(
                            node_id, domain, subject, sources,
                            "train" if suffix == "root" else split_for(global_index + offset), "concept",
                        ),
                        "label": node_label,
                        "statement": statement,
                        "aliases": [node_label.lower()],
                        "tags": ["foundation", domain, f"engineering-profile-{slug}"],
                    }
                )
                target = f"{prefix}.root" if suffix == "root" else f"{prefix}.{slug}.root"
                relation_id = f"engworld.membership.{prefix}.{slug}.{suffix}"
                records.append(
                    {
                        **make_base(relation_id, domain, subject, sources, split_for(global_index + offset + 5), "relation"),
                        "label": f"{node_label} engineering-world membership",
                        "statement": f"{node_label} is a distinct component of {label} with explicit requirements, evidence, and failure conditions.",
                        "aliases": [],
                        "relation": {
                            "source_node": node_id,
                            "target_node": target,
                            "kind": "part_of",
                            "polarity": 1,
                            "direction": "forward",
                            "conditions": ["the declared system boundary, operating condition, and lifecycle stage apply"],
                            "exceptions": [],
                        },
                        "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                    }
                )
            control_id = f"engworld.control.{prefix}.{slug}"
            records.append(
                {
                    **make_base(
                        control_id, domain, subject, [],
                        ["train", "validation", "sealed_test", "cross_domain_holdout"][global_index % 4],
                        "synthetic_control", "synthetic_control",
                    ),
                    "label": control_label,
                    "statement": control_statement,
                    "aliases": [control_label.lower()],
                    "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                    "synthetic": True,
                    "tags": ["negative-control", domain, f"engineering-profile-{slug}"],
                }
            )
            global_index += 1

    all_sources = sorted({source for _prefix, _domain, _profiles, sources, _label, _statement in GROUPS for source in sources})
    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in CROSS_RELATIONS])
    for identifier, source_node, target_node, kind, statement in CROSS_RELATIONS:
        prefix = source_node.split(".", 1)[0]
        domain, sources, subject = context_for_prefix(prefix)
        cross = source_node.split(".", 1)[0] != target_node.split(".", 1)[0] or identifier.startswith("bridge-")
        records.append(
            {
                **make_base(
                    f"engworld.relation.{identifier}", domain, subject,
                    all_sources if cross else sources,
                    splitter.split(kind, cross_requested=cross), "relation",
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source_node,
                    "target_node": target_node,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["the stated requirements, interfaces, loads, environment, model, and lifecycle assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (prefix, identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        domain, sources, _root_subject = context_for_prefix(prefix)
        split = example_splits[index % 4]
        node_id = f"engworld.example.{prefix}.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, sources, split, "worked_example"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "uncertainty_competing_hypotheses"],
                "tags": ["worked-example", domain],
            }
        )
        relation_id = f"engworld.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(relation_id, domain, subject, sources, split, "relation"),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded engineering mechanism or assurance composition.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": f"{prefix}.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains bounded and configuration controlled"],
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
