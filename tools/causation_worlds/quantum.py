"""Quantum foundations with explicit physical regimes and measurement boundaries."""

WORLD = 'quantum-causation-v0'
PREFIX = 'qtm'
DOMAIN = 'quantum-science'
SUBJECT = 'quantum-science.foundations'
SOURCES = ['nasa-science', 'nist-quantum-information', 'griffiths-schroeter-qm-3e', 'zurek-decoherence-2003']
SCOPE = 'Nonrelativistic quantum foundations and single-photon optical mechanisms; ideal state preparation and measurements are stated per edge; no quantum-computing performance or interpretation claim.'
ROOT_LABEL = 'Quantum causation world'
ROOT_STATEMENT = 'Root of the quantum causation world: how quantization, superposition, measurement and decoherence cause the behaviour of atoms, light and everyday quantum-based devices.'

CONCEPTS = [
    ('energy-quantization', 'Energy quantization', 'A discrete energy spectrum for the bound states of the specified Hamiltonian.', []),
    ('energy-level', 'Energy level', 'One of the discrete allowed energies of a bound system.', []),
    ('photon', 'Photon', 'A quantum of the electromagnetic field, with energy h times frequency for a monochromatic mode.', []),
    ('photon-energy', 'Photon energy', "A photon's energy equals Planck's constant times its frequency.", []),
    ('planck-constant', 'Planck constant', 'The constant h relating electromagnetic frequency to photon energy and setting the scale of quantum action.', []),
    ('photoelectric-effect', 'Photoelectric effect', 'Light kicking electrons out of a metal surface.', []),
    ('work-function', 'Work function', 'Minimum energy required to remove an electron at the Fermi level through the surface of a metal into vacuum.', []),
    ('wave-particle-duality', 'Wave-particle duality', 'Quantum objects showing wave behaviour in some setups and particle behaviour in others.', []),
    ('superposition', 'Superposition of states', 'A pure state expressed as a weighted complex-amplitude combination of basis states, not a hidden choice among them.', []),
    ('measurement-collapse', 'Measurement collapse', 'The conditional state update associated with a recorded outcome in the projective-measurement model.', []),
    ('born-rule', 'Born rule probabilities', 'For a normalized pure state measured in an orthonormal basis, the probability of each basis outcome is the squared magnitude of its expansion coefficient.', []),
    ('interference-pattern', 'Interference pattern', 'Spatial modulation of detection probability or intensity from cross terms between coherent overlapping amplitudes.', []),
    ('double-slit', 'Double-slit experiment', 'A two-aperture arrangement whose single-particle detections can accumulate interference fringes when the paths overlap coherently without a distinguishing path record.', []),
    ('which-path', 'Which-path information', 'Any record revealing which route a particle took.', []),
    ('uncertainty-principle', 'Uncertainty principle', 'The state-dependent uncertainty relations implied by noncommuting observables, including sigma_x sigma_p >= hbar/2.', []),
    ('position-momentum-tradeoff', 'Momentum spread lower bound', 'The minimum allowed momentum standard deviation hbar/(2 sigma_x) for a state with finite, nonzero position standard deviation sigma_x.', []),
    ('entanglement', 'Entanglement of particles', 'A joint pure state that cannot factor into subsystem states; a mixed state is entangled if it is not a mixture of product states.', []),
    ('bell-correlation', 'Bell correlation', 'A correlation among outcomes at different measurement settings that violates a Bell inequality.', []),
    ('no-signalling', 'No signalling from correlation', 'Correlated randomness alone cannot carry a chosen message.', []),
    ('potential-barrier', 'Potential barrier', 'A region of potential energy exceeding the incident particle energy in the tunneling problem.', []),
    ('tunneling', 'Quantum tunneling', 'A particle appearing past a barrier it lacked the energy to climb.', []),
    ('atomic-spectrum', 'Atomic spectral lines', 'The sharp set of colours each element emits and absorbs.', []),
    ('orbital', 'Atomic orbital', 'A one-electron spatial wavefunction used for an atom; not a definite classical trajectory.', []),
    ('electron-transition', 'Electron transition', 'An electron jumping between two atomic levels.', []),
    ('exclusion-principle', 'Pauli exclusion principle', 'An antisymmetric state of identical fermions has at most one particle occupying any given single-particle state.', []),
    ('shell-filling', 'Electron shell filling', 'Occupancy of atomic spin orbitals in a specified electronic configuration, with energy ordering and ground or excited preparation stated separately.', []),
    ('spin', 'Particle spin', 'Intrinsic angular momentum with quantized projections; it is not literal rotation of a solid particle.', []),
    ('zero-point-energy', 'Zero-point energy', 'Ground-state energy relative to the classical potential minimum, positive for a quantum harmonic oscillator.', []),
    ('decoherence', 'Decoherence by environment', 'Suppression of reduced-state off-diagonal terms in a selected basis through correlations with unobserved environmental degrees of freedom.', []),
    ('classical-emergence', 'Classical everyday behaviour', 'Effective absence of observable interference between macroscopic alternatives in the stated measurement regime; not a solution of the single-outcome problem.', []),
    ('schrodinger-evolution', 'Schrodinger equation evolution', 'Closed-system state-vector evolution obeying i*hbar*d|psi>/dt = H|psi> with a self-adjoint Hamiltonian H.', []),
    ('unitary-evolution', 'Unitary evolution', 'State evolution by a linear operator U satisfying U-dagger*U = U*U-dagger = I, preserving inner products and state norm.', []),
    ('stimulated-emission', 'Stimulated emission', 'Radiation-induced transition of an excited system to a lower energy state, increasing the population of the driving field mode.', []),
    ('laser-light', 'Laser light', 'Optical output from stimulated-emission gain in an operating laser, usually concentrated in a limited set of modes.', []),
    ('photon-frequency', 'Photon frequency', 'Temporal frequency f of a monochromatic electromagnetic mode.', []),
    ('probability-normalization', 'Probability normalization', 'The sum of probabilities of a complete mutually exclusive set of outcomes equals one.', []),
    ('sharp-classical-orbit', 'Sharp classical orbit', 'An ideal path assigning simultaneous exact position and momentum to a particle.', []),
    ('local-message', 'Controllable remote signal', 'A change in locally observable outcome statistics controlled by a remote party.', []),
    ('photovoltaic-effect', 'Photovoltaic effect', 'Generation and separation of charge carriers in an illuminated semiconductor device, producing electrical output.', []),
    ('nuclear-precession', 'Nuclear spin precession', 'Evolution of nuclear magnetization about an applied magnetic field at the Larmor frequency.', []),
]

RELATIONS = [
    ('frequency-predicts-photonenergy', 'photon-frequency', 'photon-energy', 'predicts', 'Photon frequency predicts photon energy through E = hf, with h the Planck constant.', 'a photon occupies a monochromatic mode of frequency f measured in the same inertial frame', ''),
    ('photonenergy-prereq-photoelectric', 'photon-energy', 'photoelectric-effect', 'prerequisite', 'Photon energy at least equal to the work function is a prerequisite for the photoelectric effect in the single-photon model.', 'electrons near the Fermi level escape a metal into vacuum by absorption of one photon; thermal and field assistance are negligible', ''),
    ('workfunction-prevents-weak-light', 'work-function', 'photoelectric-effect', 'prevents', 'Work function prevents the photoelectric effect for light below the threshold frequency, regardless of intensity within the single-photon regime.', 'hf is below the surface work function and multiphoton absorption, heating and field emission are negligible', ''),
    ('superposition-enables-interference', 'superposition', 'interference-pattern', 'enables', 'Superposition of states enables an interference pattern through cross terms between coherent path amplitudes.', 'path amplitudes overlap at the detector with stable relative phase and no which-path record exists', ''),
    ('whichpath-inhibits-interference', 'which-path', 'interference-pattern', 'inhibits', 'Which-path information inhibits an interference pattern by reducing coherence between path alternatives.', 'an unobserved detector or environment stores distinguishable path records and no postselected quantum erasure is performed', ''),
    ('collapse-causes-outcome', 'born-rule', 'measurement-collapse', 'predicts', 'The set of Born rule probabilities predicts the outcome distribution used in measurement collapse.', 'an ideal projective measurement with a specified orthonormal basis is repeated on identically prepared systems', ''),
    ('born-predicts-weights', 'superposition', 'born-rule', 'predicts', 'Superposition of states predicts Born rule probabilities from the squared magnitudes of its basis amplitudes.', 'the pure state is normalized and the measurement projects onto the orthonormal basis used in its expansion', ''),
    ('uncertainty-causes-tradeoff', 'uncertainty-principle', 'position-momentum-tradeoff', 'predicts', 'Uncertainty principle predicts the momentum spread lower bound hbar/(2 sigma_x).', 'the position-momentum relation holds for every quantum state of the particle for which the finite standard deviations exist; sigma_x is nonzero', ''),
    ('tradeoff-prevents-orbits', 'position-momentum-tradeoff', 'sharp-classical-orbit', 'prevents', 'Momentum spread lower bound prevents a sharp classical orbit from representing a quantum state with exact position and momentum.', 'canonical position and momentum are considered for a nonrelativistic particle with nonzero hbar', ''),
    ('unitary-preserves-born', 'unitary-evolution', 'probability-normalization', 'predicts', 'Unitary evolution predicts probability normalization at every subsequent time by preserving the state norm.', 'the initial state has norm one and a self-adjoint Hamiltonian generates closed-system evolution', ''),
    ('entanglement-causes-correlation', 'entanglement', 'bell-correlation', 'enables', 'Entanglement of particles enables a Bell correlation attaining |S| = 2*sqrt(2) for the specified singlet and CHSH observables.', 'identically prepared singlets (|01>-|10>)/sqrt(2) undergo ideal local projective measurements using Pauli X and Z with outcomes +/-1, A0=Z, A1=X, B0=(Z+X)/sqrt(2), B1=(Z-X)/sqrt(2), and S=<A0*B0>+<A0*B1>+<A1*B0>-<A1*B1>; experimental loopholes are excluded', ''),
    ('nosignalling-prevents-message', 'no-signalling', 'local-message', 'predicts', 'No signalling from correlation predicts the absence of a controllable remote signal from local operations on entanglement alone.', 'remote operations are trace-preserving, outcomes are not postselected using communicated information, and only local outcome statistics are read', ''),
    ('barrier-enables-tunneling', 'potential-barrier', 'tunneling', 'prerequisite', 'Potential barrier is a prerequisite for quantum tunneling through a classically forbidden region.', 'the one-dimensional scattering problem has a finite-width region with V greater than incident energy E and a transmitted propagating region', ''),
    ('transition-causes-spectrum', 'electron-transition', 'atomic-spectrum', 'causes', 'Electron transition causes atomic spectral lines by radiative exchange at an allowed level gap.', 'bound atomic levels participate in allowed radiative transitions and line broadening is narrower than the resolved gap structure', ''),
    ('quantization-prereq-spectrum', 'energy-quantization', 'atomic-spectrum', 'prerequisite', 'Energy quantization is a prerequisite for atomic spectral lines associated with discrete bound-level differences.', 'the spectrum contains bound-bound electronic transitions of isolated atoms rather than a continuum', ''),
    ('transition-emits-photon', 'electron-transition', 'photon', 'causes', 'Electron transition causes photon emission when an excited atom decays through a single-photon radiative channel.', 'the downward transition is radiative and nonradiative or multiphoton channels are excluded from this event', ''),
    ('exclusion-causes-filling', 'exclusion-principle', 'shell-filling', 'predicts', 'Pauli exclusion principle predicts at most one electron per spin orbital in electron shell filling.', 'identical electrons have an antisymmetric many-electron state represented in an orthonormal spin-orbital basis', ''),
    ('spin-enables-filling', 'spin', 'shell-filling', 'enables', 'Particle spin enables electron shell filling to place two electrons in the same spatial orbital with opposite spin projections.', 'the independent-electron orbital description uses an antisymmetric two-electron state with two available spin projections', ''),
    ('uncertainty-causes-zeropoint', 'uncertainty-principle', 'zero-point-energy', 'predicts', 'Uncertainty principle predicts a positive zero-point energy lower bound for a harmonic oscillator.', 'the Hamiltonian is p squared over 2m plus m omega squared x squared over 2, with m and omega positive and the potential minimum taken as zero', ''),
    ('decoherence-causes-classical', 'decoherence', 'classical-emergence', 'enables', 'Decoherence by environment enables classical everyday behaviour by suppressing observable interference between macroscopic alternatives.', 'environment-selected pointer states decohere much faster than the observation timescale and environmental records are inaccessible', 'Decoherence alone does not select a single realized measurement outcome.'),
    ('decoherence-inhibits-interference', 'decoherence', 'interference-pattern', 'inhibits', 'Decoherence by environment inhibits interference pattern visibility through loss of reduced-state coherence.', 'the environment becomes correlated with paths whose amplitudes would otherwise overlap coherently at detection', ''),
    ('stimulated-causes-laser', 'stimulated-emission', 'laser-light', 'enables', 'Stimulated emission enables laser light by supplying gain to an optical field mode.', 'an operating pumped gain medium has net gain above losses and the laser feedback or amplification geometry supports the mode', ''),
    ('photon-enables-stimulated', 'photon', 'stimulated-emission', 'enables', 'Photon enables stimulated emission by occupying a mode resonant with an allowed downward transition.', 'an excited emitter couples to an electromagnetic mode at its transition frequency within the linewidth', ''),
    ('level-enables-transition', 'energy-level', 'electron-transition', 'enables', 'Energy level enables electron transition when another accessible level and a coupling mechanism are present.', 'the initial level is occupied, the final level is available, and the perturbation satisfies the applicable selection rule', ''),
    ('orbital-enables-filling', 'orbital', 'shell-filling', 'enables', 'Atomic orbital enables electron shell filling by providing spatial states with spin degrees of freedom.', 'a specified atomic independent-particle approximation provides a bound orbital basis and occupancies obey antisymmetry', ''),
    ('spectrum-predicts-element', 'atomic-spectrum', 'electron-transition', 'predicts', 'The set of atomic spectral lines predicts electron transition energies through their measured photon frequencies.', 'the identified line arises from a specified isolated atomic transition; Doppler and external-field shifts are corrected', ''),
    ('photon-enables-transition', 'photon', 'electron-transition', 'enables', 'Photon enables an upward electron transition by resonant absorption.', 'the initial atomic level is occupied and an allowed transition matches photon energy within its linewidth', ''),
    ('spin-enables-precession', 'spin', 'nuclear-precession', 'enables', 'Particle spin enables nuclear spin precession through its associated magnetic moment.', 'a nucleus with nonzero magnetic moment experiences a static field and transverse magnetization is prepared', ''),
]

MYTHS = [
    ('observer-consciousness', 'A conscious observer causes collapse', 'Measurement means any physical interaction that leaves a record, not a watching mind.', 'measurement-collapse'),
    ('entanglement-telephone', 'Entanglement sends instant messages', 'Correlated outcomes carry no controllable signal from one party to the other.', 'no-signalling'),
    ('uncertainty-is-clumsiness', 'The uncertainty principle is just clumsy instruments', 'The tradeoff is built into the quantum state itself, not only into our tools.', 'uncertainty-principle'),
    ('cat-both-alive', 'Schrodinger cat establishes a unique outcome', 'Environment-induced decoherence suppresses observable macroscopic interference but does not by itself establish a unique measurement outcome.', 'decoherence'),
    ('quantum-anything-goes', 'Quantum mechanics means anything can happen', 'Outcomes follow strict probability laws; impossible events stay impossible.', 'born-rule'),
]

BOUNDARIES = [
    ('no-everyday-qpu', 'Everyday devices are not quantum computers', 'Quantization and tunneling underlie modern electronics, but that does not make a laptop a quantum computer.', 'energy-quantization'),
    ('probabilities-not-lawlessness', 'Conditional predictions need a model', 'Quantum outcome probabilities require a specified preparation, dynamics and measurement; ignorance of these is not resolved by the Born rule alone.', 'born-rule'),
    ('scale-fades-quantum', 'Size alone does not forbid coherence', 'Observable coherence depends on coupling, preparation and measurement timescale; sufficiently isolated macroscopic collective systems can retain quantum coherence.', 'superposition'),
]

EXAMPLES = [
    ('solar-cells', 'Solar panels use internal carrier generation', 'In an illuminated semiconductor junction, interband absorption of photons with sufficient energy generates electron-hole pairs and the device separates carriers; this photovoltaic effect does not eject electrons into vacuum.', ['photon-energy', 'photovoltaic-effect']),
    ('atomic-gas-lines', 'Line emission from excited atomic gas', 'In a dilute hydrogen gas, an allowed downward single-photon transition between prepared atomic bound levels emits a spectral-line photon; neglecting recoil, its energy equals the level difference.', ['electron-transition', 'energy-level', 'photon', 'atomic-spectrum']),
    ('flash-tunneling', 'Flash memory writes by tunneling', 'Electrons cross a thin potential barrier by quantum tunneling to store each bit.', ['potential-barrier', 'tunneling']),
    ('mri-spin', 'MRI reads precessing nuclear magnetization', 'A static magnet produces a small net nuclear polarization; resonant RF pulses tip the magnetization and receiver coils detect the precession signal.', ['spin', 'nuclear-precession']),
]

CONTROLS = [
    ('collapse-signal', 'Measurement collapse travels faster than light', 'Collapse must not be treated as a physical signal moving between places.'),
    ('tunneling-walls', 'People can quantum tunnel through walls', 'Everyday objects must not be treated as tunneling usefully through walls.'),
    ('zero-point-free-energy', 'Zero-point energy powers machines for free', 'Zero-point energy must not be treated as a free energy source.'),
    ('entanglement-radio', 'Entanglement replaces radio', 'Entanglement of particles must not be treated as a communication channel.'),
]
