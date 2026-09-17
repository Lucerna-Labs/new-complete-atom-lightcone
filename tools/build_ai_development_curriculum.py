#!/usr/bin/env python3
"""Author AI/ML development, evaluation, safety, and accelerator foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "ai-development" / "foundations.jsonl"
WORLD = "ai-development-v0"
LANES = ["reasoning.inductive", "reasoning.probabilistic", "thinking.bottom_up", "reasoning.causal"]
SOURCES = [
    "deep-learning-book", "attention-1706-03762", "jax-documentation", "pytorch-213-docs",
    "huggingface-transformers", "nist-ai-rmf-10", "nist-ai-600-1", "datasheets-datasets",
    "model-cards", "mlperf-training", "sutton-barto-rl", "ddpm-2006-11239",
]


CONCEPTS = [
    ("root", "AI development evidence loop", "AI development defines a task and affected context, governs data, selects a model and objective, trains under a reproducible protocol, evaluates held-out behavior and risk, deploys a versioned artifact, monitors drift and harm, and feeds evidence back into revision.", "ai-machine-learning.ml-foundations"),
    ("task", "Machine-learning task", "A machine-learning task defines inputs, outputs, use context, decision role, success criteria, affected stakeholders, and unacceptable failures before model selection.", "ai-machine-learning.ml-foundations"),
    ("example", "Learning example", "A learning example is one sampled unit containing features, targets where available, metadata, provenance, and inclusion context from a data-generating process.", "ai-machine-learning.ml-foundations"),
    ("feature", "Feature", "A feature is an observed or derived input variable presented to a model under a representation and availability boundary.", "ai-machine-learning.ml-foundations"),
    ("label", "Label", "A label is a recorded target or annotation produced by a measurement or judgment process with possible noise, ambiguity, bias, and missingness.", "ai-machine-learning.ml-foundations"),
    ("model", "Machine-learning model", "A model is a parameterized mapping or probability distribution chosen to approximate selected relationships for a defined task and population.", "ai-machine-learning.ml-foundations"),
    ("parameter", "Model parameter", "A parameter is a learned or fitted value that influences model behavior and is estimated from training evidence.", "ai-machine-learning.ml-foundations"),
    ("hyperparameter", "Hyperparameter", "A hyperparameter controls architecture, optimization, regularization, sampling, or training procedure and must be selected without using sealed-test outcomes.", "ai-machine-learning.ml-foundations"),
    ("loss", "Training loss", "A loss maps prediction and target or preference evidence to an optimization signal and is only a proxy for deployment value and harm.", "ai-machine-learning.ml-foundations"),
    ("empirical-risk", "Empirical risk", "Empirical risk averages or aggregates loss over sampled data and estimates expected task loss under sampling assumptions.", "ai-machine-learning.ml-foundations"),
    ("train-split", "Training split", "The training split supplies examples and derived statistics used to fit parameters or choose learned representations.", "ai-machine-learning.ml-foundations"),
    ("validation-split", "Validation split", "The validation split supports model and hyperparameter selection and becomes part of the development process after repeated inspection.", "ai-machine-learning.ml-foundations"),
    ("test-split", "Sealed test split", "A sealed test split estimates behavior only after development choices are frozen and must remain isolated from training, prompt tuning, threshold selection, and repeated debugging.", "ai-machine-learning.ml-foundations"),
    ("distribution", "Data distribution", "A data distribution describes the joint prevalence and relationships among inputs, targets, contexts, and groups for a specified population and period.", "ai-machine-learning.ml-foundations"),
    ("iid", "Independent identically distributed assumption", "An IID assumption treats examples as independent draws from one distribution and must not be silently applied to grouped, temporal, spatial, or networked data.", "ai-machine-learning.ml-foundations"),
    ("generalization", "Generalization", "Generalization is performance on relevant unseen examples or environments under a declared relation to training data.", "ai-machine-learning.ml-foundations"),
    ("overfit", "Overfitting", "Overfitting occurs when development improves fit to sampled or repeatedly inspected evidence without comparable improvement on the target distribution.", "ai-machine-learning.ml-foundations"),
    ("underfit", "Underfitting", "Underfitting occurs when the learned system lacks optimization, representation, capacity, or information needed even for the modeled training relationships.", "ai-machine-learning.ml-foundations"),
    ("regularization", "Regularization", "Regularization constrains effective model capacity or training dynamics to improve desired generalization under a specific data regime.", "ai-machine-learning.ml-foundations"),
    ("calibration", "Probabilistic calibration", "A predictor is calibrated when events assigned a probability occur at corresponding frequencies for the evaluated population and conditioning scheme.", "ai-machine-learning.ml-foundations"),
    ("predictive-causal", "Prediction-causation boundary", "Predictive association does not identify the effect of intervention without causal assumptions, design, and evidence beyond predictive accuracy.", "ai-machine-learning.ml-foundations"),
    ("tensor", "Tensor", "A tensor is a typed multidimensional array with shape, layout, device, precision, and differentiation status.", "ai-machine-learning.deep-learning"),
    ("layer", "Neural-network layer", "A neural-network layer applies a parameterized or fixed transformation to tensors within a computation graph.", "ai-machine-learning.deep-learning"),
    ("activation", "Activation function", "An activation function introduces nonlinear or gated behavior that shapes signal and gradient propagation.", "ai-machine-learning.deep-learning"),
    ("computation-graph", "Computation graph", "A computation graph represents operations and tensor dependencies used for execution, differentiation, transformation, and optimization.", "ai-machine-learning.deep-learning"),
    ("autodiff", "Automatic differentiation", "Automatic differentiation applies chain-rule transformations to executable operations, producing exact derivatives of the implemented computation up to numerical effects.", "ai-machine-learning.deep-learning"),
    ("backprop", "Backpropagation", "Backpropagation traverses a computation graph in reverse dependency order to accumulate gradients of a scalar objective.", "ai-machine-learning.deep-learning"),
    ("gradient", "Gradient", "A gradient gives local first-order objective sensitivity with respect to parameters and does not by itself identify a globally optimal direction under finite steps.", "ai-machine-learning.deep-learning"),
    ("minibatch", "Minibatch", "A minibatch estimates an objective and gradient from selected examples, trading variance, memory, throughput, and update frequency.", "ai-machine-learning.deep-learning"),
    ("normalization", "Neural normalization", "Normalization transforms activations or statistics to stabilize optimization, with behavior depending on axes, learned scale, training mode, and inference state.", "ai-machine-learning.deep-learning"),
    ("residual", "Residual connection", "A residual connection adds or combines a block input with its transformed path, supporting gradient flow and incremental representation updates.", "ai-machine-learning.deep-learning"),
    ("dropout", "Dropout", "Dropout randomly masks selected activations during training and changes expected scaling or behavior at inference according to the implementation.", "ai-machine-learning.deep-learning"),
    ("embedding", "Learned embedding", "An embedding maps discrete or structured identities into continuous vectors whose geometry is learned for the training objective.", "ai-machine-learning.deep-learning"),
    ("tokenizer", "Tokenizer", "A tokenizer maps text or other input into discrete token identifiers under a fixed vocabulary, normalization, special-token, and byte-handling contract.", "ai-machine-learning.transformers-llms"),
    ("vocabulary", "Model vocabulary", "A vocabulary assigns token identities and special meanings; changing it without aligned embedding and output weights changes the model interface.", "ai-machine-learning.transformers-llms"),
    ("token-embedding", "Token embedding", "A token embedding maps discrete identifiers to model vectors before contextual transformation.", "ai-machine-learning.transformers-llms"),
    ("position", "Positional representation", "A positional representation supplies token-order or relative-position information that content-only attention would otherwise lack.", "ai-machine-learning.transformers-llms"),
    ("query-key-value", "Query, key, and value projections", "Attention projects representations into queries that request information, keys that mediate matching, and values that carry aggregated content.", "ai-machine-learning.transformers-llms"),
    ("attention-score", "Attention score", "An attention score compares a query and key under scaling, mask, and positional transformations before normalization.", "ai-machine-learning.transformers-llms"),
    ("causal-mask", "Causal attention mask", "A causal mask prevents a token position from attending to later target positions during autoregressive training or decoding.", "ai-machine-learning.transformers-llms"),
    ("multihead", "Multi-head attention", "Multi-head attention applies multiple learned projection and aggregation subspaces, then combines their outputs.", "ai-machine-learning.transformers-llms"),
    ("attention-output", "Attention aggregation", "Normalized attention weights form a weighted combination of value vectors for each query position.", "ai-machine-learning.transformers-llms"),
    ("ffn", "Transformer feed-forward block", "A feed-forward block applies position-wise learned nonlinear transformations and often expands then contracts hidden width.", "ai-machine-learning.transformers-llms"),
    ("transformer-block", "Transformer block", "A transformer block composes attention, feed-forward transformation, residual paths, normalization, masks, and optional routing under an architecture-specific order.", "ai-machine-learning.transformers-llms"),
    ("decoder", "Autoregressive decoder", "An autoregressive decoder predicts the next-token distribution from a bounded prefix and repeats this conditional factorization during generation.", "ai-machine-learning.transformers-llms"),
    ("logit", "Token logit", "A token logit is an unnormalized output score whose relative values determine a probability distribution after normalization and decoding transforms.", "ai-machine-learning.transformers-llms"),
    ("context-window", "Context window", "A context window bounds the token sequence available to a model invocation and does not guarantee equal effective use of all positions.", "ai-machine-learning.transformers-llms"),
    ("kv-cache", "Key-value cache", "A key-value cache reuses prior attention projections during autoregressive decoding and trades memory, precision, and layout against repeated computation.", "ai-machine-learning.transformers-llms"),
    ("pretraining", "Language-model pretraining", "Pretraining fits a broad predictive objective over governed data and produces statistical capability rather than verified factual authority.", "ai-machine-learning.transformers-llms"),
    ("instruction-tuning", "Instruction tuning", "Instruction tuning trains on task-and-response demonstrations to shape conditional behavior and format without guaranteeing truth or policy compliance outside the data.", "ai-machine-learning.transformers-llms"),
    ("tool-use", "Model tool use", "Tool use lets a model propose structured calls whose schema, authorization, execution, result, and side effects remain owned by the host system.", "ai-machine-learning.transformers-llms"),
    ("retrieval-augmentation", "Retrieval augmentation", "Retrieval supplies external passages or records at inference time, but the host must preserve source identity, relevance, version, and instruction-data separation.", "ai-machine-learning.transformers-llms"),
    ("hallucination", "Unsupported model generation", "An unsupported generation presents content not warranted by available evidence; fluency and internal probability do not convert it into fact.", "ai-machine-learning.transformers-llms"),
    ("mixture-experts", "Mixture of experts", "A mixture-of-experts layer routes tokens among selected parameter experts, trading conditional capacity against routing balance, communication, and failure complexity.", "ai-machine-learning.transformers-llms"),
    ("optimizer", "Optimizer", "An optimizer updates parameters from gradients and internal state under a learning rate, numerical precision, regularization, and schedule.", "ai-machine-learning.training-optimization"),
    ("learning-rate", "Learning rate", "A learning rate scales parameter updates and interacts with optimizer state, batch size, curvature, warmup, and numerical precision.", "ai-machine-learning.training-optimization"),
    ("schedule", "Learning-rate schedule", "A schedule changes optimization step size over training according to warmup, decay, plateaus, restarts, or token count.", "ai-machine-learning.training-optimization"),
    ("mixed-precision", "Mixed-precision training", "Mixed precision uses lower-precision arithmetic or storage where acceptable while protecting numerically sensitive reductions, accumulators, and updates.", "ai-machine-learning.training-optimization"),
    ("loss-scale", "Loss scaling", "Loss scaling multiplies a loss before low-precision backpropagation and reverses the scale before update to reduce gradient underflow.", "ai-machine-learning.training-optimization"),
    ("gradient-clip", "Gradient clipping", "Gradient clipping bounds a gradient norm or value to limit unstable updates while changing the effective optimization rule.", "ai-machine-learning.training-optimization"),
    ("gradient-accum", "Gradient accumulation", "Gradient accumulation combines multiple microbatch gradients before an optimizer step to emulate a larger batch subject to normalization and state semantics.", "ai-machine-learning.training-optimization"),
    ("data-parallel", "Data parallelism", "Data parallelism replicates model computation over different examples and aggregates gradients under synchronization and batch-semantics rules.", "ai-machine-learning.training-optimization"),
    ("tensor-parallel", "Tensor parallelism", "Tensor parallelism shards operations and parameters across devices and inserts collectives along partitioned dimensions.", "ai-machine-learning.training-optimization"),
    ("pipeline-parallel", "Pipeline parallelism", "Pipeline parallelism places sequential model stages on different devices and schedules microbatches while managing bubbles, activation memory, and dependency order.", "ai-machine-learning.training-optimization"),
    ("sharding", "Parameter and state sharding", "Sharding partitions parameters, gradients, optimizer state, activations, or data across devices under layout and collective contracts.", "ai-machine-learning.training-optimization"),
    ("checkpoint", "Training checkpoint", "A checkpoint records model, optimizer, scheduler, random, data-position, precision, topology, and version state needed for faithful resume or evaluation.", "ai-machine-learning.training-optimization"),
    ("seed", "Training random seed", "A seed identifies one pseudorandom stream initialization but does not guarantee identical results across algorithms, devices, parallel orders, and library versions.", "ai-machine-learning.training-optimization"),
    ("training-curve", "Training curve", "A training curve records objective and diagnostic metrics against steps, tokens, examples, time, or compute with event and configuration context.", "ai-machine-learning.training-optimization"),
    ("metric", "Evaluation metric", "An evaluation metric operationalizes one property of outputs under a scoring rule and population; no single metric captures all capability and risk.", "ai-machine-learning.evaluation"),
    ("benchmark", "AI benchmark", "A benchmark fixes tasks, data, prompts or protocols, scoring, environment, and version so systems can be compared within its scope.", "ai-machine-learning.evaluation"),
    ("contamination", "Evaluation contamination", "Contamination occurs when test examples, labels, solutions, or close mechanism variants influence training or development decisions.", "ai-machine-learning.evaluation"),
    ("stratification", "Stratified evaluation", "Stratified evaluation reports behavior across relevant groups, difficulty, domains, lengths, conditions, and intersections rather than only an aggregate.", "ai-machine-learning.evaluation"),
    ("confidence-interval", "Metric uncertainty interval", "An uncertainty interval quantifies sampling variability under assumptions and must not hide systematic measurement or distribution error.", "ai-machine-learning.evaluation"),
    ("robustness", "Robustness evaluation", "Robustness evaluation measures behavior under plausible perturbations, corruptions, shifts, adversarial pressure, and component failure.", "ai-machine-learning.evaluation"),
    ("ood", "Out-of-distribution evaluation", "Out-of-distribution evaluation tests environments or examples outside the modeled training relation and should define how the shift is constructed.", "ai-machine-learning.evaluation"),
    ("human-eval", "Human evaluation", "Human evaluation requires a defined rubric, rater qualification, blinding or randomization where possible, agreement analysis, and affected-population context.", "ai-machine-learning.evaluation"),
    ("red-team", "AI red-team evaluation", "Red-team evaluation probes failure and misuse hypotheses under authorization, scope, safe handling, reproducible protocols, and disclosure rules.", "ai-machine-learning.evaluation"),
    ("system-performance", "AI system performance", "System evaluation includes latency distributions, throughput, concurrency, memory, energy, cost, availability, and quality under one workload and serving configuration.", "ai-machine-learning.evaluation"),
    ("objective-misspec", "Objective misspecification", "Objective misspecification occurs when optimizing the declared loss produces behavior that diverges from stakeholder intent or safety constraints.", "ai-machine-learning.alignment-safety"),
    ("behavior-spec", "AI behavior specification", "A behavior specification distinguishes desired, permitted, disallowed, uncertain, and escalation outcomes across contexts and affected stakeholders.", "ai-machine-learning.alignment-safety"),
    ("preference-data", "Preference data", "Preference data records comparative or scalar judgments with rater context, rubric, disagreement, quality control, and population limits.", "ai-machine-learning.alignment-safety"),
    ("preference-optimization", "Preference optimization", "Preference optimization changes model behavior toward recorded judgments under an algorithm whose proxy, coverage, and distribution limits remain explicit.", "ai-machine-learning.alignment-safety"),
    ("abstention", "Model abstention", "Abstention declines or escalates when evidence, competence, authorization, or safety conditions do not support a reliable response.", "ai-machine-learning.alignment-safety"),
    ("grounding", "Grounded generation", "Grounded generation links material claims to retrieved or executed evidence whose identity, relevance, and entailment are checked outside model fluency.", "ai-machine-learning.alignment-safety"),
    ("oversight", "Human and system oversight", "Oversight defines which decisions require review, what evidence is visible, who can intervene, and how automation bias and workload affect effectiveness.", "ai-machine-learning.alignment-safety"),
    ("ai-threat-model", "AI system threat model", "An AI threat model covers data poisoning, model theft, prompt injection, tool abuse, sensitive disclosure, evasion, supply chain, and misuse across system boundaries.", "ai-machine-learning.alignment-safety"),
    ("defense-layer", "Layered AI defense", "Layered defense combines data controls, model training, runtime policy, tool authorization, isolation, monitoring, response, and user-interface design because no one layer is complete.", "ai-machine-learning.alignment-safety"),
    ("risk-owner", "AI risk owner", "A risk owner has authority and responsibility to accept, mitigate, transfer, monitor, or stop a defined AI risk with affected-stakeholder input.", "ai-machine-learning.alignment-safety"),
    ("feature-representation", "Learned feature representation", "A learned feature is a model-internal direction, subspace, unit pattern, circuit input, or distributed relation hypothesized to encode behaviorally relevant information.", "ai-machine-learning.interpretability"),
    ("attribution", "Attribution method", "Attribution estimates how inputs, components, or activations contribute to an output under a chosen baseline and approximation, not necessarily the true causal mechanism.", "ai-machine-learning.interpretability"),
    ("probe", "Representation probe", "A probe measures whether information can be decoded from activations while controlling probe capacity and distinguishing decodability from model use.", "ai-machine-learning.interpretability"),
    ("activation-intervention", "Activation intervention", "An activation intervention changes internal state and measures downstream effects, supporting causal claims only within the intervention and distribution scope.", "ai-machine-learning.interpretability"),
    ("mechanistic-hypothesis", "Mechanistic interpretability hypothesis", "A mechanistic hypothesis predicts how identified components and computations cause a behavior and must survive targeted intervention and counterexamples.", "ai-machine-learning.interpretability"),
    ("faithfulness", "Explanation faithfulness", "A faithful explanation tracks the actual decision mechanism under defined tests rather than merely sounding plausible to a reader.", "ai-machine-learning.interpretability"),
    ("interpretability-scope", "Interpretability scope", "An interpretation must declare model version, layers, prompts, data, behavior, intervention, and failure conditions before generalization.", "ai-machine-learning.interpretability"),
    ("mdp", "Markov decision process", "An MDP models states, actions, transition probabilities, rewards, and discounting under a Markov-state assumption.", "ai-machine-learning.reinforcement-learning"),
    ("rl-state", "Reinforcement-learning state", "A state contains information sufficient for modeled transition and reward prediction under the Markov assumption; observations may be only partial.", "ai-machine-learning.reinforcement-learning"),
    ("rl-action", "Reinforcement-learning action", "An action is a policy-selected intervention whose availability and consequences depend on state and environment.", "ai-machine-learning.reinforcement-learning"),
    ("reward", "Reward signal", "A reward is a scalar feedback signal defined by the environment or designer and is not identical to human value or long-term utility.", "ai-machine-learning.reinforcement-learning"),
    ("policy", "Policy", "A policy maps states or observations to action distributions.", "ai-machine-learning.reinforcement-learning"),
    ("return", "Discounted return", "Return aggregates future rewards along a trajectory under a horizon and discount convention.", "ai-machine-learning.reinforcement-learning"),
    ("value", "State value", "A value function estimates expected return from a state under a policy and environment model.", "ai-machine-learning.reinforcement-learning"),
    ("q-value", "Action value", "An action-value function estimates expected return after selecting an action in a state and then following a policy.", "ai-machine-learning.reinforcement-learning"),
    ("bellman", "Bellman relation", "A Bellman relation decomposes value into immediate reward and expected discounted successor value.", "ai-machine-learning.reinforcement-learning"),
    ("exploration", "Exploration", "Exploration chooses information-gathering actions whose opportunity cost and safety must be balanced against exploitation.", "ai-machine-learning.reinforcement-learning"),
    ("on-policy", "On-policy learning", "On-policy learning estimates or improves the same policy that generates the relevant behavior data.", "ai-machine-learning.reinforcement-learning"),
    ("off-policy", "Off-policy learning", "Off-policy learning uses data generated by another behavior policy and must correct or bound distribution mismatch.", "ai-machine-learning.reinforcement-learning"),
    ("actor-critic", "Actor-critic", "Actor-critic methods pair a parameterized policy actor with a learned value critic that supplies lower-variance update information.", "ai-machine-learning.reinforcement-learning"),
    ("autoregressive", "Autoregressive generation", "Autoregressive generation factorizes a joint distribution into ordered conditional predictions sampled or selected one step at a time.", "ai-machine-learning.generative-models"),
    ("diffusion", "Diffusion model", "A diffusion model learns to reverse a progressive noising process or its score-related equivalent to generate samples from noise.", "ai-machine-learning.generative-models"),
    ("latent-model", "Latent-variable model", "A latent-variable model represents observations through unobserved variables whose inference and prior shape generation and uncertainty.", "ai-machine-learning.generative-models"),
    ("sampler", "Generative sampler", "A sampler converts model scores or probabilities into one output trajectory under temperature, truncation, guidance, seed, and stopping rules.", "ai-machine-learning.generative-models"),
    ("temperature", "Sampling temperature", "Temperature rescales logits before normalization, altering distribution entropy but not repairing model beliefs or unsupported content.", "ai-machine-learning.generative-models"),
    ("top-p", "Nucleus sampling", "Nucleus sampling retains the smallest token set reaching a cumulative probability threshold and samples after renormalization.", "ai-machine-learning.generative-models"),
    ("guidance", "Generative guidance", "Guidance modifies a generative trajectory toward a condition or preference and can trade diversity, fidelity, artifacts, and distribution shift.", "ai-machine-learning.generative-models"),
    ("image-tensor", "Image tensor", "An image tensor represents sampled spatial channels under color, range, layout, resolution, and preprocessing conventions.", "ai-machine-learning.computer-vision"),
    ("convolution", "Convolutional layer", "A convolution applies shared local kernels across spatial positions, encoding translation-related inductive bias under stride, padding, and dilation.", "ai-machine-learning.computer-vision"),
    ("receptive-field", "Receptive field", "A unit's receptive field is the input region that can influence it through the architecture, with theoretical and effective influence differing.", "ai-machine-learning.computer-vision"),
    ("augmentation", "Vision data augmentation", "Augmentation applies label-preserving or task-aware transformations whose validity depends on the target phenomenon.", "ai-machine-learning.computer-vision"),
    ("classification", "Image classification", "Image classification assigns one or more labels to an input under a defined class ontology and decision threshold.", "ai-machine-learning.computer-vision"),
    ("detection", "Object detection", "Object detection estimates object classes and spatial regions with matching, overlap, confidence, and missed-object metrics.", "ai-machine-learning.computer-vision"),
    ("segmentation", "Image segmentation", "Segmentation assigns classes or instances at pixel or region resolution under boundary and class-imbalance evaluation.", "ai-machine-learning.computer-vision"),
    ("vision-transformer", "Vision transformer", "A vision transformer represents image patches or features as tokens processed by attention, positional information, and feed-forward blocks.", "ai-machine-learning.computer-vision"),
    ("waveform", "Audio waveform", "A waveform samples signal amplitude over time under a sampling rate, bit depth, channel, calibration, and clipping convention.", "ai-machine-learning.speech-audio"),
    ("stft", "Short-time Fourier transform", "An STFT maps overlapping windowed waveform segments into time-frequency coefficients under window, hop, and transform choices.", "ai-machine-learning.speech-audio"),
    ("spectrogram", "Spectrogram", "A spectrogram represents magnitude, power, phase, or derived frequency features over time and is not identical to the original waveform.", "ai-machine-learning.speech-audio"),
    ("asr", "Automatic speech recognition", "ASR maps speech audio to text or tokens under acoustic, language, speaker, environment, segmentation, and decoding assumptions.", "ai-machine-learning.speech-audio"),
    ("tts", "Text-to-speech synthesis", "TTS maps text and conditioning such as speaker, language, style, and prosody into acoustic features or waveforms.", "ai-machine-learning.speech-audio"),
    ("vocoder", "Neural vocoder", "A vocoder converts acoustic representations into waveform samples under fidelity, speed, conditioning, and artifact tradeoffs.", "ai-machine-learning.speech-audio"),
    ("model-registry", "Model registry", "A model registry stores immutable artifact identity, configuration, lineage, evaluation, approvals, intended use, and lifecycle state.", "ai-machine-learning.mlop"),
    ("ml-pipeline", "ML pipeline", "An ML pipeline connects versioned ingestion, validation, transformation, training, evaluation, packaging, deployment, and monitoring steps with recorded inputs and outputs.", "ai-machine-learning.mlop"),
    ("data-validation", "ML data validation", "Data validation checks schema, ranges, distributions, identities, missingness, leakage, and policy before examples enter training or inference.", "ai-machine-learning.mlop"),
    ("serving", "Model serving", "Model serving maps versioned requests through preprocessing, batching, model execution, decoding, policy, and response handling under capacity and security limits.", "ai-machine-learning.mlop"),
    ("shadow", "Shadow deployment", "A shadow deployment runs a candidate on copied production inputs without controlling user outcomes and compares behavior under privacy and load constraints.", "ai-machine-learning.mlop"),
    ("canary", "Model canary", "A canary exposes a candidate to a bounded population under predeclared quality, safety, latency, and rollback gates.", "ai-machine-learning.mlop"),
    ("drift", "Model drift", "Drift is a change in input, target, relationship, use, or measurement distribution that can alter model validity.", "ai-machine-learning.mlop"),
    ("monitoring", "Model monitoring", "Monitoring measures inputs, outputs, latency, errors, feedback, outcomes, subgroup behavior, abuse, and drift with alert and response ownership.", "ai-machine-learning.mlop"),
    ("rollback", "Model rollback", "Rollback restores a prior compatible artifact, preprocessing, policy, and state path when a deployed candidate violates a gate.", "ai-machine-learning.mlop"),
    ("accelerator", "ML accelerator", "An ML accelerator provides specialized parallel computation, memory, and communication for tensor operations under a device programming model.", "ai-machine-learning.accelerators"),
    ("device-memory", "Accelerator memory hierarchy", "Accelerator performance depends on registers, on-chip buffers or caches, high-bandwidth memory, host memory, transfer, placement, and reuse.", "ai-machine-learning.accelerators"),
    ("matmul", "Matrix multiplication kernel", "Matrix multiplication maps tiled operands through parallel multiply-accumulate units under shape, layout, precision, and accumulation constraints.", "ai-machine-learning.accelerators"),
    ("jit-compile", "Accelerator JIT compilation", "JIT tracing and compilation specialize array programs by shapes, dtypes, static values, sharding, and target while constraining dynamic Python effects.", "ai-machine-learning.accelerators"),
    ("device-sharding", "Device sharding", "Device sharding maps tensor dimensions and replicas onto a device mesh and determines communication required by each operation.", "ai-machine-learning.accelerators"),
    ("collective", "Accelerator collective", "A collective such as all-reduce, all-gather, reduce-scatter, or all-to-all coordinates data among a device group under ordering and topology costs.", "ai-machine-learning.accelerators"),
    ("tpu-topology", "TPU topology", "A TPU topology describes available devices and interconnect relations that qualify sharding, collective cost, and fault scope.", "ai-machine-learning.accelerators"),
    ("host-device", "Host-device boundary", "Host-device transfer and synchronization cross execution domains and can serialize an otherwise parallel program if introduced implicitly.", "ai-machine-learning.accelerators"),
    ("data-provenance", "Training-data provenance", "Data provenance records origin, collection, transformations, versions, custodians, and lineage into training and evaluation artifacts.", "ai-machine-learning.data-governance"),
    ("data-rights", "Training-data rights", "Training-data rights record license, consent, contract, jurisdiction, attribution, purpose, and redistribution or model-training restrictions.", "ai-machine-learning.data-governance"),
    ("data-consent", "Data consent", "Consent is specific to actor, purpose, data, use, recipients, duration, and withdrawal conditions and is not inferred from public accessibility alone.", "ai-machine-learning.data-governance"),
    ("representativeness", "Dataset representativeness", "Representativeness describes how a dataset covers the target population, contexts, groups, and mechanisms rather than its size alone.", "ai-machine-learning.data-governance"),
    ("label-process", "Labeling process", "A labeling process defines annotators, instructions, tools, ambiguity, quality control, agreement, adjudication, and affected perspectives.", "ai-machine-learning.data-governance"),
    ("dedup", "Dataset deduplication", "Deduplication identifies identical or near-related examples under a declared similarity rule to manage leakage, weighting, privacy, and memorization.", "ai-machine-learning.data-governance"),
    ("pii", "Sensitive training data", "Sensitive data includes direct identifiers, linkable attributes, private content, secrets, and inferred traits requiring minimization and access controls.", "ai-machine-learning.data-governance"),
    ("retention", "Training-data retention", "Retention defines how long raw, processed, labeled, cached, and derived data is stored and how deletion propagates through artifacts where feasible.", "ai-machine-learning.data-governance"),
    ("datasheet", "Dataset datasheet", "A dataset datasheet documents motivation, composition, collection, processing, uses, distribution, maintenance, risks, and known limits for a versioned dataset.", "ai-machine-learning.data-governance"),
    ("model-card", "Model card", "A model card documents identity, intended and excluded uses, training context, evaluations, subgroup behavior, risks, limitations, and maintenance for a versioned model.", "ai-machine-learning.data-governance"),
]


RELATIONS = [
    ("task-data", "ai.task", "ai.example", "qualifies", "The task and use context qualify what constitutes a relevant learning example."),
    ("example-feature", "ai.feature", "ai.example", "part_of", "Features form part of a learning example."),
    ("example-label", "ai.label", "ai.example", "part_of", "A target label can form part of supervised learning evidence."),
    ("model-parameter", "ai.parameter", "ai.model", "part_of", "Learned parameters form part of a model artifact."),
    ("loss-model", "ai.loss", "ai.model", "qualifies", "The optimization loss qualifies which model behaviors training rewards."),
    ("loss-risk", "ai.loss", "ai.empirical-risk", "part_of", "Example losses are aggregated into empirical risk."),
    ("train-parameter", "ai.train-split", "ai.parameter", "causes", "Optimization over the training split causes fitted parameter values."),
    ("validation-hyper", "ai.validation-split", "ai.hyperparameter", "qualifies", "Validation outcomes qualify hyperparameter and model selection."),
    ("test-general", "ai.test-split", "ai.generalization", "measures", "A sealed test measures selected generalization after choices are frozen."),
    ("distribution-split", "ai.distribution", "ai.train-split", "qualifies", "Sampling and population relations qualify the training distribution."),
    ("iid-general", "ai.iid", "ai.generalization", "qualifies", "IID assumptions qualify which generalization estimate is justified."),
    ("overfit-validation", "ai.overfit", "ai.generalization", "inhibits", "Overfitting to development evidence inhibits target generalization."),
    ("underfit-train", "ai.underfit", "ai.empirical-risk", "causes", "Underfitting can cause persistently high training loss."),
    ("regular-general", "ai.regularization", "ai.generalization", "supports", "Appropriate regularization can support generalization."),
    ("calibration-prob", "ai.calibration", "ai.metric", "measures", "Calibration metrics measure probability-frequency agreement under a population definition."),
    ("predict-causal", "ai.predictive-causal", "ai.model", "qualifies", "The prediction-causation boundary qualifies interpretations of model associations."),
    ("tensor-layer", "ai.tensor", "ai.layer", "prerequisite", "Tensors are inputs and outputs of neural layers."),
    ("activation-layer", "ai.activation", "ai.layer", "part_of", "Activation functions form part of many neural layers."),
    ("layer-graph", "ai.layer", "ai.computation-graph", "part_of", "Layer operations compose a computation graph."),
    ("graph-autodiff", "ai.computation-graph", "ai.autodiff", "prerequisite", "A differentiable operation graph is prerequisite to reverse automatic differentiation."),
    ("autodiff-backprop", "ai.autodiff", "ai.backprop", "implements", "Reverse-mode automatic differentiation implements backpropagation through the graph."),
    ("backprop-gradient", "ai.backprop", "ai.gradient", "causes", "Backpropagation causes gradient accumulation for parameters."),
    ("batch-gradient", "ai.minibatch", "ai.gradient", "qualifies", "The selected minibatch qualifies the stochastic gradient estimate."),
    ("normal-layer", "ai.normalization", "ai.layer", "qualifies", "Normalization qualifies activation scale and training versus inference behavior."),
    ("residual-layer", "ai.residual", "ai.layer", "part_of", "Residual paths form part of deep blocks."),
    ("dropout-general", "ai.dropout", "ai.regularization", "implements", "Dropout implements one stochastic regularization mechanism."),
    ("embedding-layer", "ai.embedding", "ai.layer", "implements", "An embedding layer implements a discrete-to-continuous lookup."),
    ("token-vocab", "ai.vocabulary", "ai.tokenizer", "qualifies", "Vocabulary and normalization rules qualify tokenization."),
    ("token-embed", "ai.tokenizer", "ai.token-embedding", "prerequisite", "Token identifiers are prerequisite to embedding lookup."),
    ("position-attention", "ai.position", "ai.attention-score", "qualifies", "Positional information qualifies attention scores or representations."),
    ("qkv-score", "ai.query-key-value", "ai.attention-score", "causes", "Query and key projections cause pairwise attention scores."),
    ("mask-score", "ai.causal-mask", "ai.attention-score", "qualifies", "The causal mask qualifies which attention logits can contribute."),
    ("score-output", "ai.attention-score", "ai.attention-output", "causes", "Normalized scores cause weighted value aggregation."),
    ("multi-output", "ai.multihead", "ai.attention-output", "implements", "Multiple projection heads implement multi-head attention aggregation."),
    ("attention-block", "ai.attention-output", "ai.transformer-block", "part_of", "Attention output forms part of a transformer block."),
    ("ffn-block", "ai.ffn", "ai.transformer-block", "part_of", "The feed-forward sublayer forms part of a transformer block."),
    ("residual-block", "ai.residual", "ai.transformer-block", "part_of", "Residual pathways form part of transformer blocks."),
    ("block-decoder", "ai.transformer-block", "ai.decoder", "part_of", "Stacked transformer blocks form an autoregressive decoder."),
    ("decoder-logit", "ai.decoder", "ai.logit", "causes", "The decoder maps a prefix representation to next-token logits."),
    ("context-decoder", "ai.context-window", "ai.decoder", "qualifies", "Context length qualifies the prefix information available to a decoder."),
    ("cache-attention", "ai.kv-cache", "ai.query-key-value", "supports", "A KV cache supports reuse of prior key and value projections."),
    ("pretrain-decoder", "ai.pretraining", "ai.decoder", "causes", "Autoregressive pretraining causes decoder parameters to fit next-token prediction."),
    ("instruction-pretrain", "ai.pretraining", "ai.instruction-tuning", "prerequisite", "A pretrained model commonly provides the starting parameters for instruction tuning."),
    ("tool-host", "ai.tool-use", "ai.defense-layer", "qualifies", "Host authorization and isolation qualify model-proposed tool use."),
    ("retrieval-ground", "ai.retrieval-augmentation", "ai.grounding", "supports", "Source-preserving retrieval supports grounded generation."),
    ("hallucination-ground", "ai.grounding", "ai.hallucination", "inhibits", "Evidence checking inhibits unsupported factual generation."),
    ("moe-block", "ai.mixture-experts", "ai.transformer-block", "qualifies", "Expert routing qualifies the feed-forward computation in a mixture model."),
    ("gradient-optimizer", "ai.gradient", "ai.optimizer", "prerequisite", "Gradients are inputs to gradient-based optimizer updates."),
    ("lr-optimizer", "ai.learning-rate", "ai.optimizer", "qualifies", "Learning rate qualifies optimizer update magnitude."),
    ("schedule-lr", "ai.schedule", "ai.learning-rate", "transforms_to", "A schedule transforms the learning rate over training progress."),
    ("precision-gradient", "ai.mixed-precision", "ai.gradient", "qualifies", "Numerical precision qualifies gradient range and error."),
    ("scale-precision", "ai.loss-scale", "ai.mixed-precision", "supports", "Loss scaling supports low-precision gradient range."),
    ("clip-gradient", "ai.gradient-clip", "ai.gradient", "transforms_to", "Clipping transforms a gradient before the update."),
    ("accum-gradient", "ai.gradient-accum", "ai.gradient", "transforms_to", "Accumulation combines microbatch gradients into one update estimate."),
    ("data-batch", "ai.data-parallel", "ai.minibatch", "qualifies", "Data parallelism qualifies how a global batch is partitioned and reduced."),
    ("tensor-matmul", "ai.tensor-parallel", "ai.matmul", "qualifies", "Tensor parallelism qualifies matrix dimension sharding and collectives."),
    ("pipeline-block", "ai.pipeline-parallel", "ai.transformer-block", "qualifies", "Pipeline parallelism qualifies stage placement and microbatch scheduling."),
    ("shard-state", "ai.sharding", "ai.parameter", "qualifies", "Sharding qualifies parameter and optimizer-state placement."),
    ("checkpoint-optimizer", "ai.checkpoint", "ai.optimizer", "supports", "A complete checkpoint supports faithful optimizer resume."),
    ("seed-run", "ai.seed", "ai.training-curve", "qualifies", "Seed and runtime versions qualify a recorded training trajectory."),
    ("curve-optimizer", "ai.training-curve", "ai.optimizer", "measures", "Training curves measure optimizer progress and instability."),
    ("metric-benchmark", "ai.metric", "ai.benchmark", "part_of", "Metrics form part of a benchmark protocol."),
    ("contamination-test", "ai.contamination", "ai.test-split", "undercuts", "Test contamination undercuts a sealed generalization claim."),
    ("strata-metric", "ai.stratification", "ai.metric", "qualifies", "Stratification qualifies aggregate metrics by relevant subpopulations."),
    ("interval-metric", "ai.confidence-interval", "ai.metric", "qualifies", "Sampling uncertainty qualifies a metric estimate."),
    ("robust-benchmark", "ai.robustness", "ai.benchmark", "part_of", "Robustness suites form one benchmark component."),
    ("ood-general", "ai.ood", "ai.generalization", "measures", "OOD evaluation measures one form of shifted generalization."),
    ("human-metric", "ai.human-eval", "ai.metric", "implements", "A rater rubric implements a human evaluation metric."),
    ("red-threat", "ai.red-team", "ai.ai-threat-model", "supports", "Authorized red-team tests support evaluation of threat-model hypotheses."),
    ("performance-benchmark", "ai.system-performance", "ai.benchmark", "part_of", "Serving performance forms a separate benchmark family from output quality."),
    ("misspec-loss", "ai.loss", "ai.objective-misspec", "enables", "A proxy loss can enable objective misspecification when it omits stakeholder constraints."),
    ("spec-preference", "ai.behavior-spec", "ai.preference-data", "qualifies", "Behavior specifications qualify preference rubrics and examples."),
    ("preference-opt", "ai.preference-data", "ai.preference-optimization", "prerequisite", "Preference evidence is prerequisite to data-driven preference optimization."),
    ("abstain-spec", "ai.behavior-spec", "ai.abstention", "qualifies", "The behavior specification qualifies when abstention or escalation is required."),
    ("ground-spec", "ai.grounding", "ai.behavior-spec", "supports", "Grounded evidence supports factual behavior requirements."),
    ("oversight-risk", "ai.oversight", "ai.risk-owner", "supports", "Effective oversight supports accountable risk decisions."),
    ("threat-defense", "ai.ai-threat-model", "ai.defense-layer", "qualifies", "The threat model qualifies which layered defenses are necessary."),
    ("risk-deploy", "ai.risk-owner", "ai.canary", "qualifies", "Risk ownership qualifies canary stop and expansion decisions."),
    ("feature-probe", "ai.probe", "ai.feature-representation", "measures", "A probe measures decodable information in a representation."),
    ("attribute-faith", "ai.attribution", "ai.faithfulness", "qualifies", "Faithfulness tests qualify interpretation of attribution results."),
    ("intervention-mechanism", "ai.activation-intervention", "ai.mechanistic-hypothesis", "supports", "Targeted interventions support causal mechanism hypotheses."),
    ("scope-mechanism", "ai.interpretability-scope", "ai.mechanistic-hypothesis", "qualifies", "Version and behavior scope qualify mechanistic claims."),
    ("mdp-state", "ai.rl-state", "ai.mdp", "part_of", "States form part of an MDP."),
    ("mdp-action", "ai.rl-action", "ai.mdp", "part_of", "Actions form part of an MDP."),
    ("mdp-reward", "ai.reward", "ai.mdp", "part_of", "Rewards form part of an MDP."),
    ("policy-action", "ai.policy", "ai.rl-action", "causes", "A policy causes an action distribution conditioned on state or observation."),
    ("reward-return", "ai.reward", "ai.return", "part_of", "Trajectory rewards aggregate into return."),
    ("return-value", "ai.return", "ai.value", "grounds", "Expected return grounds the definition of a value function."),
    ("q-value", "ai.q-value", "ai.value", "qualifies", "Action value qualifies expected return by a selected first action."),
    ("bellman-value", "ai.bellman", "ai.value", "clarifies", "The Bellman relation clarifies recursive value decomposition."),
    ("explore-policy", "ai.exploration", "ai.policy", "qualifies", "Exploration qualifies policy action selection toward information gain."),
    ("on-policy", "ai.on-policy", "ai.policy", "qualifies", "On-policy data is generated by the evaluated or improved policy."),
    ("off-policy", "ai.off-policy", "ai.policy", "qualifies", "Off-policy learning qualifies updates by behavior-policy mismatch."),
    ("actor-policy", "ai.actor-critic", "ai.policy", "implements", "The actor implements a parameterized policy."),
    ("critic-value", "ai.actor-critic", "ai.value", "implements", "The critic implements a learned value estimate."),
    ("decoder-auto", "ai.decoder", "ai.autoregressive", "implements", "A causal decoder implements autoregressive conditional generation."),
    ("diffusion-sampler", "ai.diffusion", "ai.sampler", "qualifies", "The learned reverse process qualifies diffusion sampling steps."),
    ("latent-sampler", "ai.latent-model", "ai.sampler", "qualifies", "Latent variables qualify the distribution sampled into observations."),
    ("temperature-logit", "ai.temperature", "ai.logit", "transforms_to", "Temperature transforms logit scale before sampling."),
    ("topp-sampler", "ai.top-p", "ai.sampler", "qualifies", "Nucleus threshold qualifies the candidate set for each sampling step."),
    ("guidance-sampler", "ai.guidance", "ai.sampler", "transforms_to", "Guidance transforms a model trajectory toward a condition."),
    ("image-conv", "ai.image-tensor", "ai.convolution", "prerequisite", "Image tensors are inputs to convolutional layers."),
    ("conv-field", "ai.convolution", "ai.receptive-field", "causes", "Stacked local kernels cause a growing theoretical receptive field."),
    ("augment-distribution", "ai.augmentation", "ai.distribution", "transforms_to", "Augmentation transforms the effective training distribution."),
    ("class-task", "ai.classification", "ai.task", "part_of", "Classification is one machine-learning task family."),
    ("detect-task", "ai.detection", "ai.task", "part_of", "Object detection is one spatial prediction task."),
    ("segment-task", "ai.segmentation", "ai.task", "part_of", "Segmentation is one dense prediction task."),
    ("vit-transformer", "ai.vision-transformer", "ai.transformer-block", "implements", "Vision transformers implement attention over image-derived tokens."),
    ("wave-stft", "ai.waveform", "ai.stft", "transforms_to", "The STFT transforms a waveform into time-frequency coefficients."),
    ("stft-spectrogram", "ai.stft", "ai.spectrogram", "causes", "Magnitude or power transforms of STFT coefficients cause a spectrogram representation."),
    ("spectrogram-asr", "ai.spectrogram", "ai.asr", "supports", "Time-frequency features can support speech recognition."),
    ("tts-vocoder", "ai.tts", "ai.vocoder", "qualifies", "A TTS acoustic model can condition a vocoder."),
    ("registry-model", "ai.model", "ai.model-registry", "part_of", "Versioned model artifacts form entries in a model registry."),
    ("pipeline-data", "ai.data-validation", "ai.ml-pipeline", "part_of", "Data validation forms part of an ML pipeline."),
    ("pipeline-registry", "ai.ml-pipeline", "ai.model-registry", "causes", "A passing pipeline causes registration of an identified candidate artifact."),
    ("registry-serving", "ai.model-registry", "ai.serving", "prerequisite", "An approved artifact identity is prerequisite to controlled serving."),
    ("shadow-canary", "ai.shadow", "ai.canary", "prerequisite", "Shadow evidence can precede user-impacting canary exposure."),
    ("canary-monitor", "ai.monitoring", "ai.canary", "prerequisite", "Monitoring and stop gates are prerequisites to a controlled canary."),
    ("drift-monitor", "ai.monitoring", "ai.drift", "measures", "Monitoring measures selected forms of distribution and behavior drift."),
    ("monitor-rollback", "ai.monitoring", "ai.rollback", "causes", "A breached predeclared gate can cause model rollback."),
    ("accelerator-matmul", "ai.matmul", "ai.accelerator", "part_of", "Matrix multiplication is a central accelerator workload."),
    ("memory-matmul", "ai.device-memory", "ai.matmul", "qualifies", "Memory layout and reuse qualify matrix-kernel throughput."),
    ("jit-accelerator", "ai.jit-compile", "ai.accelerator", "supports", "JIT compilation supports target-specialized accelerator execution."),
    ("shard-device", "ai.device-sharding", "ai.sharding", "implements", "Device sharding implements logical tensor partitioning on a mesh."),
    ("collective-shard", "ai.collective", "ai.device-sharding", "qualifies", "Collectives qualify communication induced by a sharding layout."),
    ("topology-collective", "ai.tpu-topology", "ai.collective", "qualifies", "TPU topology qualifies collective latency and bandwidth."),
    ("host-jit", "ai.host-device", "ai.jit-compile", "qualifies", "Host-device synchronization qualifies compiled execution and throughput."),
    ("provenance-datasheet", "ai.data-provenance", "ai.datasheet", "part_of", "Data lineage forms part of a dataset datasheet."),
    ("rights-data", "ai.data-rights", "ai.train-split", "qualifies", "Rights and purpose restrictions qualify which data may enter training."),
    ("consent-rights", "ai.data-consent", "ai.data-rights", "part_of", "Consent can form one component of lawful and ethical data rights."),
    ("represent-general", "ai.representativeness", "ai.generalization", "qualifies", "Dataset coverage qualifies generalization to the target population."),
    ("label-process", "ai.label-process", "ai.label", "causes", "The labeling process causes recorded target judgments."),
    ("dedup-contam", "ai.dedup", "ai.contamination", "inhibits", "Mechanism-aware deduplication inhibits some train-test contamination."),
    ("pii-minimize", "ai.pii", "ai.data-rights", "qualifies", "Sensitive-data presence qualifies access, minimization, and training permission."),
    ("retention-provenance", "ai.retention", "ai.data-provenance", "qualifies", "Retention and deletion events qualify data lineage over time."),
    ("card-registry", "ai.model-card", "ai.model-registry", "part_of", "A model card forms part of a registry's release evidence."),
    ("bridge-data-objective", "ai.datasheet", "ai.objective-misspec", "inhibits", "Dataset documentation inhibits silent mismatch between collected evidence and intended objective."),
    ("bridge-eval-risk", "ai.stratification", "ai.risk-owner", "supports", "Stratified evaluation supports accountable risk decisions for affected groups."),
    ("bridge-serving-grounding", "ai.serving", "ai.grounding", "qualifies", "The serving host qualifies retrieval, tool, and evidence checks around model generation."),
    ("bridge-tpu-training", "ai.tpu-topology", "ai.data-parallel", "qualifies", "TPU topology qualifies data-parallel replication and gradient collective structure."),
]


CONTROLS = [
    ("large-exhaustive", "Large dataset means exhaustive", "Dataset size must not be treated as exhaustive coverage of mechanisms, populations, tails, contexts, or future shifts."),
    ("benchmark-general", "Benchmark score proves general intelligence", "A benchmark score must not be generalized beyond its tasks, data, protocol, contamination controls, and measured properties."),
    ("test-tune", "Repeated sealed-test tuning", "A sealed test must not remain labeled sealed after its examples or aggregate outcomes guide model, prompt, threshold, or hyperparameter changes."),
    ("loss-value", "Low loss equals stakeholder value", "Lower proxy loss must not be treated as improved real-world value or safety without outcome evidence."),
    ("accuracy-causal", "Prediction proves causation", "Predictive accuracy must not support intervention claims without causal assumptions and evidence."),
    ("confidence-correct", "High model probability means correct", "A high internal probability must not be treated as calibrated correctness outside a validated population."),
    ("train-eval-mode", "Training and inference modes are identical", "Dropout, normalization, stochastic layers, quantization, and decoding must not be assumed identical between training and inference."),
    ("gradient-global", "Gradient points to global optimum", "A local gradient must not be described as a guarantee of global improvement under a finite nonlinear update."),
    ("seed-reproduce", "Seed alone guarantees reproduction", "A seed must not substitute for code, data, topology, operation, precision, ordering, library, and hardware identity."),
    ("checkpoint-weights", "Weights alone are complete checkpoint", "Model weights must not be described as a faithful training resume without optimizer, scheduler, random, data, and configuration state."),
    ("token-word", "Token equals word", "A model token must not be treated as a linguistic word across tokenizers, languages, bytes, and special symbols."),
    ("attention-explanation", "Attention weight is explanation", "An attention weight must not be presented as a faithful causal explanation without intervention and alternative-mechanism tests."),
    ("context-memory", "Context window is durable memory", "Tokens supplied to one invocation must not be described as persistent learned or durable memory after the context is removed."),
    ("retrieval-truth", "Retrieved passage is true", "Retrieval relevance must not be treated as source authority, currency, or entailment."),
    ("tool-authority", "Model tool call grants authority", "A model-proposed tool call must not expand host authorization or bypass schema, capability, and side-effect checks."),
    ("pretrain-fact", "Pretraining stores verified facts", "Next-token pretraining must not be described as a verified factual database with source-level provenance."),
    ("fluent-grounded", "Fluency means grounded", "Fluent prose must not be treated as supported when no source, proof, execution, or observation warrants its material claims."),
    ("temperature-knowledge", "Temperature changes knowledge", "Sampling temperature changes output distribution but must not be described as improving factual knowledge or reasoning correctness."),
    ("mixed-equal", "Mixed precision is exact", "Low-precision training must not be treated as numerically identical to full precision without error and stability evidence."),
    ("more-steps-better", "More training steps always improve", "Additional optimization must not be assumed beneficial after overfitting, divergence, forgetting, or objective mismatch begins."),
    ("aggregate-fair", "Aggregate metric proves subgroup quality", "An aggregate metric must not hide materially different subgroup, intersectional, language, or tail behavior."),
    ("interval-bias", "Confidence interval covers systematic bias", "A sampling interval must not be treated as accounting for label error, contamination, construct invalidity, or distribution mismatch."),
    ("human-objective", "Human rating is objective ground truth", "Human evaluation must retain rater disagreement, rubric effects, cultural context, fatigue, and sampling limitations."),
    ("red-safe", "Red-team prompt is safe everywhere", "A red-team procedure must not leave authorized scope, expose unrelated data, or become a reusable harm-enabling artifact without controls."),
    ("preference-values", "Preference data equals universal values", "Recorded preferences must not be treated as unanimous or universal human values across contexts and populations."),
    ("alignment-complete", "One alignment method completes safety", "Preference tuning, filtering, prompting, or policy alone must not be treated as a complete AI safety system."),
    ("oversight-rubber", "Human in loop guarantees safety", "Human review must not be treated as effective when evidence, authority, time, incentives, or workload make intervention impractical."),
    ("probe-use", "Probe decodability proves model use", "Information decoded by a probe must not establish that the model uses that information in the target behavior."),
    ("attribution-cause", "Attribution proves causal mechanism", "Attribution magnitude must not be promoted to causal mechanism without intervention and faithfulness evidence."),
    ("reward-value", "Reward equals desired behavior", "A reward signal must not be treated as complete human or stakeholder value, especially off the training distribution."),
    ("offline-policy", "Offline RL ignores behavior policy", "Off-policy learning must not ignore coverage and distribution mismatch between logged behavior and candidate actions."),
    ("diffusion-deterministic", "Diffusion seed defines universal output", "A sampling seed must not be treated as portable output identity across scheduler, precision, device, library, and model versions."),
    ("augmentation-valid", "Every image transform preserves label", "An augmentation must not be applied as label-preserving when orientation, color, scale, text, or context changes the task target."),
    ("spectrogram-wave", "Spectrogram is lossless waveform", "A magnitude spectrogram must not be treated as preserving waveform phase and every invertible detail."),
    ("registry-approved", "Registry presence means approved", "A model registry entry must not imply deployment approval unless evidence and lifecycle state explicitly say so."),
    ("shadow-no-effect", "Shadow deployment has no impact", "Shadow inference must not be treated as impact-free when it consumes resources, copies sensitive data, logs outputs, or calls dependencies."),
    ("drift-failure", "No detected drift means no failure", "Stable input statistics must not prove model outcomes, targets, abuse patterns, or measurement systems remain valid."),
    ("accelerator-used", "Accelerator visibility proves training", "Listing a TPU or GPU device must not prove the training state and heavy computation actually executed there."),
    ("util-quality", "High utilization proves useful training", "Accelerator utilization must not substitute for loss, generalization, correctness, and sealed evaluation evidence."),
    ("public-permission", "Public data means training permission", "Public accessibility must not be treated as license, consent, privacy clearance, or permission for model training."),
    ("datasheet-safe", "Datasheet proves dataset safe", "Dataset documentation must not be treated as proof that recorded facts are complete, current, lawful, representative, or harmless."),
    ("card-capability", "Model card creates capability", "A model-card claim must not replace reproducible evaluation of the exact artifact, adapter, and deployment path."),
]


WORKED_EXAMPLES = [
    ("split-group", "Mechanism-first data split", "A worked split assigns all paraphrases and variants of one causal mechanism to a single partition before augmentation, preventing template leakage into validation and sealed tests.", "ai-machine-learning.ml-foundations"),
    ("backprop", "Backpropagation dependency", "A scalar loss depends on two branches sharing a parameter; reverse traversal accumulates both partial contributions before one optimizer update.", "ai-machine-learning.deep-learning"),
    ("attention-mask", "Causal attention mask", "A four-token score matrix masks every future column before softmax, so position two can aggregate positions one and two but never positions three or four.", "ai-machine-learning.transformers-llms"),
    ("resume", "Faithful distributed resume", "A training resume restores sharded parameters, optimizer moments, schedule step, RNG streams, dataset cursor, precision, mesh, and exact code before comparing the next loss.", "ai-machine-learning.training-optimization"),
    ("stratified-eval", "Stratified sealed evaluation", "A benchmark reports per-domain, per-language, per-length, and cross-domain results with intervals, then rejects the model because one mandatory subgroup fails despite a passing aggregate.", "ai-machine-learning.evaluation"),
    ("grounded-tool", "Grounded tool execution", "A model proposes a typed calculation, the host checks authority and schema, an exact runtime and independent oracle agree, and only the receipt-backed result may support the answer.", "ai-machine-learning.alignment-safety"),
    ("intervention", "Mechanistic intervention", "A probe decodes a feature, but only patching the hypothesized activation predictably changes the target output while matched controls do not, strengthening the causal hypothesis.", "ai-machine-learning.interpretability"),
    ("off-policy", "Off-policy coverage limit", "Logged behavior never chose one action in a state region, so an evaluator marks the candidate policy value there unidentified instead of extrapolating without support.", "ai-machine-learning.reinforcement-learning"),
    ("sampling", "Constrained sampling", "A decoder applies temperature and nucleus truncation only after hard schema tokens are constrained, then records seed, model, tokenizer, sampler, and stop condition.", "ai-machine-learning.generative-models"),
    ("vision-augment", "Task-aware augmentation", "Horizontal reflection is admitted for generic object presence but rejected for text recognition and laterality labels because it changes the target meaning.", "ai-machine-learning.computer-vision"),
    ("canary", "Model canary rollback", "A candidate serves five percent of traffic; subgroup error and tail latency cross frozen gates, so routing returns to the prior artifact while inputs and receipts remain available for diagnosis.", "ai-machine-learning.mlop"),
    ("tpu-evidence", "TPU execution evidence", "A training receipt records eight TPU devices, places arrays and compiled updates on a TPU device, captures framework and topology, and rejects CPU smoke output as accelerator validation.", "ai-machine-learning.accelerators"),
]


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 41 == 0:
        return "cross_domain_holdout"
    if index % 31 == 0:
        return "sealed_test"
    if index % 23 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 37 == 0:
        return "cross_domain_holdout"
    if index and index % 29 == 0:
        return "sealed_test"
    if index and index % 19 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    subject: str,
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str = "established",
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": "ai-machine-learning",
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "AI and machine-learning development foundation tranche",
        "limitations": [
            "Architecture, library, accelerator, benchmark, and risk-management behavior is version and deployment sensitive.",
            "Empirical observations do not become causal claims without an identified design and assumptions.",
            "This foundation does not exhaust algorithms, modalities, populations, hazards, or the open research frontier.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "ai-development-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", "ai-machine-learning"],
    }


def sources_for_subject(subject: str) -> list[str]:
    if subject == "ai-machine-learning.transformers-llms":
        return ["attention-1706-03762", "huggingface-transformers"]
    if subject in {"ai-machine-learning.training-optimization", "ai-machine-learning.accelerators"}:
        return ["jax-documentation", "pytorch-213-docs", "mlperf-training"]
    if subject == "ai-machine-learning.alignment-safety":
        return ["nist-ai-rmf-10", "nist-ai-600-1", "model-cards"]
    if subject == "ai-machine-learning.reinforcement-learning":
        return ["sutton-barto-rl"]
    if subject == "ai-machine-learning.generative-models":
        return ["ddpm-2006-11239", "attention-1706-03762"]
    if subject == "ai-machine-learning.mlop":
        return ["model-cards", "mlperf-training", "nist-ai-rmf-10"]
    if subject == "ai-machine-learning.data-governance":
        return ["datasheets-datasets", "model-cards", "nist-ai-rmf-10"]
    return ["deep-learning-book", "nist-ai-rmf-10"]


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        node_id = f"ai.{identifier}"
        sources = sources_for_subject(subject)
        epistemic = "provisional" if subject == "ai-machine-learning.interpretability" else "established"
        records.append(
            {
                **make_base(
                    node_id, subject, sources, split_for(index, root=identifier == "root"),
                    "concept", epistemic,
                ),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
            }
        )
        if identifier != "root":
            membership_id = f"ai.membership.{identifier}"
            records.append(
                {
                    **make_base(membership_id, subject, sources, edge_split_for(index), "relation", epistemic),
                    "label": f"{label} AI-world membership",
                    "statement": f"{label} is a distinct component of the AI development evidence loop with explicit empirical and version limits.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": "ai.root",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared task, population, artifact, protocol, and version apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter(
        [kind for _identifier, _source, _target, kind, _statement in RELATIONS],
        cross_plan=[
            identifier.startswith("bridge-")
            for identifier, _source, _target, _kind, _statement in RELATIONS
        ],
    )
    for identifier, source_node, target_node, kind, statement in RELATIONS:
        records.append(
            {
                **make_base(
                    f"ai.relation.{identifier}", "ai-machine-learning.ml-foundations", SOURCES,
                    splitter.split(kind),
                    "relation",
                    "provisional" if "interpret" in identifier or "mechanism" in identifier else "established",
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
                    "conditions": ["the stated task, data distribution, model, protocol, deployment, and uncertainty assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        record_id = f"ai.control.{identifier}"
        records.append(
            {
                **make_base(
                    record_id, "ai-machine-learning.evaluation", [], control_splits[index % 4],
                    "synthetic_control", "synthetic_control",
                ),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", "ai-machine-learning"],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        split = example_splits[index % 4]
        sources = sources_for_subject(subject)
        node_id = f"ai.example.{identifier}"
        records.append(
            {
                **make_base(node_id, subject, sources, split, "worked_example"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", "ai-machine-learning"],
            }
        )
        membership_id = f"ai.example-membership.{identifier}"
        records.append(
            {
                **make_base(membership_id, subject, sources, split, "relation"),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded AI-development mechanism composition.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": "ai.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains task-specific and illustrative"],
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
