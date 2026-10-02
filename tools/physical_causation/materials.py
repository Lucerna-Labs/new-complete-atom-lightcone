"""Condensed matter and materials: elasticity, fracture, conduction, corrosion."""

SUBJECT = "physics.condensed-matter"
SOURCES = ["nasa-glenn-beginners-guide", "eia-energy-explained"]

CONCEPTS = [
    ("applied-stress", "Applied mechanical stress", "Force applied over an area of a material, stretching, squeezing or bending it.", []),
    ("elastic-deformation", "Elastic deformation", "A material stretched or compressed within its elastic limit returns to its original shape when released.", []),
    ("elastic-limit", "Elastic limit exceeded", "Stress beyond a material's elastic limit.", []),
    ("plastic-deformation", "Permanent plastic deformation", "Beyond the elastic limit a ductile material bends or stretches permanently.", []),
    ("fracture", "Fracture of a material", "A material breaks apart when stress exceeds its strength.", []),
    ("brittle-material", "Brittle material", "Glass, ceramics and cast iron fracture with little deformation.", []),
    ("crack", "Crack or flaw in a material", "A small crack concentrates stress at its tip.", []),
    ("spring-stretch", "Spring stretch", "Stretching a spring stores elastic energy; its restoring force grows with the stretch.", []),
    ("elastic-energy", "Stored elastic energy", "Energy held in a deformed elastic object.", []),
    ("metal-free-electrons", "Free electrons in metals", "Metals have electrons free to move through the crystal.", []),
    ("electrical-conductor", "Electrical conductor", "A material that lets electric current pass easily.", []),
    ("thermal-conductor", "Good thermal conductor", "A material, such as a metal, that conducts heat quickly.", []),
    ("electrical-insulator", "Electrical insulator", "A material such as rubber or plastic in which charges cannot move freely.", []),
    ("touch-coldness", "Feeling of coldness on touch", "Skin senses how fast heat leaves it, not the temperature of the object directly.", []),
    ("iron-exposure", "Iron exposed to water and oxygen", "Iron or steel in contact with both moisture and oxygen.", []),
    ("rusting", "Rusting of iron", "Iron oxidises into flaky iron oxide in the presence of water and oxygen.", ["corrosion"]),
    ("salt-water-exposure", "Salt water exposure", "Contact with salty water, as near the sea or on salted roads.", []),
    ("protective-coating", "Protective paint or coating", "Paint, oil or zinc plating sealing a metal surface.", []),
    ("water-anomalous-expansion", "Water expanding as it freezes", "Water expands by about 9 percent when it freezes into ice.", []),
    ("burst-pipe", "Burst frozen pipe", "A water pipe split open by ice forming inside it.", []),
    ("ice-floating", "Ice floating on water", "Ice is less dense than liquid water and floats.", []),
    ("material-fatigue", "Metal fatigue", "Repeated loading below the breaking stress grows cracks until the part fails.", []),
    ("cyclic-loading", "Repeated cyclic loading", "Stress applied and removed many times.", []),
]

RELATIONS = [
    ("stress-elastic", "applied-stress", "elastic-deformation", "causes", "Applied mechanical stress causes elastic deformation.", "the stress stays below the elastic limit", ""),
    ("limit-plastic", "elastic-limit", "plastic-deformation", "causes", "An elastic limit exceeded causes permanent plastic deformation in ductile materials.", "the material is ductile, like copper or mild steel", "brittle materials fracture instead"),
    ("stress-fracture", "applied-stress", "fracture", "causes", "Applied mechanical stress beyond a material's strength causes fracture of the material.", "the stress exceeds the breaking strength", ""),
    ("brittle-fracture", "brittle-material", "fracture", "enables", "A brittle material enables sudden fracture with little warning deformation.", "the stress rises past the strength", ""),
    ("crack-fracture", "crack", "fracture", "causes", "A crack or flaw in a material causes fracture at lower overall stress by concentrating stress at its tip.", "the crack is loaded so that it opens", ""),
    ("spring-energy", "spring-stretch", "elastic-energy", "causes", "Spring stretch causes stored elastic energy.", "the spring stays within its elastic limit", ""),
    ("elasticenergy-kinetic", "elastic-energy", "kinetic-energy", "transforms_to", "Stored elastic energy transforms into kinetic energy of motion when a stretched spring or band is released.", "the object is free to move", "friction diverts part of the energy into heat"),
    ("electrons-conductor", "metal-free-electrons", "electrical-conductor", "causes", "Free electrons in metals cause metals to be good electrical conductors.", "the metal is not oxidised at the contacts", ""),
    ("electrons-thermal", "metal-free-electrons", "thermal-conductor", "causes", "Free electrons in metals cause metals to be good thermal conductors.", "the metal is pure enough", ""),
    ("insulator-current", "electrical-insulator", "electric-current", "prevents", "An electrical insulator prevents electric current flow at ordinary voltages.", "the voltage is below the insulator's breakdown voltage", ""),
    ("thermal-coldness", "thermal-conductor", "touch-coldness", "causes", "A good thermal conductor causes a stronger feeling of coldness on touch because it draws heat from the skin faster.", "the object is colder than the skin", ""),
    ("exposure-rust", "iron-exposure", "rusting", "causes", "Iron exposed to water and oxygen causes rusting of iron.", "the surface is unprotected", ""),
    ("salt-rust", "salt-water-exposure", "rusting", "causes", "Salt water exposure causes faster rusting of iron by making water conduct better.", "the iron is unprotected", ""),
    ("coating-rust", "protective-coating", "rusting", "prevents", "A protective paint or coating prevents rusting of iron by keeping water and oxygen away.", "the coating is unbroken", "scratches expose bare metal"),
    ("anomalous-burst", "water-anomalous-expansion", "burst-pipe", "causes", "Water expanding as it freezes causes a burst frozen pipe.", "the water is trapped in the pipe", ""),
    ("anomalous-ice", "water-anomalous-expansion", "ice-floating", "causes", "Water expanding as it freezes causes ice floating on water.", "the water is fresh or only slightly salty", ""),
    ("cyclic-fatigue", "cyclic-loading", "material-fatigue", "causes", "Repeated cyclic loading causes metal fatigue.", "the load cycles many times", ""),
    ("fatigue-crack", "material-fatigue", "crack", "causes", "Metal fatigue causes a crack or flaw to grow with each cycle.", "loading continues", ""),
]
