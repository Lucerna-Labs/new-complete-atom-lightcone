#!/usr/bin/env python3
"""Author a geometry-grounded typography and color foundation world."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "typography-color" / "foundations.jsonl"
WORLD = "typography-color-v0"
DOMAIN = "typography-color-visual-design"
LANES = ["geometry.structural", "psychology.evidence", "creativity.constraint_based", "thinking.lateral"]
SOURCES = ["w3c-css-color-4", "w3c-wcag-22", "opentype-191", "unicode-uax14", "nist-measurement-uncertainty"]


CONCEPTS = [
    ("root", "Typography and color systems", "Typography and color combine physical signals, human perception, geometric form, encoded text, layout, rendering, accessibility, and rhetorical use under explicit media and user conditions.", "typography-color-visual-design.visual-hierarchy"),
    ("spectral-power", "Spectral power distribution", "A spectral power distribution describes energy across wavelengths and is not itself a perceived color.", "typography-color-visual-design.color-science"),
    ("reflectance", "Surface reflectance", "Surface reflectance interacts with illumination to shape light reaching an observer.", "typography-color-visual-design.color-science"),
    ("color-perception", "Color perception", "Color perception arises from visual-system responses and context rather than existing as a single intrinsic scalar property of an object.", "typography-color-visual-design.color-science"),
    ("colorimetry", "Colorimetry", "Colorimetry measures and models human color perception under defined observers and viewing conditions.", "typography-color-visual-design.color-science"),
    ("color-space", "Color space", "A color space defines coordinates, reference conditions, and transformations for representing color.", "typography-color-visual-design.color-science"),
    ("white-point", "White point", "A white point specifies the reference chromaticity treated as neutral under a color-space or viewing condition.", "typography-color-visual-design.color-science"),
    ("chromatic-adaptation", "Chromatic adaptation", "Chromatic adaptation models changes in visual response as illumination and reference white change.", "typography-color-visual-design.color-science"),
    ("srgb", "sRGB", "sRGB is a specified RGB color space with defined primaries, white point, and transfer functions; raw RGB triples have no complete meaning without such a space.", "typography-color-visual-design.color-science"),
    ("lab", "CIELAB", "CIELAB represents color relative to a reference white and aims for greater perceptual uniformity than device RGB, without being perfectly uniform.", "typography-color-visual-design.color-science"),
    ("oklab", "Oklab", "Oklab is a perceptual color space used for color manipulation and interpolation under its specified conversion model.", "typography-color-visual-design.color-science"),
    ("gamut", "Color gamut", "A gamut is the set of colors representable or reproducible by a device, medium, or color space under stated conditions.", "typography-color-visual-design.color-science"),
    ("gamut-map", "Gamut mapping", "Gamut mapping transforms out-of-gamut colors into a target gamut while trading among hue, chroma, lightness, and relationships.", "typography-color-visual-design.color-science"),
    ("relative-luminance", "Relative luminance", "Relative luminance is a defined linear-light measure used by accessibility contrast calculations and is distinct from hue or encoded channel value.", "typography-color-visual-design.color-accessibility"),
    ("contrast-ratio", "Contrast ratio", "WCAG contrast ratio compares the relative luminance of lighter and darker colors under a defined formula.", "typography-color-visual-design.color-accessibility"),
    ("use-of-color", "Use of color", "Color must not be the sole visual means of conveying essential information when accessible alternatives are required.", "typography-color-visual-design.color-accessibility"),
    ("color-deficiency", "Color-vision variation", "Color-vision variation changes discriminability for some color combinations and requires redundant cues and contrast-aware design.", "typography-color-visual-design.color-accessibility"),
    ("hue", "Hue", "Hue describes a color-family dimension and does not determine luminance, chroma, accessibility, or emotional meaning by itself.", "typography-color-visual-design.color-theory"),
    ("chroma", "Chroma", "Chroma describes colorfulness relative to a reference and differs from device-specific saturation controls.", "typography-color-visual-design.color-theory"),
    ("lightness", "Perceptual lightness", "Perceptual lightness describes perceived brightness relative to a reference and differs from physical luminance.", "typography-color-visual-design.color-theory"),
    ("palette", "Color palette", "A palette is a constrained set of colors assigned functional, semantic, or expressive roles.", "typography-color-visual-design.color-theory"),
    ("harmony", "Color harmony", "Color harmony is an aesthetic and contextual relation among colors, not a universal physical law or guarantee of accessibility.", "typography-color-visual-design.color-theory"),
    ("interpolation", "Color interpolation", "Color interpolation follows a path in a declared color space, so different spaces can produce visibly different intermediate colors.", "typography-color-visual-design.color-science"),
    ("alpha", "Alpha compositing", "Alpha compositing combines foreground and background contributions; the resulting contrast depends on the composite, not the foreground channels alone.", "typography-color-visual-design.color-science"),
    ("character", "Character", "A character is an abstract textual unit and is not identical to a glyph, key press, byte, or visible mark.", "typography-color-visual-design.font-technology"),
    ("code-point", "Unicode code point", "A Unicode code point is an integer assigned in the Unicode codespace; user-perceived characters may contain multiple code points.", "typography-color-visual-design.font-technology"),
    ("grapheme", "Grapheme cluster", "A grapheme cluster approximates a user-perceived character boundary and may contain multiple code points.", "typography-color-visual-design.font-technology"),
    ("glyph", "Glyph", "A glyph is a particular visual form used to render one or more characters in context.", "typography-color-visual-design.type-anatomy"),
    ("typeface", "Typeface", "A typeface is a related visual design system for glyphs across styles or instances.", "typography-color-visual-design.type-anatomy"),
    ("font", "Font resource", "A font is an implementation resource containing glyph data, metrics, mappings, and layout information for a typeface instance or variation space.", "typography-color-visual-design.font-technology"),
    ("outline", "Glyph outline", "A glyph outline represents contours using geometric segments such as lines and Bézier curves.", "typography-color-visual-design.font-technology"),
    ("shaping", "Text shaping", "Text shaping maps encoded characters to context-appropriate glyphs and positions under script, language, direction, and font features.", "typography-color-visual-design.font-technology"),
    ("substitution", "Glyph substitution", "Glyph substitution selects alternate glyph sequences for required or optional typographic behavior.", "typography-color-visual-design.font-technology"),
    ("positioning", "Glyph positioning", "Glyph positioning adjusts placement for marks, cursive attachment, kerning, and other layout relationships.", "typography-color-visual-design.font-technology"),
    ("kerning", "Kerning", "Kerning adjusts spacing for particular glyph relationships and is not equivalent to tracking across an entire run.", "typography-color-visual-design.typesetting"),
    ("ligature", "Ligature", "A ligature represents a sequence with a combined glyph and may be required by a script or optional for style.", "typography-color-visual-design.typesetting"),
    ("baseline", "Baseline", "A baseline is a geometric reference used to align glyphs and runs; different scripts can require different baseline behavior.", "typography-color-visual-design.typesetting"),
    ("metrics", "Font metrics", "Font metrics provide geometric values used in glyph and line layout and may differ from visible outline bounds.", "typography-color-visual-design.font-technology"),
    ("x-height", "X-height", "X-height describes the height of lowercase forms relative to the baseline in a Latin type design and affects apparent size and texture.", "typography-color-visual-design.type-anatomy"),
    ("weight", "Type weight", "Type weight describes stroke darkness or mass within a family and interacts with size, rendering, contrast, and spacing.", "typography-color-visual-design.type-anatomy"),
    ("width", "Type width", "Type width describes horizontal proportion within a family and affects fit, texture, and hierarchy.", "typography-color-visual-design.type-anatomy"),
    ("optical-size", "Optical size", "Optical-size design adapts glyph construction and spacing for intended display size rather than merely scaling one outline.", "typography-color-visual-design.font-technology"),
    ("variable-font", "Variable font", "A variable font represents a continuous or discrete design space through registered or custom axes and interpolation data.", "typography-color-visual-design.font-technology"),
    ("line-breaking", "Line breaking", "Line breaking selects among mandatory and permitted opportunities using Unicode properties, language context, and layout strategy.", "typography-color-visual-design.typesetting"),
    ("bidirectionality", "Bidirectional text", "Bidirectional layout resolves display order for mixed-direction text without changing the underlying logical character order.", "typography-color-visual-design.typesetting"),
    ("measure", "Line measure", "Line measure is the usable line length and interacts with type size, spacing, language, and reading conditions.", "typography-color-visual-design.readability"),
    ("leading", "Line spacing", "Line spacing controls vertical distance among lines and interacts with metrics, scripts, measure, and reading conditions.", "typography-color-visual-design.readability"),
    ("tracking", "Tracking", "Tracking adjusts spacing across a run and differs from pair-specific kerning.", "typography-color-visual-design.typesetting"),
    ("hierarchy", "Typographic hierarchy", "Typographic hierarchy uses scale, weight, spacing, position, color, and consistency to signal content relationships.", "typography-color-visual-design.visual-hierarchy"),
    ("grid", "Typographic grid", "A grid provides geometric alignment and spacing constraints while allowing purposeful exceptions.", "typography-color-visual-design.grid-layout"),
    ("legibility", "Legibility", "Legibility concerns distinguishing characters and words under a particular typeface, rendering, size, and viewing condition.", "typography-color-visual-design.readability"),
    ("readability", "Readability", "Readability concerns how easily extended text can be read given language, composition, typography, content, and reader conditions.", "typography-color-visual-design.readability"),
    ("rasterization", "Rasterization", "Rasterization converts geometric glyph descriptions into pixels under a scale, grid, and rendering method.", "typography-color-visual-design.font-technology"),
    ("hinting", "Font hinting", "Hinting supplies instructions or constraints that adjust outline rasterization at particular pixel grids and sizes.", "typography-color-visual-design.font-technology")
]


RELATIONS = [
    ("spectrum-reflectance", "spectral-power", "reflectance", "qualifies", "Illumination spectrum qualifies the light produced by surface reflectance."),
    ("reflectance-perception", "reflectance", "color-perception", "enables", "Reflected light can enable color perception under an observer and context."),
    ("perception-colorimetry", "color-perception", "colorimetry", "grounds", "Colorimetry is grounded in standardized models of human color perception."),
    ("space-white", "white-point", "color-space", "qualifies", "A reference white qualifies interpretation and conversion for many color spaces."),
    ("adapt-white", "chromatic-adaptation", "white-point", "transforms_to", "Chromatic adaptation transforms color appearance estimates between reference whites."),
    ("srgb-space", "srgb", "color-space", "part_of", "sRGB is one specified RGB color space."),
    ("lab-space", "lab", "color-space", "part_of", "CIELAB is one reference-relative color space."),
    ("oklab-space", "oklab", "color-space", "part_of", "Oklab is one perceptual color space."),
    ("space-gamut", "color-space", "gamut", "qualifies", "A bounded color space or device determines an available gamut."),
    ("gamut-map", "gamut", "gamut-map", "enables", "A target gamut enables out-of-gamut mapping decisions."),
    ("luminance-contrast", "relative-luminance", "contrast-ratio", "grounds", "Relative luminance grounds the WCAG contrast-ratio calculation."),
    ("deficiency-color-use", "color-deficiency", "use-of-color", "supports", "Color-vision variation supports the need for redundant non-color cues."),
    ("hue-harmony", "hue", "harmony", "supports", "Hue relations can support a palette's aesthetic harmony but do not determine it alone."),
    ("lightness-contrast", "lightness", "contrast-ratio", "qualifies", "Perceptual lightness can guide design, while normative contrast uses its specified luminance calculation."),
    ("palette-hierarchy", "palette", "hierarchy", "supports", "Consistent color roles can support visual hierarchy."),
    ("interpolation-space", "color-space", "interpolation", "qualifies", "The chosen color space qualifies the path and result of interpolation."),
    ("alpha-contrast", "alpha", "contrast-ratio", "qualifies", "Alpha compositing qualifies the actual foreground-background colors used for contrast."),
    ("codepoint-character", "code-point", "character", "implements", "Unicode code points encode abstract characters and controls."),
    ("grapheme-codepoint", "grapheme", "code-point", "qualifies", "A grapheme cluster can contain more than one code point."),
    ("glyph-character", "glyph", "character", "implements", "Glyphs visually implement characters in a font and shaping context."),
    ("font-typeface", "font", "typeface", "implements", "A font resource implements a typeface instance or variation space."),
    ("outline-glyph", "outline", "glyph", "implements", "An outline is one geometric representation of a glyph."),
    ("character-shaping", "character", "shaping", "prerequisite", "Encoded characters and context are inputs to shaping."),
    ("font-shaping", "font", "shaping", "prerequisite", "Font mappings and layout data are inputs to shaping."),
    ("shaping-substitution", "shaping", "substitution", "enables", "Shaping enables context-sensitive glyph substitution."),
    ("shaping-position", "shaping", "positioning", "enables", "Shaping enables glyph positioning."),
    ("kerning-position", "kerning", "positioning", "part_of", "Kerning is one pair-specific positioning operation."),
    ("ligature-substitution", "ligature", "substitution", "part_of", "Ligature selection is one glyph-substitution behavior."),
    ("baseline-position", "baseline", "positioning", "qualifies", "Baselines qualify vertical alignment during positioning."),
    ("metrics-line", "metrics", "leading", "qualifies", "Font metrics qualify line-box and spacing calculations."),
    ("xheight-legibility", "x-height", "legibility", "qualifies", "X-height can affect apparent size and legibility under specific conditions."),
    ("weight-legibility", "weight", "legibility", "qualifies", "Weight affects stroke visibility and character differentiation under size and contrast constraints."),
    ("width-measure", "width", "measure", "qualifies", "Type width affects how much text fits within a line measure."),
    ("optical-legibility", "optical-size", "legibility", "supports", "Optical-size adaptations can support legibility at intended sizes."),
    ("variable-font", "variable-font", "font", "part_of", "A variable font is one OpenType font resource with a design space."),
    ("linebreak-measure", "measure", "line-breaking", "qualifies", "Available line measure qualifies which permitted break is selected."),
    ("bidi-linebreak", "line-breaking", "bidirectionality", "prerequisite", "Line boundaries are resolved before final line-level bidirectional reordering."),
    ("tracking-measure", "tracking", "measure", "qualifies", "Tracking changes text fit and texture within a line measure."),
    ("hierarchy-grid", "grid", "hierarchy", "supports", "A grid supports consistent hierarchy and alignment."),
    ("legibility-readability", "legibility", "readability", "supports", "Character and word legibility supports but does not guarantee extended-text readability."),
    ("outline-raster", "outline", "rasterization", "prerequisite", "Outline geometry is an input to rasterization."),
    ("hint-raster", "hinting", "rasterization", "qualifies", "Hinting qualifies outline rasterization at particular grids and sizes."),
    ("geometry-type", "grid", "baseline", "supports", "Grid and baseline geometry support consistent typographic alignment."),
    ("color-type", "contrast-ratio", "legibility", "supports", "Adequate foreground-background contrast supports legibility."),
    ("rhetoric-hierarchy", "hierarchy", "readability", "qualifies", "Hierarchy guides reading order, while excessive or inconsistent hierarchy can reduce readability.")
]


CONTROLS = [
    ("rgb-without-space", "RGB without a color space", "An RGB triple without primaries, white point, and transfer function must not be treated as a fully specified color."),
    ("color-alone", "Color-only information", "Essential state or meaning conveyed only by color must not pass the accessibility boundary."),
    ("harmony-accessible", "Harmony is not accessibility", "An aesthetically harmonious palette must not be assumed to meet contrast or color-vision requirements."),
    ("hue-emotion", "Universal hue-emotion claim", "A hue must not be assigned one universal emotional meaning across cultures, contexts, and individuals."),
    ("encoded-luminance", "Encoded channel is not luminance", "A gamma-encoded channel value must not be used directly as linear relative luminance."),
    ("alpha-ignore", "Ignored compositing", "Contrast must not be computed from a translucent foreground without composing it over the actual background."),
    ("character-glyph", "Character-glyph conflation", "A character must not be assumed to map one-to-one to a visible glyph."),
    ("codepoint-grapheme", "Code-point grapheme conflation", "String length in code points must not be assumed to equal user-perceived character count."),
    ("font-typeface", "Font-typeface conflation", "A font file or instance must not be treated as the entire typeface design family."),
    ("kerning-tracking", "Kerning-tracking conflation", "Pair kerning must not be reported as global tracking."),
    ("bidi-storage", "Display order is not storage order", "Bidirectional display reordering must not rewrite logical character order as though it were source text."),
    ("font-metrics-bounds", "Metrics are not visible bounds", "Font ascent, descent, or advance metrics must not be assumed to equal every glyph's visible outline bounds."),
    ("large-contrast-rounding", "Contrast threshold rounding", "A computed contrast value below a normative threshold must not be rounded up and reported as passing."),
    ("projection-type", "Rendered pixels are not source geometry", "A rasterized glyph image must not be treated as the original outline or font program."),
    ("readability-universal", "Universal readability claim", "One typographic setting must not be called universally most readable without population, language, task, and medium evidence.")
]


def base(identifier: str, subject: str, split: str, kind: str, epistemic: str, sources: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": f"type-color.v0.{identifier}",
        "world_id": WORLD,
        "domain_id": DOMAIN,
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "representations_transformations", "applications_toolchains"],
        "source_ids": sources,
        "scope": "typography, text layout, color science, color theory, and accessibility foundation",
        "limitations": ["Aesthetic interpretations remain contextual; draft standards carry their stated maturity."],
        "as_of": "2026-09-03",
        "version_boundary": "OpenType 1.9.1; WCAG 2.2; CSS Color 4 CRD 2026-08-06",
        "split_group": f"type-color.v0.{identifier}",
        "split": split,
        "tags": ["typography", "color", "geometry", "accessibility"]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        records.append({
            **base(identifier, subject, "validation" if index and index % 19 == 0 else "train", "concept", "interpretive" if subject.endswith("color-theory") else "established", SOURCES),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()]
        })
        if identifier != "root":
            records.append({
                **base(f"membership-{identifier}", subject, "train", "relation", "established", SOURCES),
                "label": f"{label} typography-color membership",
                "statement": f"{label} is a distinct component of the typography and color world.",
                "aliases": [],
                "relation": {"source_node": f"type-color.v0.{identifier}", "target_node": "type-color.v0.root", "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": [], "exceptions": []},
                "coverage_axes": ["primitives_invariants", "within_domain_composition"]
            })
    for index, (identifier, source, target, kind, statement) in enumerate(RELATIONS):
        split = "sealed_test" if index % 13 == 0 else "validation" if index % 9 == 0 else "cross_domain_holdout" if index % 17 == 0 else "train"
        records.append({
            **base(f"relation-{identifier}", "typography-color-visual-design.visual-hierarchy", split, "relation", "established", SOURCES),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": f"type-color.v0.{source}",
                "target_node": f"type-color.v0.{target}",
                "kind": kind,
                "polarity": 1,
                "direction": "forward",
                "conditions": ["color space, medium, script, and user conditions are declared where relevant"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "representations_transformations", "cross_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        records.append({
            **base(identifier, "typography-color-visual-design.color-accessibility", "validation" if index % 2 == 0 else "sealed_test", "synthetic_control", "synthetic_control", []),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["negative-control", "typography", "color", "accessibility"]
        })
    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records: {dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
