"""Visual design: contrast, colour, readability, hierarchy and layout rhythm."""

DOMAIN = "typography-color-visual-design"
SUBJECT = "typography-color-visual-design.visual-hierarchy"
SOURCES = ["w3c-wcag-22", "w3c-css-color-4", "nngroup-heuristics"]

CONCEPTS = [
    ("low-text-contrast", "Low text contrast", "Text whose contrast ratio with its background is below 4.5:1 for body text or 3:1 for large text.", []),
    ("reading-difficulty", "Reading difficulty", "Text is slow, tiring or impossible to read, especially in sunlight or with low vision.", []),
    ("sufficient-contrast", "Sufficient text contrast", "Text meeting at least a 4.5:1 contrast ratio, or 3:1 for large text.", []),
    ("color-only-meaning", "Meaning conveyed by colour alone", "Status, errors or categories distinguished only by hue, such as red versus green.", []),
    ("color-vision-deficiency", "Colour vision deficiency", "About 8 percent of men and 0.5 percent of women of Northern European descent have reduced ability to tell some hues apart.", ["colour blindness"]),
    ("information-lost-to-colorblind", "Information lost to colour-blind users", "Users with colour vision deficiency cannot tell the states or categories apart.", []),
    ("redundant-encoding", "Redundant encoding with shape or text", "Pairing colour with icons, patterns, labels or position.", []),
    ("long-line-length", "Very long text lines", "Lines of body text much longer than about 80 characters.", []),
    ("line-tracking-errors", "Losing one's place between lines", "Readers jump to the wrong line when returning from the end of a long line.", []),
    ("tight-line-height", "Tight line spacing", "Body text line height well below about 1.5 times the font size.", []),
    ("small-body-text", "Small body text", "Body text set much below about 16 CSS pixels on screens.", []),
    ("comfortable-measure", "Comfortable line length and spacing", "Body lines of roughly 50 to 75 characters with line height around 1.5.", []),
    ("all-caps-body", "Long passages in all capitals", "Paragraphs set entirely in capital letters.", []),
    ("clear-visual-hierarchy", "Clear visual hierarchy", "Size, weight, colour and spacing differences that show what matters most and what belongs together.", []),
    ("flat-hierarchy", "Flat visual hierarchy", "All elements share similar size and weight, so nothing stands out.", []),
    ("scanning-efficiency", "Efficient scanning", "Users quickly find headings, key facts and actions.", []),
    ("proximity-grouping", "Grouping by proximity", "Related items placed closer together than unrelated ones.", []),
    ("inconsistent-spacing", "Inconsistent spacing", "Gaps between elements vary without meaning.", []),
    ("misperceived-grouping", "Misperceived grouping", "Users read unrelated items as belonging together, or related items as separate.", []),
    ("spacing-scale", "Consistent spacing scale", "Spacing drawn from a small fixed scale, such as multiples of 4 or 8 pixels.", []),
    ("primary-action-emphasis", "Single emphasised primary action", "One visually dominant button for the main action on a screen.", []),
    ("competing-primary-buttons", "Several equally emphasised buttons", "Multiple filled, high-contrast buttons of equal weight side by side.", []),
    ("action-hesitation", "Hesitation over which action to take", "Users pause or choose the wrong action because no action stands out.", []),
    ("dark-mode-pure-white", "Pure white text on pure black", "Dark themes using #FFFFFF text on #000000 backgrounds.", []),
    ("halation-glare", "Halation glare", "Bright text appears to bleed or vibrate against a black background for some readers, notably those with astigmatism.", []),
    ("softened-dark-palette", "Softened dark palette", "Off-white text on dark grey backgrounds that still meet contrast requirements.", []),
]

RELATIONS = [
    ("contrast-reading", "low-text-contrast", "reading-difficulty", "causes", "Low text contrast causes reading difficulty.", "the reader has low vision or reads in bright light", ""),
    ("sufficient-prevents", "sufficient-contrast", "low-text-contrast", "prevents", "Sufficient text contrast prevents low text contrast problems.", "the ratio holds for every text and background pair, including hover states", ""),
    ("coloronly-lost", "color-only-meaning", "information-lost-to-colorblind", "causes", "Meaning conveyed by colour alone causes information lost to colour-blind users.", "the distinguishing hues fall in a confusable range such as red and green", ""),
    ("cvd-lost", "color-vision-deficiency", "information-lost-to-colorblind", "enables", "Colour vision deficiency enables information lost to colour-blind users.", "the interface relies on hue differences", ""),
    ("redundant-prevents", "redundant-encoding", "information-lost-to-colorblind", "prevents", "Redundant encoding with shape or text prevents information lost to colour-blind users.", "the non-colour cue alone is enough to tell states apart", ""),
    ("longline-tracking", "long-line-length", "line-tracking-errors", "causes", "Very long text lines cause losing one's place between lines.", "the text is continuous body copy", ""),
    ("tracking-reading", "line-tracking-errors", "reading-difficulty", "causes", "Losing one's place between lines causes reading difficulty.", "the reader reads line by line", ""),
    ("tight-reading", "tight-line-height", "reading-difficulty", "causes", "Tight line spacing causes reading difficulty in body text.", "paragraphs run several lines", ""),
    ("small-reading", "small-body-text", "reading-difficulty", "causes", "Small body text causes reading difficulty.", "it is read on a phone or by older readers", ""),
    ("measure-prevents", "comfortable-measure", "reading-difficulty", "inhibits", "Comfortable line length and spacing inhibit reading difficulty.", "the text is body copy rather than labels", ""),
    ("caps-reading", "all-caps-body", "reading-difficulty", "causes", "Long passages in all capitals cause reading difficulty by removing word-shape cues.", "the passage is longer than a short label", ""),
    ("hierarchy-scanning", "clear-visual-hierarchy", "scanning-efficiency", "causes", "Clear visual hierarchy causes efficient scanning.", "the emphasis matches the content's real importance", ""),
    ("flat-scanning", "flat-hierarchy", "scanning-efficiency", "inhibits", "Flat visual hierarchy inhibits efficient scanning.", "the page holds more than a few elements", ""),
    ("flat-missed", "flat-hierarchy", "key-content-missed", "causes", "Flat visual hierarchy causes key content overlooked.", "the key content is not otherwise marked", ""),
    ("spacing-misperceived", "inconsistent-spacing", "misperceived-grouping", "causes", "Inconsistent spacing causes misperceived grouping.", "the gaps between unrelated items are as small as between related ones", ""),
    ("proximity-prevents", "proximity-grouping", "misperceived-grouping", "prevents", "Grouping by proximity prevents misperceived grouping.", "the within-group gap is clearly smaller than the between-group gap", ""),
    ("scale-prevents", "spacing-scale", "inconsistent-spacing", "prevents", "A consistent spacing scale prevents inconsistent spacing.", "components use the scale values", ""),
    ("competing-hesitation", "competing-primary-buttons", "action-hesitation", "causes", "Several equally emphasised buttons cause hesitation over which action to take.", "the actions have different consequences", ""),
    ("primary-prevents", "primary-action-emphasis", "action-hesitation", "inhibits", "A single emphasised primary action inhibits hesitation over which action to take.", "the emphasised action is the one most users need", ""),
    ("purewhite-halation", "dark-mode-pure-white", "halation-glare", "causes", "Pure white text on pure black causes halation glare for some readers.", "the text is thin or small", ""),
    ("softened-prevents", "softened-dark-palette", "halation-glare", "inhibits", "A softened dark palette inhibits halation glare.", "contrast stays above the required ratio", ""),
    ("halation-reading", "halation-glare", "reading-difficulty", "causes", "Halation glare causes reading difficulty.", "the reader has astigmatism", ""),
]
