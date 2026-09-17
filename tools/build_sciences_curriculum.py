#!/usr/bin/env python3
"""Author physical, quantum, chemical, biological, Earth, and space sciences."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "sciences" / "foundations.jsonl"
WORLD = "sciences-v0"
LANES = ["reasoning.causal", "reasoning.inductive", "reasoning.probabilistic", "thinking.bottom_up", "geometry.structural"]

PHYSICS_SOURCES = ["nist-codata-2022", "nist-measurement-uncertainty", "msc2020", "national-academies-reproducibility"]
QUANTUM_SOURCES = ["nist-quantum-information", "nist-codata-2022", "msc2020", "sep-probability"]
CHEMISTRY_SOURCES = ["iupac-goldbook-500", "nist-chemistry-webbook", "mesh2026", "nist-measurement-uncertainty"]
BIOLOGY_SOURCES = ["mesh2026", "nhgri-genomics-facts", "ncbi-molecular-cell", "national-academies-reproducibility"]
EARTH_SOURCES = ["usgs-earth-water-science", "noaa-climate-ocean", "nasa-science", "national-academies-reproducibility"]
ASTRONOMY_SOURCES = ["nasa-science", "nasa-astrophysics", "nist-codata-2022", "national-academies-reproducibility"]


# subject, slug, label, definition, primitive label, primitive statement,
# mechanism label, mechanism statement, negative-control label and statement.
PHYSICS = [
    ("physics.classical-mechanics", "mechanics", "Classical mechanics", "Classical mechanics models motion and interaction through configuration, time, mass, momentum, force, energy, and constraints within nonrelativistic and nonquantum regimes.", "Mechanical state", "A mechanical state supplies positions and momenta or equivalent generalized coordinates at a declared time.", "Equation of motion", "An equation of motion maps forces or an action principle and initial conditions to allowed trajectories.", "Universal classical mechanics", "Classical equations must not be applied without checking relativistic, quantum, continuum, and scale assumptions."),
    ("physics.electromagnetism", "electromagnetism", "Electromagnetism", "Electromagnetism relates charge, current, electric and magnetic fields, potentials, forces, energy, radiation, and material response through Maxwell and constitutive equations.", "Electromagnetic field", "Electric and magnetic fields assign force and energy structure over spacetime under a chosen frame and unit system.", "Maxwell evolution", "Sources and changing fields jointly constrain divergence, curl, wave propagation, and boundary behavior.", "Field line is trajectory", "A drawn field line must not be treated as the path of a charged particle without solving its dynamics."),
    ("physics.thermodynamics", "thermodynamics", "Thermodynamics", "Thermodynamics relates macroscopic state variables, heat, work, energy, entropy, equilibrium, and irreversible limits without requiring microscopic detail.", "Thermodynamic state", "A thermodynamic state is specified by sufficient macroscopic variables for the equilibrium or nonequilibrium model in use.", "Energy and entropy balance", "The first law constrains energy change while the second law constrains entropy production and direction of spontaneous processes.", "Heat as substance", "Heat must not be treated as material stored in a body rather than energy transfer caused by a temperature-related process."),
    ("physics.statistical-mechanics", "statistical-mechanics", "Statistical mechanics", "Statistical mechanics connects probability distributions over microstates to macroscopic observables and thermodynamic behavior.", "Microstate ensemble", "An ensemble assigns probabilities to microscopic states under constraints such as energy, particle number, and temperature.", "Macroscopic averaging", "Expectation and concentration over many degrees of freedom produce thermodynamic quantities under ergodic and limit assumptions.", "Most probable equals certain", "A dominant macrostate must not be treated as excluding fluctuations or finite-size deviations."),
    ("physics.relativity", "relativity", "Relativity", "Special relativity uses invariant spacetime intervals and Lorentz symmetry, while general relativity models gravitation through curved spacetime and stress-energy.", "Spacetime event", "A spacetime event is a location in a four-dimensional manifold whose coordinates depend on the observer frame.", "Geometric gravitation", "Stress-energy and spacetime curvature are related by field equations, and free test bodies follow geometric trajectories.", "Coordinate effect is physical singularity", "A coordinate divergence must not be called a physical singularity without invariant analysis."),
    ("physics.optics", "optics", "Optics and photonics", "Optics studies propagation, reflection, refraction, interference, diffraction, polarization, detection, and light-matter interaction across ray, wave, and quantum models.", "Optical field", "An optical field carries amplitude, phase, polarization, frequency, and spatial mode information.", "Interference and diffraction", "Superposed complex field amplitudes produce intensity patterns through relative phase and aperture propagation.", "Ray model is universal", "Geometric rays must not replace wave or quantum optics when wavelength, coherence, or photon statistics matter."),
    ("physics.acoustics", "acoustics", "Acoustics", "Acoustics studies mechanical waves, sources, propagation, impedance, resonance, radiation, and perception in gases, liquids, solids, and structures.", "Acoustic pressure field", "An acoustic field describes pressure, particle velocity, displacement, or stress variations around an equilibrium medium.", "Wave propagation", "Material inertia and restoring forces propagate acoustic disturbances with dispersion, attenuation, reflection, and mode structure.", "Sound speed is constant everywhere", "A sound speed must not be transferred across media, temperature, pressure, frequency, or mode without checking the constitutive model."),
    ("physics.fluid-dynamics", "fluid-dynamics", "Fluid dynamics", "Fluid dynamics models mass, momentum, energy, vorticity, viscosity, pressure, and transport in deformable continua.", "Fluid field", "Velocity, density, pressure, temperature, and composition fields describe a continuum state under a scale-separation assumption.", "Conservation transport", "Continuity and momentum balances transport conserved quantities while constitutive laws close stress and flux relations.", "Incompressible means constant pressure", "Incompressibility constrains density or divergence and must not be confused with spatially constant pressure."),
    ("physics.plasma", "plasma", "Plasma physics", "Plasma physics studies ionized many-particle systems with collective electromagnetic behavior, screening, waves, instabilities, collisions, and kinetic effects.", "Plasma distribution", "Species distribution functions describe particle positions and velocities beyond fluid moments.", "Collective response", "Self-consistent fields couple charged-particle motion into screening, waves, confinement, and instability.", "Ionized gas is always ideal", "A plasma must not be reduced to a neutral ideal gas when collective fields, magnetization, or nonthermal distributions matter."),
    ("physics.condensed-matter", "condensed-matter", "Condensed-matter physics", "Condensed-matter physics studies collective phases and excitations of interacting particles in solids, liquids, soft matter, and engineered materials.", "Many-body state", "A many-body state encodes correlated degrees of freedom under lattice, continuum, symmetry, and boundary conditions.", "Emergent phase", "Interactions and symmetry can produce collective order, quasiparticles, transport, and phase transitions not evident from isolated constituents.", "Material property from one atom", "A bulk material property must not be inferred from one constituent atom without many-body structure and conditions."),
    ("physics.atomic-molecular", "atomic-molecular", "Atomic and molecular physics", "Atomic and molecular physics studies bound electronic and nuclear states, spectra, collisions, fields, molecular structure, and dynamical transitions.", "Energy level", "An energy level is an eigenvalue or resonance of a modeled atomic or molecular Hamiltonian with quantum numbers and uncertainty.", "Spectral transition", "Light-matter coupling and selection rules cause transitions with frequencies, strengths, and linewidths tied to state differences.", "Spectral line uniquely identifies cause", "A line position alone must not establish species, state, or mechanism without resolution, intensity, interference, and calibration evidence."),
    ("physics.nuclear", "nuclear", "Nuclear physics", "Nuclear physics studies nuclei, nuclear forces, structure, decays, reactions, fission, fusion, and radiation interactions.", "Nuclide state", "A nuclide is specified by proton and neutron numbers plus excitation and angular-momentum state where relevant.", "Nuclear transformation", "Decay or reaction changes nuclear composition or state while conserving charge, energy-momentum, angular momentum, and other applicable quantum numbers.", "Half-life predicts one nucleus", "A half-life must not be used to predict the exact decay time of an individual unstable nucleus."),
    ("physics.particle", "particle", "Particle physics", "Particle physics studies elementary fields and particles, symmetries, interactions, scattering, decays, and experimental signatures.", "Quantum field excitation", "A particle is modeled as a quantized field excitation with mass, spin, charges, and interaction representations.", "Scattering amplitude", "An interaction model produces amplitudes whose squared combinations and phase space predict event distributions.", "Detector event is direct particle picture", "A detector signature must not be treated as direct visual proof of one particle process without reconstruction and competing backgrounds."),
    ("physics.complex-systems", "complex-systems", "Nonlinear dynamics and complex systems", "Complex-systems physics studies nonlinear evolution, feedback, bifurcation, chaos, networks, pattern formation, criticality, and collective behavior.", "Dynamical state space", "A state space represents possible system states and trajectories under deterministic or stochastic evolution.", "Nonlinear feedback", "Feedback and coupling can amplify perturbations, create multiple attractors, synchronize components, or generate emergent patterns.", "Chaos means randomness", "Deterministic chaos must not be equated with stochastic randomness or absence of governing equations."),
    ("physics.measurement", "measurement", "Physical measurement", "Measurement assigns a value and uncertainty to a measurand through a calibrated system, model, unit, traceability chain, and stated conditions.", "Measurand", "A measurand is the quantity intended to be measured, defined with enough conditions to identify what the result means.", "Measurement model", "A measurement model maps indications, calibration quantities, corrections, and influence factors into a result and uncertainty.", "Precision means accuracy", "Small repeated spread must not be treated as closeness to the true value without bias and traceability analysis."),
]


QUANTUM = [
    ("quantum-science.foundations", "foundations", "Quantum foundations", "Quantum theory assigns states, observables, transformations, and probabilities through a mathematical framework whose empirical predictions are distinct from philosophical interpretation.", "Quantum amplitude", "A complex amplitude contributes phase-sensitive probability structure and is not itself an ordinary classical probability.", "Born probability", "A measurement model converts state amplitudes into outcome probabilities through positive operators or projective special cases.", "Quantum means anything uncertain", "Ordinary uncertainty must not be called quantum without a quantum state, observable algebra, and empirical regime."),
    ("quantum-science.state-spaces", "state-spaces", "Quantum states and observables", "Quantum states are rays or density operators on a Hilbert space, while observables are represented by self-adjoint operators or generalized measurements.", "Hilbert-space state", "A normalized state vector represents a pure state up to global phase, while a density operator represents pure or mixed state statistics.", "Observable expectation", "The trace or inner-product rule maps state and observable to expected measurement values.", "State vector is physical wave in every interpretation", "A mathematical state vector must not be assigned one ontological interpretation as an experimentally settled fact."),
    ("quantum-science.dynamics", "dynamics", "Quantum dynamics", "Closed quantum dynamics is unitary and generated by a Hamiltonian, while controlled, relativistic, and open regimes use corresponding extensions.", "Hamiltonian", "A Hamiltonian represents energy and generates time evolution for a closed system under the Schrödinger equation.", "Unitary evolution", "A unitary map preserves inner products and total probability while evolving superpositions coherently.", "Energy eigenstate never changes", "An energy eigenstate's global phase evolution must not be confused with every observable or coupled-system state remaining unchanged."),
    ("quantum-science.measurement", "measurement", "Quantum measurement", "Quantum measurement couples a system to an apparatus and assigns outcome probabilities and conditional post-measurement states under a specified instrument.", "Measurement operator", "A measurement instrument associates outcomes with positive effects and state-update maps satisfying normalization.", "State update", "Conditioning on an observed outcome transforms the predicted state for subsequent measurements.", "Measurement reveals preexisting value universally", "A measurement outcome must not always be treated as revealing a context-independent preexisting classical value."),
    ("quantum-science.entanglement", "entanglement", "Quantum entanglement", "Entanglement is nonseparability of a composite quantum state relative to a subsystem tensor-product structure.", "Composite state", "A composite system uses a tensor-product state space with reduced states obtained by partial trace.", "Bell correlation", "Entangled states and incompatible measurements can produce correlations that violate Bell inequalities under experimental assumptions.", "Entanglement sends controllable faster-than-light messages", "Nonclassical correlation must not be described as controllable superluminal communication."),
    ("quantum-science.field-theory", "field-theory", "Quantum field theory", "Quantum field theory combines quantum principles, fields, locality, symmetries, particles, and relativistic dynamics with regularization and renormalization.", "Quantum field", "A quantum field is an operator-valued distribution or algebraic object whose excitations and correlations represent particles and interactions.", "Renormalized prediction", "Scale-dependent parameters and controlled subtraction or effective descriptions produce finite observable predictions within a theory's domain.", "Virtual particle is directly observed object", "Internal perturbative terms must not be described as directly detected particles or unique physical trajectories."),
    ("quantum-science.information", "information", "Quantum information", "Quantum information studies encoding, transformation, communication, entropy, measurement, and resource limits of quantum states and channels.", "Qubit", "A qubit is a two-dimensional quantum system whose pure state includes coherent superpositions relative to a chosen basis.", "Quantum channel", "A quantum channel is a completely positive trace-preserving map representing physically allowed state evolution without postselection.", "Qubit stores both classical values for free", "A superposition must not be described as two readable classical bit values obtainable from one measurement."),
    ("quantum-science.computation", "computation", "Quantum computation", "Quantum computation applies state preparation, gates, measurements, error control, and classical coordination to solve selected problems under hardware and complexity constraints.", "Quantum circuit", "A quantum circuit is an ordered composition of unitary gates, measurements, resets, and classical controls on named qubits.", "Interference algorithm", "An algorithm arranges amplitude interference so desired outcomes gain probability while unwanted paths cancel.", "Quantum computer accelerates every problem", "Quantum computation must not be described as a universal exponential speedup over classical algorithms."),
    ("quantum-science.open-systems", "open-systems", "Open quantum systems", "Open-system theory describes a subsystem interacting with an environment through reduced states, decoherence, dissipation, noise, and memory effects.", "Reduced density state", "Tracing out an environment produces a mixed subsystem state that retains only locally accessible statistics.", "Decoherence", "System-environment entanglement suppresses selected phase coherence in a basis determined by the interaction and dynamics.", "Decoherence alone selects one interpretation", "Environmental decoherence must not be presented as experimentally proving one solution to every quantum measurement interpretation."),
    ("quantum-science.interpretations", "interpretations", "Quantum interpretations", "Interpretations propose accounts of the formalism's ontology, probability, measurement, and classical experience while agreeing on tested predictions where empirically equivalent.", "Interpretive postulate", "An interpretive postulate connects mathematical objects to claims about reality beyond the shared predictive core.", "Empirical equivalence", "Interpretations with identical operational predictions require nonempirical criteria or new discriminating proposals for comparison.", "Interpretation is experimental law", "A favored interpretation must not be stored as settled empirical fact when alternatives share the tested predictions."),
]


CHEMISTRY = [
    ("chemistry.general", "general", "General chemistry", "General chemistry relates matter, composition, amount, structure, bonding, energy, equilibrium, reactions, and measurement using atomic and molecular models.", "Chemical amount", "Amount of substance counts specified entities in moles and must identify the entity and composition.", "Stoichiometric transformation", "Balanced reaction equations constrain relative amounts through conservation of atoms and charge.", "Balanced equation proves reaction occurs", "Stoichiometric balance must not be treated as evidence that a reaction is favorable, fast, selective, or safe."),
    ("chemistry.physical", "physical", "Physical chemistry", "Physical chemistry applies thermodynamics, kinetics, quantum mechanics, statistical mechanics, and spectroscopy to molecular systems and phases.", "Chemical potential", "Chemical potential measures free-energy change with composition and governs equilibrium transfer and reaction under stated constraints.", "Free-energy competition", "Enthalpy, entropy, composition, and external conditions determine equilibrium tendency through an appropriate thermodynamic potential.", "Negative free energy means instantaneous", "Thermodynamic favorability must not be treated as a fast reaction without kinetic evidence."),
    ("chemistry.organic", "organic", "Organic chemistry", "Organic chemistry studies carbon-based molecular structure, functional groups, stereochemistry, reactivity, synthesis, and mechanisms.", "Functional group", "A functional group is a recurring bonded atom pattern that shapes electronic structure and reactivity within molecular context.", "Electron-flow mechanism", "Bond-making and bond-breaking pathways are modeled through electron redistribution, intermediates, transition states, solvent, and conditions.", "One functional group fixes behavior", "A functional-group label must not determine whole-molecule reactivity without steric, electronic, conformational, and condition context."),
    ("chemistry.inorganic", "inorganic", "Inorganic chemistry", "Inorganic chemistry studies elements, coordination compounds, solids, organometallics, acid-base behavior, redox, and structure across the periodic table.", "Coordination environment", "A coordination environment specifies a central atom or ion, ligands, geometry, oxidation state, electron count, and bonding model.", "Ligand-field splitting", "The geometry and ligand interaction split metal electronic levels and influence spectra, magnetism, and reactivity.", "Oxidation state is localized charge", "A formal oxidation state must not be treated as the measured charge residing on one atom."),
    ("chemistry.analytical", "analytical", "Analytical chemistry", "Analytical chemistry identifies and quantifies chemical components through sampling, separation, calibration, detection, uncertainty, selectivity, and validation.", "Analyte", "An analyte is the specified chemical component or property intended to be measured in a defined matrix.", "Calibration model", "Standards and instrument responses produce a calibration relation used to infer analyte amount with blanks, matrix effects, range, and uncertainty.", "Instrument reading equals concentration", "A raw signal must not be reported as concentration without identity, calibration, blank, matrix, range, and uncertainty."),
    ("chemistry.biochemistry", "biochemistry", "Biochemistry", "Biochemistry studies molecular structures, reactions, energetics, catalysis, information, and regulation in living systems.", "Enzyme active system", "An enzyme's activity depends on sequence, folded structure, cofactors, substrates, products, pH, temperature, and regulatory context.", "Biochemical catalysis", "Enzymes lower activation barriers and reshape rates without changing the equilibrium free-energy difference.", "Enzyme makes impossible reaction favorable", "Catalysis must not be described as changing thermodynamic equilibrium or creating energy."),
    ("chemistry.electrochemistry", "electrochemistry", "Electrochemistry", "Electrochemistry relates redox reactions, charge transport, electrode potentials, interfaces, current, mass transfer, and energy conversion.", "Electrochemical cell", "A cell couples oxidation and reduction half-reactions through electronic and ionic paths under defined activities and interfaces.", "Electrode potential", "Chemical activities and redox thermodynamics determine equilibrium potential, while current adds kinetic and transport overpotentials.", "Cell voltage alone gives capacity", "Open-circuit voltage must not be used as battery capacity, power, rate capability, or state-of-health without additional evidence."),
    ("chemistry.polymer", "polymer", "Polymer chemistry", "Polymer chemistry studies macromolecule synthesis, molecular-weight distributions, architecture, conformation, phase behavior, mechanics, transport, and degradation.", "Polymer chain distribution", "A polymer sample contains a distribution of chain lengths, compositions, branches, and end groups rather than one molecular mass.", "Polymerization", "Initiation, propagation, transfer, termination, monomer conversion, and transport shape polymer architecture and distribution.", "Polymer has one molecular weight", "A polymer sample must not be described by one exact molecular weight without naming the averaging definition and dispersity."),
    ("chemistry.computational", "computational", "Computational chemistry", "Computational chemistry approximates molecular electronic structure, dynamics, thermodynamics, spectra, and reactions under explicit Hamiltonian, basis, parameter, and sampling choices.", "Molecular model", "A molecular model specifies particles or fields, energy function, electronic treatment, boundary conditions, and numerical representation.", "Energy-surface sampling", "Optimization or dynamics explores a modeled potential or free-energy surface, with barriers and sampling controlling observed states.", "Computed minimum proves real structure", "A local minimum in one approximate model must not be treated as the unique experimental structure or dominant state."),
    ("chemistry.reaction-mechanisms", "reaction-mechanisms", "Reaction mechanisms and kinetics", "Chemical kinetics studies reaction rates and mechanisms through elementary steps, rate laws, activation barriers, transport, and temperature dependence.", "Elementary step", "An elementary step is one modeled molecular event whose molecularity and rate law follow that mechanism rather than the net equation.", "Rate-limiting network", "Observed kinetics emerge from coupled elementary steps, intermediates, steady states, equilibria, and competing pathways.", "Stoichiometric coefficient is rate order", "Net reaction coefficients must not be copied into an empirical rate law unless an elementary mechanism justifies it."),
    ("chemistry.spectroscopy", "spectroscopy", "Chemical spectroscopy", "Spectroscopy relates matter to absorbed, emitted, scattered, or resonant radiation through quantum states, transitions, selection rules, line shapes, and instrumentation.", "Spectrum", "A spectrum records signal versus frequency, wavelength, energy, field, mass-to-charge, or another resolved variable with calibration and response.", "Transition signature", "State energy differences, transition moments, populations, environment, and instrument response shape spectral peaks.", "Peak label is unique identification", "One peak must not uniquely identify a compound without resolution, reference, matrix, abundance, and alternative assignments."),
    ("chemistry.safety", "safety", "Chemical safety", "Chemical safety evaluates identity, amount, concentration, route, exposure, reactivity, incompatibility, energy, controls, waste, and emergency response before handling.", "Chemical hazard", "A hazard is an inherent capacity to cause harm, distinct from risk under a particular exposure and control context.", "Control hierarchy", "Elimination, substitution, engineering controls, administrative controls, and protective equipment reduce exposure with differing reliability.", "Familiar chemical is harmless", "Common use, natural origin, dilute appearance, or prior uneventful handling must not establish chemical safety."),
]


BIOLOGY = [
    ("biology.cell", "cell", "Cell biology", "Cell biology studies membranes, compartments, metabolism, signaling, growth, division, death, mechanics, and interactions in the basic living unit.", "Cellular compartment", "A compartment maintains a controlled chemical and physical environment through boundaries, transport, and localized machinery.", "Cell-state transition", "Signals, gene regulation, metabolism, structure, and checkpoints drive transitions among growth, division, differentiation, stress, and death states.", "Cell is a bag of molecules", "A component list must not replace spatial organization, dynamics, regulation, and cell-state evidence."),
    ("biology.molecular", "molecular", "Molecular biology", "Molecular biology studies replication, transcription, translation, repair, regulation, and interactions among DNA, RNA, proteins, and other cellular molecules.", "Sequence information", "Nucleic-acid sequence constrains molecular recognition and products while context and regulation determine when it is used.", "Gene expression", "Transcription, RNA processing, translation, localization, modification, and degradation convert genomic regions into regulated functional products.", "One gene one fixed protein", "A gene must not be reduced to one invariant protein when isoforms, RNA products, regulation, processing, and context differ."),
    ("biology.genetics", "genetics", "Genetics", "Genetics studies inheritance, variation, recombination, gene action, genotype-phenotype relations, pedigrees, populations, and experimental crosses.", "Allele", "An allele is a sequence or structural variant at a genetic locus relative to a reference and population context.", "Inheritance segregation", "Chromosome transmission, recombination, dominance, penetrance, environment, and interaction shape inheritance and phenotype distributions.", "Variant determines trait", "A genetic variant must not be treated as deterministically causing a complex trait without effect, penetrance, background, environment, and population evidence."),
    ("biology.genomics", "genomics", "Genomics", "Genomics studies complete genomes, variation, organization, annotation, expression, regulation, comparative structure, and population-scale associations.", "Genome assembly", "A genome assembly reconstructs sequences from reads under coverage, repeat, ploidy, error, and graph assumptions.", "Variant association", "Population genotype and phenotype data can reveal statistical associations whose causal and transfer limits require separate analysis.", "Reference genome is one normal genome", "A reference assembly must not be treated as a complete, universal, or normative human genome."),
    ("biology.evolution", "evolution", "Evolutionary biology", "Evolutionary biology explains heritable population change through mutation, recombination, selection, drift, migration, inheritance, and historical contingency.", "Population variation", "Evolution acts on heritable variation distributed across individuals and populations rather than organisms changing because they need to.", "Natural selection", "Differential survival and reproduction associated with heritable variants changes their frequencies under an environment and tradeoffs.", "Evolution has a goal", "Evolution must not be described as progressing toward predetermined perfection or satisfying an organism's needs."),
    ("biology.development", "development", "Developmental biology", "Developmental biology studies how cells and organisms change form and function through gene regulation, signaling, mechanics, patterning, growth, and environment.", "Cell fate", "Cell fate is the eventual differentiated outcome of a lineage under intrinsic state, signals, position, and history.", "Morphogenetic patterning", "Spatial signals, thresholds, gene networks, mechanics, and feedback coordinate tissue pattern and form.", "DNA alone specifies exact anatomy", "Genome sequence must not be treated as a complete geometric blueprint independent of cellular dynamics, environment, and stochasticity."),
    ("biology.microbiology", "microbiology", "Microbiology", "Microbiology studies bacteria, archaea, microbial eukaryotes, viruses, communities, metabolism, genetics, ecology, pathogenesis, and beneficial interactions.", "Microbial population", "A microbial population contains variable cells or particles whose growth, death, dormancy, mutation, and interactions depend on conditions.", "Microbial growth", "Resource uptake, metabolism, division, mortality, limitation, and environmental feedback shape population dynamics.", "All microbes are pathogens", "Microorganisms must not be equated with disease agents; most interactions are neutral, beneficial, environmental, or context-dependent."),
    ("biology.immunology", "immunology", "Immunology", "Immunology studies recognition, barriers, innate and adaptive responses, tolerance, memory, inflammation, infection, vaccination, and immune-mediated disease.", "Immune recognition", "Receptors recognize molecular patterns or specific antigens under cellular, tissue, and signaling context.", "Adaptive clonal response", "Antigen-driven activation, clonal expansion, differentiation, regulation, contraction, and memory shape an adaptive response.", "Antibody presence equals protection", "Detectable antibody must not be treated as complete protection without specificity, function, amount, timing, cellular immunity, and pathogen context."),
    ("biology.physiology", "physiology", "Physiology", "Physiology studies integrated function and regulation across cells, tissues, organs, and organisms through transport, signaling, mechanics, and homeostasis.", "Physiological variable", "A physiological variable such as pressure, concentration, temperature, or flow has a measurement site, range, dynamics, and regulatory role.", "Homeostatic feedback", "Sensors, controllers, effectors, delays, limits, and competing demands regulate variables around context-dependent operating ranges.", "Homeostasis means constant value", "Homeostasis must not be described as a perfectly fixed value rather than dynamic regulated variation."),
    ("biology.ecology", "ecology", "Ecology", "Ecology studies organisms, populations, communities, ecosystems, energy, nutrients, interactions, disturbance, spatial structure, and change across scales.", "Ecological population", "An ecological population is a set of organisms of a species or operational group occupying a defined region and time with births, deaths, immigration, and emigration.", "Food-web transfer", "Consumption and decomposition transfer matter and energy through a network with losses, stoichiometry, behavior, and environmental constraints.", "Correlation across sites proves ecological cause", "A spatial association must not be called causal without design, confounder, scale, and mechanism evidence."),
    ("biology.botany", "botany", "Botany", "Botany studies plant structure, development, physiology, reproduction, evolution, diversity, ecology, and interactions.", "Plant meristem", "A meristem contains proliferative cells whose division and differentiation generate plant organs under positional signals.", "Photosynthetic carbon fixation", "Light capture, electron transfer, proton gradients, ATP and reducing power support biochemical carbon fixation under water, nutrient, and temperature constraints.", "Plants obtain mass mainly from soil", "Plant dry biomass must not be attributed mainly to soil minerals rather than carbon dioxide fixation, water, and nutrient contributions."),
    ("biology.zoology", "zoology", "Zoology", "Zoology studies animal diversity, anatomy, physiology, development, behavior, evolution, ecology, and phylogenetic relations.", "Animal body plan", "A body plan describes axes, tissues, cavities, segmentation, appendages, and developmental organization shared or transformed across lineages.", "Behavioral adaptation", "Neural, hormonal, developmental, learned, ecological, and evolutionary factors jointly shape animal behavior.", "Behavior has one genetic cause", "An animal behavior must not be assigned one gene or one adaptive story without developmental, environmental, comparative, and experimental evidence."),
    ("biology.systems", "systems", "Systems biology", "Systems biology models interacting molecular, cellular, physiological, and ecological networks through dynamics, feedback, multiscale data, and perturbation.", "Biological network", "A biological network represents entities and typed interactions with direction, sign, context, time, and uncertainty.", "Feedback regulation", "Positive and negative feedback, feedforward, redundancy, and crosstalk shape stability, sensitivity, switching, and adaptation.", "Network diagram proves mechanism", "A correlation-derived network edge must not be treated as a causal biochemical interaction without perturbation and temporal evidence."),
    ("biology.bioinformatics", "bioinformatics", "Bioinformatics", "Bioinformatics develops algorithms, databases, statistics, and reproducible workflows for biological sequences, structures, expression, variation, and systems data.", "Biological sequence alignment", "An alignment proposes positional homology or similarity under a scoring, gap, alphabet, and evolutionary model.", "Inference pipeline", "Quality control, reference selection, alignment or assembly, statistical inference, annotation, and validation transform raw biological data into claims.", "Best database hit proves function", "A high-scoring sequence match must not uniquely establish biological function without coverage, homology, domain, context, and experimental evidence."),
]


EARTH = [
    ("earth-environment.geology", "geology", "Geology", "Geology studies Earth materials, structures, strata, tectonics, surface processes, resources, hazards, and history from field, laboratory, and geophysical evidence.", "Rock and stratum", "A rock body or stratum has composition, texture, geometry, contacts, age relations, and alteration history.", "Geologic reconstruction", "Cross-cutting relations, superposition, fossils, radiometric ages, structures, and process models constrain an ordered Earth history.", "One outcrop proves regional history", "A local exposure must not be generalized without spatial correlation, dating, structural, and alternative-history evidence."),
    ("earth-environment.geophysics", "geophysics", "Geophysics", "Geophysics uses seismic, gravity, magnetic, electrical, thermal, geodetic, and mechanical observations to infer inaccessible Earth structure and dynamics.", "Geophysical field", "A geophysical field is a spatial and temporal measurement of gravity, magnetism, displacement, waves, heat, or electrical response.", "Inverse inference", "A forward physical model maps candidate Earth structure to observations, while inversion compares nonunique models under regularization and uncertainty.", "One anomaly has one cause", "A geophysical anomaly must not be assigned a unique subsurface structure without resolution and nonuniqueness analysis."),
    ("earth-environment.geochemistry", "geochemistry", "Geochemistry", "Geochemistry studies elemental and isotopic composition, reactions, transport, reservoirs, cycles, and dating across Earth systems.", "Geochemical reservoir", "A reservoir stores specified elements or isotopes with composition, mass, fluxes, residence time, and boundary definition.", "Isotope fractionation", "Physical, chemical, and biological processes preferentially partition isotopes according to mechanism and conditions.", "Isotope ratio is direct age", "An isotope ratio must not be converted to age without a decay system, initial conditions, closure, calibration, and uncertainty."),
    ("earth-environment.climate", "climate", "Climate science", "Climate science studies long-term distributions of atmosphere, ocean, ice, land, biosphere, and radiation through observations, paleorecords, theory, and models.", "Climate state", "A climate state is a statistical distribution of coupled Earth-system variables over a defined region, period, and forcing context.", "Radiative-energy imbalance", "Changes in incoming, reflected, and outgoing energy drive heat accumulation and coupled feedback responses.", "Weather event alone proves climate trend", "A single weather event must not establish or refute a climate trend without attribution and distribution evidence."),
    ("earth-environment.meteorology", "meteorology", "Meteorology", "Meteorology studies atmospheric state, dynamics, thermodynamics, moisture, clouds, radiation, weather systems, observation, and prediction.", "Atmospheric parcel", "A parcel model tracks temperature, pressure, moisture, buoyancy, and phase change for a small air mass under stated mixing assumptions.", "Weather evolution", "Pressure gradients, rotation, buoyancy, moisture, radiation, friction, and boundary forcing evolve atmospheric flows.", "Forecast is deterministic certainty", "A weather forecast must not be presented without initialization, model, ensemble, horizon, resolution, and uncertainty."),
    ("earth-environment.oceanography", "oceanography", "Oceanography", "Oceanography studies seawater properties, circulation, waves, tides, mixing, biogeochemistry, ecosystems, seafloor, and atmosphere-ocean coupling.", "Water mass", "A water mass is characterized by temperature, salinity, density, tracers, origin, and mixing history.", "Ocean circulation", "Wind stress, buoyancy flux, rotation, pressure gradients, tides, topography, and mixing drive ocean circulation across scales.", "Ocean is a passive heat bucket", "The ocean must not be treated as spatially uniform or passive when circulation, stratification, biology, and feedback redistribute heat and carbon."),
    ("earth-environment.hydrology", "hydrology", "Hydrology", "Hydrology studies water storage, precipitation, infiltration, runoff, evapotranspiration, groundwater, rivers, transport, quality, and human use.", "Watershed", "A watershed is a topographically and subsurface-defined region contributing flow to an outlet under scale and routing assumptions.", "Water balance", "Changes in storage equal inputs minus outputs over a defined region and interval, with measurement and unobserved flux uncertainty.", "Groundwater is underground river", "Aquifer flow must not be reduced to open-channel flow without porous-medium properties, gradients, recharge, and boundaries."),
    ("earth-environment.soil", "soil", "Soil science", "Soil science studies mineral and organic horizons, structure, water, air, chemistry, organisms, formation, fertility, erosion, and land use.", "Soil profile", "A soil profile records horizons with texture, structure, organic matter, chemistry, roots, moisture, and parent-material relations.", "Pedogenesis", "Climate, organisms, relief, parent material, time, transport, and human activity transform soil horizons.", "Soil type follows color alone", "Soil color must not determine classification, fertility, drainage, or contamination without profile and laboratory evidence."),
    ("earth-environment.ecosystems", "ecosystems", "Ecosystem science", "Ecosystem science studies organisms, physical environment, energy, nutrients, disturbance, succession, feedback, services, and resilience across scales.", "Ecosystem boundary", "An ecosystem boundary declares spatial extent, organisms, abiotic compartments, fluxes, period, and included human processes.", "Nutrient cycling", "Biological uptake, transformation, decomposition, transport, storage, and loss cycle elements among ecosystem compartments.", "Stable appearance means equilibrium", "An ecosystem's persistent appearance must not be treated as static equilibrium without flux, disturbance, turnover, and trend evidence."),
    ("earth-environment.environmental-modeling", "environmental-modeling", "Environmental modeling", "Environmental modeling represents coupled physical, chemical, biological, and human processes to explain, predict, compare interventions, and quantify uncertainty.", "Model state and forcing", "State variables evolve from initial conditions under boundary forcing, parameters, process equations, and numerical discretization.", "Scenario simulation", "A scenario conditions a model on assumed drivers and interventions to explore consequences rather than predict unconditional reality.", "Scenario is observation", "A simulated scenario must not be stored or cited as an observed event or certain forecast."),
    ("earth-environment.sustainability", "sustainability", "Sustainability science", "Sustainability science studies coupled human-natural systems, needs, limits, justice, resilience, technology, governance, and tradeoffs across generations and regions.", "Sustainability indicator", "An indicator measures one declared environmental, social, economic, or institutional dimension with scope, baseline, and distribution.", "Systems intervention", "An intervention changes technologies, incentives, behavior, infrastructure, institutions, or ecosystems and can create rebound, leakage, and unequal effects.", "One metric proves sustainable", "Improvement in one indicator must not establish overall sustainability while other impacts, populations, scales, and time horizons remain unmeasured."),
]


ASTRONOMY = [
    ("astronomy-space.observational", "observational", "Observational astronomy", "Observational astronomy infers celestial properties from photons, particles, gravitational waves, timing, astrometry, and calibrated instruments under selection and foreground effects.", "Astronomical observation", "An observation records signal, coordinates, time, band, instrument state, calibration, exposure, uncertainty, and data-reduction provenance.", "Forward observation model", "A physical source model, propagation, foregrounds, instrument response, sampling, and noise produce the measured data distribution.", "Image is direct visual reality", "A processed astronomical image must not be treated as an unaided-color photograph or complete object state without band and processing metadata."),
    ("astronomy-space.astrophysics", "astrophysics", "Astrophysics", "Astrophysics applies gravitation, radiation, fluid, plasma, nuclear, particle, and statistical physics to stars, compact objects, galaxies, and interstellar matter.", "Astrophysical source", "A source is characterized by distance, geometry, composition, mass, temperature, fields, motion, luminosity, and evolutionary state inferred from multiple observations.", "Radiative transfer", "Emission, absorption, scattering, geometry, velocity, and optical depth transform intrinsic source radiation into an observed spectrum and image.", "Brightness means nearby or powerful uniquely", "Observed flux must not uniquely determine luminosity or distance without independent constraints and extinction."),
    ("astronomy-space.cosmology", "cosmology", "Cosmology", "Cosmology studies spacetime expansion, contents, origin, structure formation, background radiation, and cosmic history through relativistic models and observations.", "Cosmological model", "A cosmological model declares spacetime symmetry, matter-energy components, dynamics, initial conditions, and observable mappings.", "Expansion history", "The scale factor, energy components, curvature, and gravity model determine distance-redshift and structure-growth relations.", "Big Bang is explosion into space", "Cosmic expansion must not be described as matter exploding from one central point into preexisting space."),
    ("astronomy-space.planetary", "planetary", "Planetary science", "Planetary science studies formation, interiors, surfaces, atmospheres, magnetospheres, rings, small bodies, and evolution through missions, remote sensing, samples, and models.", "Planetary body", "A planetary body has bulk composition, internal differentiation, orbit, rotation, surface, atmosphere, thermal history, and environment.", "Planetary differentiation", "Gravity, heating, melting, chemistry, and transport separate materials by density and affinity during body evolution.", "Surface appearance gives age directly", "A planetary surface feature must not receive an absolute age without crater chronology, stratigraphy, samples, or calibrated models."),
    ("astronomy-space.celestial-mechanics", "celestial-mechanics", "Celestial mechanics", "Celestial mechanics models gravitational orbits, rotations, perturbations, resonances, tides, stability, and trajectory design.", "Orbital state", "An orbital state gives position and velocity at an epoch in a frame with masses and force model.", "Gravitational propagation", "Equations of motion propagate an orbit while nonspherical gravity, third bodies, radiation, drag, and maneuvers perturb ideal two-body motion.", "Orbit is permanent ellipse", "An osculating ellipse must not be treated as an unchanging physical track under perturbations and frame changes."),
    ("astronomy-space.exoplanets", "exoplanets", "Exoplanet science", "Exoplanet science detects and characterizes planets around other stars through transits, radial velocities, imaging, timing, microlensing, spectra, and population inference.", "Transit signal", "A transit is a periodic or single flux decrease whose depth, shape, duration, color, and timing depend on planet, star, orbit, and contamination.", "Joint planet inference", "Combining transit, radial velocity, stellar, imaging, and dynamical evidence constrains radius, mass, density, orbit, and atmosphere.", "Transit dip proves planet", "A brightness dip must not be called a planet without excluding eclipsing binaries, activity, instrumental systematics, and blends."),
    ("astronomy-space.astrobiology", "astrobiology", "Astrobiology", "Astrobiology studies life's origins, limits, signatures, environments, planetary habitability, and search strategies using biology, chemistry, geology, and astronomy.", "Biosignature", "A biosignature is a substance, pattern, or process whose biological explanation must be compared with abiotic production, survival, transport, and detection.", "Habitability assessment", "Energy, solvents, elements, stability, gradients, environment, history, and detectability constrain whether conditions could support a specified form of life.", "Habitable means inhabited", "A potentially habitable environment must not be reported as containing life without independent biosignature evidence."),
    ("astronomy-space.space-systems", "space-systems", "Space systems and missions", "Space systems engineering coordinates science objectives, payload, spacecraft, launch, orbit, communications, navigation, operations, environment, reliability, and data products.", "Mission architecture", "A mission architecture allocates objectives and constraints across orbit, spacecraft, instruments, ground systems, operations, and data processing.", "Observation chain", "Target geometry, commanding, instrument exposure, onboard processing, downlink, calibration, archive, and analysis produce a scientific data product.", "Mission launch proves science success", "A successful launch must not be treated as proof of commissioning, calibrated observations, complete downlink, or scientific conclusions."),
]


CROSS_RELATIONS = [
    ("phy-force-motion", "phy.mechanics.primitive", "phy.mechanics.mechanism", "causes", "Mechanical state and interaction laws determine acceleration and trajectory under initial conditions."),
    ("phy-em-optics", "phy.electromagnetism.mechanism", "phy.optics.primitive", "supports", "Maxwell field evolution supports wave-optics propagation and polarization."),
    ("phy-thermo-stat", "phy.statistical-mechanics.mechanism", "phy.thermodynamics.primitive", "grounds", "Microscopic ensemble averages ground thermodynamic state quantities under limit and equilibrium assumptions."),
    ("phy-rel-gravity", "phy.relativity.mechanism", "astro.celestial-mechanics.mechanism", "qualifies", "Relativistic gravity qualifies celestial motion where Newtonian approximations are insufficient."),
    ("phy-optics-atomic", "phy.atomic-molecular.mechanism", "phy.optics.primitive", "causes", "Atomic and molecular transitions cause frequency-selective optical emission and absorption."),
    ("phy-acoustic-fluid", "phy.fluid-dynamics.mechanism", "phy.acoustics.mechanism", "supports", "Linearized fluid conservation supports acoustic-wave equations in fluids."),
    ("phy-plasma-em", "phy.electromagnetism.primitive", "phy.plasma.mechanism", "causes", "Self-consistent electromagnetic fields cause collective plasma response."),
    ("phy-condensed-chem", "phy.condensed-matter.mechanism", "chem.physical.primitive", "supports", "Many-body phases support material thermodynamic and chemical-potential behavior."),
    ("phy-nuclear-particle", "phy.particle.primitive", "phy.nuclear.mechanism", "qualifies", "Particle interactions and symmetries qualify nuclear transformations."),
    ("phy-measure-all", "phy.measurement.mechanism", "phy.root", "supports", "Calibrated measurement supports empirical tests across physics."),
    ("qua-state-dynamics", "qua.state-spaces.primitive", "qua.dynamics.mechanism", "prerequisite", "A state space and Hamiltonian are prerequisites to specified unitary dynamics."),
    ("qua-dynamics-measure", "qua.dynamics.mechanism", "qua.measurement.mechanism", "qualifies", "Pre-measurement dynamics qualifies outcome probabilities and conditional state updates."),
    ("qua-composite-entangle", "qua.entanglement.primitive", "qua.entanglement.mechanism", "supports", "Tensor-product composite states support Bell-correlation predictions."),
    ("qua-field-particle", "qua.field-theory.primitive", "phy.particle.primitive", "grounds", "Quantum fields ground the field-excitation model of particles."),
    ("qua-info-channel", "qua.information.primitive", "qua.information.mechanism", "part_of", "Qubit states form inputs to quantum channels."),
    ("qua-circuit-compute", "qua.computation.primitive", "qua.computation.mechanism", "implements", "Quantum circuits implement amplitude interference algorithms."),
    ("qua-open-measure", "qua.open-systems.mechanism", "qua.measurement.primitive", "qualifies", "Decoherence and environmental coupling qualify realistic measurement models."),
    ("qua-interpret-found", "qua.interpretations.primitive", "qua.foundations.root", "qualifies", "Interpretive postulates qualify ontological readings without changing shared empirical predictions."),
    ("qua-atomic-level", "qua.state-spaces.mechanism", "phy.atomic-molecular.primitive", "grounds", "Quantum observables ground atomic and molecular energy levels."),
    ("qua-chem-model", "qua.dynamics.primitive", "chem.computational.primitive", "supports", "Quantum Hamiltonians support electronic-structure models in computational chemistry."),
    ("chem-stoich-mechanism", "chem.general.mechanism", "chem.reaction-mechanisms.primitive", "qualifies", "Stoichiometry constrains net amounts while elementary steps qualify kinetics."),
    ("chem-physical-rate", "chem.physical.mechanism", "chem.reaction-mechanisms.mechanism", "qualifies", "Free-energy surfaces and temperature qualify reaction pathways and rates."),
    ("chem-organic-spectra", "chem.organic.primitive", "chem.spectroscopy.mechanism", "qualifies", "Molecular functional groups and environments qualify spectral transitions."),
    ("chem-inorganic-electro", "chem.inorganic.primitive", "chem.electrochemistry.mechanism", "qualifies", "Oxidation states and coordination environments qualify electrochemical potentials and kinetics."),
    ("chem-analytical-spectra", "chem.spectroscopy.primitive", "chem.analytical.mechanism", "supports", "Calibrated spectra support analyte identification and quantification."),
    ("chem-biochem-enzyme", "chem.biochemistry.primitive", "chem.biochemistry.mechanism", "causes", "Enzyme structure and environment cause bounded catalytic rate changes."),
    ("chem-polymer-condensed", "chem.polymer.primitive", "phy.condensed-matter.mechanism", "qualifies", "Polymer architecture qualifies collective phase and mechanical behavior."),
    ("chem-compute-experiment", "chem.computational.mechanism", "chem.analytical.primitive", "supports", "Computed spectra and energies support experimental assignment only with calibrated comparison."),
    ("chem-safety-control", "chem.safety.mechanism", "chem.root", "inhibits", "A hierarchy of controls inhibits exposure and reaction risk across chemistry work."),
    ("bio-cell-molecular", "bio.molecular.mechanism", "bio.cell.mechanism", "causes", "Regulated molecular expression contributes to cell-state transitions."),
    ("bio-gene-genome", "bio.genetics.primitive", "bio.genomics.primitive", "part_of", "Allelic variation forms one component of genome-scale variation."),
    ("bio-genome-evolution", "bio.genomics.mechanism", "bio.evolution.primitive", "supports", "Population genomic variation supports inference about evolutionary history and selection."),
    ("bio-evolution-development", "bio.evolution.mechanism", "bio.development.mechanism", "qualifies", "Evolutionary history qualifies conserved and changed developmental mechanisms."),
    ("bio-micro-immune", "bio.microbiology.mechanism", "bio.immunology.mechanism", "causes", "Microbial molecules and replication can cause innate and adaptive immune responses."),
    ("bio-cell-physiology", "bio.cell.mechanism", "bio.physiology.mechanism", "part_of", "Cell-state and transport mechanisms compose organism physiology."),
    ("bio-ecology-evolution", "bio.ecology.mechanism", "bio.evolution.mechanism", "qualifies", "Ecological interactions qualify differential survival and reproduction."),
    ("bio-botany-ecology", "bio.botany.mechanism", "bio.ecology.mechanism", "supports", "Plant carbon fixation and nutrient use support ecosystem energy and material flows."),
    ("bio-zoology-physiology", "bio.zoology.primitive", "bio.physiology.primitive", "qualifies", "Animal body plans qualify physiological transport and control architectures."),
    ("bio-systems-network", "bio.systems.primitive", "bio.cell.mechanism", "supports", "Typed biological networks support multiscale models of cell-state transitions."),
    ("bio-info-genomics", "bio.bioinformatics.mechanism", "bio.genomics.mechanism", "supports", "Reproducible bioinformatics pipelines support genomic association and annotation."),
    ("bio-chem-metabolism", "chem.biochemistry.mechanism", "bio.cell.primitive", "supports", "Biochemical catalysis supports compartmental cellular metabolism."),
    ("earth-geology-geophysics", "earth.geophysics.mechanism", "earth.geology.mechanism", "supports", "Geophysical inversion supports geologic reconstruction below exposed surfaces."),
    ("earth-geochem-geology", "earth.geochemistry.mechanism", "earth.geology.mechanism", "qualifies", "Isotopic and elemental evidence qualifies geologic histories and reservoir exchange."),
    ("earth-climate-weather", "earth.meteorology.mechanism", "earth.climate.primitive", "part_of", "Weather-state evolution contributes samples to climate distributions."),
    ("earth-ocean-climate", "earth.oceanography.mechanism", "earth.climate.mechanism", "qualifies", "Ocean heat and carbon transport qualify climate energy imbalance and feedback."),
    ("earth-hydro-climate", "earth.climate.mechanism", "earth.hydrology.mechanism", "causes", "Climate forcing changes precipitation, evaporation, snow, runoff, and water storage."),
    ("earth-soil-ecosystem", "earth.soil.mechanism", "earth.ecosystems.mechanism", "qualifies", "Soil formation and properties qualify ecosystem nutrient, water, and rooting processes."),
    ("earth-ecosystem-bio", "bio.ecology.mechanism", "earth.ecosystems.primitive", "supports", "Ecological food webs support ecosystem-scale material and energy models."),
    ("earth-model-scenario", "earth.environmental-modeling.mechanism", "earth.sustainability.mechanism", "supports", "Scenario simulations support comparison of sustainability interventions with uncertainty."),
    ("astro-observe-model", "astro.observational.mechanism", "astro.astrophysics.primitive", "supports", "Forward observation models support astrophysical source inference."),
    ("astro-physics-source", "phy.relativity.mechanism", "astro.astrophysics.mechanism", "qualifies", "Relativistic, radiative, plasma, and nuclear physics qualify astrophysical source models."),
    ("astro-cosmology-observe", "astro.observational.primitive", "astro.cosmology.mechanism", "measures", "Calibrated distance, redshift, background, and structure observations measure cosmological expansion relations."),
    ("astro-celestial-planet", "astro.celestial-mechanics.mechanism", "astro.planetary.primitive", "qualifies", "Orbital dynamics qualify planetary histories and mission geometry."),
    ("astro-exoplanet-observe", "astro.observational.mechanism", "astro.exoplanets.mechanism", "supports", "Instrument and foreground models support joint exoplanet inference."),
    ("astro-astrobiology-planet", "astro.planetary.mechanism", "astro.astrobiology.mechanism", "qualifies", "Planetary evolution qualifies long-term habitability and biosignature preservation."),
    ("astro-mission-observe", "astro.space-systems.mechanism", "astro.observational.primitive", "causes", "The mission observation chain causes calibrated astronomical data products."),
    ("bridge-climate-astro", "astro.observational.primitive", "earth.climate.primitive", "analogous_to", "Astronomical and climate inference both reconstruct inaccessible systems through forward models, calibration, and uncertainty."),
    ("bridge-quantum-info", "qua.information.mechanism", "phy.measurement.mechanism", "qualifies", "Quantum channels and measurement instruments qualify information accessible from physical systems."),
    ("bridge-chem-bio", "chem.biochemistry.mechanism", "bio.molecular.mechanism", "causes", "Chemical catalysis and molecular recognition cause regulated biological transformations."),
]


WORKED_EXAMPLES = [
    ("phy", "energy-boundary", "Mechanical energy boundary", "A sliding block loses mechanical energy to thermal motion through friction; total energy is conserved only after the modeled environment is included.", "physics.classical-mechanics"),
    ("phy", "measurement-budget", "Measurement uncertainty budget", "A length result combines calibration, resolution, temperature expansion, alignment, repeatability, and correlation before rounding to justified digits.", "physics.measurement"),
    ("qua", "two-path", "Quantum two-path interference", "Two indistinguishable amplitudes add before magnitude-squaring, while acquiring distinguishing path information removes the interference term in the reduced statistics.", "quantum-science.foundations"),
    ("qua", "bell", "Bell-correlation boundary", "A Bell test compares measured correlations with an inequality under locality, setting, detection, and independence assumptions without treating entanglement as a signaling channel.", "quantum-science.entanglement"),
    ("chem", "limiting-reagent", "Limiting-reagent calculation", "Balanced stoichiometry and initial moles identify the limiting reagent, then theoretical product is qualified by conversion, selectivity, and measured yield.", "chemistry.general"),
    ("chem", "calibration", "Analytical calibration", "Standards and blanks fit a valid-range response model; an unknown within range receives concentration, uncertainty, and matrix-effect qualification.", "chemistry.analytical"),
    ("bio", "gene-claim", "Genotype-phenotype claim", "A variant association is stratified by ancestry and environment, replicated independently, and remains probabilistic until perturbation and mechanism evidence support causality.", "biology.genetics"),
    ("bio", "food-web", "Food-web perturbation", "Removing one consumer changes prey, competitors, nutrients, and habitat through multiple paths, so the analysis retains indirect effects and uncertainty.", "biology.ecology"),
    ("earth", "water-balance", "Watershed water balance", "Precipitation minus evapotranspiration and outlet flow equals storage change plus an uncertainty residual over a declared watershed and month.", "earth-environment.hydrology"),
    ("earth", "climate-attribution", "Climate-event attribution", "Model ensembles compare event probability under observed and counterfactual forcings while retaining model adequacy, variability, and regional uncertainty.", "earth-environment.climate"),
    ("astro", "transit-validation", "Exoplanet transit validation", "Repeated achromatic dips, stellar characterization, centroid stability, radial velocities, and blend simulations jointly constrain planet and false-positive hypotheses.", "astronomy-space.exoplanets"),
    ("astro", "mission-chain", "Space-mission evidence chain", "A calibrated spectrum retains target geometry, exposure, detector state, downlink, processing version, uncertainty, and archive identity before physical interpretation.", "astronomy-space.space-systems"),
]


GROUPS = [
    ("phy", "physics", PHYSICS, PHYSICS_SOURCES, "Physical sciences", "Physics models matter, energy, fields, spacetime, interactions, collective systems, and measurement through quantitative laws with explicit regimes and uncertainty."),
    ("qua", "quantum-science", QUANTUM, QUANTUM_SOURCES, "Quantum science", "Quantum science models states, observables, amplitudes, dynamics, measurement, entanglement, fields, information, computation, environments, and interpretation boundaries."),
    ("chem", "chemistry", CHEMISTRY, CHEMISTRY_SOURCES, "Chemical sciences", "Chemistry relates composition, structure, bonding, energy, reactions, rates, measurement, computation, biological molecules, materials, and safety across molecular and macroscopic scales."),
    ("bio", "biology", BIOLOGY, BIOLOGY_SOURCES, "Biological sciences", "Biology explains living systems through cellular organization, molecular information, inheritance, evolution, development, physiology, ecology, diversity, networks, and reproducible evidence."),
    ("earth", "earth-environment", EARTH, EARTH_SOURCES, "Earth and environmental sciences", "Earth science reconstructs and predicts coupled solid-Earth, atmosphere, ocean, water, soil, ecosystem, and human processes across spatial and temporal scales."),
    ("astro", "astronomy-space", ASTRONOMY, ASTRONOMY_SOURCES, "Astronomy and space science", "Astronomy infers distant physical systems and cosmic history through calibrated observations, forward models, dynamics, planetary science, astrobiology, and mission evidence chains."),
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
    epistemic: str,
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
        "scope": "physics, quantum, chemistry, biology, Earth, and astronomy foundation tranche",
        "limitations": [
            "Every observation and numerical value requires instrument, unit, calibration, uncertainty, population, and version context.",
            "Models and theories retain regimes, approximations, alternatives, and possible falsifiers; simulations are not observations.",
            "Specialist literature, current primary research, and the full MeSH and MSC discovery frontiers remain open.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "sciences-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def epistemic_for(subject: str) -> str:
    if subject == "quantum-science.interpretations":
        return "contested"
    if subject in {"astronomy-space.astrobiology", "earth-environment.environmental-modeling"}:
        return "provisional"
    return "established"


def context_for_prefix(prefix: str) -> tuple[str, list[str]]:
    for group_prefix, domain, _profiles, sources, _label, _statement in GROUPS:
        if group_prefix == prefix:
            return domain, sources
    raise ValueError(f"unknown science prefix {prefix}")


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    global_index = 0
    for prefix, domain, profiles, sources, domain_label, domain_statement in GROUPS:
        root_subject = profiles[0][0]
        records.append(
            {
                **make_base(f"{prefix}.root", domain, root_subject, sources, "train", "concept", "established"),
                "label": domain_label,
                "statement": domain_statement,
                "aliases": [domain_label.lower()],
            }
        )
        for subject, slug, label, definition, primitive_label, primitive_statement, mechanism_label, mechanism_statement, control_label, control_statement in profiles:
            epistemic = epistemic_for(subject)
            nodes = [
                ("root", label, definition),
                ("primitive", primitive_label, primitive_statement),
                ("mechanism", mechanism_label, mechanism_statement),
            ]
            for offset, (suffix, node_label, statement) in enumerate(nodes):
                node_id = f"{prefix}.{slug}.{suffix}"
                records.append(
                    {
                        **make_base(
                            node_id, domain, subject, sources,
                            "train" if suffix == "root" else split_for(global_index + offset),
                            "concept", epistemic,
                        ),
                        "label": node_label,
                        "statement": statement,
                        "aliases": [node_label.lower()],
                        "tags": ["foundation", domain, f"science-profile-{slug}"],
                    }
                )
                membership_id = f"sci.membership.{prefix}.{slug}.{suffix}"
                target = f"{prefix}.root" if suffix == "root" else f"{prefix}.{slug}.root"
                records.append(
                    {
                        **make_base(
                            membership_id, domain, subject, sources,
                            split_for(global_index + offset + 5), "relation", epistemic,
                        ),
                        "label": f"{node_label} science-world membership",
                        "statement": f"{node_label} is a distinct component of {label} with its own evidence, regime, and failure boundary.",
                        "aliases": [],
                        "relation": {
                            "source_node": node_id,
                            "target_node": target,
                            "kind": "part_of",
                            "polarity": 1,
                            "direction": "forward",
                            "conditions": ["the declared scale, system, model, and measurement regime apply"],
                            "exceptions": [],
                        },
                        "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                    }
                )
            control_id = f"sci.control.{prefix}.{slug}"
            control_split = ["train", "validation", "sealed_test", "cross_domain_holdout"][global_index % 4]
            records.append(
                {
                    **make_base(
                        control_id, domain, subject, [], control_split,
                        "synthetic_control", "synthetic_control",
                    ),
                    "label": control_label,
                    "statement": control_statement,
                    "aliases": [control_label.lower()],
                    "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                    "synthetic": True,
                    "tags": ["negative-control", domain, f"science-profile-{slug}"],
                }
            )
            global_index += 1

    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in CROSS_RELATIONS])
    all_sources = sorted({source for _prefix, _domain, _profiles, sources, _label, _statement in GROUPS for source in sources})
    for identifier, source_node, target_node, kind, statement in CROSS_RELATIONS:
        prefix = source_node.split(".", 1)[0]
        domain, sources = context_for_prefix(prefix)
        cross = identifier.startswith("bridge-") or source_node.split(".", 1)[0] != target_node.split(".", 1)[0]
        records.append(
            {
                **make_base(
                    f"sci.relation.{identifier}", domain,
                    next(profile[0] for group_prefix, _domain, profiles, _sources, _label, _statement in GROUPS if group_prefix == prefix for profile in profiles),
                    all_sources if cross else sources,
                    splitter.split(kind, cross_requested=cross), "relation", "established",
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
                    "conditions": ["the cited scale, material, population, boundary, and model assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (prefix, identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        domain, sources = context_for_prefix(prefix)
        split = example_splits[index % 4]
        node_id = f"sci.example.{prefix}.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, sources, split, "worked_example", epistemic_for(subject)),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "uncertainty_competing_hypotheses"],
                "tags": ["worked-example", domain],
            }
        )
        relation_id = f"sci.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(relation_id, domain, subject, sources, split, "relation", epistemic_for(subject)),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded scientific inference or mechanism composition.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": f"{prefix}.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains illustrative and not a universal claim"],
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
