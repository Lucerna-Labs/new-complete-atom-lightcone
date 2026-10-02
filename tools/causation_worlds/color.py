"""Colour theory causation: additive versus subtractive, contrast, perception, accessibility."""

WORLD = "color-causation-v0"
PREFIX = "col"
DOMAIN = "typography-color-visual-design"
SUBJECT = "typography-color-visual-design.color-theory"
SOURCES = ["w3c-css-color-4"]
SCOPE = "Everyday colour theory: additive and subtractive mixing, hue saturation lightness, luminance and contrast, perception effects, colour vision deficiency, colour notation"
ROOT_LABEL = "Colour theory causation world"
ROOT_STATEMENT = "Root of the colour theory causation world: how light mixing, luminance and human perception cause colours to combine, contrast and mislead."

CONCEPTS = [
    ("additive-rgb", "Additive RGB mixing", "Screen light combining toward white as channels add.", []),
    ("subtractive-cmy", "Subtractive pigment mixing", "Ink layers absorbing light and darkening as they stack.", []),
    ("screen-emissive", "Screen emissive pixels", "A display making its own coloured light.", []),
    ("print-reflection", "Print reflective inks", "Inks surviving by reflecting leftover light off paper.", []),
    ("primary-colors-system", "System-dependent primaries", "Primaries changing with the medium: red green blue for screens, cyan magenta yellow for print.", []),
    ("complementary-pair", "Complementary colour pair", "Two hues opposite on the colour circle.", []),
    ("color-wheel", "Hue wheel", "Colours arranged in a circle by hue.", []),
    ("hue-angle", "Hue angle", "A hue's position in degrees around the circle.", []),
    ("saturation", "Saturation", "How far a colour sits from grey at the same lightness.", []),
    ("lightness", "Lightness", "How light or dark a colour appears.", []),
    ("hsl-triple", "HSL notation", "A colour written as hue, saturation and lightness numbers.", []),
    ("hex-notation", "Hex colour notation", "A colour written as red green blue byte pairs.", []),
    ("relative-luminance", "Relative luminance", "Perceived brightness weighted as human vision weights it.", []),
    ("contrast-ratio", "Contrast ratio", "The luminance distance between text and background.", []),
    ("wcag-contrast", "WCAG contrast minimums", "Accessibility floors for readable text contrast.", []),
    ("simultaneous-contrast", "Simultaneous contrast illusion", "The same colour shifting with its surround.", []),
    ("afterimage", "Afterimage effect", "A ghost complement appearing after staring at a hue.", []),
    ("warm-advance", "Warm colour advance", "Warm hues seeming nearer and larger.", []),
    ("cool-recede", "Cool colour recede", "Cool hues seeming farther and smaller.", []),
    ("colour-blindness", "Colour vision deficiency", "Reduced ability to separate certain hues.", []),
    ("red-green-confusion", "Red-green confusion risk", "Pairs relying only on red versus green failing for many viewers.", []),
    ("srgb-gamma", "sRGB gamma curve", "Non-linear value encoding matching eye sensitivity.", []),
    ("alpha-blending", "Alpha transparency blending", "Partial transparency compositing layer over backdrop.", []),
    ("gamut-limit", "Display gamut limit", "The fixed triangle of colours a device can show.", []),
    ("mixing-lights-versus-pigments", "Mixing lights versus pigments", "Light adding brightness while pigment subtracts it.", []),
    ("neutral-gray", "Neutral grey baseline", "Grey with no hue, the reference for judging shifts.", []),
    ("tint-shade", "Tint and shade", "Lightening a hue with white or darkening it with black.", []),
    ("colour-harmony", "Colour harmony schemes", "Angle-based palettes like triads and analogues.", []),
    ("luminance-weights", "Luminance weights of R G B", "Green counting most in perceived brightness.", []),
]

RELATIONS = [
    ("emissive-causes-additive", "screen-emissive", "additive-rgb", "causes", "The additive behaviour of screen emissive pixels causes additive RGB mixing toward white.", "more channels light up", ""),
    ("reflection-causes-subtractive", "print-reflection", "subtractive-cmy", "causes", "Layering print reflective inks causes subtractive pigment mixing toward mud.", "each ink absorbs more light", ""),
    ("additive-primaries", "additive-rgb", "primary-colors-system", "causes", "Additive RGB mixing causes system-dependent primaries of red, green and blue.", "the medium is a screen", ""),
    ("subtractive-primaries", "subtractive-cmy", "primary-colors-system", "causes", "Subtractive pigment mixing causes system-dependent primaries of cyan, magenta and yellow.", "the medium is pigment on paper", ""),
    ("wheel-enables-hue", "color-wheel", "hue-angle", "enables", "The hue wheel enables hue angle positions from red at zero degrees.", "colours are arranged around the circle", ""),
    ("hsl-groups-components", "hsl-triple", "hue-angle", "enables", "HSL notation enables hue angle, saturation and lightness to be stated together.", "a colour is described numerically", ""),
    ("hue-predicts-slice", "hue-angle", "color-wheel", "predicts", "A hue angle predicts the hue wheel slice a colour falls in.", "the angle is measured from red", ""),
    ("complements-oppose", "complementary-pair", "hue-angle", "predicts", "A complementary colour pair predicts hue angle positions roughly opposite by 180 degrees.", "the pair sits across the wheel", ""),
    ("mixing-complements-dulls", "complementary-pair", "neutral-gray", "causes", "Mixing a complementary colour pair causes neutral grey baseline drift instead of vivid colour.", "both pigments mix physically", ""),
    ("weights-enable-luminance", "luminance-weights", "relative-luminance", "enables", "The dominance of the luminance weights of R G B enables relative luminance to count green most.", "human vision is the standard", ""),
    ("luminance-predicts-contrast", "relative-luminance", "contrast-ratio", "predicts", "Relative luminance of text and background predicts the contrast ratio between them.", "both colours are known", ""),
    ("ratio-prereq-wcag", "contrast-ratio", "wcag-contrast", "prerequisite", "A computed contrast ratio is a prerequisite for WCAG contrast minimums checking.", "text sizes are known", ""),
    ("simultaneous-shifts-grey", "simultaneous-contrast", "neutral-gray", "causes", "Simultaneous contrast illusion causes neutral grey baseline patches to look different on different surrounds.", "the same grey sits on dark and light fields", ""),
    ("afterimage-predicts-complement", "afterimage", "complementary-pair", "predicts", "The afterimage effect predicts a complementary colour pair ghost after staring at a hue.", "one colour fatigues the cones", ""),
    ("warm-predicts-cool", "warm-advance", "cool-recede", "predicts", "Warm colour advance predicts cool colour recede in the same layout.", "depth must be signalled by hue", ""),
    ("gamma-enables-hex", "srgb-gamma", "hex-notation", "enables", "The sRGB gamma curve enables hex colour notation values to look evenly spaced.", "values encode display signals", ""),
    ("alpha-inhibits-stable-contrast", "alpha-blending", "contrast-ratio", "inhibits", "Alpha transparency blending inhibits a stable contrast ratio by shifting the composite.", "the backdrop varies", ""),
    ("gamut-inhibits-extremes", "gamut-limit", "saturation", "inhibits", "A display gamut limit inhibits saturation and lightness combinations beyond its reach.", "the requested colour sits outside the gamut", ""),
    ("medium-prereq-primaries", "mixing-lights-versus-pigments", "primary-colors-system", "prerequisite", "Knowing mixing lights versus pigments is a prerequisite for system-dependent primaries choices.", "choosing primaries for a medium", ""),
    ("tint-shade-moves-lightness", "tint-shade", "lightness", "causes", "Adding white or black tint and shade causes lightness to rise or fall.", "a pure hue is mixed", ""),
    ("wheel-enables-harmony", "color-wheel", "colour-harmony", "enables", "The hue wheel enables colour harmony schemes like triads and analogues.", "colours are picked by angle", ""),
    ("deficiency-causes-confusion", "colour-blindness", "red-green-confusion", "causes", "Red-green colour vision deficiency causes red-green confusion risk for paired hues.", "hue differs only between red and green", ""),
    ("deficiency-enables-luminance", "colour-blindness", "relative-luminance", "enables", "The pattern of colour vision deficiency enables relative luminance differences as the safe channel.", "colour alone must not carry meaning", ""),
    ("wcag-inhibits-confusion", "wcag-contrast", "red-green-confusion", "inhibits", "The WCAG contrast minimums rule inhibits red-green confusion risk by forcing lightness separation.", "paired elements differ in luminance", ""),
    ("hex-enables-rgb", "hex-notation", "additive-rgb", "enables", "Hex colour notation enables additive RGB mixing channels to be stated exactly.", "a web colour is written", ""),
    ("hsl-predicts-hex", "hsl-triple", "hex-notation", "predicts", "An HSL notation triple predicts an exact hex colour notation equivalent.", "a converter applies the formulas", ""),
    ("saturation-inhibits-grey", "saturation", "neutral-gray", "inhibits", "Raising saturation inhibits neutral grey baseline flatness by pulling toward pure hue.", "the hue stays fixed", ""),
    ("lightness-enables-contrast", "lightness", "contrast-ratio", "enables", "A gap in lightness levels enables the contrast ratio to grow between text and page.", "hue and saturation stay near", ""),
    ("screen-causes-gamut", "screen-emissive", "gamut-limit", "causes", "Any screen emissive pixels array causes a display gamut limit of showable colours.", "the device has fixed primaries", ""),
    ("print-inhibits-gamut", "print-reflection", "gamut-limit", "inhibits", "The range of print reflective inks inhibits display gamut limit crossing toward bright screen colours.", "vivid greens and blues are wanted", ""),
    ("stare-prereq-afterimage", "saturation", "afterimage", "prerequisite", "Strong saturation staring is a prerequisite for the afterimage effect to appear.", "the hue is held on one spot", ""),
    ("simultaneous-predicts-misjudgement", "simultaneous-contrast", "lightness", "predicts", "Simultaneous contrast illusion predicts lightness misjudgement near edges.", "a border meets a lighter field", ""),
    ("complement-enables-harmony", "complementary-pair", "colour-harmony", "enables", "A complementary colour pair enables colour harmony schemes with strong tension.", "opposites are placed side by side", ""),
    ("alpha-enables-additive", "alpha-blending", "additive-rgb", "enables", "Alpha transparency blending enables additive RGB mixing of layer and backdrop.", "layers composite on screen", ""),
    ("grey-enables-wcag-checks", "neutral-gray", "wcag-contrast", "enables", "A neutral grey baseline text enables WCAG contrast minimums checks against any hue.", "the page colour varies", ""),
    ("hue-predicts-dominant-channel", "hue-angle", "hex-notation", "predicts", "A hue angle predicts the dominant channel in hex colour notation.", "the colour is fully saturated", ""),
    ("dark-room-causes-glare", "screen-emissive", "simultaneous-contrast", "causes", "Screen emissive pixels brightness in a dark room causes simultaneous contrast illusion glare.", "surrounds are near black", ""),
    ("pigment-inhibits-lightness", "subtractive-cmy", "lightness", "inhibits", "Subtractive pigment mixing inhibits lightness recovery as layers stack.", "each ink adds absorption", ""),
    ("deficiency-inhibits-harmony", "colour-blindness", "colour-harmony", "inhibits", "Uncompensated colour vision deficiency inhibits colour harmony schemes from landing as intended.", "schemes rely on red-green separation", ""),
    ("luminance-predicts-lightness-roughly", "relative-luminance", "lightness", "predicts", "Relative luminance predicts perceived lightness only roughly.", "hues differ strongly", ""),
]

MYTHS = [
    ("rby-primaries", "Red, blue and yellow are the true primaries",
     "Primaries depend on the medium: screens use red green blue, print uses cyan magenta yellow.", "primary-colors-system"),
    ("paint-mixes-like-light", "Paint mixes like light",
     "Mixing lights versus pigments differ: one adds brightness, one subtracts it.", "mixing-lights-versus-pigments"),
    ("colour-constant", "A colour looks the same everywhere",
     "Simultaneous contrast illusion shifts the same patch with its surround.", "simultaneous-contrast"),
    ("bright-means-readable", "Bright colour pairs are readable",
     "Only the contrast ratio from relative luminance predicts readability, not vividness.", "contrast-ratio"),
    ("contrast-fixes-deficiency", "Good contrast fixes colour blindness",
     "Contrast helps, but red-green confusion risk stays for hue-only differences.", "red-green-confusion"),
]

BOUNDARIES = [
    ("hsl-not-perceptual", "HSL is not perceptually even",
     "Equal lightness steps in HSL notation differ in perceived brightness.", "hsl-triple"),
    ("gamut-shift", "Colours shift across devices",
     "Past a display gamut limit, out-of-range colours are clipped or mapped.", "gamut-limit"),
    ("deficiency-spectrum", "Colour deficiency varies",
     "Red-green confusion risk differs by type and degree per viewer.", "colour-blindness"),
]

EXAMPLES = [
    ("yellow-on-white", "Yellow text on white",
     "High hue difference but a low relative luminance gap fails contrast ratio checks.",
     ["relative-luminance", "contrast-ratio", "wcag-contrast"]),
    ("blue-orange-poster", "A blue and orange poster",
     "A complementary colour pair drives the strong pull of movie posters.",
     ["complementary-pair", "color-wheel", "colour-harmony"]),
    ("dark-mode-glare", "Dark mode glare",
     "Screen emissive pixels in a dark surround trigger simultaneous contrast illusion brightness.",
     ["screen-emissive", "simultaneous-contrast", "lightness"]),
    ("colourblind-safe-charts", "Charts safe for colour-blind viewers",
     "Encodings separated by lightness beat hue-only red-green pairs.",
     ["colour-blindness", "red-green-confusion", "lightness"]),
]

CONTROLS = [
    ("yellow-readable", "Yellow on white is readable",
     "Yellow text on a white page must not be treated as readable."),
    ("gamma-linear", "Displays show linear values",
     "The sRGB gamma curve must not be treated as linear light."),
    ("print-neon", "Print reproduces neon",
     "Print reflective inks must not be treated as matching screen gamut."),
    ("alpha-free-contrast", "Transparency never changes contrast",
     "Alpha transparency blending must not be treated as leaving contrast fixed."),
]
