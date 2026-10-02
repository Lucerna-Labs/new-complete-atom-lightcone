"""Statistical mechanics: diffusion, mixing, entropy, irreversibility."""

SUBJECT = "physics.statistical-mechanics"
SOURCES = ["eia-energy-explained", "nist-codata-2022"]

CONCEPTS = [
    ("random-molecular-motion", "Random molecular motion", "Molecules in fluids move randomly and collide constantly; faster on average at higher temperature.", []),
    ("concentration-difference", "Concentration difference", "More particles of a substance in one region than in a neighbouring one.", []),
    ("diffusion", "Diffusion spreading", "Particles spread from regions of higher to lower concentration through random motion.", []),
    ("dye-spreading", "Dye spreading in water", "A drop of dye gradually colours the whole glass of water.", []),
    ("smell-spreading", "Smell spreading through a room", "Odour molecules from a source gradually reach the whole room.", []),
    ("stirring", "Stirring a fluid", "Mechanical stirring moves fluid around in bulk.", []),
    ("mixing", "Mixing of substances", "Substances becoming evenly distributed through each other.", []),
    ("entropy-increase", "Entropy increase", "In an isolated system the number of accessible microscopic arrangements tends to grow; energy spreads out.", ["second law of thermodynamics"]),
    ("irreversibility", "Irreversible everyday processes", "Mixed liquids do not unmix and broken cups do not reassemble on their own.", []),
    ("energy-dispersal", "Energy dispersal as heat", "Useful concentrated energy spreads into disordered thermal energy of many particles.", []),
    ("energy-conservation", "Energy conservation", "Energy is neither created nor destroyed, only converted between forms.", ["first law of thermodynamics"]),
    ("perpetual-motion", "Perpetual motion machine claim", "A claimed device that runs forever or outputs more energy than it takes in.", []),
    ("brownian-motion", "Brownian jiggling", "Small particles suspended in a fluid jiggle randomly because molecules strike them unevenly.", []),
    ("pressure-equalisation", "Pressure equalisation", "Gas in connected containers spreads until pressure is equal throughout.", []),
    ("open-valve", "Opening a valve between containers", "Connecting two gas containers through an open path.", []),
]

RELATIONS = [
    ("motion-diffusion", "random-molecular-motion", "diffusion", "causes", "Random molecular motion causes diffusion spreading.", "the fluid is not frozen solid", ""),
    ("concentration-diffusion", "concentration-difference", "diffusion", "enables", "A concentration difference enables net diffusion spreading from high to low concentration.", "the regions are connected", ""),
    ("rise-motion", "temperature-rise", "random-molecular-motion", "causes", "A temperature rise causes faster random molecular motion.", "the substance stays in the same phase", ""),
    ("diffusion-dye", "diffusion", "dye-spreading", "causes", "Diffusion spreading causes dye spreading in water.", "the water is still", ""),
    ("diffusion-smell", "diffusion", "smell-spreading", "causes", "Diffusion spreading causes smell spreading through a room, though air currents usually dominate.", "the air is still", "drafts and convection carry odours much faster than diffusion"),
    ("stirring-mixing", "stirring", "mixing", "causes", "Stirring a fluid causes rapid mixing of substances.", "the substances are miscible", ""),
    ("diffusion-mixing", "diffusion", "mixing", "causes", "Diffusion spreading causes slow mixing of substances.", "the substances are miscible", "oil and water do not mix"),
    ("mixing-entropy", "mixing", "entropy-increase", "causes", "Mixing of substances causes entropy increase.", "the system is isolated", ""),
    ("entropy-irreversible", "entropy-increase", "irreversibility", "causes", "Entropy increase causes irreversible everyday processes.", "the system is not driven backward by outside work", ""),
    ("dispersal-entropy", "energy-dispersal", "entropy-increase", "causes", "Energy dispersal as heat causes entropy increase.", "no outside work reverses it", ""),
    ("conservation-perpetual", "energy-conservation", "perpetual-motion", "prevents", "Energy conservation prevents a perpetual motion machine from producing energy from nothing.", "the device is isolated from energy inputs", ""),
    ("entropy-perpetual", "entropy-increase", "perpetual-motion", "prevents", "Entropy increase prevents a perpetual motion machine from running forever without losses.", "friction or heat exchange exists", ""),
    ("motion-brownian", "random-molecular-motion", "brownian-motion", "causes", "Random molecular motion causes Brownian jiggling of small suspended particles.", "the particles are microscopic", ""),
    ("valve-equalisation", "open-valve", "pressure-equalisation", "causes", "Opening a valve between containers causes pressure equalisation.", "the containers start at different pressures", ""),
    ("conservation-dispersal", "energy-conservation", "energy-dispersal", "predicts", "Energy conservation predicts that dispersed energy as heat is still present, only less useful.", "the system is isolated", ""),
    ("friction-dispersal", "sliding-friction", "energy-dispersal", "causes", "Sliding friction causes energy dispersal as heat.", "the surfaces slide", ""),
]
