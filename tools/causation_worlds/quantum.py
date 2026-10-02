"""Quantum foundations causation: quantization, superposition, measurement, entanglement, decoherence."""

WORLD = "quantum-causation-v0"
PREFIX = "qtm"
DOMAIN = "quantum-science"
SUBJECT = "quantum-science.foundations"
SOURCES = ["nasa-science", "nist-quantum-information"]
SCOPE = "Everyday-scale quantum physics facts: quantized energy, photons, superposition, measurement, uncertainty, entanglement, tunneling, decoherence"
ROOT_LABEL = "Quantum causation world"
ROOT_STATEMENT = "Root of the quantum causation world: how quantization, superposition, measurement and decoherence cause the behaviour of atoms, light and everyday quantum-based devices."

CONCEPTS = [
    ("energy-quantization", "Energy quantization", "Bound systems hold energy only in discrete steps rather than any value.", []),
    ("energy-level", "Energy level", "One of the discrete allowed energies of a bound system.", []),
    ("photon", "Photon", "A single indivisible packet of light.", []),
    ("photon-energy", "Photon energy", "A photon's energy equals Planck's constant times its frequency.", []),
    ("planck-constant", "Planck constant", "The tiny fixed constant setting the scale of quantum steps.", []),
    ("photoelectric-effect", "Photoelectric effect", "Light kicking electrons out of a metal surface.", []),
    ("work-function", "Work function", "The minimum energy binding each electron inside a metal.", []),
    ("wave-particle-duality", "Wave-particle duality", "Quantum objects showing wave behaviour in some setups and particle behaviour in others.", []),
    ("superposition", "Superposition of states", "A system holding several possibilities at once until it is measured.", []),
    ("measurement-collapse", "Measurement collapse", "A measurement interaction reducing a superposition to one recorded outcome.", []),
    ("born-rule", "Born rule probabilities", "The rule that squared amplitudes give each outcome's probability.", []),
    ("interference-pattern", "Interference pattern", "Bright and dark bands from overlapping possibility waves.", []),
    ("double-slit", "Double-slit experiment", "Particles sent one by one through two slits still build wave-like bands.", []),
    ("which-path", "Which-path information", "Any record revealing which route a particle took.", []),
    ("uncertainty-principle", "Uncertainty principle", "A floor on how sharply paired quantities can be fixed together.", []),
    ("position-momentum-tradeoff", "Position and momentum tradeoff", "Sharper position knowledge forces blurrier momentum knowledge, and back.", []),
    ("entanglement", "Entanglement of particles", "Two particles sharing one joint state whose results stay linked at any distance.", []),
    ("bell-correlation", "Bell correlation", "Entangled measurement correlations stronger than any pre-agreed classical plan allows.", []),
    ("no-signalling", "No signalling from correlation", "Correlated randomness alone cannot carry a chosen message.", []),
    ("potential-barrier", "Potential barrier", "An energy hill a particle classically cannot climb.", []),
    ("tunneling", "Quantum tunneling", "A particle appearing past a barrier it lacked the energy to climb.", []),
    ("atomic-spectrum", "Atomic spectral lines", "The sharp set of colours each element emits and absorbs.", []),
    ("orbital", "Atomic orbital", "The cloud-like standing wave pattern an electron occupies in an atom.", []),
    ("electron-transition", "Electron transition", "An electron jumping between two atomic levels.", []),
    ("exclusion-principle", "Pauli exclusion principle", "No two identical fermions can share one quantum state.", []),
    ("shell-filling", "Electron shell filling", "Electrons occupying atomic states from low energy outward, one per state.", []),
    ("spin", "Particle spin", "An intrinsic fixed rotation-like property of each particle.", []),
    ("zero-point-energy", "Zero-point energy", "The leftover minimum motion a confined particle cannot lose.", []),
    ("decoherence", "Decoherence by environment", "Leakage of quantum information into surroundings that scrambles superpositions.", []),
    ("classical-emergence", "Classical everyday behaviour", "The definite, single-outcome behaviour of large objects.", []),
    ("schrodinger-evolution", "Schrodinger equation evolution", "The smooth law carrying a quantum state forward between measurements.", []),
    ("unitary-evolution", "Unitary evolution", "Evolution that shuffles amplitudes without losing any probability.", []),
    ("stimulated-emission", "Stimulated emission", "An excited atom releasing a photon copied from a passing one.", []),
    ("laser-light", "Laser light", "Light amplified in one exact mode into a coherent beam.", []),
]

RELATIONS = [
    ("quantization-causes-levels", "energy-quantization", "energy-level", "causes", "Energy quantization causes the discrete energy level set of a bound system.", "the particle is bound in an atom or a trap", ""),
    ("planck-causes-photonenergy", "planck-constant", "photon-energy", "causes", "The Planck constant causes the photon energy of each photon to equal its frequency times h.", "light is described as photons", ""),
    ("photonenergy-prereq-photoelectric", "photon-energy", "photoelectric-effect", "prerequisite", "Photon energy above the threshold is a prerequisite for the photoelectric effect to eject an electron.", "light shines on a metal surface", ""),
    ("workfunction-prevents-weak-light", "work-function", "photoelectric-effect", "prevents", "A high work function prevents weak light from triggering the photoelectric effect.", "each photon carries less energy than the binding", ""),
    ("photoelectric-causes-duality", "photoelectric-effect", "wave-particle-duality", "causes", "The photoelectric effect causes wave-particle duality to favour a particle picture of light.", "electrons leave instantly even in dim light", ""),
    ("slits-cause-interference", "double-slit", "interference-pattern", "causes", "The double-slit experiment causes an interference pattern to build up one particle at a time.", "both slits stay open and unwatched", ""),
    ("superposition-enables-interference", "superposition", "interference-pattern", "enables", "Superposition of states enables the interference pattern of many quantum particles.", "the paths are not distinguished", ""),
    ("whichpath-inhibits-interference", "which-path", "interference-pattern", "inhibits", "Which-path information inhibits the interference pattern by distinguishing the paths.", "a detector reveals which slit was used", ""),
    ("collapse-causes-outcome", "measurement-collapse", "born-rule", "causes", "Measurement collapse causes Born rule probabilities to resolve into one recorded outcome.", "a measuring device interacts with the system", ""),
    ("born-predicts-weights", "born-rule", "superposition", "predicts", "The pattern of Born rule probabilities predicts the weight of each branch in a superposition of states.", "the state amplitudes are squared", ""),
    ("uncertainty-causes-tradeoff", "uncertainty-principle", "position-momentum-tradeoff", "causes", "The uncertainty principle causes the position and momentum tradeoff.", "both are measured on the same particle", ""),
    ("tradeoff-prevents-orbits", "position-momentum-tradeoff", "orbital", "prevents", "The position and momentum tradeoff prevents electrons from following sharp orbits, giving an atomic orbital cloud instead.", "the electron is bound to a nucleus", ""),
    ("schrodinger-enables-unitary", "schrodinger-evolution", "unitary-evolution", "enables", "Schrodinger equation evolution enables unitary evolution of the quantum state between measurements.", "no measurement intervenes", ""),
    ("unitary-preserves-born", "unitary-evolution", "born-rule", "enables", "Unitary evolution enables Born rule probabilities to stay consistent over time.", "the state keeps evolving without loss", ""),
    ("entanglement-causes-correlation", "entanglement", "bell-correlation", "causes", "Entanglement of particles causes a Bell correlation stronger than any classical link.", "the pair is measured in suitable settings", ""),
    ("nosignalling-prevents-message", "no-signalling", "entanglement", "prevents", "No signalling from correlation prevents entanglement of particles from carrying a message by itself.", "each side reads only its own outcomes", ""),
    ("barrier-enables-tunneling", "potential-barrier", "tunneling", "enables", "A thin potential barrier enables quantum tunneling to let particles through despite too little energy.", "the barrier is thin and finite", ""),
    ("transition-causes-spectrum", "electron-transition", "atomic-spectrum", "causes", "An electron transition causes atomic spectral lines when it emits or absorbs a photon.", "the jump crosses a definite energy gap", ""),
    ("quantization-prereq-spectrum", "energy-quantization", "atomic-spectrum", "prerequisite", "Energy quantization is a prerequisite for atomic spectral lines being sharp.", "the atom's levels are discrete", ""),
    ("transition-emits-photon", "electron-transition", "photon", "causes", "A downward electron transition causes a photon to be emitted with the gap's energy.", "the electron falls to a lower level", ""),
    ("exclusion-causes-filling", "exclusion-principle", "shell-filling", "causes", "The Pauli exclusion principle causes electron shell filling to run one electron per state outward from the nucleus.", "electrons are fermions in one atom", ""),
    ("spin-enables-filling", "spin", "shell-filling", "enables", "Opposite particle spin enables electron shell filling to pair two electrons per orbital.", "the two electrons have opposite spin", ""),
    ("uncertainty-causes-zeropoint", "uncertainty-principle", "zero-point-energy", "causes", "The uncertainty principle causes zero-point energy by forbidding a particle from resting completely.", "the particle is trapped in a small region", ""),
    ("decoherence-causes-classical", "decoherence", "classical-emergence", "causes", "Decoherence by environment causes classical everyday behaviour to emerge from quantum rules.", "large objects interact constantly with their surroundings", ""),
    ("decoherence-inhibits-interference", "decoherence", "interference-pattern", "inhibits", "Decoherence by environment inhibits interference pattern visibility for large objects.", "environmental records leak which-path information", ""),
    ("collapse-interrupts-evolution", "measurement-collapse", "schrodinger-evolution", "inhibits", "A measurement collapse inhibits Schrodinger equation evolution of the pre-measurement state.", "the measurement result is recorded", ""),
    ("stimulated-causes-laser", "stimulated-emission", "laser-light", "causes", "Stimulated emission causes laser light to amplify in one exact mode.", "a population inversion is pumped", ""),
    ("photon-enables-stimulated", "photon", "stimulated-emission", "enables", "A passing photon enables stimulated emission of an identical twin photon from an excited atom.", "an excited atom sits in the photon's path", ""),
    ("duality-prereq-slits", "wave-particle-duality", "double-slit", "prerequisite", "Wave-particle duality is a prerequisite for the double-slit experiment showing single-particle interference.", "particles are sent one at a time", ""),
    ("planck-prereq-quantization", "planck-constant", "energy-quantization", "prerequisite", "A nonzero Planck constant is a prerequisite for energy quantization to appear.", "the system is bound on small scales", ""),
    ("level-enables-transition", "energy-level", "electron-transition", "enables", "A discrete energy level enables an electron transition of exactly the gap size.", "a matching photon or collision arrives", ""),
    ("workfunction-prereq-photoelectric", "work-function", "photoelectric-effect", "prerequisite", "A finite work function is a prerequisite for the photoelectric effect threshold to exist.", "electrons are bound inside the metal", ""),
    ("superposition-prereq-entanglement", "superposition", "entanglement", "prerequisite", "A joint superposition of states of two particles is a prerequisite for entanglement of particles.", "the joint state cannot be split into parts", ""),
    ("slits-enable-whichpath", "double-slit", "which-path", "enables", "The double-slit experiment enables which-path information to be gathered by watching one slit.", "a detector is placed at a slit", ""),
    ("interference-predicts-duality", "interference-pattern", "wave-particle-duality", "predicts", "A single-particle interference pattern predicts wave-particle duality better than any single event.", "many particles accumulate on the screen", ""),
    ("collapse-enables-record", "measurement-collapse", "classical-emergence", "enables", "Measurement collapse enables classical everyday behaviour such as a definite pointer reading.", "the amplifier chain is macroscopic", ""),
    ("orbital-enables-filling", "orbital", "shell-filling", "enables", "Each atomic orbital enables ordered electron shell filling by offering fixed states.", "states fill from lowest energy upward", ""),
    ("spectrum-predicts-element", "atomic-spectrum", "electron-transition", "predicts", "The set of atomic spectral lines predicts the electron transition set unique to each element.", "the light is spread by a prism or grating", ""),
    ("photon-enables-transition", "photon", "electron-transition", "enables", "An absorbed photon enables an upward electron transition when the energies match.", "the photon energy equals a level gap", ""),
    ("zeropoint-inhibits-stillness", "zero-point-energy", "classical-emergence", "inhibits", "Zero-point energy inhibits classical everyday behaviour of perfect rest at molecular scales.", "motion is cooled toward absolute zero", ""),
]

MYTHS = [
    ("observer-consciousness", "A conscious observer causes collapse",
     "Measurement means any physical interaction that leaves a record, not a watching mind.", "measurement-collapse"),
    ("entanglement-telephone", "Entanglement sends instant messages",
     "Correlated outcomes carry no controllable signal from one party to the other.", "no-signalling"),
    ("uncertainty-is-clumsiness", "The uncertainty principle is just clumsy instruments",
     "The tradeoff is built into the quantum state itself, not only into our tools.", "uncertainty-principle"),
    ("cat-both-alive", "Schrödinger's cat proves big things sit in two states",
     "The thought experiment frames the measurement problem; real cats decohere almost instantly.", "decoherence"),
    ("quantum-anything-goes", "Quantum mechanics means anything can happen",
     "Outcomes follow strict probability laws; impossible events stay impossible.", "born-rule"),
]

BOUNDARIES = [
    ("no-everyday-qpu", "Everyday devices are not quantum computers",
     "Quantization and tunneling underlie modern electronics, but that does not make a laptop a quantum computer.", "energy-quantization"),
    ("probabilities-not-lawlessness", "Probabilities, not lawlessness",
     "The theory predicts exact odds for every experiment, not vague anything-goes chance.", "born-rule"),
    ("scale-fades-quantum", "Quantum effects fade with size",
     "Decoherence grows with size and interaction, hiding superpositions from everyday view.", "superposition"),
]

EXAMPLES = [
    ("solar-cells", "Solar panels and the photoelectric effect",
     "Photons with sufficient photon energy free electrons through the photoelectric effect, making current.",
     ["photon-energy", "photoelectric-effect", "work-function"]),
    ("led-colours", "LED colours from level gaps",
     "Each LED colour comes from the energy gap its material's electron transition releases.",
     ["electron-transition", "energy-level", "photon"]),
    ("flash-tunneling", "Flash memory writes by tunneling",
     "Electrons cross a thin potential barrier by quantum tunneling to store each bit.",
     ["potential-barrier", "tunneling"]),
    ("mri-spin", "MRI reads nuclear spin",
     "Scanner pulses align particle spin signals from hydrogen nuclei and read the echoes.",
     ["spin", "measurement-collapse"]),
]

CONTROLS = [
    ("collapse-signal", "Measurement collapse travels faster than light",
     "Collapse must not be treated as a physical signal moving between places."),
    ("tunneling-walls", "People can quantum tunnel through walls",
     "Everyday objects must not be treated as tunneling usefully through walls."),
    ("zero-point-free-energy", "Zero-point energy powers machines for free",
     "Zero-point energy must not be treated as a free energy source."),
    ("entanglement-radio", "Entanglement replaces radio",
     "Entanglement of particles must not be treated as a communication channel."),
]
