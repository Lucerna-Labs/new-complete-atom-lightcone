"""Cell and molecular biology causation: membranes, enzymes, DNA, protein synthesis, division."""

WORLD = "biology-causation-v0"
PREFIX = "bioc"
DOMAIN = "biology"
SUBJECT = "biology.cell"
SOURCES = ["ncbi-molecular-cell", "nhgri-genomics-facts"]
SCOPE = "Everyday cell and molecular biology: membranes and transport, enzymes, DNA to protein, energy pathways, cell division, heredity"
ROOT_LABEL = "Biology causation world"
ROOT_STATEMENT = "Root of the biology causation world: how membranes, enzymes, genes and energy pathways cause cells to live, divide and pass on traits."

CONCEPTS = [
    ("cell-membrane", "Cell membrane barrier", "A lipid bilayer and associated proteins separating the cell interior from its surroundings.", []),
    ("selective-permeability", "Selective permeability", "Different permeabilities to different solutes arising from lipid properties and selective transport proteins.", []),
    ("diffusion", "Diffusion down a gradient", "Net passive movement down a chemical or electrochemical potential gradient through random molecular motion.", []),
    ("osmosis", "Osmosis of water", "Net water movement through a selectively permeable membrane toward higher effective solute concentration when hydrostatic pressure does not oppose it.", []),
    ("facilitated-transport", "Facilitated transport", "Passive movement through a membrane channel or carrier down the transported species' electrochemical gradient.", []),
    ("active-transport", "Active transport pumping", "Energy-coupled transport of a solute against its electrochemical gradient, directly or through another gradient.", []),
    ("atp-energy", "ATP energy currency", "ATP serving as a chemical energy carrier whose hydrolysis can be coupled to otherwise unfavourable cellular processes.", []),
    ("enzyme-catalysis", "Enzyme substrate catalysis", "Enzymatic acceleration of a reaction through substrate interactions and transition-state stabilization without net enzyme consumption.", []),
    ("activation-lowering", "Activation barrier lowering", "A reduction in the activation free-energy barrier of an accessible reaction pathway.", []),
    ("enzyme-denaturation", "Enzyme denaturation", "Loss of an enzyme's native conformation through conditions such as heat, extreme pH or chemical denaturants.", []),
    ("ph-effect", "pH effect on proteins", "Changes in protein protonation, interactions and conformation as hydrogen-ion activity changes.", []),
    ("dna-helix", "DNA double helix", "Two antiparallel DNA strands arranged in a helix stabilized by base stacking and complementary base pairing.", []),
    ("base-pairing", "Complementary base pairing", "Specific pairing of nucleobases, including A-T and G-C in DNA and A-U and G-C during RNA synthesis.", []),
    ("replication", "Semi-conservative replication", "DNA replication producing two duplexes, each containing one parental strand and one newly synthesized strand.", []),
    ("transcription", "Transcription to mRNA", "RNA-polymerase synthesis of messenger RNA complementary to a protein-coding DNA template strand.", []),
    ("translation", "Translation at ribosomes", "Ribosomal decoding of messenger RNA using charged tRNAs to synthesize a polypeptide.", []),
    ("codon-triplet", "Codon triplet code", "Nonoverlapping three-nucleotide mRNA units specifying amino acids or translation termination in a reading frame.", []),
    ("genetic-code-redundant", "Redundant genetic code", "The mapping of more than one codon to the same amino acid in a specified genetic code.", []),
    ("mutation", "Mutation of DNA", "A change in DNA nucleotide sequence that can be propagated during subsequent replication.", []),
    ("protein-folding", "Protein folding into shape", "Adoption of a polypeptide conformation through intramolecular interactions, sometimes assisted by chaperones.", []),
    ("structure-function", "Protein molecular function", "A protein's molecular activity supported by its sequence, conformation, interactions and chemical environment.", []),
    ("respiration", "Cellular respiration", "Oxidation of substrates coupled to electron transfer to a terminal acceptor and ATP production.", []),
    ("glucose-breakdown", "Glucose energy release", "Net free-energy release during coupled glucose oxidation, rather than energy release from bond breaking alone.", []),
    ("photosynthesis", "Photosynthesis capture", "Light-driven reactions supplying energy and reducing power for carbon fixation into organic compounds in photosynthetic organisms.", []),
    ("mitosis", "Mitosis division", "Eukaryotic nuclear division segregating replicated chromosomes into daughter nuclei, distinct from DNA replication and cytokinesis.", []),
    ("meiosis", "Meiosis halving", "A reductional division programme yielding haploid products from a diploid precursor after one replication and two divisions.", []),
    ("fertilization", "Fertilization restoring", "Fusion of gametes and their genomes; two haploid gametes restore diploidy.", []),
    ("dominant-recessive", "Dominant and recessive alleles", "Alleles whose heterozygous phenotype matches the dominant homozygote under a specified complete-dominance relationship.", []),
    ("genotype-phenotype", "Phenotypic trait expression", "Observable traits produced by genetic variants interacting with gene expression, development and environment.", []),
    ("gene-expression", "Gene expression control", "Regulation of the production, processing and lifetime of functional gene products.", []),
    ("membrane-receptors", "Membrane receptor signalling", "Transduction of an extracellular input through a plasma-membrane receptor to intracellular effectors.", []),
    ("glucose", "Glucose sugar", "A six-carbon monosaccharide that can be oxidized for cellular energy or incorporated into larger carbohydrates.", []),
    ("protein-sequence-change", "Protein sequence change", "A change in the amino acid sequence of an expressed protein.", []),
    ("template-exposure", "DNA template exposure", "Local separation of duplex DNA strands so RNA polymerase can access the template in a transcription bubble.", []),
    ("base-mismatch", "DNA base mismatch", "A noncomplementary base pair introduced into a DNA duplex, for example during replication.", []),
    ("osmotic-gradient", "Osmotic solute gradient", "A difference in effective concentration of membrane-impermeant solutes across a water-permeable membrane.", []),
    ("inner-mitochondrial-membrane", "Inner mitochondrial membrane", "The mitochondrial membrane carrying the respiratory electron transport chain and ATP synthase while restricting proton leakage.", []),
    ("oxidative-phosphorylation", "Mitochondrial oxidative phosphorylation", "ATP synthesis coupled to an electrochemical proton gradient generated by mitochondrial electron transport.", []),
]

RELATIONS = [
    ("membrane-enables-permeability", "cell-membrane", "selective-permeability", "enables", "The cell membrane barrier enables selective permeability through its lipid bilayer and transport proteins.", "an intact lipid bilayer contains selective channels or carriers and lacks a nonspecific membrane rupture", ""),
    ("membrane-prereq-osmosis", "cell-membrane", "osmosis", "prerequisite", "The cell membrane barrier is a prerequisite for osmosis of water between the cytoplasm and extracellular fluid.", "the process under discussion is trans-plasma-membrane osmosis, with water permeant and the relevant solute effectively impermeant", ""),
    ("facilitated-enables-diffusion", "facilitated-transport", "diffusion", "enables", "Facilitated transport enables diffusion down a gradient across a membrane otherwise poorly permeable to the solute.", "a matching passive channel or carrier is present and the solute has a favourable electrochemical gradient", ""),
    ("respiration-refills-atp", "respiration", "atp-energy", "causes", "Cellular respiration causes ATP energy currency replenishment, most efficiently with oxygen for ordinary aerobic glucose metabolism.", "a eukaryotic cell oxidizes available substrate with oxygen as terminal electron acceptor and has coupled ATP synthesis, ADP and phosphate", ""),
    ("glucose-enables-respiration", "glucose", "respiration", "enables", "Glucose sugar enables cellular respiration by supplying oxidizable carbon and electrons.", "the cell has active glucose-catabolic enzymes, required cofactors and an available terminal electron acceptor", ""),
    ("photosynthesis-transforms-fuel", "photosynthesis", "glucose", "enables", "Photosynthesis capture enables glucose sugar synthesis from carbon dioxide and water using absorbed light energy.", "oxygenic plant photosynthesis supplies ATP and NADPH for carbon fixation, and downstream carbohydrate synthesis converts fixed-carbon intermediates into hexoses", ""),
    ("enzyme-causes-lowering", "enzyme-catalysis", "activation-lowering", "causes", "Enzyme substrate catalysis causes activation barrier lowering by stabilizing an accessible reaction pathway.", "an active enzyme binds its substrate and supports the transition state under its specified solution conditions", ""),
    ("denaturation-inhibits-catalysis", "enzyme-denaturation", "enzyme-catalysis", "inhibits", "Enzyme denaturation inhibits enzyme substrate catalysis by disrupting the catalytically active conformation.", "unfolding or structural disruption affects an enzyme whose active site requires the lost native fold", ""),
    ("ph-inhibits-catalysis", "ph-effect", "enzyme-catalysis", "inhibits", "The pH effect on proteins inhibits enzyme substrate catalysis when catalytic groups acquire unsuitable protonation states.", "pH moves away from the activity range of the specified enzyme and changes a group required for substrate binding or catalysis", ""),
    ("ph-causes-denaturation", "ph-effect", "enzyme-denaturation", "enables", "The pH effect on proteins enables enzyme denaturation by disrupting interactions that stabilize the fold.", "a pH change destabilizes a pH-sensitive enzyme sufficiently that its folded population decreases under the exposure conditions", ""),
    ("helix-enables-pairing", "base-pairing", "dna-helix", "enables", "Complementary base pairing enables DNA double helix assembly together with base stacking.", "complementary antiparallel DNA strands encounter one another in solution below their duplex melting temperature", ""),
    ("pairing-enables-replication", "base-pairing", "replication", "enables", "Complementary base pairing enables semi-conservative replication by selecting nucleotides against a DNA template.", "DNA polymerase has a template, a primed terminus, nucleotide substrates and the required replication machinery", ""),
    ("mismatch-causes-mutation", "base-mismatch", "mutation", "enables", "A DNA base mismatch enables mutation of DNA when the mismatched nucleotide is copied into a stable sequence change.", "the mismatch escapes proofreading and repair and a subsequent replication or repair event fixes the altered sequence in a descendant duplex", ""),
    ("replication-prereq-mitosis", "replication", "mitosis", "prerequisite", "Semi-conservative replication is a prerequisite for mitosis division that segregates a complete replicated chromosome set to each daughter nucleus.", "a diploid eukaryotic cell follows a chromosome-conserving mitotic cycle rather than an experimentally checkpoint-bypassed or pathological division", ""),
    ("transcription-uses-pairing", "base-pairing", "transcription", "enables", "Complementary base pairing enables transcription to mRNA by selecting RNA nucleotides against the DNA template.", "RNA polymerase transcribes a protein-coding DNA template with available ribonucleotides, pairing RNA U with DNA A", ""),
    ("translation-enables-codons", "codon-triplet", "translation", "enables", "The codon triplet code enables translation at ribosomes to read mRNA three bases at a time into a polypeptide.", "a ribosome uses the cellular genetic code in an established reading frame with charged tRNAs and termination factors", ""),
    ("redundancy-buffers-mutation", "genetic-code-redundant", "protein-sequence-change", "prevents", "The redundant genetic code prevents protein sequence change for a synonymous point mutation.", "the altered coding codon specifies the same amino acid in the applicable genetic code and does not alter splicing or the reading frame", ""),
    ("mutation-causes-folding-change", "mutation", "protein-folding", "enables", "Mutation of DNA enables altered protein folding into shape through an amino acid substitution.", "the expressed coding mutation changes a structurally important amino acid in a folding-dependent protein", ""),
    ("folding-enables-function", "protein-folding", "structure-function", "enables", "Protein folding into shape enables protein molecular function by arranging required interaction and catalytic groups.", "the specified protein requires the resulting folded conformation and has its required partners and cofactors", ""),
    ("denaturation-inhibits-function", "enzyme-denaturation", "structure-function", "inhibits", "Enzyme denaturation inhibits protein molecular function by disrupting a conformation required for activity.", "the enzyme remains denatured during the assay and its measured activity depends on the lost fold", ""),
    ("meiosis-prereq-fertilization", "meiosis", "fertilization", "enables", "Meiosis halving enables fertilization restoring a diploid chromosome count by producing haploid gametes.", "a diploid animal's conventional sexual life cycle produces functional haploid gametes that subsequently fuse", ""),
    ("fertilization-enables-alleles", "fertilization", "dominant-recessive", "enables", "Fertilization restoring diploidy enables dominant and recessive alleles to coexist in a heterozygous zygote.", "two haploid gametes carry different alleles of an autosomal locus exhibiting complete dominance", ""),
    ("alleles-predict-phenotype", "dominant-recessive", "genotype-phenotype", "predicts", "The combination of dominant and recessive alleles predicts phenotypic trait expression from the genotype under complete dominance.", "one autosomal locus has complete penetrance without relevant epistasis or environmental modification in the population being modelled", ""),
    ("expression-prereq-phenotype", "gene-expression", "genotype-phenotype", "enables", "Gene expression control enables changes in phenotypic trait expression by altering gene-product abundance.", "the measured trait responds to expression of the regulated gene in the specified cell type and developmental setting", ""),
    ("receptors-prereq-membrane", "cell-membrane", "membrane-receptors", "prerequisite", "The cell membrane barrier is a prerequisite for membrane receptor signalling across the plasma membrane.", "the receptor's signalling mechanism requires its transmembrane orientation and intact intracellular and extracellular compartments", ""),
    ("receptors-enable-expression", "membrane-receptors", "gene-expression", "enables", "Membrane receptor signalling enables gene expression control through a linked intracellular regulatory pathway.", "ligand activation reaches a functional pathway that modifies a transcription regulator in the receiving cell", ""),
    ("gradient-causes-osmosis", "osmotic-gradient", "osmosis", "causes", "An osmotic solute gradient causes osmosis of water toward the higher effective solute concentration.", "the membrane passes water but not the gradient-forming solute, temperatures are equal and no opposing hydrostatic pressure cancels the water chemical-potential difference", ""),
    ("atp-enables-pumping", "atp-energy", "active-transport", "enables", "ATP energy currency enables active transport pumping when ATP hydrolysis is coupled to solute transport.", "a functional primary ATP-driven pump has ATP and a hydrolysis free-energy release sufficient to overcome the cargo's electrochemical gradient", ""),
    ("atp-prereq-translation", "atp-energy", "translation", "prerequisite", "ATP energy currency is a prerequisite for translation at ribosomes sustained by aminoacyl-tRNA charging from free amino acids.", "the cellular translation cycle uses ATP-dependent aminoacyl-tRNA synthetases and must replenish charged tRNAs, while ribosomal steps also consume GTP", ""),
    ("transcription-prereq-translation", "transcription", "translation", "prerequisite", "Transcription to mRNA is a prerequisite for translation at ribosomes of a nuclear protein-coding gene.", "a eukaryotic gene is expressed by nuclear transcription, RNA processing and export before its mRNA is translated in the cytoplasm", ""),
    ("helix-prereq-transcription", "template-exposure", "transcription", "prerequisite", "DNA template exposure is a prerequisite for transcription to mRNA from duplex DNA.", "DNA-dependent RNA polymerase must expose a template strand in a transcription bubble of a double-stranded cellular gene", ""),
    ("meiosis-enables-new-combos", "meiosis", "dominant-recessive", "enables", "Meiosis halving enables new combinations of dominant and recessive alleles through segregation and recombination.", "a diploid parent is heterozygous at multiple loci and independent assortment or crossing-over changes the transmitted allele combinations", ""),
    ("enzymes-enable-respiration", "enzyme-catalysis", "respiration", "enables", "Enzyme substrate catalysis enables cellular respiration to proceed at cellular temperatures.", "the required catabolic enzymes, substrates, electron carriers and acceptor are available in their functional compartments", ""),
    ("respiration-enables-pumping", "respiration", "active-transport", "enables", "Cellular respiration enables active transport pumping by supplying usable chemical energy.", "respiratory ATP production supplies a functional ATP-driven membrane pump with enough free energy to move its cargo against its gradient", ""),
    ("membrane-prereq-respiration", "inner-mitochondrial-membrane", "oxidative-phosphorylation", "prerequisite", "The inner mitochondrial membrane is a prerequisite for mitochondrial oxidative phosphorylation by sustaining its proton electrochemical gradient.", "an intact mitochondrion generates ATP through a coupled respiratory chain and ATP synthase across its inner membrane", ""),
]

MYTHS = [
    ("one-gene-one-trait", "Single genes control single traits",
     "Most traits flow from many genes plus environment through genetic and developmental processes.", "genotype-phenotype"),
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
     "Water entry in a sufficiently hypotonic environment can lyse an animal cell; cell walls, solute regulation and opposing hydrostatic pressure can limit swelling.", "osmosis"),
    ("expression-context", "Genes need cellular context",
     "Gene expression control depends on cell type and signals, not DNA alone.", "gene-expression"),
    ("synonymous-not-effectless", "Synonymous does not mean effectless",
     "A synonymous substitution preserves the encoded amino acid at that codon but can affect splicing, RNA stability or translation kinetics.", "genetic-code-redundant"),
]

EXAMPLES = [
    ("oxygen-lungs", "Oxygen crossing the lungs",
     "Small nonpolar gases cross by diffusion down a gradient straight into blood.",
     ["diffusion", "selective-permeability", "cell-membrane"]),
    ("lactase-dairy", "Lactase and dairy",
     "Lactase hydrolyses lactose in the small intestine; insufficient lactase leaves more lactose available for bacterial fermentation in the colon.",
     ["enzyme-catalysis", "activation-lowering"]),
    ("sickle-one-letter", "One letter, sickled cells",
     "The sickle-cell beta-globin substitution changes one amino acid; deoxygenated haemoglobin S can polymerise, distorting red-cell shape.",
     ["mutation", "protein-sequence-change", "structure-function"]),
    ("family-resemblance", "Family resemblance",
     "Meiosis halving and fertilization restoring reshuffle dominant and recessive alleles each generation.",
     ["meiosis", "fertilization", "dominant-recessive"]),
]

CONTROLS = [
    ("water-uncontrolled", "Water crosses without any control",
     "Osmosis of water must not be treated as unregulated flooding."),
    ("enzymes-destroy", "Catalysis consumes the enzyme",
     "Enzyme substrate catalysis must not be treated as consuming the enzyme itself; substrates can be consumed and converted into products."),
    ("learning-edits-dna", "Learned skills edit DNA",
     "Gene expression control must not be treated as rewriting the genome sequence."),
    ("photosynthesis-dark", "Photosynthesis runs in the dark",
     "Sustained oxygenic photosynthesis capture must not be treated as independent of light merely because carbon fixation is called a dark reaction."),
]
