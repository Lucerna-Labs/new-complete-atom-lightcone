"""Cell and molecular biology causation: membranes, enzymes, DNA, protein synthesis, division."""

WORLD = "biology-causation-v0"
PREFIX = "bio"
DOMAIN = "biology"
SUBJECT = "biology.cell"
SOURCES = ["ncbi-molecular-cell", "nhgri-genomics-facts"]
SCOPE = "Everyday cell and molecular biology: membranes and transport, enzymes, DNA to protein, energy pathways, cell division, heredity"
ROOT_LABEL = "Biology causation world"
ROOT_STATEMENT = "Root of the biology causation world: how membranes, enzymes, genes and energy pathways cause cells to live, divide and pass on traits."

CONCEPTS = [
    ("cell-membrane", "Cell membrane barrier", "The fatty double-layered sheet controlling what enters and leaves a cell.", []),
    ("selective-permeability", "Selective permeability", "The membrane letting some molecules through and holding others back.", []),
    ("diffusion", "Diffusion down a gradient", "Molecules spreading from crowded to sparse without energy input.", []),
    ("osmosis", "Osmosis of water", "Water crossing toward the more concentrated side.", []),
    ("facilitated-transport", "Facilitated transport", "Channels and carriers helping specific molecules across.", []),
    ("active-transport", "Active transport pumping", "Spending energy to move cargo against its gradient.", []),
    ("atp-energy", "ATP energy currency", "The cell's spendable energy coin.", []),
    ("enzyme-catalysis", "Enzyme substrate catalysis", "An enzyme speeding one reaction by holding its substrate right.", []),
    ("activation-lowering", "Activation barrier lowering", "Catalysis shaving the energy hill reactants must climb.", []),
    ("enzyme-denaturation", "Enzyme denaturation", "Heat or pH wrecking an enzyme's working shape.", []),
    ("ph-effect", "pH effect on proteins", "Acidity shifting protein charge and shape.", []),
    ("dna-helix", "DNA double helix", "Two strands of paired letters storing heredity.", []),
    ("base-pairing", "Complementary base pairing", "A pairing with T, C pairing with G, strand to strand.", []),
    ("replication", "Semi-conservative replication", "Each strand templating a new partner before division.", []),
    ("transcription", "Transcription to mRNA", "Copying a gene's letters into a messenger strand.", []),
    ("translation", "Translation at ribosomes", "Reading messenger codons into an amino acid chain.", []),
    ("codon-triplet", "Codon triplet code", "Three letters naming one amino acid.", []),
    ("genetic-code-redundant", "Redundant genetic code", "Several codons often naming the same amino acid.", []),
    ("mutation", "Mutation of DNA", "A lasting change in the letter sequence.", []),
    ("protein-folding", "Protein folding into shape", "A new chain curling into its working form.", []),
    ("structure-function", "Structure determines function", "A protein's job flowing from its shape.", []),
    ("respiration", "Cellular respiration", "Stepwise harvesting of food energy into ATP.", []),
    ("glucose-breakdown", "Glucose energy release", "Unlocking the energy stored in sugar bonds.", []),
    ("photosynthesis", "Photosynthesis capture", "Light energy packed into sugar inside chloroplasts.", []),
    ("mitosis", "Mitosis division", "One cell copying itself into two identical cells.", []),
    ("meiosis", "Meiosis halving", "Making gametes with half the chromosome number.", []),
    ("fertilization", "Fertilization restoring", "Two gametes uniting to restore the full set.", []),
    ("dominant-recessive", "Dominant and recessive alleles", "Versions of a gene where one can mask the other.", []),
    ("genotype-phenotype", "Genotype to phenotype", "The letter code unfolding into visible traits.", []),
    ("gene-expression", "Gene expression control", "Switching genes on and off per cell and moment.", []),
    ("membrane-receptors", "Membrane receptor signalling", "Surface proteins catching signals and passing them inward.", []),
]

RELATIONS = [
    ("membrane-enables-permeability", "cell-membrane", "selective-permeability", "enables", "The cell membrane barrier enables selective permeability by gating what crosses.", "embedded proteins control passage", ""),
    ("diffusion-prevents-pumping", "diffusion", "active-transport", "prevents", "Diffusion down a gradient prevents the need for active transport pumping.", "molecules move from crowded to sparse", ""),
    ("membrane-prereq-osmosis", "cell-membrane", "osmosis", "prerequisite", "A semi-permeable cell membrane barrier is a prerequisite for osmosis of water.", "solutes cannot cross but water can", ""),
    ("facilitated-enables-diffusion", "facilitated-transport", "diffusion", "enables", "Facilitated transport enables diffusion down a gradient for molecules too large or polar to slip through.", "channels or carriers match the solute", ""),
    ("atp-prereq-pumping", "atp-energy", "active-transport", "prerequisite", "ATP energy currency spending is a prerequisite for active transport pumping against the gradient.", "the cargo must accumulate", ""),
    ("respiration-refills-atp", "respiration", "atp-energy", "causes", "Running cellular respiration causes ATP energy currency stocks to refill.", "oxygen is available", ""),
    ("glucose-enables-respiration", "glucose-breakdown", "respiration", "enables", "Stepwise glucose energy release enables cellular respiration to squeeze out ATP.", "the cell takes in glucose", ""),
    ("photosynthesis-transforms-fuel", "photosynthesis", "glucose-breakdown", "transforms_to", "Photosynthesis capture of light transforms into glucose energy release fuel for cells.", "sunlight reaches chloroplasts", ""),
    ("enzyme-causes-lowering", "enzyme-catalysis", "activation-lowering", "causes", "Enzyme substrate catalysis causes activation barrier lowering for its specific substrate.", "the substrate fits the active site", ""),
    ("denaturation-inhibits-catalysis", "enzyme-denaturation", "enzyme-catalysis", "inhibits", "Heat driven enzyme denaturation inhibits enzyme substrate catalysis by reshaping the site.", "temperature passes the protein's tolerance", ""),
    ("ph-inhibits-catalysis", "ph-effect", "enzyme-catalysis", "inhibits", "An extreme pH effect on proteins inhibits enzyme substrate catalysis by charging the site.", "pH leaves the working range", ""),
    ("ph-causes-denaturation", "ph-effect", "enzyme-denaturation", "causes", "A severe pH effect on proteins causes enzyme denaturation of folded structure.", "the pH shift is extreme", ""),
    ("helix-enables-pairing", "dna-helix", "base-pairing", "enables", "The DNA double helix enables complementary base pairing along its rungs.", "strands stay antiparallel", ""),
    ("pairing-enables-replication", "base-pairing", "replication", "enables", "Complementary base pairing enables semi-conservative replication to copy each strand.", "polymerase reads a template", ""),
    ("mismatch-causes-mutation", "base-pairing", "mutation", "causes", "A mismatch in complementary base pairing causes a mutation of DNA if uncorrected.", "proofreading misses the error", ""),
    ("replication-prereq-mitosis", "replication", "mitosis", "prerequisite", "Completed semi-conservative replication is a prerequisite for mitosis division to start.", "the cell commits to divide", ""),
    ("transcription-uses-pairing", "transcription", "base-pairing", "enables", "Transcription to mRNA enables complementary base pairing to guide the copied letters.", "RNA polymerase binds the gene", ""),
    ("translation-enables-codons", "translation", "codon-triplet", "enables", "Translation at ribosomes enables codon triplet code reading one codon at a time.", "a start codon is found", ""),
    ("codons-enable-redundancy", "codon-triplet", "genetic-code-redundant", "enables", "The codon triplet code set enables redundant genetic code synonyms for most amino acids.", "several codons name one acid", ""),
    ("redundancy-buffers-mutation", "genetic-code-redundant", "mutation", "inhibits", "A redundant genetic code synonym inhibits some mutation of DNA damage by meaning the same.", "the swap stays within a synonym group", ""),
    ("mutation-causes-folding-change", "mutation", "protein-folding", "causes", "A coding mutation of DNA causes protein folding into shape alterations.", "the change hits a coding letter", ""),
    ("folding-enables-function", "protein-folding", "structure-function", "enables", "Correct protein folding into shape enables structure determines function relationships.", "the chain reaches its native state", ""),
    ("denaturation-inhibits-function", "enzyme-denaturation", "structure-function", "inhibits", "Enzyme denaturation inhibits the structure determines function pairing by destroying shape.", "the fold cannot return", ""),
    ("meiosis-prereq-fertilization", "meiosis", "fertilization", "prerequisite", "Meiosis halving of chromosomes is a prerequisite for fertilization restoring the full set.", "gametes form before meeting", ""),
    ("fertilization-enables-alleles", "fertilization", "dominant-recessive", "enables", "Fertilization restoring of two gametes enables dominant and recessive alleles pairing.", "parents pass different alleles", ""),
    ("alleles-predict-phenotype", "dominant-recessive", "genotype-phenotype", "predicts", "The dominant and recessive alleles pair predicts genotype to phenotype outcomes in simple traits.", "one gene controls the trait", ""),
    ("expression-prereq-phenotype", "gene-expression", "genotype-phenotype", "prerequisite", "Regulated gene expression control is a prerequisite for genotype to phenotype unfolding.", "cells differ in which genes are on", ""),
    ("receptors-prereq-membrane", "membrane-receptors", "cell-membrane", "prerequisite", "An intact cell membrane barrier is a prerequisite for membrane receptor signalling.", "the receptor spans the bilayer", ""),
    ("receptors-enable-expression", "membrane-receptors", "gene-expression", "enables", "Membrane receptor signalling enables gene expression control changes in the nucleus.", "a signal molecule docks", ""),
    ("gradient-causes-osmosis", "diffusion", "osmosis", "causes", "A water concentration gradient causes diffusion down a gradient behaviour and osmosis of water across the membrane.", "water chases solutes the membrane holds back", ""),
    ("atp-enables-pumping", "atp-energy", "active-transport", "enables", "ATP energy currency enables active transport pumping against gradients.", "ATP is spent at the pump", ""),
    ("atp-prereq-translation", "atp-energy", "translation", "prerequisite", "ATP energy currency spending is a prerequisite for translation at ribosomes to run.", "amino acids are charged", ""),
    ("transcription-prereq-translation", "transcription", "translation", "prerequisite", "Finished transcription to mRNA is a prerequisite for translation at ribosomes.", "the messenger reaches the ribosome", ""),
    ("helix-prereq-transcription", "dna-helix", "transcription", "prerequisite", "An unwound DNA double helix stretch is a prerequisite for transcription to mRNA.", "the gene's promoter opens", ""),
    ("meiosis-enables-new-combos", "meiosis", "dominant-recessive", "enables", "Meiosis halving with shuffling enables new dominant and recessive alleles combinations.", "chromosomes assort independently", ""),
    ("enzymes-enable-respiration", "enzyme-catalysis", "respiration", "enables", "Enzyme substrate catalysis enables cellular respiration to run at body temperature.", "each step has its enzyme", ""),
    ("misfold-predicts-mutation", "protein-folding", "mutation", "predicts", "Broken protein folding into shape predicts a mutation of DNA in the code.", "a family shares the misfold", ""),
    ("respiration-enables-pumping", "respiration", "active-transport", "enables", "Cellular respiration output enables active transport pumping to keep running.", "ATP levels stay stocked", ""),
    ("membrane-prereq-respiration", "cell-membrane", "respiration", "prerequisite", "An intact cell membrane barrier is a prerequisite for cellular respiration gradients.", "the proton gradient must hold", ""),
    ("mitosis-predicts-copies", "mitosis", "replication", "predicts", "Faithful mitosis division predicts intact semi-conservative replication copies in each cell.", "spindles pull evenly", ""),
]

MYTHS = [
    ("one-gene-one-trait", "Single genes control single traits",
     "Most traits flow from many genes plus environment through genotype to phenotype.", "genotype-phenotype"),
    ("dominant-means-common", "Dominant alleles are the common ones",
     "Dominance describes which allele shows, not how frequent it is.", "dominant-recessive"),
    ("membrane-static-wall", "The membrane is a sealed wall",
     "The cell membrane barrier carries dynamic receptors, channels and fluid movement.", "cell-membrane"),
    ("enzymes-forever", "Enzymes never wear out",
     "Denaturation and turnover end enzyme lives; cells replace them constantly.", "enzyme-denaturation"),
    ("dna-read-once", "DNA is read once",
     "Repeated semi-conservative replication and transcription reuse the same genome.", "replication"),
]

BOUNDARIES = [
    ("multifactorial-traits", "Simple genetics covers only some traits",
     "Most common traits are multifactorial beyond single dominant and recessive alleles.", "dominant-recessive"),
    ("osmosis-limits", "Osmosis has limits in real cells",
     "Extreme osmosis of water lyses animal cells; walls and pumps resist in others.", "osmosis"),
    ("expression-context", "Genes need cellular context",
     "Gene expression control depends on cell type and signals, not DNA alone.", "gene-expression"),
]

EXAMPLES = [
    ("oxygen-lungs", "Oxygen crossing the lungs",
     "Small nonpolar gases cross by diffusion down a gradient straight into blood.",
     ["diffusion", "selective-permeability", "cell-membrane"]),
    ("lactase-dairy", "Lactase and dairy",
     "Lactase enzyme substrate catalysis breaks milk sugar; missing it leaves digestion to bacteria.",
     ["enzyme-catalysis", "activation-lowering", "enzyme-denaturation"]),
    ("sickle-one-letter", "One letter, sickled cells",
     "A single mutation of DNA changes protein folding into shape and thus red cell form.",
     ["mutation", "protein-folding", "structure-function"]),
    ("family-resemblance", "Family resemblance",
     "Meiosis halving and fertilization restoring reshuffle dominant and recessive alleles each generation.",
     ["meiosis", "fertilization", "dominant-recessive"]),
]

CONTROLS = [
    ("water-uncontrolled", "Water crosses without any control",
     "Osmosis of water must not be treated as unregulated flooding."),
    ("enzymes-destroy", "Enzymes destroy their substrates",
     "Enzyme substrate catalysis must not be treated as consuming the enzyme or substrate wholesale."),
    ("learning-edits-dna", "Learned skills edit DNA",
     "Gene expression control must not be treated as rewriting the genome sequence."),
    ("photosynthesis-dark", "Photosynthesis runs in the dark",
     "Photosynthesis capture must not be treated as running without light."),
]
