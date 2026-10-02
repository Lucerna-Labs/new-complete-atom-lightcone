"""Chemistry causation: bonds, reactions, energy, equilibrium, acids and bases, solutions."""

WORLD = "chemistry-causation-v0"
PREFIX = "chm"
DOMAIN = "chemistry"
SUBJECT = "chemistry.general"
SOURCES = ["iupac-goldbook-500", "nist-chemistry-webbook"]
SCOPE = "Everyday chemistry: bonding and valence, reaction and mass accounting, energy and rates, equilibrium, acids and bases, redox, solutions"
ROOT_LABEL = "Chemistry causation world"
ROOT_STATEMENT = "Root of the chemistry causation world: how electrons, bonds and energy cause substances to react, dissolve, ionise and change."

CONCEPTS = [
    ("chemical-bond", "Chemical bond", "An attractive link holding atoms together in a substance.", []),
    ("covalent-bond", "Covalent bond", "Two atoms sharing a pair of electrons.", []),
    ("ionic-bond", "Ionic bond", "Opposite-charged ions held together by full electron transfer.", []),
    ("valence-electrons", "Valence electrons", "The outer-shell electrons that do the bonding.", []),
    ("octet-rule", "Octet rule tendency", "Atoms reaching toward a filled outer shell of eight electrons.", []),
    ("electronegativity", "Electronegativity difference", "How much harder one atom pulls shared electrons than the other.", []),
    ("bond-polarity", "Bond polarity", "A shared pair pulled closer to one atom, making bond ends charged.", []),
    ("polar-molecule", "Polar molecule", "A molecule whose charge pulls do not cancel, leaving sticky ends.", []),
    ("hydrogen-bonding", "Hydrogen bonding between molecules", "A strong attraction between a hydrogen-plus-O-N-F end and a lone pair.", []),
    ("intermolecular-forces", "Intermolecular forces", "The attractions between neighbouring molecules.", []),
    ("boiling-point", "Boiling point of a liquid", "The temperature where molecules escape the liquid bulk as vapour.", []),
    ("states-of-matter", "States of matter changes", "Melting, freezing, boiling and condensing between solid, liquid and gas.", []),
    ("chemical-reaction", "Chemical reaction", "Bonds rearranging into new substances.", []),
    ("conservation-of-mass", "Conservation of mass", "No atoms are created or destroyed in a reaction.", []),
    ("balanced-equation", "Balanced equation", "A reaction recipe with equal atom counts on both sides.", []),
    ("mole-ratio", "Mole ratios in an equation", "The fixed proportions coefficients give ingredients and products.", []),
    ("limiting-reagent", "Limiting reagent", "The ingredient that runs out first and caps the yield.", []),
    ("exothermic", "Exothermic reaction", "A reaction releasing energy as it runs.", []),
    ("endothermic", "Endothermic reaction", "A reaction absorbing energy as it runs.", []),
    ("activation-energy", "Activation energy barrier", "The energy hump reactants must clear to react.", []),
    ("catalyst-rate", "Catalyst speeding a reaction", "An additive that offers a lower-energy path without being consumed.", []),
    ("dynamic-equilibrium", "Dynamic equilibrium", "Forward and backward reactions matching so amounts freeze.", []),
    ("le-chatelier", "Le Chatelier shift", "An equilibrium pushed to relieve an applied stress.", []),
    ("acid-definition", "Acid as proton donor", "A substance releasing hydrogen ions in water.", []),
    ("base-definition", "Base as proton acceptor", "A substance taking up hydrogen ions in water.", []),
    ("ph-scale", "pH scale", "The hydrogen-ion yardstick from strong acid to strong base.", []),
    ("neutralization", "Neutralization reaction", "An acid and a base making salt and water.", []),
    ("oxidation", "Oxidation losing electrons", "A species giving electrons away in a reaction.", []),
    ("reduction", "Reduction gaining electrons", "A species taking electrons in a reaction.", []),
    ("redox-pairing", "Redox pairing", "Oxidation and reduction always travelling together.", []),
    ("combustion-reaction", "Combustion reaction", "Rapid combination of fuel with oxygen releasing heat and light.", []),
    ("dissolving", "Dissolving a solute", "A solvent pulling a substance apart into a uniform mix.", []),
    ("solubility-temperature", "Solubility shift with temperature", "How much dissolves changing as temperature changes.", []),
    ("precipitate-formation", "Precipitate formation", "Dissolved ions suddenly forming an insoluble solid.", []),
    ("concentration", "Concentration of a solution", "How much solute sits in a given amount of solvent.", []),
]

RELATIONS = [
    ("valence-causes-bond", "valence-electrons", "chemical-bond", "causes", "The pairing drive of valence electrons causes a chemical bond to form.", "outer shells are not full", ""),
    ("octet-enables-covalent", "octet-rule", "covalent-bond", "enables", "The octet rule tendency enables covalent bond sharing to fill outer shells.", "both atoms need electrons", ""),
    ("transfer-causes-ionic", "electronegativity", "ionic-bond", "causes", "A large electronegativity difference causes an ionic bond by full electron transfer.", "one atom pulls far harder than the other", ""),
    ("moderate-causes-polarity", "electronegativity", "bond-polarity", "causes", "A moderate electronegativity difference causes bond polarity by unequal sharing.", "the difference is neither tiny nor extreme", ""),
    ("polarity-causes-polar-molecule", "bond-polarity", "polar-molecule", "causes", "Unbalanced bond polarity causes a polar molecule.", "the pulls do not cancel in space", ""),
    ("polar-enables-hbond", "polar-molecule", "hydrogen-bonding", "enables", "A polar molecule with hydrogen enables hydrogen bonding between molecules.", "hydrogen bonds to nitrogen, oxygen or fluorine", ""),
    ("hbond-causes-boiling", "hydrogen-bonding", "boiling-point", "causes", "Strong hydrogen bonding between molecules causes a high boiling point of a liquid.", "the liquid has O-H or N-H bonds", ""),
    ("imf-causes-boiling", "intermolecular-forces", "boiling-point", "causes", "The strength of intermolecular forces causes a high boiling point of a liquid.", "the molecules attract strongly", ""),
    ("imf-enables-states", "intermolecular-forces", "states-of-matter", "enables", "The balance of intermolecular forces enables states of matter changes at fixed temperatures.", "heat is added or removed steadily", ""),
    ("reaction-causes-bonds", "chemical-reaction", "chemical-bond", "causes", "A chemical reaction causes chemical bond rearrangement into new substances.", "activation conditions are met", ""),
    ("conservation-enables-balancing", "conservation-of-mass", "balanced-equation", "enables", "Conservation of mass enables a balanced equation with equal atoms each side.", "every element is counted", ""),
    ("balanced-enables-moleratio", "balanced-equation", "mole-ratio", "enables", "A balanced equation enables the mole ratios in an equation to be read off its coefficients.", "coefficients are whole numbers", ""),
    ("moleratio-predicts-limiting", "mole-ratio", "limiting-reagent", "predicts", "Each of the mole ratios in an equation predicts which limiting reagent runs out first.", "starting amounts are known", ""),
    ("limiting-predicts-yield", "limiting-reagent", "chemical-reaction", "predicts", "The limiting reagent predicts the chemical reaction product amount.", "the reaction runs to completion", ""),
    ("exothermic-warms", "exothermic", "chemical-reaction", "causes", "An exothermic reaction causes the chemical reaction surroundings to warm.", "bonds formed hold more energy than bonds broken", ""),
    ("endothermic-cools", "endothermic", "chemical-reaction", "causes", "An endothermic reaction causes the chemical reaction surroundings to cool.", "bond breaking outweighs bond forming energy", ""),
    ("activation-inhibits-rate", "activation-energy", "chemical-reaction", "inhibits", "A high activation energy barrier inhibits the chemical reaction rate.", "few collisions carry enough energy", ""),
    ("catalyst-lowers-barrier", "catalyst-rate", "activation-energy", "inhibits", "A catalyst speeding a reaction inhibits the activation energy barrier by offering a new path.", "the catalyst surface or template participates", ""),
    ("equilibrium-inhibits-net", "dynamic-equilibrium", "chemical-reaction", "inhibits", "Reaching dynamic equilibrium inhibits net chemical reaction change though both directions continue.", "forward and backward rates match", ""),
    ("lechatelier-shifts", "le-chatelier", "dynamic-equilibrium", "causes", "The Le Chatelier shift causes dynamic equilibrium to move against an added stress.", "concentration, pressure or temperature changes", ""),
    ("acid-lowers-ph", "acid-definition", "ph-scale", "causes", "The acid as proton donor releasing hydrogen ions causes the pH scale value to fall.", "the acid dissolves in water", ""),
    ("base-raises-ph", "base-definition", "ph-scale", "causes", "The base as proton acceptor removing hydrogen ions causes the pH scale value to rise.", "the base dissolves in water", ""),
    ("ph-predicts-concentration", "ph-scale", "concentration", "predicts", "Each pH scale step predicts a tenfold jump in the concentration of a solution's hydrogen ions.", "the solution is aqueous", ""),
    ("neutralization-centers-ph", "neutralization", "ph-scale", "causes", "A matched neutralization reaction causes the pH scale reading to approach seven.", "acid and base amounts balance", ""),
    ("neutralization-forms-salt", "neutralization", "chemical-reaction", "causes", "A neutralization reaction causes the chemical reaction products salt and water.", "a strong acid meets a strong base", ""),
    ("oxidation-pairs-reduction", "oxidation", "reduction", "prerequisite", "Every oxidation losing electrons step is a prerequisite for a reduction gaining electrons partner.", "electrons transfer between species", ""),
    ("redox-enables-transfer", "redox-pairing", "chemical-reaction", "enables", "Redox pairing enables electron-transfer chemical reaction types.", "one species is easily reduced", ""),
    ("combustion-causes-oxidation", "combustion-reaction", "oxidation", "causes", "A rapid combustion reaction causes oxidation losing electrons to oxygen.", "oxygen is plentiful and fuel vaporises", ""),
    ("dissolving-enables-concentration", "dissolving", "concentration", "enables", "Dissolving a solute enables the concentration of a solution to be set by amount per volume.", "the solvent pulls the solute apart", ""),
    ("temperature-causes-solubility", "solubility-temperature", "dissolving", "causes", "A solubility shift with temperature causes dissolving a solute to increase for most solids.", "the solid dissolves endothermically", ""),
    ("concentration-causes-precipitate", "concentration", "precipitate-formation", "causes", "Passing the saturation concentration of a solution causes precipitate formation of the excess solid.", "ions collide faster than they redissolve", ""),
    ("ionic-enables-dissolving", "ionic-bond", "dissolving", "enables", "Polar water attacking an ionic bond enables dissolving a solute into ions.", "water molecules surround the ions", ""),
    ("covalent-inhibits-dissolving", "covalent-bond", "dissolving", "inhibits", "A giant covalent bond network inhibits dissolving a solute in water.", "the solid is diamond or quartz like", ""),
    ("polar-enables-dissolving-polar", "polar-molecule", "dissolving", "enables", "A polar molecule solvent enables dissolving a solute that is also polar.", "like dissolves like pairing holds", ""),
    ("exothermic-fuels-later-steps", "exothermic", "activation-energy", "enables", "Heat released by an exothermic reaction enables the activation energy barrier of later steps to be cleared.", "the heat stays in the mixture", ""),
    ("activation-prereq-reaction", "activation-energy", "chemical-reaction", "prerequisite", "Clearing the activation energy barrier is a prerequisite for a chemical reaction to proceed.", "collisions are energetic enough", ""),
    ("equilibrium-prereq-lechatelier", "dynamic-equilibrium", "le-chatelier", "prerequisite", "An established dynamic equilibrium is a prerequisite for a Le Chatelier shift to occur.", "the system is closed", ""),
    ("balanced-prereq-limiting", "balanced-equation", "limiting-reagent", "prerequisite", "A balanced equation is a prerequisite for limiting reagent reasoning.", "amounts are given in moles", ""),
    ("imf-prereq-states", "intermolecular-forces", "states-of-matter", "prerequisite", "The pull of intermolecular forces is a prerequisite for states of matter changes to happen at set temperatures.", "molecules attract at all", ""),
    ("combustion-causes-exothermic", "combustion-reaction", "exothermic", "causes", "A combustion reaction causes an exothermic reaction releasing heat and light.", "fuel and oxygen mix well", ""),
    ("dissolving-enables-rate", "dissolving", "chemical-reaction", "enables", "Dissolving a solute enables a faster chemical reaction by mixing particles freely.", "the reaction happens in solution", ""),
]

MYTHS = [
    ("bond-energy-released-always", "Breaking bonds releases energy",
     "Energy is released when stronger bonds form; breaking bonds always costs energy.", "exothermic"),
    ("catalyst-adds-energy", "A catalyst adds energy to a reaction",
     "A catalyst lowers the barrier; it supplies no energy and is not consumed.", "catalyst-rate"),
    ("ph-linear", "pH differences are step-for-step",
     "The pH scale is logarithmic, so each unit is a tenfold concentration jump.", "ph-scale"),
    ("neutral-always-seven", "Neutralising always lands on seven",
     "Weak acid-base pairs leave the product above or below seven.", "neutralization"),
    ("water-conducts", "Pure water conducts well",
     "Only ions carry current; pure water conducts very poorly.", "ionic-bond"),
]

BOUNDARIES = [
    ("rate-vs-yield", "Catalysts change speed, not yield",
     "A catalyst speeds both directions equally and leaves equilibrium amounts untouched.", "catalyst-rate"),
    ("strong-vs-weak", "Strong and weak mean ionisation, not concentration",
     "Strength is how far the acid as proton donor ionises, independent of dilution.", "acid-definition"),
    ("solubility-limits", "Dissolving has a ceiling",
     "Past saturation, extra solute stays solid regardless of stirring.", "dissolving"),
]

EXAMPLES = [
    ("ice-melting", "Ice melting in a drink",
     "Melting is states of matter changes driven by heat overcoming intermolecular forces.",
     ["states-of-matter", "intermolecular-forces", "boiling-point"]),
    ("baking-soda-vinegar", "Baking soda meets vinegar",
     "An acid as proton donor hits a base, and the fizzing neutralization reaction releases carbon dioxide.",
     ["acid-definition", "base-definition", "neutralization"]),
    ("iron-rusting", "Iron rusting in damp air",
     "Rusting is slow oxidation losing electrons to oxygen, limited by the activation energy barrier.",
     ["oxidation", "redox-pairing", "activation-energy"]),
    ("sweetening-tea", "Sweetening hot versus cold tea",
     "Hot tea dissolves more sugar because the solubility shift with temperature favours solids.",
     ["solubility-temperature", "dissolving", "concentration"]),
]

CONTROLS = [
    ("catalyst-consumed", "A catalyst is used up",
     "A catalyst speeding a reaction must not be treated as consumed by it."),
    ("ph-seven-deadly", "pH seven is dangerous",
     "A middle pH scale value must not be treated as hazardous by itself."),
    ("ions-appear", "Reactions create new atoms",
     "A chemical reaction must not be treated as creating or destroying atoms."),
    ("all-dissolves", "Everything dissolves given time",
     "Giant covalent bond networks must not be treated as dissolving in water."),
]
