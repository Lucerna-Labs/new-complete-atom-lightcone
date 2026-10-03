"""Colour theory causation: additive versus subtractive, contrast, perception, accessibility."""

WORLD = "color-causation-v0"
PREFIX = "col"
DOMAIN = "typography-color-visual-design"
SUBJECT = "typography-color-visual-design.color-theory"
SOURCES = ["w3c-css-color-4", "w3c-wcag-22", "w3c-compositing-1-20240321", "w3c-wcag22-understanding-use-color", "witzel-afterimages-2025", "sinha-brightness-contrast-2020", "dynamic-color-afterimages-2022"]
SCOPE = "Introductory colour mixing, CSS Color 4 notation, source-over compositing, WCAG 2.2 luminance and contrast, and bounded human colour-perception effects; aesthetic preference is not a causal guarantee"
ROOT_LABEL = "Colour theory causation world"
ROOT_STATEMENT = "Root of the colour theory causation world: how light mixing, luminance and human perception cause colours to combine, contrast and mislead."

CONCEPTS = [
    ("additive-rgb", "Additive RGB mixing", "Superposition of red, green and blue light contributions; an appropriate channel balance yields a chosen white point.", []),
    ("subtractive-cmy", "Subtractive pigment mixing", "Combination of absorptive colorants that removes portions of incident light; scattering and ink spectra also affect the result.", []),
    ("screen-emissive", "Screen emissive pixels", "A display making its own coloured light.", []),
    ("print-reflection", "Print reflective inks", "Printed colorants whose absorption and scattering modify light reflected from the print substrate.", []),
    ("primary-colors-system", "System-dependent primaries", "Chosen basis colorants or light sources for a colour system; RGB is common for displays and CMY with black for process printing.", []),
    ("complementary-pair", "Complementary colour pair", "Two colours separated by half a turn on a specified hue wheel; the mixing result depends on that wheel and the physical medium.", []),
    ("color-wheel", "Hue wheel", "Colours arranged in a circle by hue.", []),
    ("hue-angle", "Hue angle", "A hue's position in degrees around the circle.", []),
    ("saturation", "Colour saturation", "Colourfulness relative to brightness; numeric saturation coordinates depend on the chosen colour model.", []),
    ("lightness", "Perceived lightness", "Perceived brightness of a surface judged relative to a similarly illuminated white reference, affected by viewing context.", []),
    ("hsl-triple", "HSL notation", "A colour written as hue, saturation and lightness numbers.", []),
    ("hex-notation", "Hex colour notation", "CSS hexadecimal sRGB channel notation with optional alpha, including three-, four-, six- and eight-digit forms.", []),
    ("relative-luminance", "Relative luminance", "WCAG sRGB linear luminance normalized to reference white: 0.2126 R + 0.7152 G + 0.0722 B after inverse sRGB transfer decoding.", []),
    ("contrast-ratio", "Contrast ratio", "The WCAG luminance ratio (L1 + 0.05)/(L2 + 0.05), with L1 the lighter and L2 the darker relative luminance.", []),
    ("wcag-contrast", "WCAG contrast minimums", "WCAG 2.2 contrast thresholds for defined content classes; meeting them is not a guarantee of readability for every viewer.", []),
    ("simultaneous-contrast", "Simultaneous contrast illusion", "A change in the apparent brightness or colour of a physically unchanged patch caused by its spatial context.", []),
    ("afterimage", "Afterimage effect", "A persisting visual response after a stimulus disappears; negative colour afterimages need not equal a hue-wheel complement.", []),
    ("warm-advance", "Warm colour advance", "A context-dependent impression of warm colours appearing nearer; it is not a universal hue-to-depth law.", []),
    ("cool-recede", "Cool colour recede", "A context-dependent impression of cool colours appearing farther; it is not a necessary converse of warm-colour advance.", []),
    ("colour-blindness", "Colour vision deficiency", "Reduced ability to separate certain hues.", []),
    ("red-green-confusion", "Red-green confusion risk", "Pairs relying only on red versus green failing for many viewers.", []),
    ("srgb-gamma", "sRGB gamma curve", "The piecewise sRGB transfer function relating linear-light channel values and nonlinear encoded channels; it is not a perceptually uniform scale.", []),
    ("alpha-blending", "Alpha transparency blending", "Partial transparency compositing layer over backdrop.", []),
    ("gamut-limit", "Device gamut limit", "The set of colours a specified display or print process can reproduce under specified viewing conditions.", []),
    ("mixing-lights-versus-pigments", "Mixing lights versus pigments", "The distinction between adding independent light radiances and changing spectral absorption and scattering through colorants.", []),
    ("neutral-gray", "Neutral grey baseline", "Grey with no hue, the reference for judging shifts.", []),
    ("tint-shade", "Tint and shade", "Lightening a hue with white or darkening it with black.", []),
    ("colour-harmony", "Colour harmony schemes", "Angle-based palettes like triads and analogues.", []),
    ("luminance-weights", "Luminance weights of R G B", "The WCAG coefficients 0.2126, 0.7152 and 0.0722 for linear sRGB red, green and blue channels.", []),
    ("alpha-composite", "Composite RGB colour", "The RGB channel result after compositing a source over its backdrop in a specified compositing colour space.", []),
    ("lightness-difference", "Lightness difference", "A visible separation between paired elements in light-dark appearance, independent of naming their hues.", []),
    ("prolonged-fixation", "Prolonged colour fixation", "Sustained gaze that keeps a coloured inducer on approximately the same retinal region during adaptation.", []),
    ("exact-reproduction", "Exact colour reproduction", "Reproduction of a specified target colour in the declared colour space and viewing condition without gamut approximation.", []),
    ("surround-luminance", "Surround luminance difference", "A difference between the luminances of backgrounds surrounding otherwise equal test patches.", []),
]

RELATIONS = [
    ("emissive-causes-additive", "screen-emissive", "additive-rgb", "causes", "Light from screen emissive pixels causes additive RGB mixing when their red, green and blue light contributions reach the same visual sample.", "an RGB display emits independent channel contributions that combine without subtractive optical filtering between those contributions", ""),
    ("reflection-causes-subtractive", "print-reflection", "subtractive-cmy", "causes", "Layering print reflective inks causes subtractive pigment mixing toward dark by removing more incident light.", "transparent nonfluorescent ink layers add absorption over the same white substrate without adding light scattering or emission", ""),
    ("wheel-enables-hue", "color-wheel", "hue-angle", "enables", "A hue wheel enables hue angle to represent position within a specified circular colour coordinate system.", "the CSS HSL convention fixes red at zero degrees and orders hues around the circle", ""),
    ("hsl-groups-components", "hsl-triple", "hue-angle", "predicts", "HSL notation predicts hue angle from its hue coordinate after normalization modulo a full turn.", "a chromatic CSS HSL colour has nonzero saturation and lightness strictly between zero and one hundred percent", ""),
    ("weights-enable-luminance", "luminance-weights", "relative-luminance", "predicts", "The set of luminance weights of R G B predicts relative luminance as 0.2126 R + 0.7152 G + 0.0722 B.", "R, G and B are linear-light sRGB channels obtained by the WCAG 2.2 inverse transfer function rather than raw encoded byte values", ""),
    ("luminance-predicts-contrast", "relative-luminance", "contrast-ratio", "predicts", "Relative luminance predicts contrast ratio as (L1 + 0.05)/(L2 + 0.05), with L1 the lighter value.", "the two final rendered colours are evaluated by WCAG 2.2 after alpha compositing and conversion to its relative-luminance representation", ""),
    ("ratio-prereq-wcag", "contrast-ratio", "wcag-contrast", "prerequisite", "A contrast ratio is a prerequisite for a numerical check against WCAG contrast minimums.", "the content is subject to WCAG 2.2 text-contrast requirements and its text size, weight and applicable conformance level are known", ""),
    ("simultaneous-shifts-grey", "surround-luminance", "simultaneous-contrast", "causes", "A surround luminance difference causes simultaneous contrast illusion in equal-luminance grey test patches.", "equal small grey patches are viewed on uniform lighter and darker surrounds in the conventional simultaneous-brightness-contrast display", ""),
    ("gamma-enables-hex", "srgb-gamma", "relative-luminance", "enables", "Inverting the sRGB gamma curve enables relative luminance computation from encoded sRGB channels.", "the input is CSS sRGB and each channel is decoded with the piecewise sRGB transfer function before the WCAG linear-weight sum", ""),
    ("alpha-inhibits-stable-contrast", "alpha-blending", "contrast-ratio", "enables", "Alpha transparency blending enables contrast ratio changes when a translucent foreground is composited against changing backgrounds.", "foreground opacity lies strictly between zero and one and the backdrop changes so the two final rendered luminances have a different WCAG ratio", ""),
    ("gamut-inhibits-extremes", "gamut-limit", "exact-reproduction", "prevents", "A device gamut limit prevents exact colour reproduction of a colour outside that gamut.", "the target is outside the calibrated device gamut under the declared viewing conditions and matching means exact colorimetric reproduction", ""),
    ("tint-shade-moves-lightness", "tint-shade", "lightness", "enables", "Applying tint and shade enables perceived lightness changes by mixing a colour with white or black.", "an opaque diffuse nonfluorescent paint mixture is viewed under fixed illumination and the added paint changes the mixture's reflectance toward white or black", ""),
    ("wheel-enables-harmony", "color-wheel", "colour-harmony", "enables", "A hue wheel enables colour harmony schemes to be constructed by specified angular separations.", "the scheme is a geometric palette recipe such as three hues spaced equally around the chosen wheel, with no claim of universal aesthetic preference", ""),
    ("deficiency-causes-confusion", "colour-blindness", "red-green-confusion", "enables", "Colour vision deficiency enables red-green confusion risk when hue is the only discriminating cue.", "a viewer has a red-green deficiency and the selected pair falls within colours that viewer cannot reliably distinguish", ""),
    ("wcag-inhibits-confusion", "lightness-difference", "red-green-confusion", "inhibits", "A lightness difference inhibits red-green confusion risk by providing an additional visible distinction between paired elements.", "the pair has a perceptible lightness separation for the viewer and the task requires distinguishing the elements rather than correctly naming their red or green hues", ""),
    ("hex-enables-rgb", "hex-notation", "additive-rgb", "enables", "Hex colour notation enables additive RGB mixing channel values to be specified in CSS.", "CSS hexadecimal colour syntax is interpreted as nonlinear encoded sRGB channel values and the display pipeline renders the decoded colour", ""),
    ("hsl-predicts-hex", "hsl-triple", "hex-notation", "predicts", "HSL notation predicts hex colour notation after conversion to sRGB and explicit channel quantization.", "an opaque in-range CSS HSL colour is converted using CSS Color 4 formulas and rounded to the nearest eight-bit channel value", ""),
    ("saturation-inhibits-grey", "saturation", "neutral-gray", "inhibits", "Increasing colour saturation inhibits a neutral grey baseline appearance by introducing nonzero chromatic channel differences.", "CSS HSL saturation increases from zero at fixed hue and lightness strictly between zero and one hundred percent, with sufficient display precision to show the change", ""),
    ("screen-causes-gamut", "screen-emissive", "gamut-limit", "causes", "The range of available emissions from screen emissive pixels causes a device gamut limit set by the display primaries and channel ranges.", "a calibrated additive display has fixed primary spectra and bounded nonnegative channel intensities", ""),
    ("print-inhibits-gamut", "print-reflection", "gamut-limit", "causes", "The set of optical properties of print reflective inks causes a device gamut limit for the specified printing process.", "the ink set, substrate, halftoning process and viewing illuminant are fixed; the print gamut need not be a subset of a particular display gamut", ""),
    ("stare-prereq-afterimage", "prolonged-fixation", "afterimage", "enables", "Prolonged colour fixation enables an afterimage effect when a sustained coloured inducer is replaced by a neutral field.", "a sighted observer maintains retinal adaptation to a visible coloured patch and then views an approximately uniform achromatic field", ""),
    ("complement-enables-harmony", "complementary-pair", "colour-harmony", "enables", "A complementary colour pair enables colour harmony schemes using opposite hues in a specified wheel.", "the palette recipe is defined by a half-turn separation in that wheel and does not imply guaranteed contrast or visual appeal", ""),
    ("alpha-enables-additive", "alpha-blending", "alpha-composite", "predicts", "Alpha transparency blending predicts composite RGB colour as alpha F + (1-alpha) B, a weighted average of foreground and backdrop.", "normal source-over compositing uses an opaque backdrop, a foreground opacity alpha between zero and one, and F and B expressed in the same compositing colour space", ""),
    ("grey-enables-wcag-checks", "neutral-gray", "relative-luminance", "predicts", "A neutral grey baseline predicts relative luminance equal to its common linear sRGB channel value.", "a CSS sRGB grey has equal encoded red, green and blue channels and those channels have been decoded to linear light", ""),
    ("hue-predicts-dominant-channel", "hue-angle", "hex-notation", "predicts", "Hue angle predicts the largest RGB channel or tied channels in hex colour notation for a chromatic CSS HSL colour.", "HSL saturation is positive, lightness is strictly between its endpoints, and eight-bit quantization has not erased the channel ordering", ""),
    ("pigment-inhibits-lightness", "subtractive-cmy", "lightness", "inhibits", "Subtractive pigment mixing inhibits perceived lightness as additional absorbing layers reduce reflected luminance.", "nonfluorescent transparent colorants add absorption without changing scattering, illumination or the observer's surrounding field", ""),
    ("saturation-strengthens-afterimage", "saturation", "afterimage", "enables", "Higher colour saturation enables a stronger afterimage effect by increasing the chromatic adaptation signal.", "a fixed-hue inducer is compared at the same luminance, exposure duration, retinal location and neutral test field within a range where stronger chromatic adaptation remains possible", "Adaptation saturation and changes in hue or test context can defeat a simple monotonic strength prediction."),
]

MYTHS = [
    ("rby-primaries", "Red, blue and yellow are the true primaries",
     "There is no unique universal set of primaries; displays commonly use RGB and process printing commonly uses CMY plus black, with other systems possible.", "primary-colors-system"),
    ("paint-mixes-like-light", "Paint mixes like light",
     "Adding independent light sources adds their radiances; mixing colorants changes absorption and scattering and need not produce the same colour.", "mixing-lights-versus-pigments"),
    ("colour-constant", "A colour looks the same everywhere",
     "Simultaneous contrast illusion shifts the same patch with its surround.", "simultaneous-contrast"),
    ("bright-means-readable", "Bright colour pairs are readable",
     "Vividness does not guarantee readable text; WCAG contrast uses relative luminance, while size, weight, context and the viewer also affect readability.", "contrast-ratio"),
    ("contrast-fixes-deficiency", "Good contrast fixes colour blindness",
     "Lightness separation and additional labels can improve discrimination, but they do not restore the ability to identify particular hues.", "red-green-confusion"),
]

BOUNDARIES = [
    ("hsl-not-perceptual", "HSL is not perceptually even",
     "Equal lightness steps in HSL notation differ in perceived brightness.", "hsl-triple"),
    ("gamut-shift", "Colours shift across devices",
     "Outside a device gamut limit, a rendering pipeline must approximate the target colour, for example by clipping or gamut mapping.", "gamut-limit"),
    ("deficiency-spectrum", "Colour deficiency varies",
     "Red-green confusion risk differs by type and degree per viewer.", "colour-blindness"),
    ("afterimage-not-complement", "Afterimages are not exact wheel complements",
     "The hue of a negative afterimage can differ from the additive or hue-wheel complement of its inducer, and depends on adaptation and viewing conditions.", "afterimage"),
    ("deficiency-luminance-limit", "Luminance is an additional cue",
     "Colour vision deficiency does not create relative luminance or make it universally sufficient; use distinguishable lightness differences and redundant labels or shapes.", "colour-blindness"),
    ("fixation-is-one-protocol", "Fixation is one induction protocol",
     "Prolonged fixation is used for a stable coloured-patch afterimage demonstration; it is not a universal prerequisite for afterimages from brief or changing stimuli.", "afterimage"),
    ("hsl-hex-quantization", "Hex conversion can round",
     "Some continuous HSL colours have no exactly equal eight-bit RGB representation; converting to six-digit hexadecimal notation rounds their channels.", "hex-notation"),
    ("alpha-colour-space", "Alpha averaging depends on colour space",
     "Source-over compositing against an opaque backdrop averages the chosen colour-space channels; only linear-light channels make that formula a physical light average.", "alpha-blending"),
]

EXAMPLES = [
    ("yellow-on-white", "Yellow text on white",
     "Saturated yellow #ffff00 on white #ffffff is vivid but has a low relative luminance gap and fails WCAG text-contrast minimums.",
     ["relative-luminance", "contrast-ratio", "wcag-contrast"]),
    ("blue-orange-poster", "A blue and orange poster",
     "A designer can choose a blue-orange pair from a specified hue wheel as a palette recipe; text legibility still requires a separate contrast check.",
     ["complementary-pair", "color-wheel", "colour-harmony"]),
    ("dark-mode-glare", "Dark mode glare",
     "Equal grey display patches can appear different on dark and light surrounds; this simultaneous contrast effect should not be equated with optical glare.",
     ["screen-emissive", "simultaneous-contrast", "lightness"]),
    ("colourblind-safe-charts", "Charts safe for colour-blind viewers",
     "A chart can separate red and green series by lightness and add different symbols and labels so identifying the series does not require naming their hues.",
     ["colour-blindness", "red-green-confusion", "lightness"]),
]

CONTROLS = [
    ("yellow-readable", "Yellow on white is readable",
     "Saturated sRGB yellow #ffff00 on white #ffffff must not be treated as passing WCAG 2.2 text-contrast minimums."),
    ("gamma-linear", "Displays show linear values",
     "The sRGB gamma curve must not be treated as linear light."),
    ("print-neon", "Print reproduces neon",
     "A print process must not be treated as reproducing every colour in an arbitrary display gamut."),
    ("alpha-free-contrast", "Transparency never changes contrast",
     "Alpha transparency blending must not be treated as guaranteeing the same contrast ratio against every background."),
]
