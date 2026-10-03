"""Information theory causation: surprise, entropy, coding, noisy channels."""

WORLD = "information-causation-v0"
PREFIX = "inf"
DOMAIN = "information-communication"
SUBJECT = "information-communication.entropy-information"
SOURCES = ['nist-stat-handbook', 'shannon-1948', 'ecma-130-cdrom-2e']
SCOPE = 'Finite discrete Shannon information, binary lossless codes, discrete memoryless channel limits, specified Gaussian channel bounds, and ECMA-130 second edition CIRC; no universal claim about individual files or password security.'
ROOT_LABEL = "Information causation world"
ROOT_STATEMENT = 'Root of the information causation world: how source statistics predict coding bounds and how structured redundancy enables detection and correction under explicit channel assumptions.'

CONCEPTS = [
    ('bit', 'Bit of information', 'The unit obtained by using base-two logarithms in discrete information quantities; an equiprobable binary outcome carries one bit.', []),
    ('message-source', 'Message source', 'A probability law for a discrete symbol stream; independence and stationarity are separate assumptions.', []),
    ('outcome-probability', 'Outcome probability', 'How likely a source is to emit each particular symbol.', []),
    ('surprise', 'Surprise of an outcome', 'The self-information -log2(p) bits of an outcome with probability p > 0.', ['self-information']),
    ('entropy', 'Entropy of a source', 'For a finite discrete symbol X, H(X) = -sum_x p(x)log2(p(x)), with 0log2(0)=0; a dependent stream has a separate per-symbol entropy rate.', []),
    ('uniform-max', 'Uniform source distribution', 'A probability distribution assigning 1/M to each of M possible symbols.', []),
    ('certainty-zero', 'Certain source outcome', 'A source outcome whose probability is one.', []),
    ('independence', 'Independent outcomes', 'Random variables X and Y whose joint probabilities factor as p(x,y) = p(x)p(y).', []),
    ('entropy-additivity', 'Additivity of independent information', 'Joint entropy of independent sources equals the sum of their entropies.', []),
    ('coding', 'Code for a source', 'A mapping from source symbols to codeword strings.', []),
    ('prefix-free', 'Prefix-free code', 'An injective code in which no codeword is a prefix of another distinct codeword.', []),
    ('unique-decoding', 'Unique decoding', 'Injectivity of the extension of a symbol code to every finite concatenated symbol sequence.', []),
    ('expected-length', 'Expected code length', 'The mean L = sum_x p(x)l(x) of codeword lengths l(x) under a specified source distribution.', []),
    ('entropy-lower-bound', 'Entropy compression floor', 'The lower bound H(X) <= L for binary uniquely decodable coding of a finite discrete source, or H(X^n) <= L_n for source blocks.', ['source coding theorem']),
    ('incompressibility', 'Incompressible random data', 'Uniformly sampled finite bit strings that resist substantial shortening under a specified injective lossless encoder; individual random draws can still be short-encodable.', []),
    ('pigeonhole-compression', 'Pigeonhole compression limit', 'Counting prevents an injective map from all n-bit strings into the fewer binary strings of length below n.', []),
    ('redundancy', 'Redundancy in messages', 'Dependence or constrained codeword structure that leaves fewer legal messages than unconstrained strings of the same length.', []),
    ('natural-language-redundancy', 'Redundancy of language', 'Statistical constraints and dependence between symbols of a language source relative to an unconstrained alphabet model.', []),
    ('noisy-channel', 'Noisy channel', 'A stochastic input-output transformation with a specified conditional law p(y|x).', []),
    ('channel-capacity', 'Channel capacity', 'The supremum of communication rates achievable with block error tending to zero under a specified channel model and input constraints.', []),
    ('shannon-limit', 'Shannon limit on rate', 'The capacity boundary on asymptotically reliable communication for the specified channel model, not a fixed universal bit rate.', []),
    ('channel-coding', 'Channel coding with redundancy', 'Encoding messages into a constrained codebook to permit decoding despite channel corruption.', []),
    ('error-detection', 'Error detection', 'Recognizing that a received word is not an allowed codeword, without necessarily identifying the sent word.', []),
    ('error-correction', 'Error correction', 'Recovering a transmitted codeword or message within specified error or erasure assumptions.', []),
    ('parity-bit', 'Parity check', 'A binary linear constraint requiring the XOR of selected bits, including a check bit, to equal a fixed value.', []),
    ('repetition-code', 'Repetition coding', 'A binary block code mapping each source bit to m identical copies, with a chosen decoder such as majority vote.', []),
    ('mutual-information', 'Mutual information', 'For finite discrete X and Y, I(X;Y) = H(X)-H(X|Y), equal to the divergence of p(x,y) from p(x)p(y).', []),
    ('data-processing', 'Data processing inequality', 'For a Markov chain X->Y->Z, I(X;Z) <= I(X;Y); processing Y adds no new information about X.', ['data processing inequality']),
    ('conditional-entropy', 'Conditional entropy', 'The average H(X|Y) = sum_y p(y)H(X|Y=y) for finite discrete variables, rather than the entropy for one particular observation.', []),
    ('learning-reduces', 'Observation of evidence', 'Revealing a correlated discrete variable Y to update the distribution of an unknown variable X.', []),
    ('typical-set', 'Typical sequences', 'For an iid finite-alphabet source, length-n sequences whose per-symbol negative log probability is within epsilon of H(X).', []),
    ('power-bandwidth', 'Signal power and bandwidth', 'An average signal-power constraint P and bandwidth B specified together with a channel noise spectrum.', []),
    ('password-entropy', 'Password entropy', 'The Shannon entropy of a specified password-generation distribution, conditional on attacker knowledge; it is not by itself a bound on optimal guessing success.', []),
    ('code-rate', 'Code rate', 'For M equiprobable messages encoded into n channel uses, R = log2(M)/n information bits per channel use.', []),
    ('circ', 'Cross-interleaved Reed-Solomon coding', 'The CIRC encoding in ECMA-130 second edition clause 17 and Annex C, combining two Reed-Solomon codes and byte interleaving.', ['CIRC']),
]

RELATIONS = [
    ('prob-predicts-surprise', 'outcome-probability', 'surprise', 'predicts', 'Outcome probability p predicts surprise of an outcome equal to log2(1/p) bits.', 'the outcome belongs to a discrete source and 0 < p <= 1; the logarithm base is two', ''),
    ('source-predicts-entropy', 'message-source', 'entropy', 'predicts', 'A message source with known symbol probabilities predicts the entropy of a source as their probability-weighted mean self-information.', 'X has a fixed finite probability distribution p(x), and zero-probability terms contribute zero to H(X)', ''),
    ('uniform-predicts-max', 'uniform-max', 'entropy', 'predicts', 'A uniform source distribution predicts the largest possible entropy of a source on the specified alphabet, log2(M) bits.', 'the alphabet has exactly M >= 1 symbols and the entropy is compared across all probability distributions on that same alphabet', ''),
    ('certainty-predicts-surprise', 'certainty-zero', 'surprise', 'predicts', 'A certain source outcome predicts zero surprise of an outcome when it occurs.', 'one discrete outcome has probability p = 1, so -log2(p) = 0 bits', ''),
    ('independence-predicts-additivity', 'independence', 'entropy-additivity', 'predicts', 'A pair of independent outcomes predicts additivity of independent information through H(X,Y) = H(X)+H(Y).', 'X and Y are independent finite discrete random variables and the joint entropy is measured with the same logarithm base', ''),
    ('entropy-predicts-floor', 'entropy', 'entropy-lower-bound', 'predicts', 'The entropy of a source predicts an entropy compression floor of H(X) bits per source symbol.', 'a finite discrete source X is encoded by a binary uniquely decodable symbol code and every possible source sequence must be recovered exactly', ''),
    ('prefix-enables-unique', 'prefix-free', 'unique-decoding', 'enables', 'A prefix-free code enables unique decoding of concatenated codewords as they arrive.', 'the binary symbol code is injective, each codeword is finite and nonempty, and no distinct codeword is a prefix of another', ''),
    ('floor-predicts-length', 'entropy-lower-bound', 'expected-length', 'predicts', 'The entropy compression floor predicts H(X) <= L_n/n < H(X)+1/n for an appropriately constructed expected code length L_n.', 'the source is iid on a finite alphabet with at least two positive-probability symbols and a binary prefix code is designed for n-symbol blocks', ''),
    ('pigeonhole-predicts-incompressibility', 'pigeonhole-compression', 'incompressibility', 'predicts', 'The pigeonhole compression limit predicts incompressible random data in the sense that large savings are unlikely for a fixed lossless encoder.', 'X is uniform over n-bit strings, the encoder is injective, and 0 <= k < n is an integer: fewer than a 2^(-k) fraction can have output length strictly below n-k', ''),
    ('redundancy-enables-detection', 'redundancy', 'error-detection', 'enables', 'Structured redundancy in messages enables error detection by checking whether the received word belongs to the codebook.', 'the binary block code has minimum Hamming distance d >= 2 and between 1 and d-1 bit substitutions occur in a transmitted codeword', ''),
    ('parity-enables-detection', 'parity-bit', 'error-detection', 'enables', 'A parity check enables error detection of every odd number of flipped bits in the checked block.', 'the original XOR constraint is satisfied and an odd number of checked bits, including the check bit if affected, are flipped once', ''),
    ('repetition-enables-correction', 'repetition-code', 'error-correction', 'enables', 'Repetition coding enables error correction by majority vote when fewer than half the copies are wrong.', 'one bit is sent as m identical copies for odd m >= 3 and at most (m-1)/2 of those copies are flipped', ''),
    ('channelcoding-enables-noisy-use', 'channel-coding', 'noisy-channel', 'enables', 'Channel coding with redundancy enables a noisy channel to transmit at any fixed rate below capacity with block error tending to zero as block length grows.', 'the channel is discrete and memoryless with finite alphabets, 0 < R < C, and block length may grow without bound and the codebook and decoder may be designed for the channel', ''),
    ('noise-predicts-rate', 'noisy-channel', 'code-rate', 'predicts', 'A noisy channel predicts an upper bound on asymptotically reliable code rate of 1-h2(p) bits per use for a binary symmetric channel.', 'independent bit flips occur with fixed probability 0 <= p <= 1/2, messages are equiprobable, block error tends to zero as length grows with a limiting rate R, and h2(p)=-p*log2(p)-(1-p)*log2(1-p) with 0log2(0)=0', ''),
    ('power-predicts-capacity', 'power-bandwidth', 'channel-capacity', 'predicts', 'A choice of signal power and bandwidth predicts channel capacity C = B*log2(1+P/(N0*B)) bits per second.', 'the channel is band-limited additive white Gaussian noise with bandwidth B > 0 Hz, finite average signal power P >= 0 watts and one-sided noise density N0 > 0 watts per Hz, so noise power is N0*B', ''),
    ('mutual-predicts-capacity', 'mutual-information', 'channel-capacity', 'predicts', 'Maximizing mutual information I(X;Y) over input distributions predicts channel capacity.', 'the channel has fixed transition probabilities p(y|x), finite alphabets and no memory, and capacity is measured in bits per channel use', ''),
    ('processing-predicts-mutual-bound', 'data-processing', 'mutual-information', 'predicts', 'The data processing inequality predicts the mutual information bound I(X;Z) <= I(X;Y).', 'X,Y,Z are finite discrete variables forming X->Y->Z, so Z is conditionally independent of X given Y and no extra side information is supplied', ''),
    ('evidence-predicts-conditional', 'learning-reduces', 'conditional-entropy', 'predicts', 'Observation of evidence predicts conditional entropy no larger on average than the prior entropy.', 'X and Y are finite discrete variables and H(X|Y) averages over the actual distribution of all observations Y, rather than fixing one surprising y', ''),
    ('conditional-predicts-mutual', 'conditional-entropy', 'mutual-information', 'predicts', 'Conditional entropy predicts mutual information through I(X;Y) = H(X)-H(X|Y).', 'X and Y are finite discrete variables with a fixed marginal law of X; any comparison keeps H(X) constant', ''),
    ('independence-predicts-zero-mutual', 'independence', 'mutual-information', 'predicts', 'A pair of independent outcomes predicts zero mutual information between the two random variables.', 'the joint law of finite discrete X and Y satisfies p(x,y)=p(x)p(y) at every pair', ''),
    ('typical-enables-coding', 'typical-set', 'coding', 'enables', 'Identifying typical sequences enables a fixed-length code for a source with rate approaching its entropy and decoding error tending to zero.', 'the source is iid on a finite alphabet, block length tends to infinity, and atypical blocks are counted as errors rather than falsely claiming exact lossless recovery', ''),
    ('entropy-predicts-typical', 'entropy', 'typical-set', 'predicts', 'The entropy of a source predicts the exponential size of its typical sequences set.', 'X_i are iid on a finite alphabet with entropy H; for epsilon > 0 and sufficiently large n, the epsilon-typical set has probability at least 1-epsilon and size between (1-epsilon)*2^(n*(H-epsilon)) and 2^(n*(H+epsilon))', ''),
    ('uniform-predicts-password', 'uniform-max', 'password-entropy', 'predicts', 'A uniform source distribution predicts password entropy of L*log2(M) bits for independently sampled characters.', 'the generator chooses each of L characters uniformly and independently from the same M-symbol alphabet, and the attacker knows the procedure but has no correlated side information', ''),
    ('language-predicts-entropy-bound', 'natural-language-redundancy', 'entropy', 'predicts', 'Redundancy of language predicts an entropy of a source below the unconstrained alphabet maximum in a statistical language model.', 'a stationary source over M symbols has nonuniform single-symbol probabilities or H(X_t|X_(t-1),...,X_(t-k)) < log2(M) for some finite k, and the comparison concerns its entropy rate', ''),
    ('coding-predicts-length', 'coding', 'expected-length', 'predicts', 'A code for a source predicts expected code length L = sum_x p(x)*l(x).', 'a finite source distribution p(x) and finite binary codeword lengths l(x) are fixed before taking the expectation', ''),
    ('unique-prereq-coding', 'unique-decoding', 'coding', 'prerequisite', 'Unique decoding is a prerequisite for a code for a source to recover every concatenated source sequence without separate delimiters.', 'one symbol code is extended by concatenation to all finite source sequences, recovery must be exact, and no framing or side channel resolves boundaries', ''),
    ('repetition-predicts-rate', 'repetition-code', 'code-rate', 'predicts', 'Repetition coding predicts a code rate of 1/m source bit per transmitted bit.', 'each binary source symbol is mapped to exactly m identical channel bits with fixed integer m >= 1 and no additional framing symbols', ''),
    ('circ-enables-correction', 'circ', 'error-correction', 'enables', 'Cross-interleaved Reed-Solomon coding enables error correction of limited symbol corruptions after deinterleaving.', 'ECMA-130 second edition clause 17 and Annex C encoding is used, and each constituent Reed-Solomon decoding step has error count e and known erasure count s satisfying 2e+s <= 4', ''),
]

MYTHS = [
    ('compression-always', 'Any file can be compressed further', 'A fixed injective lossless encoder cannot shorten all n-bit files: at least one must retain its length or grow.', 'pigeonhole-compression'),
    ('entropy-is-disorder', 'Information entropy measures physical disorder', 'Discrete Shannon entropy measures uncertainty under a specified probability model, rather than an undefined visual or physical messiness.', 'entropy'),
    ('power-beats-limit', 'Enough finite power removes the Shannon limit', 'In the band-limited Gaussian-noise model, increasing finite power raises capacity but does not abolish the capacity bound.', 'shannon-limit'),
    ('correlation-communicates', 'Shared correlation alone sends a chosen message', 'Shared correlated variables do not alone let a sender choose what a remote receiver observes; communication requires a message-dependent signal.', 'mutual-information'),
    ('randomness-compresses', 'Every truly random sample is incompressible', 'Uniform random n-bit inputs resist substantial compression with high probability under any fixed injective code, but a particular draw such as an all-zero string can have a short encoding.', 'incompressibility'),
    ('conditioning-always-shrinks', 'Every observation lowers entropy', 'Conditioning lowers finite discrete entropy on average; a particular observation can produce a more uncertain posterior than the prior.', 'conditional-entropy'),
]

BOUNDARIES = [
    ('lossy-vs-lossless', 'Lossy and framed coding use different bounds', 'The H(X) <= expected-length bound assumes binary unique decodability; lossy reconstruction and separately framed single-message encodings require their own rate or side-information accounting.', 'entropy-lower-bound'),
    ('finite-blocks', 'Asymptotic reliability is not zero-error delivery', 'The channel coding theorem supplies sequences of codes below capacity with block error tending to zero; it does not make any chosen finite code error-free.', 'channel-capacity'),
    ('entropy-not-security', 'Shannon entropy is not a guessing guarantee', 'Shannon entropy alone does not determine an attacker optimal guessing success or expected guesses for a nonuniform password distribution, and says nothing about storage or disclosure.', 'password-entropy'),
    ('parity-correction-limit', 'One parity bit does not locate an unknown flip', 'For the full single-parity-check binary code with at least two data bits, an odd-flip syndrome does not identify the erroneous position; one known-position erasure can nevertheless be recovered.', 'parity-bit'),
    ('processing-limit', 'Data processing bounds target information', 'A downstream processor using only Y cannot increase I(X;Y) about X, but it can change the entropy of its own output or improve decisions by presenting existing information usefully.', 'data-processing'),
    ('above-capacity', 'Redundancy does not evade capacity', 'For a discrete memoryless channel, codes whose rate stays strictly above capacity cannot have block error probability tending to zero.', 'shannon-limit'),
    ('noise-not-finite', 'Noise alone does not imply finite capacity', 'Finite alphabets or input-power and bandwidth constraints are needed for the usual finite-capacity bounds; merely labeling a channel noisy supplies no such bound.', 'noisy-channel'),
    ('certainty-not-meaningless', 'Zero entropy does not mean no practical value', 'An outcome already known with probability one has zero self-information in that probability model, while its semantic or practical value is a separate issue.', 'certainty-zero'),
]

EXAMPLES = [
    ('coin-flips', 'Fair versus biased coin flips', 'A fair independent binary source has entropy 1 bit per flip; with probability 1/4 for heads, surprise of heads is 2 bits while average entropy is about 0.811 bits per flip.', ['bit', 'entropy', 'surprise', 'uniform-max']),
    ('zip-a-zip', 'Already-compressed is not a mathematical certificate', 'A file containing the same compressed archive twice still has repetition that another format can exploit; the pigeonhole limit concerns all inputs of a length, not a claim that every compressed file is incompressible.', ['incompressibility', 'entropy-lower-bound', 'pigeonhole-compression']),
    ('scratched-disc', 'A scratched compact disc', 'ECMA-130 clause 17 and Annex C specify cross-interleaved Reed-Solomon coding, which distributes bytes and adds parity to support bounded error correction; simple repetition is not the CD coding scheme.', ['error-correction', 'redundancy', 'circ']),
    ('hard-passwords', 'Uniform password choices', 'An ideal generator choosing 12 independent uniform characters from a 64-character alphabet has 72 bits of password entropy; an attacker with no extra information succeeds with probability q/2^72 after q distinct guesses, for q <= 2^72.', ['password-entropy', 'uniform-max', 'surprise']),
    ('surprising-evidence', 'An observation that raises posterior entropy', 'Let P(X=1)=0.1, P(Y=1|X=1)=1 and P(Y=1|X=0)=1/9; then P(Y=1)=0.2 and P(X=1|Y=1)=1/2, so observing Y=1 raises entropy to 1 bit while average conditional entropy is 0.2 bits, below the prior of about 0.469 bits.', ['learning-reduces', 'conditional-entropy', 'entropy']),
    ('three-copy-code', 'A three-copy decoder', 'The repetition code 0->000 and 1->111 has rate 1/3 and corrects any one bit flip by majority vote; two flips can make it choose the wrong source bit.', ['repetition-code', 'code-rate', 'error-correction']),
]

CONTROLS = [
    ('noisy-zero-capacity', 'Every noisy channel has zero capacity', 'A channel with nonzero noise must not be treated as necessarily unable to carry information.'),
    ('compression-adds-info', 'Compression creates source information', 'Lossless compression without side information must not be treated as adding mutual information about the original source.'),
    ('parity-repairs', 'One parity check locates an unknown bit flip', 'A single parity check over at least two data bits must not be treated as identifying an arbitrary unknown-position bit flip.'),
    ('independent-shares', 'Independent variables share information', 'Independent finite discrete random variables must not be treated as having positive mutual information.'),
    ('one-observation', 'Every posterior has lower entropy', 'The entropy inequality averaged over evidence must not be treated as applying separately to every observed evidence value.'),
    ('finite-perfect', 'Below-capacity means error-free finite blocks', 'A rate below capacity must not be treated as guaranteeing that an arbitrary finite code has zero error.'),
    ('all-random-incompressible', 'Every random draw resists compression', 'A high-probability counting statement about uniform random inputs must not be treated as a guarantee for each sampled string.'),
]
