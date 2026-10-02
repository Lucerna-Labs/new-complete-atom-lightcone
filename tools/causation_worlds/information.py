"""Information theory causation: surprise, entropy, coding, noisy channels."""

WORLD = "information-causation-v0"
PREFIX = "inf"
DOMAIN = "information-communication"
SUBJECT = "information-communication.entropy-information"
SOURCES = ["nist-stat-handbook", "shannon-1948"]
SCOPE = "Everyday information theory: bits and surprise, entropy, lossless coding limits, redundancy, noisy channels, capacity"
ROOT_LABEL = "Information causation world"
ROOT_STATEMENT = "Root of the information causation world: how surprise, entropy, coding and noisy channels cause what messages can and cannot do."

CONCEPTS = [
    ("bit", "Bit of information", "The unit of information: the content of one fully uncertain two-way choice.", []),
    ("message-source", "Message source", "A sender producing symbols with fixed probabilities.", []),
    ("outcome-probability", "Outcome probability", "How likely a source is to emit each particular symbol.", []),
    ("surprise", "Surprise of an outcome", "The information of one outcome, growing as its probability shrinks.", ["self-information"]),
    ("entropy", "Entropy of a source", "The average surprise per symbol of a whole source.", []),
    ("uniform-max", "Uniform spread maximum", "Spreading probability evenly over outcomes gives the largest entropy.", []),
    ("certainty-zero", "Zero entropy at certainty", "A source with only one possible outcome carries no information.", []),
    ("independence", "Independent outcomes", "Outcomes whose probabilities multiply because neither informs the other.", []),
    ("entropy-additivity", "Additivity of independent information", "Joint entropy of independent sources equals the sum of their entropies.", []),
    ("coding", "Code for a source", "A mapping from source symbols to codeword strings.", []),
    ("prefix-free", "Prefix-free code", "A code where no codeword begins another, so streams read unambiguously.", []),
    ("unique-decoding", "Unique decoding", "Every codeword stream decodes to exactly one original message.", []),
    ("expected-length", "Expected code length", "The average codeword length a code achieves for a source.", []),
    ("entropy-lower-bound", "Entropy compression floor", "No lossless code can push average length below the source entropy.", ["source coding theorem"]),
    ("incompressibility", "Incompressible random data", "Data whose shortest description is essentially itself.", []),
    ("pigeonhole-compression", "Pigeonhole compression limit", "Some inputs must grow or stay the same under any lossless compressor.", []),
    ("redundancy", "Redundancy in messages", "Extra symbols beyond the bare information, added or natural.", []),
    ("natural-language-redundancy", "Redundancy of language", "Spelling and grammar make natural text far more predictable than its alphabet allows.", []),
    ("noisy-channel", "Noisy channel", "A link that sometimes scrambles what passes through it.", []),
    ("channel-capacity", "Channel capacity", "The highest information rate a channel can carry with vanishing error.", []),
    ("shannon-limit", "Shannon limit on rate", "Reliable communication becomes impossible past a channel's capacity.", []),
    ("channel-coding", "Channel coding with redundancy", "Adding structured redundancy so noise can be detected or corrected.", []),
    ("error-detection", "Error detection", "Noticing that received bits were flipped, without repairing them.", []),
    ("error-correction", "Error correction", "Recovering the original message despite flipped bits.", []),
    ("parity-bit", "Parity check", "One extra bit making a block's total parity fixed so flips stand out.", []),
    ("repetition-code", "Repetition coding", "Sending each symbol several times and taking a majority vote.", []),
    ("mutual-information", "Mutual information", "How much knowing one variable tells about another.", []),
    ("data-processing", "Processing cannot add information", "No transformation of a signal reveals more than the signal held.", ["data processing inequality"]),
    ("conditional-entropy", "Conditional entropy", "The uncertainty left about an outcome after seeing related evidence.", []),
    ("learning-reduces", "Evidence shrinking entropy", "Relevant evidence lowers uncertainty about an outcome.", []),
    ("typical-set", "Typical sequences", "The small family of long blocks a source nearly always produces.", []),
    ("power-bandwidth", "Signal power and bandwidth", "The two resources whose growth raises how much a channel can carry.", []),
    ("password-entropy", "Password entropy", "The guess-resistance of a password measured in bits of choice.", []),
]

RELATIONS = [
    ("prob-causes-surprise", "outcome-probability", "surprise", "causes", "A small outcome probability causes the surprise of an outcome to grow.", "the probability is well below one", ""),
    ("surprise-causes-bits", "surprise", "bit", "causes", "The surprise of an outcome causes its bit of information content through the base-two logarithm of one over its probability.", "logarithms are taken base two", ""),
    ("source-causes-entropy", "message-source", "entropy", "causes", "A message source causes the entropy of a source to settle at a definite average surprise.", "the source keeps stable probabilities", ""),
    ("uniform-causes-max", "uniform-max", "entropy", "causes", "Choosing every symbol equally likely causes the uniform spread maximum of the entropy of a source.", "every outcome is equally likely", ""),
    ("certainty-prevents-surprise", "certainty-zero", "surprise", "prevents", "Zero entropy at certainty prevents any surprise of an outcome from the source.", "one outcome has probability one", ""),
    ("independence-enables-additivity", "independence", "entropy-additivity", "enables", "Independence among independent outcomes enables the additivity of independent information.", "symbols from separate sources are combined", ""),
    ("entropy-causes-floor", "entropy", "entropy-lower-bound", "causes", "The entropy of a source causes the entropy compression floor under any lossless code.", "the code must be exactly reversible", ""),
    ("prefix-enables-unique", "prefix-free", "unique-decoding", "enables", "A prefix-free code enables unique decoding read straight off the bit stream.", "no codeword starts another codeword", ""),
    ("floor-predicts-length", "entropy-lower-bound", "expected-length", "predicts", "The entropy compression floor predicts the best expected code length a source allows.", "codes may use long blocks", ""),
    ("pigeonhole-prevents-compressing", "pigeonhole-compression", "incompressibility", "prevents", "The pigeonhole compression limit prevents lossless shrinking of incompressible random data.", "every input file must remain recoverable", ""),
    ("redundancy-enables-detection", "redundancy", "error-detection", "enables", "Extra redundancy in messages enables error detection when noise flips symbols.", "the added symbols disagree with the data", ""),
    ("parity-enables-detection", "parity-bit", "error-detection", "enables", "A parity check enables error detection of any single flipped bit in the block.", "an odd number of bits has flipped", ""),
    ("repetition-enables-correction", "repetition-code", "error-correction", "enables", "Repetition coding enables error correction by majority vote among the copies.", "noise flips fewer than half the copies", ""),
    ("channelcoding-prevents-loss", "channel-coding", "shannon-limit", "prevents", "Channel coding with redundancy prevents delivery failure at rates below the Shannon limit on rate.", "block lengths grow long enough", ""),
    ("noise-causes-capacity", "noisy-channel", "channel-capacity", "causes", "A noisy channel causes a finite channel capacity.", "noise power stays fixed while coding varies", ""),
    ("power-causes-capacity", "power-bandwidth", "channel-capacity", "causes", "Growing signal power and bandwidth causes the channel capacity to rise.", "noise stays constant while power grows", ""),
    ("limit-inhibits-coding", "shannon-limit", "channel-coding", "inhibits", "The Shannon limit on rate inhibits channel coding with redundancy from rescuing rates above capacity.", "the source rate exceeds capacity", ""),
    ("capacity-causes-mutual", "channel-capacity", "mutual-information", "causes", "Tuned use of channel capacity causes the largest mutual information input and output can share.", "the input distribution is matched to the channel", ""),
    ("processing-inhibits-mutual", "data-processing", "mutual-information", "inhibits", "Processing cannot add information inhibits mutual information from growing under later transformations.", "each step is a fixed function of its input", ""),
    ("evidence-causes-conditional", "learning-reduces", "conditional-entropy", "causes", "Evidence shrinking entropy causes conditional entropy below the raw entropy.", "the evidence is correlated with the outcome", ""),
    ("conditional-enables-mutual", "conditional-entropy", "mutual-information", "enables", "Falling conditional entropy enables mutual information to grow between message and evidence.", "the raw entropy stays fixed", ""),
    ("independence-prevents-mutual", "independence", "mutual-information", "prevents", "The factoring apart of independent outcomes prevents mutual information between the two variables.", "the joint probability factorises into parts", ""),
    ("typical-enables-coding", "typical-set", "coding", "enables", "The small family of typical sequences enables a compact code for a source.", "blocks are taken long enough", ""),
    ("entropy-predicts-typical", "entropy", "typical-set", "predicts", "The entropy of a source predicts the size of its typical sequences family.", "blocks grow very long", ""),
    ("bit-enables-entropy", "bit", "entropy", "enables", "The bit of information enables the entropy of a source to be measured in bits per symbol.", "outcome probabilities are known", ""),
    ("surprise-enables-entropy", "surprise", "entropy", "enables", "Averaging the surprise of an outcome enables the entropy of a source to be computed.", "each outcome is weighted by its probability", ""),
    ("uniform-enables-password", "uniform-max", "password-entropy", "enables", "A uniform spread maximum of choices enables strong password entropy.", "each character is drawn independently at random", ""),
    ("language-causes-lowentropy", "natural-language-redundancy", "entropy", "causes", "Redundancy of language causes the entropy of a source of English text to stay far below its alphabet maximum.", "text follows normal spelling and grammar", ""),
    ("correction-enables-noisy-use", "error-correction", "noisy-channel", "enables", "Error correction enables a noisy channel to be used reliably.", "redundant checks outnumber the expected errors", ""),
    ("channelcoding-causes-redundancy", "channel-coding", "redundancy", "causes", "Channel coding with redundancy causes deliberate redundancy in messages beyond the bare information.", "the channel flips bits sometimes", ""),
    ("coding-causes-length", "coding", "expected-length", "causes", "A code for a source causes an expected code length through its chosen codeword lengths.", "the source probabilities are fixed", ""),
    ("unique-prereq-coding", "unique-decoding", "coding", "prerequisite", "Unique decoding is a prerequisite for a code for a source to be useful.", "streams may contain any message", ""),
    ("processing-prevents-restoring", "data-processing", "noisy-channel", "prevents", "Processing cannot add information prevents restoring what a noisy channel already destroyed.", "the transformation sees only the noisy output", ""),
    ("pigeonhole-causes-growth", "pigeonhole-compression", "coding", "causes", "The pigeonhole compression limit causes some inputs to grow under any code for a source.", "the set of possible inputs is fixed", ""),
    ("bit-prereq-length", "bit", "expected-length", "prerequisite", "The bit of information is a prerequisite for measuring an expected code length.", "code lengths are counted in bits", ""),
    ("floor-prereq-limit", "entropy-lower-bound", "shannon-limit", "prerequisite", "The entropy compression floor is a prerequisite for the Shannon limit on rate on a clean link.", "the channel itself adds no noise", ""),
    ("noise-causes-detection-need", "noisy-channel", "error-detection", "causes", "A noisy channel causes the need for error detection in every reliable link.", "flips cannot be prevented at the source", ""),
    ("repetition-causes-length", "repetition-code", "expected-length", "causes", "Repetition coding causes the expected code length to triple for each protected symbol.", "each symbol is sent three times", ""),
    ("additivity-enables-blockcoding", "entropy-additivity", "coding", "enables", "Additivity of independent information enables a block code for a source to approach the entropy compression floor.", "symbols are coded in growing blocks", ""),
    ("typical-predicts-channel", "typical-set", "channel-coding", "predicts", "The behaviour of typical sequences predicts how channel coding with redundancy fares on long blocks.", "blocks are long enough for the law of large numbers", ""),
    ("parity-inhibits-correction", "parity-bit", "error-correction", "inhibits", "A lone parity check inhibits error correction by revealing only that something flipped, not where.", "no other redundancy is present", ""),
]

MYTHS = [
    ("compression-always", "Any file can be compressed further",
     "Lossless compression cannot shrink every file; some inputs must grow or stay the same size.", "pigeonhole-compression"),
    ("entropy-is-disorder", "Information entropy measures disorder",
     "Entropy measures the average surprise of a source's outcomes, not physical messiness.", "entropy"),
    ("power-beats-limit", "Enough power removes the Shannon limit",
     "Adding power raises capacity, but noise and finite bandwidth keep it finite.", "shannon-limit"),
    ("correlation-communicates", "Shared correlation alone sends a message",
     "Correlation without a chosen signal carries no message; the receiver still sees only their own outcomes.", "mutual-information"),
    ("randomness-compresses", "Random data compresses well",
     "Truly random data is incompressible; only structure makes data shrink.", "incompressibility"),
]

BOUNDARIES = [
    ("lossy-vs-lossless", "Lossy coding breaks the floor",
     "The entropy compression floor binds lossless coding only; lossy methods may discard information freely.", "entropy-lower-bound"),
    ("finite-blocks", "Real codes use finite blocks",
     "Capacity results need long blocks; short real codes fall short of the ideal bound.", "channel-capacity"),
    ("entropy-not-security", "Entropy alone is not security",
     "High password entropy resists guessing but says nothing about how a secret is stored or used.", "password-entropy"),
]

EXAMPLES = [
    ("coin-flips", "Fair versus biased coin flips",
     "A fair coin carries one bit per flip, while a biased coin carries less, showing a uniform spread maximising entropy.",
     ["bit", "entropy", "uniform-max"]),
    ("zip-a-zip", "Zipping an already-zipped file",
     "Compressing already-compressed data barely helps because its remaining structure is near its entropy floor.",
     ["incompressibility", "entropy-lower-bound", "pigeonhole-compression"]),
    ("scratched-disc", "A scratched disc still plays",
     "Disc players recover missing bits from deliberately redundant error correction layers.",
     ["error-correction", "redundancy", "repetition-code"]),
    ("hard-passwords", "Hard-to-guess passwords",
     "Long random passwords carry high password entropy and resist systematic guessing.",
     ["password-entropy", "uniform-max", "surprise"]),
]

CONTROLS = [
    ("noisy-zero-capacity", "A noisy channel has zero capacity",
     "A noisy channel must not be treated as unable to carry information."),
    ("compression-adds-info", "Compression adds information",
     "Compression must not be treated as adding information to data."),
    ("parity-repairs", "A parity check repairs flipped bits",
     "A parity check must not be treated as correcting errors by itself."),
    ("independent-shares", "Independent variables share information",
     "Independent outcomes must not be treated as carrying mutual information."),
]
