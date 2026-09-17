#!/usr/bin/env python3
"""Author a rights-safe literature, creative-writing, and technical-writing world."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "literature-writing" / "foundations.jsonl"
WORLD = "literature-writing-v0"

LIT_LANES = [
    "philosophy.analysis",
    "rhetoric.analysis",
    "thinking.lateral",
    "reasoning.analogical",
]
CREATIVE_LANES = [
    "creativity.generation_selection",
    "creativity.conceptual_blending",
    "creativity.constraint_based",
    "creativity.novelty_value",
    "creativity.problem_framing",
    "creativity.tension_transformation",
    "creativity.memory_recombination",
    "thinking.lateral",
]
TECHNICAL_LANES = [
    "rhetoric.analysis",
    "creativity.constraint_based",
    "reasoning.deductive",
    "thinking.bottom_up",
]

LIT_SOURCES = [
    "loc-lcgft-2025",
    "loc-lcgft-literature-manual",
    "gutenberg-aristotle-poetics",
]
CREATIVE_SOURCES = [
    "gutenberg-aristotle-poetics",
    "gutenberg-elements-style",
    "loc-lcgft-2025",
    "purdue-owl",
]
TECHNICAL_SOURCES = [
    "diataxis-documentation-framework",
    "google-developer-style",
    "gutenberg-elements-style",
    "rfc8174",
    "w3c-wcag-22",
]


# Statements are original summaries. Citation-only source text is never copied.
LITERATURE = [
    ("root", "Literary analysis", "Literary analysis constructs a warranted interpretation from textual form, language, genre, context, and counterreadings while distinguishing evidence from the interpreter's claims.", "literature.criticism"),
    ("story-discourse", "Story and discourse", "Narrative analysis distinguishes the represented events from the order, duration, frequency, and manner in which a work presents them.", "literature.narrative"),
    ("narrator", "Narrator", "A narrator is the textual voice that presents a narrative and must not automatically be identified with the historical author.", "literature.narrative"),
    ("narratee", "Narratee", "A narratee is the audience position addressed or implied inside a narrative rather than every actual reader.", "literature.narrative"),
    ("focalization", "Focalization", "Focalization tracks whose perceptual or cognitive access filters the represented world, independently of who grammatically narrates it.", "literature.narrative"),
    ("reliability", "Narrative reliability", "Reliability is an interpretation of how far a narrator's account aligns with other textual evidence, and it requires specific discrepancies rather than mere dislike.", "literature.narrative"),
    ("temporal-order", "Narrative temporal order", "Temporal order compares event chronology with presentation order, including retrospection, anticipation, and withheld intervals.", "literature.narrative"),
    ("duration", "Narrative duration", "Narrative duration compares the represented time of events with the textual space or performance time devoted to them.", "literature.narrative"),
    ("frequency", "Narrative frequency", "Narrative frequency compares how often an event occurs in the story with how often discourse recounts it.", "literature.narrative"),
    ("plot", "Plot", "Plot is the designed arrangement of actions, revelations, and consequences that produces an intelligible trajectory rather than a bare event list.", "literature.narrative"),
    ("causal-chain", "Narrative causal chain", "A narrative causal chain links choices, conditions, events, and consequences; sequence alone does not prove causation inside or outside the work.", "literature.narrative"),
    ("conflict", "Narrative conflict", "Conflict arises when goals, values, obligations, environments, or internal commitments cannot all be satisfied without change or cost.", "literature.narrative"),
    ("character", "Literary character", "Character is a textual construction inferred from action, speech, thought, description, relationships, omissions, and genre conventions.", "literature.narrative"),
    ("setting", "Literary setting", "Setting comprises spatial, temporal, social, material, and institutional conditions that enable and constrain action.", "literature.narrative"),
    ("theme", "Theme", "A theme is a recurring problem or proposition developed through form and pattern; it is not reducible to a one-word topic.", "literature.criticism"),
    ("motif", "Motif", "A motif is a recurrent element whose changing contexts can accumulate structural or interpretive significance.", "literature.criticism"),
    ("symbol", "Symbol", "A symbol invites significance beyond literal reference through patterned use, but an interpretation must remain answerable to textual context.", "literature.criticism"),
    ("irony", "Irony", "Irony creates a structured divergence among wording, situation, expectation, knowledge, or evaluation and cannot be established from contradiction alone.", "literature.criticism"),
    ("ambiguity", "Literary ambiguity", "Literary ambiguity sustains more than one contextually defensible meaning without implying that every reading is equally supported.", "literature.criticism"),
    ("intertextuality", "Intertextuality", "Intertextuality analyzes how a work transforms, echoes, contests, or presupposes other texts and cultural forms.", "literature.comparative"),
    ("genre", "Literary genre", "Genre is a historically changing family of conventions that shapes expectations while allowing hybridization, revision, and exceptions.", "literature.criticism"),
    ("form-content", "Form and content", "Form organizes what a work can make perceptible or thinkable; analysis should explain their interaction rather than treat them as separable containers.", "literature.criticism"),
    ("close-reading", "Close reading", "Close reading builds an interpretation from precise patterns of diction, syntax, imagery, sound, structure, and contradiction in a bounded passage.", "literature.criticism"),
    ("contextual-reading", "Contextual reading", "Contextual reading relates textual evidence to historical, linguistic, material, and institutional conditions without replacing the text with background.", "literature.criticism"),
    ("counterreading", "Counterreading", "A counterreading tests a proposed interpretation against neglected details, alternative frames, and evidence that should look different if the interpretation were sound.", "literature.criticism"),
    ("formalism", "Formalist lens", "A formalist lens emphasizes internal pattern, device, structure, and defamiliarization while bracketing some external explanations.", "literature.criticism"),
    ("historical-lens", "Historical lens", "A historical lens examines how a work participates in the language, institutions, conflicts, and available forms of its time.", "literature.criticism"),
    ("reader-response", "Reader-response lens", "A reader-response lens studies how textual cues and reader positions jointly produce an interpretation without assuming one universal reader.", "literature.criticism"),
    ("feminist-lens", "Feminist lens", "A feminist lens examines gendered representation, agency, labor, embodiment, voice, and power while remaining attentive to intersecting differences.", "literature.criticism"),
    ("postcolonial-lens", "Postcolonial lens", "A postcolonial lens examines empire, race, language, displacement, resistance, and the politics of representation without treating cultures as homogeneous.", "literature.criticism"),
    ("psychoanalytic-lens", "Psychoanalytic lens", "A psychoanalytic lens interprets desire, conflict, repetition, fantasy, and repression as a critical vocabulary, not as a clinical diagnosis of author or reader.", "literature.criticism"),
    ("structuralist-lens", "Structuralist lens", "A structuralist lens studies relational systems, codes, oppositions, and transformations that make individual narrative elements intelligible.", "literature.criticism"),
    ("deconstructive-lens", "Deconstructive lens", "A deconstructive lens tracks instabilities and exclusions within a text's organizing oppositions rather than merely declaring that meaning is impossible.", "literature.criticism"),
    ("line", "Poetic line", "A poetic line is a compositional unit whose syntax, rhythm, visual boundary, and break can cooperate or create tension.", "literature.poetry"),
    ("stanza", "Stanza", "A stanza groups poetic lines into a repeated or evolving structural unit comparable to, but not identical with, a prose paragraph.", "literature.poetry"),
    ("meter", "Meter", "Meter is a patterned organization of relative rhythmic prominence; an actual line can vary against the expected pattern.", "literature.poetry"),
    ("rhythm", "Poetic rhythm", "Poetic rhythm emerges from stress, duration, syntax, repetition, pause, and sound rather than from meter alone.", "literature.poetry"),
    ("rhyme", "Rhyme", "Rhyme links sound positions and can organize expectation, closure, emphasis, humor, or disruption.", "literature.poetry"),
    ("sound-pattern", "Poetic sound pattern", "Alliteration, assonance, consonance, and repetition create local relations among sound, pacing, and emphasis without fixing one meaning.", "literature.poetry"),
    ("imagery", "Imagery", "Imagery recruits sensory or embodied representation and should be analyzed through its placement and transformation, not counted as decoration.", "literature.poetry"),
    ("poetic-speaker", "Poetic speaker", "The poetic speaker is a voice constructed by the poem and should not be collapsed into the biographical poet without evidence.", "literature.poetry"),
    ("fixed-form", "Fixed poetic form", "A fixed form establishes repeatable constraints such as line count, meter, rhyme, refrain, or stanza pattern that a poem may fulfill or revise.", "literature.poetry"),
    ("free-verse", "Free verse", "Free verse lacks a governing inherited meter but still organizes lineation, cadence, syntax, image, and recurrence.", "literature.poetry"),
    ("dramatic-monologue", "Dramatic monologue", "A dramatic monologue constructs character and situation through one speaker's extended address, often revealing more than the speaker intends.", "literature.poetry"),
    ("dramatic-action", "Dramatic action", "Dramatic action is change pursued or resisted through performable behavior, speech, silence, and stage conditions.", "literature.drama"),
    ("scene", "Dramatic scene", "A dramatic scene is a bounded unit of action in which relationships, objectives, or knowledge materially change.", "literature.drama"),
    ("act", "Dramatic act", "An act is a large-scale unit of dramatic organization whose boundary can mark a major shift in action, time, or stakes.", "literature.drama"),
    ("stage-directions", "Stage directions", "Stage directions specify or suggest performable action and environment while leaving room for production interpretation.", "literature.drama"),
    ("dramatic-dialogue", "Dramatic dialogue", "Dramatic dialogue performs social action among characters and gains meaning through timing, subtext, embodiment, and response.", "literature.drama"),
    ("dramatic-irony", "Dramatic irony", "Dramatic irony arises when an audience can relate information or consequences unavailable to one or more characters.", "literature.drama"),
    ("tragedy", "Tragedy", "Tragedy is a historically variable dramatic family that organizes grave conflict, reversal, recognition, suffering, and consequence rather than requiring one formula.", "literature.drama"),
    ("comedy", "Comedy", "Comedy is a historically variable family using incongruity, error, social friction, timing, and often reintegration or altered order.", "literature.drama"),
    ("sf-speculation", "Science-fiction speculation", "Science fiction develops a counterfactual or extrapolative premise whose consequences reshape a represented world and its human or nonhuman relations.", "literature.science-fiction"),
    ("sf-novum", "Science-fiction novum", "A novum is the work's differentiating speculative element, evaluated through the changes and constraints it causes rather than novelty of label alone.", "literature.science-fiction"),
    ("sf-extrapolation", "Science-fiction extrapolation", "Extrapolation extends selected tendencies under declared assumptions and remains an imaginative exploration rather than a forecast.", "literature.science-fiction"),
    ("sf-alternate-history", "Alternate-history fiction", "Alternate history changes a historical condition and explores a causally disciplined divergence while retaining its fictional status.", "literature.science-fiction"),
    ("sf-space-opera", "Space opera", "Space opera emphasizes large-scale adventure, societies, technologies, and conflict across expansive settings rather than scientific rigor alone.", "literature.science-fiction"),
    ("sf-cyberpunk", "Cyberpunk", "Cyberpunk commonly explores advanced computation alongside concentrated power, commodified bodies, surveillance, inequality, and contested agency.", "literature.science-fiction"),
    ("sf-solarpunk", "Solarpunk", "Solarpunk explores ecological repair, social organization, and situated technologies through futures whose hope still contains material conflict and tradeoffs.", "literature.science-fiction"),
    ("horror-dread", "Horror dread", "Dread is sustained anticipation of a threatening unknown and depends on controlled uncertainty, implication, and delayed confirmation.", "literature.horror"),
    ("horror-uncanny", "The uncanny", "The uncanny destabilizes familiar categories by making the ordinary seem animate, doubled, displaced, or not fully knowable.", "literature.horror"),
    ("horror-gothic", "Gothic horror", "Gothic horror connects threat to charged spaces, inheritance, secrecy, confinement, transgression, and returns of unresolved history.", "literature.horror"),
    ("horror-body", "Body horror", "Body horror locates threat in transformation, permeability, loss of bodily autonomy, contamination, or unstable biological boundaries.", "literature.horror"),
    ("horror-cosmic", "Cosmic horror", "Cosmic horror stages disproportion between human frameworks and realities represented as vast, indifferent, or cognitively destabilizing.", "literature.horror"),
    ("horror-psychological", "Psychological horror", "Psychological horror organizes fear through perception, memory, identity, isolation, or uncertainty while not equating mental illness with monstrosity.", "literature.horror"),
    ("thriller-threat", "Thriller threat", "A thriller centers an escalating threat whose consequences require sustained action under pressure.", "literature.thriller"),
    ("thriller-suspense", "Suspense", "Suspense arises when readers anticipate consequential possibilities but lack certainty about outcome, timing, or intervention.", "literature.thriller"),
    ("thriller-deadline", "Deadline pressure", "A deadline compresses available choices and converts elapsed time into increasing consequence.", "literature.thriller"),
    ("thriller-reversal", "Thriller reversal", "A reversal changes the apparent threat, allegiance, objective, or meaning of prior evidence while remaining retrospectively supported.", "literature.thriller"),
    ("fantasy-secondary-world", "Secondary-world fantasy", "Secondary-world fantasy constructs a world not presented as ordinary historical reality and makes its institutions and causal rules internally consequential.", "literature.fantasy"),
    ("fantasy-magic", "Magic system", "A magic system defines affordances, limits, costs, knowledge, and social consequences; mystery and rigor are design choices rather than a single required balance.", "literature.fantasy"),
    ("fantasy-portal", "Portal fantasy", "Portal fantasy crosses between differently ordered worlds, using the boundary to mediate discovery, comparison, and transformation.", "literature.fantasy"),
    ("fantasy-mythic", "Mythic fantasy", "Mythic fantasy reworks archetypal structures, sacred narratives, folklore, or cosmology while requiring culturally specific attribution and care.", "literature.fantasy"),
    ("mystery-question", "Mystery question", "Mystery fiction organizes attention around an unresolved event, identity, mechanism, or motive that inquiry can progressively constrain.", "literature.mystery"),
    ("mystery-clue", "Clue", "A clue is observable story evidence that bears on competing explanations and gains value through relevance, interpretation, and timing.", "literature.mystery"),
    ("mystery-red-herring", "Red herring", "A red herring supports a plausible but ultimately displaced inference and should not depend on authorial concealment that makes correction impossible.", "literature.mystery"),
    ("mystery-reveal", "Mystery reveal", "A reveal integrates agent, means, motive, opportunity, and clues strongly enough that the solution can be checked against alternatives.", "literature.mystery"),
    ("romance-central-relationship", "Central romantic relationship", "Genre romance makes the developing romantic relationship central to the story's causal and emotional structure.", "literature.romance"),
    ("romance-emotional-arc", "Romantic emotional arc", "A romantic arc transforms intimacy, trust, vulnerability, compatibility, and choice through obstacles that matter to both characters.", "literature.romance"),
    ("romance-resolution", "Romance resolution", "Many romance traditions promise an emotionally affirmative relationship outcome, but exact ending conventions vary by subgenre and audience.", "literature.romance"),
    ("historical-research", "Historical-fiction research", "Historical fiction uses research to constrain material life, institutions, language, and available choices while still inventing represented events.", "literature.historical-fiction"),
    ("historical-anachronism", "Anachronism", "An anachronism places an object, concept, institution, or expression outside its supported historical availability and may be accidental or deliberate.", "literature.historical-fiction"),
    ("literary-nonfiction-contract", "Literary-nonfiction truth contract", "Literary nonfiction may use scene, voice, and structure but owes readers a clear boundary between verified fact, remembered experience, reconstruction, and invention.", "literature.nonfiction"),
    ("memoir-memory", "Memoir and memory", "Memoir presents situated remembered experience whose sincerity does not eliminate uncertainty, selection, or later reconstruction.", "literature.nonfiction"),
    ("translation", "Literary translation", "Literary translation reconstructs relations of meaning, sound, register, form, and cultural context under choices that should be made visible when material.", "literature.comparative"),
    ("reception", "Reception history", "Reception history studies how communities at different times interpret, value, adapt, suppress, or institutionalize a work.", "literature.comparative"),
    ("oral-performance", "Oral literary performance", "Oral literature is realized through performance, memory, variation, audience participation, and transmission rather than a single fixed written text.", "literature.world"),
    ("cultural-specificity", "Cultural specificity", "Interpretation should preserve the language, history, community categories, and power relations that make a work specific rather than treating one tradition as universal.", "literature.world"),
]


CREATIVE_WRITING = [
    ("root", "Creative-writing craft", "Creative-writing craft generates and selects invented language under a brief, constraints, genre expectations, and revision criteria while never granting invented details factual authority.", "creative-writing.constraint-preservation"),
    ("brief", "Creative brief", "A creative brief declares audience, purpose, form, length, tone, required elements, forbidden elements, factual anchors, and acceptance criteria before generation.", "creative-writing.constraint-preservation"),
    ("hard-constraint", "Hard creative constraint", "A hard constraint is a condition every candidate must satisfy, such as length, continuity, rating, factual boundary, format, or required event.", "creative-writing.constraint-preservation"),
    ("soft-preference", "Soft creative preference", "A soft preference guides ranking among valid candidates but can yield when it conflicts with a hard constraint.", "creative-writing.constraint-preservation"),
    ("candidate-set", "Creative candidate set", "Generating structurally distinct candidates exposes tradeoffs and reduces premature commitment to the first fluent continuation.", "creative-writing.story-structure"),
    ("selection-criteria", "Creative selection criteria", "Candidate selection compares novelty, coherence, value, fit, emotional force, and constraint satisfaction instead of treating surprise as sufficient.", "creative-writing.revision"),
    ("premise", "Story premise", "A premise combines a differentiating situation with agents, pressure, and an implied field of consequences that can sustain development.", "creative-writing.story-structure"),
    ("logline", "Logline", "A logline compresses protagonist, objective, central obstacle, stakes, and differentiating situation without attempting to summarize every event.", "creative-writing.story-structure"),
    ("story-question", "Story question", "A story question focuses uncertainty around whether, how, or at what cost a consequential objective or transformation can occur.", "creative-writing.story-structure"),
    ("inciting-change", "Inciting change", "An inciting change disrupts a prior equilibrium and creates a problem, opportunity, or obligation that redirects meaningful action.", "creative-writing.story-structure"),
    ("goal", "Dramatic goal", "A dramatic goal gives a character a testable desired outcome whose pursuit can organize choices and resistance.", "creative-writing.story-structure"),
    ("stakes", "Story stakes", "Stakes specify what can be gained, lost, damaged, or transformed and why that consequence matters to particular agents.", "creative-writing.story-structure"),
    ("obstacle", "Story obstacle", "An obstacle resists a goal through another agent, environment, institution, information gap, value conflict, or internal commitment.", "creative-writing.story-structure"),
    ("turning-point", "Turning point", "A turning point changes the available options, knowledge, commitment, power, or trajectory enough that prior tactics no longer suffice.", "creative-writing.story-structure"),
    ("climax", "Climax", "A climax concentrates the story's controlling conflict into an irreversible choice, confrontation, or discovery with maximum accumulated consequence.", "creative-writing.story-structure"),
    ("resolution", "Resolution", "A resolution shows the new state produced by decisive events and answers central dramatic questions while allowing intentional remainder.", "creative-writing.story-structure"),
    ("subplot", "Subplot", "A subplot develops a secondary causal and thematic trajectory that should interact with, pressure, mirror, or complicate the main plot.", "creative-writing.story-structure"),
    ("nonlinear-structure", "Nonlinear structure", "A nonlinear structure reorders presentation for a specific effect while preserving enough causal and temporal cues for intended reconstruction.", "creative-writing.story-structure"),
    ("want", "Character want", "A character want is the outcome the character consciously pursues and can conflict with a less articulated need, duty, or value.", "creative-writing.character"),
    ("need", "Character need", "A character need is a capacity, recognition, or change whose absence generates recurring costs, whether or not the character accepts it.", "creative-writing.character"),
    ("agency", "Character agency", "Agency appears when a character makes choices that alter causal possibilities rather than serving only as an object of other characters' actions.", "creative-writing.character"),
    ("motivation", "Character motivation", "Motivation connects a character's history, beliefs, desires, pressures, and information to a particular choice without requiring perfect rationality.", "creative-writing.character"),
    ("contradiction", "Character contradiction", "A character contradiction places competing traits, values, performances, or desires in one person and becomes depth when consequences reveal its structure.", "creative-writing.character"),
    ("arc", "Character arc", "A character arc tracks changes or tested persistence in belief, behavior, relationship, identity, or capacity across causally linked pressure.", "creative-writing.character"),
    ("relationship", "Character relationship", "A relationship has its own history, power distribution, expectations, tactics, ruptures, and transformations beyond two isolated profiles.", "creative-writing.character"),
    ("backstory", "Backstory", "Backstory supplies prior causes and meanings only where present action, interpretation, or stakes require them; chronology alone does not justify exposition.", "creative-writing.character"),
    ("characterization", "Characterization", "Characterization lets readers infer a person from consequential action, speech, thought, detail, contrast, and response rather than descriptive labels alone.", "creative-writing.character"),
    ("scene-goal", "Scene goal", "A scene goal gives the viewpoint agent an immediate desired change that can meet resistance inside the scene.", "creative-writing.scene"),
    ("scene-conflict", "Scene conflict", "Scene conflict is active resistance among incompatible objectives, interpretations, constraints, or conditions rather than obligatory argument.", "creative-writing.scene"),
    ("scene-turn", "Scene turn", "A scene turn alters knowledge, leverage, relationship, objective, or risk so the scene exits in a materially different state.", "creative-writing.scene"),
    ("scene-sequel", "Reflection and decision unit", "After intense action, a reflection-and-decision unit can register consequence, compare options, and produce the next commitment without stalling the causal chain.", "creative-writing.scene"),
    ("summary", "Narrative summary", "Summary compresses events, patterns, or transitions whose full dramatization would consume attention disproportionate to their function.", "creative-writing.scene"),
    ("sensory-detail", "Sensory detail", "Selected sensory detail makes setting and action perceptible while serving viewpoint, mood, characterization, or causal clarity rather than inventory.", "creative-writing.scene"),
    ("blocking", "Scene blocking", "Blocking tracks bodies, objects, sight lines, entrances, exits, and spatial affordances so action remains legible and consequential.", "creative-writing.scene"),
    ("voice", "Narrative voice", "Narrative voice is the emergent pattern of diction, syntax, rhythm, selection, evaluation, and address across a work.", "creative-writing.voice"),
    ("tone", "Narrative tone", "Tone is the work's enacted attitude toward subject, audience, and situation and may differ from a character's stated emotion.", "creative-writing.voice"),
    ("first-person", "First-person point of view", "First-person narration limits direct assertion to what the narrating voice can know, infer, remember, imagine, or misrepresent.", "creative-writing.voice"),
    ("third-limited", "Third-person limited point of view", "Third-person limited narration anchors perception and interior access primarily to one viewpoint at a time while allowing adjustable distance.", "creative-writing.voice"),
    ("omniscient", "Omniscient point of view", "Omniscient narration can range across minds, times, and explanatory levels through a governing voice whose transitions still need intelligible control.", "creative-writing.voice"),
    ("second-person", "Second-person point of view", "Second-person narration positions a you as protagonist, addressee, divided self, or generalized role and must establish which relation is active.", "creative-writing.voice"),
    ("narrative-distance", "Narrative distance", "Narrative distance controls how closely prose tracks a viewpoint's immediate perceptions and language versus a more external or retrospective account.", "creative-writing.voice"),
    ("viewpoint-transition", "Viewpoint transition", "A viewpoint transition needs a perceptible boundary or orienting cue so expanded access is deliberate rather than accidental head-hopping.", "creative-writing.voice"),
    ("dialogue-objective", "Dialogue objective", "Dialogue becomes dramatic when each participant uses speech or silence to pursue, resist, conceal, test, or redefine an objective.", "creative-writing.dialogue"),
    ("subtext", "Dialogue subtext", "Subtext is the actionable meaning created by the gap between literal wording and a speaker's stakes, knowledge, relationship, or strategy.", "creative-writing.dialogue"),
    ("idiolect", "Character idiolect", "Idiolect differentiates speakers through vocabulary, syntax, rhythm, assumptions, and conversational tactics without reducing identity to caricature.", "creative-writing.dialogue"),
    ("dialogue-beat", "Dialogue beat", "A dialogue beat is a concise action, perception, or pause that locates speech, controls rhythm, or changes interpretation.", "creative-writing.dialogue"),
    ("exposition-dialogue", "Exposition in dialogue", "Necessary information can enter dialogue when speakers have present reasons to disclose, contest, evade, or misunderstand it rather than reciting shared knowledge.", "creative-writing.dialogue"),
    ("setting-model", "Setting model", "A setting model records spatial, ecological, technological, economic, political, and cultural relations that constrain scenes and generate consequences.", "creative-writing.setting"),
    ("world-rule", "World rule", "A world rule defines a repeatable causal affordance or prohibition and should produce consistent direct and second-order consequences.", "creative-writing.setting"),
    ("world-cost", "World-system cost", "A power, technology, or institution gains narrative weight when its use has costs, dependencies, externalities, or unequal access.", "creative-writing.setting"),
    ("continuity-ledger", "Continuity ledger", "A continuity ledger tracks time, location, knowledge, injuries, objects, promises, rules, and unresolved causes across revisions.", "creative-writing.setting"),
    ("research-boundary", "Worldbuilding research boundary", "Research can constrain invented settings, but uncertainties and deliberate departures should not be laundered into real-world fact.", "creative-writing.setting"),
    ("tension", "Narrative tension", "Tension combines consequential desire with resistance and uncertainty, and can operate even when the eventual outcome is known.", "creative-writing.tension"),
    ("suspense-surprise", "Suspense and surprise", "Suspense distributes enough information for anticipation, whereas surprise withholds a decisive relation; either can prepare the other.", "creative-writing.tension"),
    ("urgency", "Urgency", "Urgency limits time, opportunity, or tolerance for delay and is convincing only when the limit has a causal basis.", "creative-writing.tension"),
    ("escalation", "Escalation", "Escalation increases cost, constraint, opposition, commitment, or moral complexity rather than merely increasing physical scale.", "creative-writing.tension"),
    ("pacing", "Pacing", "Pacing is the experienced rate of significant change shaped by scene selection, duration, syntax, information, white space, and reflection.", "creative-writing.tension"),
    ("compression-expansion", "Compression and expansion", "Narrative compression skips or summarizes low-leverage spans, while expansion devotes attention to consequential moments and perceptual shifts.", "creative-writing.tension"),
    ("reveal", "Revelation design", "A reveal changes the meaning of prior evidence and should be prepared enough to feel coherent without becoming inevitable.", "creative-writing.tension"),
    ("structural-revision", "Structural revision", "Structural revision tests premise, causal chain, character agency, stakes, sequence, omissions, and ending before polishing sentences.", "creative-writing.revision"),
    ("scene-revision", "Scene revision", "Scene revision checks each unit for entry state, objective, resistance, turn, exit state, viewpoint, spatial clarity, and contribution to the whole.", "creative-writing.revision"),
    ("line-revision", "Line revision", "Line revision improves precision, rhythm, image, emphasis, continuity, and voice after larger structural decisions are stable.", "creative-writing.revision"),
    ("copyedit", "Creative copyedit", "Copyediting corrects grammar, usage, spelling, punctuation, consistency, and house style without silently changing intended meaning or voice.", "creative-writing.revision"),
    ("feedback-triage", "Feedback triage", "Feedback triage identifies the reader effect behind a suggestion, finds repeated signals, and chooses changes that serve the work's declared intent.", "creative-writing.revision"),
    ("screen-action", "Screenplay visual action", "Screenplay action describes present, filmable behavior and selected sound with enough precision for production while avoiding unrenderable explanation.", "creative-writing.screenwriting"),
    ("screen-scene-heading", "Screenplay scene heading", "A scene heading marks interior or exterior, location, and production-relevant time so a script's spatial and scheduling units are legible.", "creative-writing.screenwriting"),
    ("screen-sequence", "Screen sequence", "A screen sequence coordinates shot-independent dramatic action, visual causality, transitions, and sound across multiple scenes.", "creative-writing.screenwriting"),
    ("play-performability", "Playwriting performability", "A stage text must support repeatable live action through speakable language, playable objectives, timing, bodies, space, and production constraints.", "creative-writing.playwriting"),
    ("play-stage-world", "Stage-world economy", "A stage world uses entrances, exits, props, light, sound, offstage space, and audience awareness as causal resources rather than prose scenery.", "creative-writing.playwriting"),
    ("poetry-image", "Poetic image making", "A poetic image selects concrete relations that can carry sensory, emotional, and conceptual pressure without requiring explanatory paraphrase.", "creative-writing.poetry"),
    ("poetry-lineation", "Poetic lineation", "Lineation controls pause, double syntax, emphasis, visual pace, and expectation through deliberate line boundaries.", "creative-writing.poetry"),
    ("poetry-constraint", "Poetic constraint", "A poetic constraint can generate unexpected language by limiting form, sound, vocabulary, pattern, or procedure while selection preserves value.", "creative-writing.poetry"),
    ("genre-promise", "Genre promise", "A genre promise is the cluster of experiences and organizing questions an intended audience reasonably expects, not a mandatory checklist of tropes.", "creative-writing.genre"),
    ("genre-hybrid", "Genre hybrid", "A genre hybrid combines convention systems only after identifying how their causal engines, tones, pacing, and audience promises interact.", "creative-writing.genre"),
    ("genre-innovation", "Genre innovation", "Genre innovation transforms a recognized convention while retaining enough structure for the transformation to be legible.", "creative-writing.genre"),
    ("factual-anchor", "Factual anchor", "A factual anchor supplied by a brief remains unchanged unless revision is explicitly authorized and must not be overwritten for dramatic convenience.", "creative-writing.constraint-preservation"),
    ("fiction-marker", "Fiction marker", "Invented people, events, citations, quotations, and data must remain marked as fiction whenever a reader could reasonably mistake them for real evidence.", "creative-writing.constraint-preservation"),
    ("continuity-constraint", "Continuity constraint", "Established story facts constrain later candidates until the work deliberately revises them through an explicit change mechanism.", "creative-writing.constraint-preservation"),
    ("transformative-style", "Transformative style design", "A style target should be decomposed into general features such as register, rhythm, imagery, distance, and structure rather than copying protected passages or impersonating a living author.", "creative-writing.constraint-preservation"),
]


TECHNICAL_WRITING = [
    ("root", "Technical and professional writing", "Technical writing enables a defined audience to understand, decide, or act correctly through verified content, explicit scope, task-centered structure, accessible presentation, and maintained version boundaries.", "technical-professional-writing.documentation"),
    ("audience", "Technical audience", "Audience analysis records roles, prior knowledge, goals, constraints, language, accessibility needs, risk exposure, and the context in which information will be used.", "technical-professional-writing.documentation"),
    ("purpose", "Document purpose", "A document purpose states the change in understanding, decision, or action the document is intended to support.", "technical-professional-writing.documentation"),
    ("task", "User task", "A user task is a goal pursued in context, not merely a product feature or menu path.", "technical-professional-writing.documentation"),
    ("prerequisite", "Documented prerequisite", "A prerequisite names the knowledge, permissions, tools, versions, state, and inputs that must exist before a procedure can succeed.", "technical-professional-writing.documentation"),
    ("scope", "Documentation scope", "Scope declares what a document covers, excludes, assumes, and leaves to linked material so readers can judge applicability.", "technical-professional-writing.documentation"),
    ("information-architecture", "Information architecture", "Information architecture organizes topics, labels, navigation, links, and progressive disclosure around user needs and conceptual structure.", "technical-professional-writing.documentation"),
    ("single-source", "Single-source content", "Single-source content separates reusable verified facts from presentation variants while preventing context-free fragments and contradictory copies.", "technical-professional-writing.documentation"),
    ("version-boundary", "Documentation version boundary", "A version boundary identifies the product, API, standard, date, or configuration for which a technical claim is valid.", "technical-professional-writing.documentation"),
    ("maintenance-owner", "Documentation ownership", "A maintained document has an accountable owner, review trigger, update obligation, and retirement path tied to the system it describes.", "technical-professional-writing.documentation"),
    ("tutorial", "Tutorial", "A tutorial creates a successful guided learning experience through a coherent sequence, controlled environment, and visible milestones rather than cataloging every option.", "technical-professional-writing.documentation"),
    ("how-to", "How-to guide", "A how-to guide helps a competent user accomplish a particular goal and centers the path and decisions needed for that situation.", "technical-professional-writing.instructions"),
    ("reference", "Reference documentation", "Reference documentation describes the system's interfaces, parameters, behavior, constraints, and errors in a predictable structure optimized for lookup.", "technical-professional-writing.documentation"),
    ("explanation", "Explanatory documentation", "Explanatory documentation builds understanding through causes, rationale, alternatives, history, and conceptual relationships rather than step execution.", "technical-professional-writing.documentation"),
    ("concept-topic", "Concept topic", "A concept topic defines an idea, locates it in a larger system, distinguishes neighboring ideas, and explains why it matters.", "technical-professional-writing.documentation"),
    ("troubleshooting", "Troubleshooting topic", "A troubleshooting topic maps observable symptoms and diagnostic evidence to likely causes, discriminating checks, repairs, and verification.", "technical-professional-writing.instructions"),
    ("api-overview", "API overview", "An API overview defines the resource model, authentication, common workflows, lifecycle, version, limits, and conventions before endpoint detail.", "technical-professional-writing.api-docs"),
    ("api-endpoint", "API endpoint", "Endpoint documentation specifies method, route, purpose, permissions, inputs, state effects, outputs, errors, idempotency, and version behavior.", "technical-professional-writing.api-docs"),
    ("api-parameter", "API parameter", "A parameter definition includes type, location, requirement level, constraints, default, units, encoding, interactions, and representative values.", "technical-professional-writing.api-docs"),
    ("api-request", "API request example", "A request example is executable or mechanically checkable, uses declared placeholders, and matches the documented schema and authentication context.", "technical-professional-writing.api-docs"),
    ("api-response", "API response example", "A response example shows status, headers, body shape, types, optionality, and semantically meaningful values consistent with the current implementation.", "technical-professional-writing.api-docs"),
    ("api-error", "API error contract", "An error contract defines machine identifier, transport status, human message, retryability, cause conditions, and caller remediation.", "technical-professional-writing.api-docs"),
    ("api-auth", "API authentication documentation", "Authentication documentation identifies credential type, acquisition, storage boundary, scopes, transmission, rotation, expiration, and failure behavior without exposing secrets.", "technical-professional-writing.api-docs"),
    ("api-idempotency", "API idempotency documentation", "Idempotency documentation states which repeated requests preserve effect, what key or identity governs repetition, retention duration, and conflict behavior.", "technical-professional-writing.api-docs"),
    ("api-pagination", "API pagination documentation", "Pagination documentation explains ordering, cursor or offset semantics, stability under mutation, limits, termination, and duplicate handling.", "technical-professional-writing.api-docs"),
    ("api-deprecation", "API deprecation notice", "A deprecation notice names the affected surface, replacement, behavioral differences, migration steps, dates, and compatibility window.", "technical-professional-writing.api-docs"),
    ("procedure-goal", "Procedure goal", "A procedure begins with the specific postcondition the reader will achieve and the supported context in which it applies.", "technical-professional-writing.instructions"),
    ("procedure-input", "Procedure input", "Procedure inputs identify required files, values, credentials, physical materials, and starting state without embedding secrets.", "technical-professional-writing.instructions"),
    ("ordered-step", "Ordered procedural step", "An ordered step contains one coherent action, an identifiable target, necessary parameters, and any immediately observable result.", "technical-professional-writing.instructions"),
    ("step-condition", "Step condition", "A condition appears before the action it governs and identifies the evidence by which the reader selects the applicable branch.", "technical-professional-writing.instructions"),
    ("procedure-verification", "Procedure verification", "Verification states how to observe the promised postcondition independently of the action merely returning without an error.", "technical-professional-writing.instructions"),
    ("rollback", "Procedure rollback", "Rollback instructions define when reversal is safe, what state is recoverable, the exact restoration path, and what cannot be undone.", "technical-professional-writing.instructions"),
    ("warning", "Safety warning", "A warning appears before the hazardous action and states the hazard, consequence, prevention, and recovery path in direct language.", "technical-professional-writing.instructions"),
    ("requirement", "Requirement", "A requirement states a necessary externally observable capability or constraint with a unique identity, scope, rationale where useful, and testable condition.", "technical-professional-writing.specifications"),
    ("normative-keyword", "Normative keyword", "A normative keyword receives its standards meaning only when the specification explicitly invokes its governing convention and uses the declared capitalization.", "technical-professional-writing.specifications"),
    ("must", "Absolute requirement", "MUST identifies a condition required for conformance within the specification's declared scope; it does not describe current implementation evidence by itself.", "technical-professional-writing.specifications"),
    ("must-not", "Absolute prohibition", "MUST NOT identifies behavior forbidden for conformance within a declared specification context.", "technical-professional-writing.specifications"),
    ("should", "Qualified recommendation", "SHOULD identifies a strong recommendation with possible justified exceptions whose implications must be understood and recorded.", "technical-professional-writing.specifications"),
    ("may", "Permission", "MAY identifies a genuinely optional behavior and does not impose a requirement on either implementer or user.", "technical-professional-writing.specifications"),
    ("acceptance-criterion", "Acceptance criterion", "An acceptance criterion defines observable setup, action, and expected result precise enough to decide whether a requirement is satisfied.", "technical-professional-writing.specifications"),
    ("traceability", "Requirements traceability", "Traceability links stakeholder need, requirement, design decision, implementation, test, result, and release so impact and proof can be followed.", "technical-professional-writing.specifications"),
    ("invariant", "System invariant", "An invariant states a property that must remain true over a declared set of states and transitions.", "technical-professional-writing.specifications"),
    ("state-machine", "State-machine specification", "A state-machine specification enumerates states, events, guards, transitions, effects, invalid inputs, and terminal behavior.", "technical-professional-writing.specifications"),
    ("sequence", "Protocol sequence", "A protocol sequence specifies actor order, messages, correlation, timing, retries, duplicate behavior, failure paths, and completion evidence.", "technical-professional-writing.specifications"),
    ("non-normative", "Non-normative material", "Examples, rationale, and notes should be marked non-normative when they aid interpretation but do not independently impose conformance requirements.", "technical-professional-writing.specifications"),
    ("research-question", "Research question", "A research question identifies the population, phenomenon, relationship, or uncertainty the inquiry is designed to resolve.", "technical-professional-writing.scientific"),
    ("methods", "Methods section", "A methods section describes design, materials, participants or data, measurements, procedures, exclusions, and analysis well enough to assess and reproduce the work.", "technical-professional-writing.scientific"),
    ("results", "Results section", "A results section reports observations and analysis with units, uncertainty, denominators, and prespecified distinctions before broader interpretation.", "technical-professional-writing.scientific"),
    ("discussion", "Discussion section", "A discussion interprets results against the question and prior work while preserving limitations, alternatives, generalization bounds, and unresolved uncertainty.", "technical-professional-writing.scientific"),
    ("uncertainty", "Scientific uncertainty statement", "An uncertainty statement distinguishes measurement uncertainty, sampling variation, model dependence, unknown bias, and unresolved mechanism where relevant.", "technical-professional-writing.scientific"),
    ("reproducibility", "Reproducibility statement", "A reproducibility statement identifies data, code, environment, parameters, seed, protocol deviations, and access restrictions needed to rerun an analysis.", "technical-professional-writing.scientific"),
    ("citation", "Technical citation", "A citation identifies the exact source and version supporting a claim while leaving the writer responsible for checking relevance, authority, and faithful representation.", "technical-professional-writing.academic"),
    ("thesis", "Academic thesis", "A thesis is a contestable central claim whose scope, terms, and stakes organize the paper's evidence and reasoning.", "technical-professional-writing.academic"),
    ("literature-synthesis", "Literature synthesis", "A literature synthesis groups sources by question, method, finding, assumption, or disagreement instead of serially summarizing one source at a time.", "technical-professional-writing.academic"),
    ("counterargument", "Academic counterargument", "A counterargument presents the strongest relevant objection or alternative, then answers, qualifies, or concedes it with evidence.", "technical-professional-writing.academic"),
    ("quotation-boundary", "Quotation boundary", "Quoted wording must remain visibly delimited, accurately transcribed, proportionate, and linked to its source; paraphrase requires fresh language and citation.", "technical-professional-writing.academic"),
    ("executive-summary", "Executive summary", "An executive summary presents the decision, finding, consequence, recommendation, and essential evidence so a time-limited reader can act before reading detail.", "technical-professional-writing.business"),
    ("decision-memo", "Decision memo", "A decision memo states the decision required, criteria, options, evidence, tradeoffs, risks, recommendation, owner, and next action.", "technical-professional-writing.business"),
    ("proposal", "Professional proposal", "A proposal connects a defined problem to an approach, deliverables, schedule, resources, risks, evidence of feasibility, and measurable success.", "technical-professional-writing.business"),
    ("professional-email", "Professional email", "A professional email makes the requested action, owner, timing, context, and attachments easy to find while matching relationship and risk.", "technical-professional-writing.business"),
    ("news-fact", "Journalistic fact", "A journalistic fact is an attributable, checked observation or record, kept distinct from allegation, analysis, prediction, and opinion.", "technical-professional-writing.journalism"),
    ("news-source", "Journalistic source", "Source evaluation considers access, competence, incentives, independence, corroboration, vulnerability, and the conditions under which attribution was agreed.", "technical-professional-writing.journalism"),
    ("news-lead", "News lead", "A news lead prioritizes the most consequential verified development and its context rather than preserving the chronology of reporting.", "technical-professional-writing.journalism"),
    ("news-attribution", "Journalistic attribution", "Attribution makes clear who claims, observed, measured, or disputes what and prevents the writer's voice from laundering an allegation into fact.", "technical-professional-writing.journalism"),
    ("news-correction", "Correction", "A correction identifies the inaccurate material, supplies the accurate replacement, records material timing, and propagates to affected versions.", "technical-professional-writing.journalism"),
    ("substantive-edit", "Substantive edit", "A substantive edit changes argument, structure, scope, evidence, sequence, or audience fit and therefore requires authorial review of meaning.", "technical-professional-writing.editing"),
    ("line-edit", "Line edit", "A line edit improves clarity, flow, tone, emphasis, and sentence relation while preserving verified content and intended meaning.", "technical-professional-writing.editing"),
    ("copyedit", "Technical copyedit", "A technical copyedit corrects usage, grammar, terminology, formatting, cross-references, and consistency against the governing style and product reality.", "technical-professional-writing.editing"),
    ("proofread", "Proofread", "Proofreading checks the final rendered artifact for residual text, numbering, layout, link, caption, and production defects after substantive edits are closed.", "technical-professional-writing.editing"),
    ("fact-check", "Fact check", "Fact checking resolves each externally verifiable claim against an authoritative, version-matched source and records uncertainty or conflict.", "technical-professional-writing.editing"),
    ("plain-language", "Plain language", "Plain language lets the intended audience find, understand, and use information through familiar words, direct structure, and explicit actions without erasing necessary precision.", "technical-professional-writing.accessibility"),
    ("heading", "Descriptive heading", "A descriptive heading names the question, task, or concept beneath it and creates a navigable outline when read apart from body text.", "technical-professional-writing.accessibility"),
    ("link-text", "Descriptive link text", "Link text describes destination or action without relying on surrounding context or generic phrases.", "technical-professional-writing.accessibility"),
    ("alt-text", "Alternative text", "Alternative text communicates the purpose and relevant information of a non-text element in its specific context rather than inventorying every visual detail.", "technical-professional-writing.accessibility"),
    ("table-access", "Accessible table", "An accessible data table has a caption or context, semantic headers, simple relationships where possible, and equivalent access to essential information.", "technical-professional-writing.accessibility"),
    ("cognitive-load", "Documentation cognitive load", "Documentation reduces avoidable cognitive load through chunking, consistent terminology, visible hierarchy, progressive disclosure, and nearby prerequisites.", "technical-professional-writing.accessibility"),
    ("global-audience", "Global audience", "Writing for a global audience avoids culture-bound assumptions, ambiguous dates, unexplained idioms, fragile humor, and unnecessary syntactic complexity.", "technical-professional-writing.localization"),
    ("terminology", "Controlled terminology", "A controlled term has one declared meaning in a product context, approved variants for search, and a migration plan when renamed.", "technical-professional-writing.localization"),
    ("locale-sensitive", "Locale-sensitive content", "Dates, times, numbers, currencies, names, addresses, units, collation, and plural forms require locale-aware representation rather than string substitution.", "technical-professional-writing.localization"),
    ("translatable-source", "Translatable source", "Translatable source text uses complete grammatical units, explicit placeholders, stable terminology, and context notes so translators can preserve function.", "technical-professional-writing.localization"),
]


RELATIONS = [
    ("lit-discourse-order", "lit.story-discourse", "lit.temporal-order", "clarifies", "Story-discourse separation clarifies when chronology and presentation order diverge."),
    ("lit-discourse-duration", "lit.story-discourse", "lit.duration", "clarifies", "Story-discourse separation clarifies how textual allocation changes experienced event duration."),
    ("lit-discourse-frequency", "lit.story-discourse", "lit.frequency", "clarifies", "Story-discourse separation clarifies how repeated telling differs from repeated occurrence."),
    ("lit-narrator-focalization", "lit.narrator", "lit.focalization", "qualifies", "Narrator identity qualifies but does not uniquely determine perceptual focalization."),
    ("lit-focalization-reliability", "lit.focalization", "lit.reliability", "qualifies", "Restricted access can qualify reliability judgments by separating ignorance from distortion."),
    ("lit-causal-plot", "lit.causal-chain", "lit.plot", "supports", "A legible causal chain supports plot coherence across selected events."),
    ("lit-conflict-plot", "lit.conflict", "lit.plot", "enables", "Incompatible pressures enable consequential plot development."),
    ("lit-setting-causal", "lit.setting", "lit.causal-chain", "qualifies", "Setting qualifies which actions and consequences are materially possible."),
    ("lit-character-causal", "lit.character", "lit.causal-chain", "enables", "Character choices enable causal transitions in agent-centered narratives."),
    ("lit-motif-theme", "lit.motif", "lit.theme", "supports", "A motif's patterned transformations can support a thematic interpretation."),
    ("lit-symbol-theme", "lit.symbol", "lit.theme", "supports", "Contextually patterned symbolism can support a theme without exhausting it."),
    ("lit-ambiguity-counterreading", "lit.ambiguity", "lit.counterreading", "enables", "Textual ambiguity enables competing readings that can be compared against evidence."),
    ("lit-close-interpretation", "lit.close-reading", "lit.root", "grounds", "Close textual evidence grounds a literary interpretation."),
    ("lit-context-interpretation", "lit.contextual-reading", "lit.root", "qualifies", "Relevant historical context qualifies the scope and plausibility of interpretation."),
    ("lit-counter-interpretation", "lit.counterreading", "lit.root", "undercuts", "A stronger counterreading can undercut an interpretation that cannot explain material evidence."),
    ("lit-genre-context", "lit.genre", "lit.contextual-reading", "supports", "Historically situated genre expectations support contextual interpretation."),
    ("lit-form-close", "lit.form-content", "lit.close-reading", "supports", "Attention to form-content interaction supports close analysis."),
    ("lit-irony-reliability", "lit.irony", "lit.reliability", "qualifies", "Irony can qualify whether narrator evaluation should be accepted at face value."),
    ("lit-intertext-context", "lit.intertextuality", "lit.contextual-reading", "supports", "Intertextual relations supply one relevant layer of context."),
    ("lit-line-rhythm", "lit.line", "lit.rhythm", "implements", "Line boundaries implement rhythmic expectation through pause and continuation."),
    ("lit-meter-rhythm", "lit.meter", "lit.rhythm", "supports", "Meter supplies a recurring expectation against which performed rhythm varies."),
    ("lit-rhyme-rhythm", "lit.rhyme", "lit.rhythm", "supports", "Rhyme supports rhythmic grouping and anticipation."),
    ("lit-sound-image", "lit.sound-pattern", "lit.imagery", "qualifies", "Sound pattern can qualify an image's affective and semantic force."),
    ("lit-form-line", "lit.fixed-form", "lit.line", "qualifies", "Fixed form qualifies line count and placement through declared constraints."),
    ("lit-free-line", "lit.free-verse", "lit.line", "qualifies", "Free verse shifts organizing responsibility from inherited meter toward local lineation and recurrence."),
    ("lit-speaker-narrator", "lit.poetic-speaker", "lit.narrator", "analogous_to", "Poetic speaker and narrator are analogous constructed voices but operate under different generic expectations."),
    ("lit-scene-action", "lit.scene", "lit.dramatic-action", "part_of", "A dramatic scene contains a bounded transformation of action."),
    ("lit-act-scene", "lit.scene", "lit.act", "part_of", "Scenes compose larger dramatic acts."),
    ("lit-stage-action", "lit.stage-directions", "lit.dramatic-action", "implements", "Stage directions help implement performable action and environment."),
    ("lit-dialogue-action", "lit.dramatic-dialogue", "lit.dramatic-action", "implements", "Dialogue implements action when speech changes relationships, knowledge, or choice."),
    ("lit-irony-dialogue", "lit.dramatic-irony", "lit.dramatic-dialogue", "qualifies", "Audience knowledge can qualify the meaning of dramatic dialogue beyond a character's awareness."),
    ("lit-sf-novum", "lit.sf-novum", "lit.sf-speculation", "part_of", "A differentiating novum is one component of science-fiction speculation."),
    ("lit-sf-extrapolation", "lit.sf-extrapolation", "lit.sf-speculation", "implements", "Extrapolation implements one method for developing speculative consequences."),
    ("lit-alt-causal", "lit.sf-alternate-history", "lit.causal-chain", "prerequisite", "Alternate history requires a legible causal divergence from its changed condition."),
    ("lit-cyber-setting", "lit.sf-cyberpunk", "lit.setting", "qualifies", "Cyberpunk conventions qualify the social and technological organization of setting."),
    ("lit-solar-setting", "lit.sf-solarpunk", "lit.setting", "qualifies", "Solarpunk conventions qualify ecological, institutional, and technological world relations."),
    ("lit-dread-suspense", "lit.horror-dread", "lit.thriller-suspense", "analogous_to", "Horror dread and thriller suspense both manage anticipated consequence but differ in typical affect and explanatory pressure."),
    ("lit-uncanny-ambiguity", "lit.horror-uncanny", "lit.ambiguity", "enables", "Unresolved category instability enables an uncanny reading."),
    ("lit-gothic-setting", "lit.horror-gothic", "lit.setting", "qualifies", "Gothic convention makes charged space and inherited history structurally consequential."),
    ("lit-body-boundary", "lit.horror-body", "lit.conflict", "enables", "Threats to bodily autonomy enable a distinctive axis of conflict."),
    ("lit-threat-suspense", "lit.thriller-threat", "lit.thriller-suspense", "enables", "A consequential threat enables suspense when its outcome remains uncertain."),
    ("lit-deadline-threat", "lit.thriller-deadline", "lit.thriller-threat", "qualifies", "A causal deadline qualifies the threat by shrinking the available response window."),
    ("lit-reversal-plot", "lit.thriller-reversal", "lit.plot", "transforms_to", "A supported reversal transforms the apparent plot trajectory and prior evidence."),
    ("lit-magic-setting", "lit.fantasy-magic", "lit.fantasy-secondary-world", "part_of", "A magic system can form one causal subsystem of a secondary world."),
    ("lit-cost-magic", "cw.world-cost", "lit.fantasy-magic", "qualifies", "Costs and dependencies qualify how magic changes choice and society."),
    ("lit-portal-world", "lit.fantasy-portal", "lit.fantasy-secondary-world", "enables", "A portal enables transition into or between differently ordered worlds."),
    ("lit-clue-question", "lit.mystery-clue", "lit.mystery-question", "supports", "A relevant clue constrains possible answers to the mystery question."),
    ("lit-red-clue", "lit.mystery-red-herring", "lit.mystery-clue", "analogous_to", "A red herring resembles a clue in local relevance while supporting a displaced global explanation."),
    ("lit-reveal-question", "lit.mystery-reveal", "lit.mystery-question", "clarifies", "The reveal resolves the organizing question by integrating evidence and mechanism."),
    ("lit-romance-relation", "lit.romance-central-relationship", "cw.relationship", "supports", "A causally developed relationship supports the central structure of genre romance."),
    ("lit-romance-arc", "lit.romance-emotional-arc", "lit.romance-central-relationship", "part_of", "The emotional arc is part of the central relationship trajectory."),
    ("lit-historical-research", "lit.historical-research", "lit.contextual-reading", "supports", "Historical research supports contextually constrained invention and interpretation."),
    ("lit-anachronism-research", "lit.historical-research", "lit.historical-anachronism", "prevents", "Versioned historical research helps prevent accidental anachronism."),
    ("lit-nonfiction-fiction", "lit.literary-nonfiction-contract", "cw.fiction-marker", "qualifies", "The nonfiction truth contract qualifies which inventions require explicit marking or exclusion."),
    ("lit-memory-uncertainty", "lit.memoir-memory", "lit.literary-nonfiction-contract", "qualifies", "Memory uncertainty qualifies the precision appropriate to memoir claims."),
    ("lit-translation-context", "lit.translation", "lit.cultural-specificity", "prerequisite", "Cultural and linguistic specificity is prerequisite to responsible literary translation choices."),
    ("lit-reception-context", "lit.reception", "lit.contextual-reading", "implements", "Reception history implements contextual analysis across communities and periods."),
    ("lit-oral-fixed", "lit.oral-performance", "lit.form-content", "qualifies", "Performance variation qualifies analysis that assumes one fixed textual form."),
    ("cw-brief-hard", "cw.brief", "cw.hard-constraint", "grounds", "The brief grounds the set of non-negotiable creative constraints."),
    ("cw-brief-soft", "cw.brief", "cw.soft-preference", "grounds", "The brief grounds preferences used to rank otherwise valid candidates."),
    ("cw-hard-candidate", "cw.hard-constraint", "cw.candidate-set", "qualifies", "Hard constraints qualify which generated candidates remain admissible."),
    ("cw-candidates-selection", "cw.candidate-set", "cw.selection-criteria", "prerequisite", "A diverse candidate set is prerequisite to comparative creative selection."),
    ("cw-criteria-candidate", "cw.selection-criteria", "cw.candidate-set", "transforms_to", "Selection criteria transform a broad candidate set into retained and rejected alternatives."),
    ("cw-premise-logline", "cw.premise", "cw.logline", "transforms_to", "A premise can be compressed into a logline that exposes its dramatic engine."),
    ("cw-logline-question", "cw.logline", "cw.story-question", "supports", "A precise logline supports a focused central story question."),
    ("cw-inciting-goal", "cw.inciting-change", "cw.goal", "causes", "An inciting change can cause an agent to adopt a new dramatic goal."),
    ("cw-goal-obstacle", "cw.goal", "cw.obstacle", "prerequisite", "An intelligible goal is prerequisite to recognizing an obstacle as resistance."),
    ("cw-obstacle-conflict", "cw.obstacle", "lit.conflict", "enables", "Effective resistance enables story conflict."),
    ("cw-stakes-tension", "cw.stakes", "cw.tension", "enables", "Consequential stakes enable sustained tension under uncertainty."),
    ("cw-turn-plot", "cw.turning-point", "lit.plot", "transforms_to", "A turning point transforms the available plot trajectory."),
    ("cw-climax-resolution", "cw.climax", "cw.resolution", "causes", "The climax causes the decisive state change that the resolution registers."),
    ("cw-subplot-main", "cw.subplot", "lit.plot", "qualifies", "A subplot qualifies the main plot through thematic, causal, or relational interaction."),
    ("cw-want-goal", "cw.want", "cw.goal", "supports", "A conscious want supports formation of a dramatic goal."),
    ("cw-need-arc", "cw.need", "cw.arc", "enables", "An unmet need enables a pressure-tested character arc."),
    ("cw-agency-causal", "cw.agency", "lit.causal-chain", "supports", "Character agency supports an action-driven causal chain."),
    ("cw-motivation-agency", "cw.motivation", "cw.agency", "grounds", "Motivation grounds why a character selects one consequential action among alternatives."),
    ("cw-contradiction-arc", "cw.contradiction", "cw.arc", "enables", "A consequential internal contradiction enables transformation or tested persistence."),
    ("cw-backstory-motivation", "cw.backstory", "cw.motivation", "supports", "Selected backstory can support present motivation."),
    ("cw-action-character", "cw.characterization", "lit.character", "implements", "Characterization implements the textual evidence from which a literary character is inferred."),
    ("cw-scene-goal-conflict", "cw.scene-goal", "cw.scene-conflict", "enables", "An immediate goal enables scene conflict when it meets resistance."),
    ("cw-conflict-turn", "cw.scene-conflict", "cw.scene-turn", "causes", "Active resistance can cause a scene's material turn."),
    ("cw-turn-next", "cw.scene-turn", "cw.scene-sequel", "causes", "A scene turn creates consequences that cause reflection and renewed decision."),
    ("cw-summary-pacing", "cw.summary", "cw.pacing", "implements", "Summary implements temporal compression and therefore changes pacing."),
    ("cw-blocking-scene", "cw.blocking", "cw.scene-conflict", "qualifies", "Spatial blocking qualifies which tactics and interactions are possible in a scene."),
    ("cw-voice-tone", "cw.voice", "cw.tone", "supports", "Consistent voice choices support a perceivable tone."),
    ("cw-first-distance", "cw.first-person", "cw.narrative-distance", "qualifies", "First-person temporal and cognitive position qualifies narrative distance."),
    ("cw-third-distance", "cw.third-limited", "cw.narrative-distance", "qualifies", "Third-limited access supports adjustable distance around one viewpoint."),
    ("cw-transition-headhop", "cw.viewpoint-transition", "cw.third-limited", "supports", "Clear viewpoint transitions support coherent multi-viewpoint use of third-person limitation."),
    ("cw-objective-subtext", "cw.dialogue-objective", "cw.subtext", "enables", "Competing dialogue objectives enable meaning beneath literal wording."),
    ("cw-idiolect-character", "cw.idiolect", "cw.characterization", "implements", "Idiolect implements one dimension of characterization through speech pattern."),
    ("cw-beat-blocking", "cw.dialogue-beat", "cw.blocking", "supports", "Dialogue beats support spatial and rhythmic clarity."),
    ("cw-setting-rule", "cw.world-rule", "cw.setting-model", "part_of", "World rules form part of a setting's causal model."),
    ("cw-cost-rule", "cw.world-cost", "cw.world-rule", "qualifies", "Costs and externalities qualify a world rule's actual affordances."),
    ("cw-ledger-continuity", "cw.continuity-ledger", "cw.continuity-constraint", "implements", "A continuity ledger implements checkable story-state constraints."),
    ("cw-research-fact", "cw.research-boundary", "cw.factual-anchor", "supports", "A declared research boundary supports preservation of factual anchors."),
    ("cw-uncertainty-tension", "cw.suspense-surprise", "cw.tension", "supports", "Managed information and uncertainty support narrative tension."),
    ("cw-urgency-tension", "cw.urgency", "cw.tension", "supports", "Causally grounded urgency supports tension by limiting delay."),
    ("cw-escalation-stakes", "cw.escalation", "cw.stakes", "transforms_to", "Escalation transforms the scale, cost, or complexity of stakes."),
    ("cw-compress-pace", "cw.compression-expansion", "cw.pacing", "implements", "Compression and expansion implement changes in experienced pace."),
    ("cw-reveal-prior", "cw.reveal", "lit.thriller-reversal", "analogous_to", "A revelation and a thriller reversal are analogous when both recast prior evidence."),
    ("cw-structure-scene", "cw.structural-revision", "cw.scene-revision", "prerequisite", "Structural decisions should stabilize before scene-level polishing where changes would otherwise be discarded."),
    ("cw-scene-line", "cw.scene-revision", "cw.line-revision", "prerequisite", "Scene function should be sound before line-level polish is treated as final."),
    ("cw-line-copy", "cw.line-revision", "cw.copyedit", "prerequisite", "Line revision normally precedes final copyediting."),
    ("cw-feedback-revision", "cw.feedback-triage", "cw.structural-revision", "supports", "Triaged reader effects can support targeted structural revision."),
    ("cw-screen-action", "cw.screen-action", "cw.screen-sequence", "part_of", "Performable visual actions compose larger screen sequences."),
    ("cw-stage-play", "cw.play-stage-world", "cw.play-performability", "supports", "Economical use of stage resources supports performability."),
    ("cw-lineation-image", "cw.poetry-lineation", "cw.poetry-image", "qualifies", "Lineation qualifies how a poetic image unfolds and doubles meaning."),
    ("cw-poetic-constraint", "cw.poetry-constraint", "cw.candidate-set", "enables", "A poetic constraint enables candidate generation by restricting the search space."),
    ("cw-promise-hybrid", "cw.genre-promise", "cw.genre-hybrid", "qualifies", "Audience promises qualify whether combined genres remain coherent."),
    ("cw-hybrid-innovation", "cw.genre-hybrid", "cw.genre-innovation", "enables", "Hybridization enables one route to legible genre innovation."),
    ("cw-fact-fiction", "cw.factual-anchor", "cw.fiction-marker", "qualifies", "Factual anchors qualify where inventions must be marked or excluded."),
    ("cw-continuity-candidate", "cw.continuity-constraint", "cw.candidate-set", "inhibits", "Established continuity inhibits candidates that contradict story state without a change mechanism."),
    ("cw-style-copy", "cw.transformative-style", "cw.hard-constraint", "supports", "Feature-based style design supports originality and rights constraints."),
    ("tw-audience-purpose", "tw.audience", "tw.purpose", "qualifies", "Audience needs qualify a document's operational purpose."),
    ("tw-purpose-task", "tw.purpose", "tw.task", "clarifies", "Purpose clarifies which user task the document must support."),
    ("tw-prereq-procedure", "tw.prerequisite", "tw.procedure-goal", "prerequisite", "Documented starting conditions are prerequisite to a reliable procedure."),
    ("tw-scope-version", "tw.scope", "tw.version-boundary", "supports", "Explicit scope supports a checkable product or standard version boundary."),
    ("tw-ia-audience", "tw.audience", "tw.information-architecture", "qualifies", "Audience tasks qualify documentation organization and navigation."),
    ("tw-owner-version", "tw.maintenance-owner", "tw.version-boundary", "supports", "Accountable ownership supports timely version-boundary maintenance."),
    ("tw-tutorial-howto", "tw.tutorial", "tw.how-to", "analogous_to", "Tutorials and how-to guides both inform action but serve learning and task application differently."),
    ("tw-reference-explanation", "tw.reference", "tw.explanation", "analogous_to", "Reference and explanation both inform cognition but optimize lookup and understanding differently."),
    ("tw-concept-explanation", "tw.concept-topic", "tw.explanation", "part_of", "Concept topics can compose a larger explanatory structure."),
    ("tw-trouble-evidence", "tw.troubleshooting", "tw.procedure-verification", "supports", "Troubleshooting depends on observable checks that discriminate causes and verify repair."),
    ("tw-api-overview-endpoint", "tw.api-endpoint", "tw.api-overview", "part_of", "Endpoint topics form part of the API documentation system."),
    ("tw-api-param-request", "tw.api-parameter", "tw.api-request", "prerequisite", "Complete parameter definitions are prerequisite to a valid request example."),
    ("tw-api-request-response", "tw.api-request", "tw.api-response", "causes", "A valid request under declared state causes one of the documented response classes."),
    ("tw-api-error-response", "tw.api-error", "tw.api-response", "qualifies", "The error contract qualifies non-success response semantics."),
    ("tw-api-auth-request", "tw.api-auth", "tw.api-request", "prerequisite", "Required authentication context is prerequisite to an authorized request."),
    ("tw-idempotency-retry", "tw.api-idempotency", "tw.api-error", "qualifies", "Idempotency semantics qualify when a caller can safely retry after uncertain failure."),
    ("tw-deprecation-version", "tw.api-deprecation", "tw.version-boundary", "transforms_to", "A deprecation notice transforms the supported version boundary through a dated migration path."),
    ("tw-goal-input", "tw.procedure-input", "tw.procedure-goal", "prerequisite", "Declared inputs are prerequisite to achieving a procedure's postcondition."),
    ("tw-step-goal", "tw.ordered-step", "tw.procedure-goal", "supports", "Ordered actions support the declared procedural postcondition."),
    ("tw-condition-step", "tw.step-condition", "tw.ordered-step", "qualifies", "A preposed condition qualifies which step branch applies."),
    ("tw-step-verify", "tw.ordered-step", "tw.procedure-verification", "causes", "Correct execution should cause an independently observable postcondition."),
    ("tw-warning-step", "tw.warning", "tw.ordered-step", "qualifies", "A warning qualifies a hazardous step before action."),
    ("tw-rollback-step", "tw.rollback", "tw.ordered-step", "qualifies", "Rollback boundaries qualify the reversibility of a procedure."),
    ("tw-keyword-must", "tw.normative-keyword", "tw.must", "clarifies", "The governing convention clarifies when uppercase MUST expresses an absolute requirement."),
    ("tw-keyword-should", "tw.normative-keyword", "tw.should", "clarifies", "The governing convention clarifies that SHOULD permits only understood, justified exceptions."),
    ("tw-keyword-may", "tw.normative-keyword", "tw.may", "clarifies", "The governing convention clarifies when MAY expresses permission."),
    ("tw-requirement-accept", "tw.requirement", "tw.acceptance-criterion", "supports", "A testable acceptance criterion supports deciding whether a requirement is satisfied."),
    ("tw-trace-requirement", "tw.traceability", "tw.requirement", "supports", "Traceability supports impact analysis and evidence linkage for requirements."),
    ("tw-invariant-state", "tw.invariant", "tw.state-machine", "qualifies", "Invariants qualify every admissible state and transition."),
    ("tw-state-sequence", "tw.state-machine", "tw.sequence", "supports", "A state model supports specification of valid protocol sequences."),
    ("tw-nonnorm-keyword", "tw.non-normative", "tw.normative-keyword", "prevents", "Marking examples non-normative prevents them from silently imposing extra conformance requirements."),
    ("tw-question-methods", "tw.research-question", "tw.methods", "qualifies", "The research question qualifies the study design and measurements."),
    ("tw-methods-results", "tw.methods", "tw.results", "prerequisite", "Declared methods are prerequisite to interpreting reported results."),
    ("tw-results-discussion", "tw.results", "tw.discussion", "grounds", "Results ground the study-specific claims developed in discussion."),
    ("tw-uncertainty-discussion", "tw.uncertainty", "tw.discussion", "qualifies", "Uncertainty qualifies interpretation and generalization."),
    ("tw-repro-methods", "tw.reproducibility", "tw.methods", "supports", "A reproducibility statement supports independent reconstruction of methods and analysis."),
    ("tw-citation-thesis", "tw.citation", "tw.thesis", "supports", "Version-matched citations support externally grounded premises of a thesis."),
    ("tw-synthesis-thesis", "tw.literature-synthesis", "tw.thesis", "qualifies", "Literature synthesis qualifies how a thesis relates to agreement and dispute."),
    ("tw-counter-thesis", "tw.counterargument", "tw.thesis", "qualifies", "A serious counterargument qualifies the scope or defense of a thesis."),
    ("tw-quote-citation", "tw.quotation-boundary", "tw.citation", "prerequisite", "A visible quotation boundary and exact source are prerequisites to responsible direct quotation."),
    ("tw-summary-decision", "tw.executive-summary", "tw.decision-memo", "part_of", "An executive summary forms the decision-first entry to a longer memo."),
    ("tw-proposal-decision", "tw.proposal", "tw.decision-memo", "analogous_to", "Proposals and decision memos share option and tradeoff structure but ask for different commitments."),
    ("tw-source-fact", "tw.news-source", "tw.news-fact", "supports", "A source with relevant access can support a fact after corroboration and checking."),
    ("tw-attribution-fact", "tw.news-attribution", "tw.news-fact", "qualifies", "Attribution qualifies whether a sentence reports observation, allegation, or analysis."),
    ("tw-fact-lead", "tw.news-fact", "tw.news-lead", "grounds", "The most consequential verified development grounds a news lead."),
    ("tw-correction-fact", "tw.news-correction", "tw.news-fact", "transforms_to", "A correction replaces an inaccurate claim with a checked account while preserving an audit trail."),
    ("tw-substantive-line", "tw.substantive-edit", "tw.line-edit", "prerequisite", "Substantive structure should stabilize before final line editing."),
    ("tw-line-copy", "tw.line-edit", "tw.copyedit", "prerequisite", "Line-level meaning and flow should stabilize before final copyediting."),
    ("tw-copy-proof", "tw.copyedit", "tw.proofread", "prerequisite", "Copyediting normally precedes final rendered proofreading."),
    ("tw-fact-substantive", "tw.fact-check", "tw.substantive-edit", "qualifies", "Fact-check results qualify substantive claims and may require structural change."),
    ("tw-plain-audience", "tw.plain-language", "tw.audience", "supports", "Plain-language decisions support the intended audience's ability to find and use information."),
    ("tw-heading-ia", "tw.heading", "tw.information-architecture", "implements", "Descriptive headings implement a scannable information hierarchy."),
    ("tw-link-ia", "tw.link-text", "tw.information-architecture", "implements", "Descriptive links implement navigable relationships among topics."),
    ("tw-alt-access", "tw.alt-text", "tw.plain-language", "supports", "Purposeful alternative text supports access to non-text information."),
    ("tw-table-access", "tw.table-access", "tw.plain-language", "supports", "Semantic table structure supports finding and interpreting tabular information."),
    ("tw-load-ia", "tw.cognitive-load", "tw.information-architecture", "qualifies", "Cognitive-load constraints qualify chunking and progressive disclosure."),
    ("tw-global-locale", "tw.global-audience", "tw.locale-sensitive", "qualifies", "Global-audience analysis qualifies which content needs locale-aware representation."),
    ("tw-term-translate", "tw.terminology", "tw.translatable-source", "supports", "Controlled terminology supports consistent translation and search."),
    ("bridge-literary-rhetoric", "lit.close-reading", "tw.audience", "analogous_to", "Literary close reading and audience analysis both infer effects from evidence, but neither alone proves actual reception."),
    ("bridge-genre-brief", "lit.genre", "cw.brief", "qualifies", "Genre expectations qualify the creative brief without becoming inviolable laws."),
    ("bridge-plot-procedure", "lit.plot", "tw.sequence", "analogous_to", "Plot and protocol sequence both organize transitions, but fictional consequence and normative behavior have different truth conditions."),
    ("bridge-world-invariant", "cw.world-rule", "tw.invariant", "analogous_to", "World rules and system invariants both constrain state transitions while belonging to creative and executable epistemic classes respectively."),
    ("bridge-revision-edit", "cw.structural-revision", "tw.substantive-edit", "analogous_to", "Creative structural revision and technical substantive editing both address global organization before line polish."),
    ("bridge-fact-anchor-check", "cw.factual-anchor", "tw.fact-check", "supports", "Fact checking supports preservation of real-world anchors inside creative work."),
    ("bridge-reveal-troubleshoot", "cw.reveal", "tw.troubleshooting", "analogous_to", "A fair reveal and a diagnostic conclusion both become stronger when prior evidence discriminates alternatives."),
    ("bridge-voice-audience", "cw.voice", "tw.audience", "qualifies", "Audience and purpose qualify voice choices across creative and technical forms."),
]


CONTROLS = [
    ("lit-author-narrator", "literature", "literature.narrative", LIT_LANES, "Author-narrator collapse", "Do not attribute every narrator statement or attitude to the historical author without independent evidence."),
    ("lit-theme-topic", "literature", "literature.criticism", LIT_LANES, "Theme reduced to topic", "A one-word subject label does not establish how a work develops a theme."),
    ("lit-device-count", "literature", "literature.criticism", LIT_LANES, "Device counting as interpretation", "Naming imagery, metaphor, or repetition without explaining its patterned effect does not constitute literary analysis."),
    ("lit-intent-effect", "literature", "literature.criticism", LIT_LANES, "Intent inferred from effect", "A plausible textual effect must not be reported as proof of the author's private intention."),
    ("lit-single-reading", "literature", "literature.criticism", LIT_LANES, "Unsupported single reading", "Do not call one interpretation definitive while material counterevidence or live alternatives remain untested."),
    ("lit-context-replacement", "literature", "literature.comparative", LIT_LANES, "Context replaces text", "Historical context must not replace analysis of the textual relation it is claimed to explain."),
    ("lit-biographical-diagnosis", "literature", "literature.criticism", LIT_LANES, "Biographical diagnosis", "A literary work must not be used by itself to diagnose its author, characters, or readers clinically."),
    ("lit-genre-law", "literature", "literature.criticism", LIT_LANES, "Genre as rigid law", "A convention's absence does not automatically make a work invalid or misclassified."),
    ("lit-anachronistic-judgment", "literature", "literature.historical-fiction", LIT_LANES, "Unmarked presentism", "Present categories must not be projected backward without checking their historical availability and consequences."),
    ("lit-translation-equivalence", "literature", "literature.comparative", LIT_LANES, "Perfect translation equivalence", "A translation choice must not be treated as lossless identity across language, form, and context."),
    ("lit-oral-fixed", "literature", "literature.world", LIT_LANES, "Oral work treated as fixed text", "Performance variation must not be erased by assuming one transcription exhausts an oral tradition."),
    ("lit-speculation-prediction", "literature", "literature.science-fiction", LIT_LANES, "Speculation reported as prediction", "A science-fiction extrapolation must not be presented as an empirical forecast."),
    ("cw-fluency-validity", "creative-writing", "creative-writing.revision", CREATIVE_LANES, "Fluency mistaken for fitness", "A fluent candidate that violates the brief or continuity must not survive selection."),
    ("cw-novelty-value", "creative-writing", "creative-writing.genre", CREATIVE_LANES, "Novelty without value", "Surprise alone must not outrank coherence, purpose, audience fit, or emotional consequence."),
    ("cw-trope-copy", "creative-writing", "creative-writing.genre", CREATIVE_LANES, "Trope copying", "Genre training must not reproduce a source's protected expression or substitute trope inventory for causal design."),
    ("cw-fact-invention", "creative-writing", "creative-writing.constraint-preservation", CREATIVE_LANES, "Invented fact laundering", "Invented citations, quotations, data, people, or events must not be emitted as real evidence."),
    ("cw-continuity-break", "creative-writing", "creative-writing.constraint-preservation", CREATIVE_LANES, "Silent continuity break", "A later passage must not contradict established state without an explicit change or correction."),
    ("cw-pov-leak", "creative-writing", "creative-writing.voice", CREATIVE_LANES, "Unsignaled viewpoint leak", "A limited viewpoint must not assert inaccessible thoughts or facts without a justified transition or inference."),
    ("cw-exposition-dialogue", "creative-writing", "creative-writing.dialogue", CREATIVE_LANES, "Shared-knowledge recital", "Characters must not recite mutually known background solely for the reader without a present conversational motive."),
    ("cw-escalation-no-cause", "creative-writing", "creative-writing.tension", CREATIVE_LANES, "Uncaused escalation", "Threat or urgency must not increase merely because the prose declares it; a causal change is required."),
    ("cw-polish-before-structure", "creative-writing", "creative-writing.revision", CREATIVE_LANES, "Premature line polish", "Surface polish must not be treated as completion while premise, causal chain, or scene function remains broken."),
    ("cw-culture-prop", "creative-writing", "creative-writing.setting", CREATIVE_LANES, "Culture as decorative prop", "A living or historical culture must not be reduced to interchangeable exotic detail without specific research and agency."),
    ("cw-mental-illness-monster", "creative-writing", "creative-writing.character", CREATIVE_LANES, "Diagnosis as monstrosity", "Mental illness must not be used as an unsupported synonym for violence, evil, or unreliability."),
    ("cw-living-author", "creative-writing", "creative-writing.constraint-preservation", CREATIVE_LANES, "Living-author imitation", "A request to copy a living author's recognizable style must be transformed into general craft dimensions rather than close imitation."),
    ("tw-feature-task", "technical-professional-writing", "technical-professional-writing.documentation", TECHNICAL_LANES, "Feature list as task documentation", "A feature inventory must not substitute for the user's goal, starting state, path, and verification."),
    ("tw-success-no-proof", "technical-professional-writing", "technical-professional-writing.instructions", TECHNICAL_LANES, "Exit zero as sole verification", "A command completing without an error must not alone prove the promised external postcondition."),
    ("tw-secret-example", "technical-professional-writing", "technical-professional-writing.api-docs", TECHNICAL_LANES, "Secret in example", "Documentation examples must never contain live credentials, private tokens, or recoverable personal data."),
    ("tw-example-contract", "technical-professional-writing", "technical-professional-writing.api-docs", TECHNICAL_LANES, "Example contradicts contract", "An example that fails the documented schema or version must not be published as authoritative."),
    ("tw-should-ambiguity", "technical-professional-writing", "technical-professional-writing.specifications", TECHNICAL_LANES, "Ambiguous should", "Lowercase advice must not be silently interpreted as a BCP 14 normative requirement."),
    ("tw-requirement-design", "technical-professional-writing", "technical-professional-writing.specifications", TECHNICAL_LANES, "Requirement hides design", "A requirement must not prescribe an implementation mechanism unless that mechanism is itself a necessary external constraint."),
    ("tw-warning-after", "technical-professional-writing", "technical-professional-writing.instructions", TECHNICAL_LANES, "Warning after hazard", "A safety warning placed only after the hazardous action fails to prevent the harm."),
    ("tw-rollback-claim", "technical-professional-writing", "technical-professional-writing.instructions", TECHNICAL_LANES, "False reversibility", "Do not promise rollback for destructive or externally propagated effects that the documented operation cannot recover."),
    ("tw-result-interpretation", "technical-professional-writing", "technical-professional-writing.scientific", TECHNICAL_LANES, "Result and interpretation collapse", "Observed results must remain distinguishable from causal explanation, generalization, and recommendation."),
    ("tw-citation-authority", "technical-professional-writing", "technical-professional-writing.academic", TECHNICAL_LANES, "Citation as automatic authority", "A citation must not count as support until source identity, relevance, version, and faithful representation are checked."),
    ("tw-allegation-fact", "technical-professional-writing", "technical-professional-writing.journalism", TECHNICAL_LANES, "Allegation laundered as fact", "A source's allegation must retain attribution and must not become the writer's unqualified factual voice."),
    ("tw-access-decoration", "technical-professional-writing", "technical-professional-writing.accessibility", TECHNICAL_LANES, "Accessibility as decoration", "Visual polish must not override semantic structure, keyboard access, contrast, alternative text, or readable language."),
    ("tw-word-substitution", "technical-professional-writing", "technical-professional-writing.localization", TECHNICAL_LANES, "Localization as word substitution", "Localization must not ignore grammar, plural rules, units, dates, layout, cultural context, and product behavior."),
]


WORKED_EXAMPLES = [
    ("lit", "passage-evidence-map", "Passage evidence map", "A worked analysis maps a repeated threshold image to its changed contexts, tests a theme claim against one counterexample, and leaves authorial intent unasserted.", "literature.criticism", LIT_LANES, LIT_SOURCES, "interpretive"),
    ("lit", "narrative-time-map", "Narrative time map", "A worked narrative map lists event chronology separately from presentation order, then marks one flashback, one omitted interval, and one repeated account.", "literature.narrative", LIT_LANES, LIT_SOURCES, "interpretive"),
    ("lit", "genre-comparison", "Genre comparison", "A worked comparison distinguishes a mystery clue from a thriller threat by the uncertainty each organizes and then notes a hybrid case.", "literature.criticism", LIT_LANES, LIT_SOURCES, "interpretive"),
    ("cw", "scene-state-delta", "Scene state delta", "A worked scene begins with trust high and evidence absent, introduces a resisted disclosure, and exits with evidence present and trust damaged.", "creative-writing.scene", CREATIVE_LANES, CREATIVE_SOURCES, "creative"),
    ("cw", "candidate-selection", "Candidate selection", "A worked ideation pass generates a chronological opening, an aftermath opening, and a mistaken-identity opening, rejects the third for violating the brief, and selects the second for tension and fit.", "creative-writing.revision", CREATIVE_LANES, CREATIVE_SOURCES, "creative"),
    ("cw", "continuity-check", "Continuity check", "A worked continuity review catches that a key destroyed in chapter two reappears unchanged in chapter four and requires either removal or an explicit recovery mechanism.", "creative-writing.constraint-preservation", CREATIVE_LANES, CREATIVE_SOURCES, "creative"),
    ("cw", "lateral-frame", "Lateral frame shift", "A worked lateral pass reframes a locked-room problem from how someone entered to whether the room itself changed ownership, time, or definition.", "creative-writing.genre", CREATIVE_LANES, CREATIVE_SOURCES, "creative"),
    ("tw", "procedure-postcondition", "Procedure postcondition", "A worked deployment instruction verifies the served build identifier from the public endpoint rather than treating a successful upload command as proof of release.", "technical-professional-writing.instructions", TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
    ("tw", "api-error-example", "API error example", "A worked API entry pairs an invalid cursor request with its exact status, stable error code, retry rule, and caller correction.", "technical-professional-writing.api-docs", TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
    ("tw", "normative-requirement", "Normative requirement", "A worked specification invokes BCP 14, assigns a unique requirement identifier, uses MUST for one conformance condition, and links it to a failing and passing test.", "technical-professional-writing.specifications", TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
    ("tw", "scientific-boundary", "Scientific claim boundary", "A worked report states the measured association with uncertainty in Results and moves causal explanations and external generalization into qualified Discussion hypotheses.", "technical-professional-writing.scientific", TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
    ("tw", "localization-review", "Localization review", "A worked review replaces an ambiguous numeric date, externalizes a sentence fragment, documents a placeholder's grammatical role, and preserves locale-aware number formatting.", "technical-professional-writing.localization", TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
]


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 31 == 0:
        return "cross_domain_holdout"
    if index % 23 == 0:
        return "sealed_test"
    if index % 17 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 29 == 0:
        return "cross_domain_holdout"
    if index and index % 19 == 0:
        return "sealed_test"
    if index and index % 13 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    domain: str,
    subject: str,
    lanes: list[str],
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": sorted(set(lanes)),
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "literature, creative-writing, and technical-writing foundation tranche",
        "limitations": [
            "This tranche maps transferable primitives and representative genre systems; historical, linguistic, cultural, and specialist expansion remains open in the coverage ledger.",
            "Genre conventions are defeasible expectations, not universal laws.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "literature-writing-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def sources_for_relation(identifier: str, source: str, target: str) -> list[str]:
    sources: set[str] = set()
    for endpoint in (source, target):
        if endpoint.startswith("lit."):
            sources.update(LIT_SOURCES)
        elif endpoint.startswith("cw."):
            sources.update(CREATIVE_SOURCES)
        elif endpoint.startswith("tw."):
            sources.update(TECHNICAL_SOURCES)
    if identifier.startswith("bridge-"):
        sources.update(LIT_SOURCES)
        sources.update(CREATIVE_SOURCES)
        sources.update(TECHNICAL_SOURCES)
    return sorted(sources)


def lanes_for_relation(source: str, target: str) -> list[str]:
    lanes: set[str] = set()
    for endpoint in (source, target):
        if endpoint.startswith("lit."):
            lanes.update(LIT_LANES)
        elif endpoint.startswith("cw."):
            lanes.update(CREATIVE_LANES)
        elif endpoint.startswith("tw."):
            lanes.update(TECHNICAL_LANES)
    return sorted(lanes)


def relation_owner(identifier: str) -> tuple[str, str, str]:
    if identifier.startswith("lit-"):
        return "literature", "literature.criticism", "interpretive"
    if identifier.startswith("cw-"):
        return "creative-writing", "creative-writing.story-structure", "creative"
    if identifier.startswith("tw-"):
        return "technical-professional-writing", "technical-professional-writing.documentation", "established"
    return "creative-writing", "creative-writing.constraint-preservation", "interpretive"


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    concept_groups = [
        ("lit", "literature", LITERATURE, LIT_LANES, LIT_SOURCES, "interpretive"),
        ("cw", "creative-writing", CREATIVE_WRITING, CREATIVE_LANES, CREATIVE_SOURCES, "creative"),
        ("tw", "technical-professional-writing", TECHNICAL_WRITING, TECHNICAL_LANES, TECHNICAL_SOURCES, "established"),
    ]

    for prefix, domain, entries, lanes, sources, epistemic in concept_groups:
        root_id = f"{prefix}.root"
        for index, (identifier, label, statement, subject) in enumerate(entries):
            node_id = f"{prefix}.{identifier}"
            concept_split = split_for(index, root=identifier == "root")
            records.append(
                {
                    **make_base(node_id, domain, subject, lanes, sources, concept_split, "concept", epistemic),
                    "label": label,
                    "statement": statement,
                    "aliases": [label.lower()],
                }
            )
            if identifier == "root":
                continue
            membership_id = f"lw.membership.{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        membership_id,
                        domain,
                        subject,
                        lanes,
                        sources,
                        edge_split_for(index),
                        "relation",
                        epistemic,
                    ),
                    "label": f"{label} world membership",
                    "statement": f"{label} is a distinct component of the {domain} world and retains its own scope and failure conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": root_id,
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared foundation-world scope applies"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in RELATIONS])
    for identifier, source, target, kind, statement in RELATIONS:
        domain, subject, epistemic = relation_owner(identifier)
        split = splitter.split(kind, cross_requested=identifier.startswith("bridge-"))
        records.append(
            {
                **make_base(
                    f"lw.relation.{identifier}",
                    domain,
                    subject,
                    lanes_for_relation(source, target),
                    sources_for_relation(identifier, source, target),
                    split,
                    "relation",
                    epistemic,
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source,
                    "target_node": target,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["the stated scope, genre, audience, and version boundaries are held fixed"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, domain, subject, lanes, label, statement) in enumerate(CONTROLS):
        split = control_splits[index % len(control_splits)]
        record_id = f"lw.control.{identifier}"
        records.append(
            {
                **make_base(record_id, domain, subject, lanes, [], split, "synthetic_control", "synthetic_control"),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", domain],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    root_for_prefix = {"lit": "lit.root", "cw": "cw.root", "tw": "tw.root"}
    domain_for_prefix = {
        "lit": "literature",
        "cw": "creative-writing",
        "tw": "technical-professional-writing",
    }
    for index, (prefix, identifier, label, statement, subject, lanes, sources, epistemic) in enumerate(WORKED_EXAMPLES):
        split = example_splits[index % len(example_splits)]
        node_id = f"{prefix}.example.{identifier}"
        domain = domain_for_prefix[prefix]
        records.append(
            {
                **make_base(node_id, domain, subject, lanes, sources, split, "worked_example", epistemic),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "within_domain_composition", "deductions_predictions_execution"],
                "tags": ["worked-example", domain],
            }
        )
        relation_id = f"lw.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(relation_id, domain, subject, lanes, sources, split, "relation", epistemic),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded composition in the {domain} world.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": root_for_prefix[prefix],
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains illustrative rather than universal"],
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
