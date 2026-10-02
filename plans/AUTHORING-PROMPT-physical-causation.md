# Prompt for the authoring assistant: extend physical-causation-v0

Copy everything below the line into the coding assistant. One batch is one new data
module. Claude reviews every batch for physical accuracy before it is merged.

---

You are adding curated, original cause-and-effect knowledge to a Lightcone world
called `physical-causation-v0` in the repository
`/home/jesse/Desktop/Projects/new-complete-atom-lightcone`.

## Your task for this batch

Create **one new file** `tools/physical_causation/<MODULE>.py` covering **<TOPIC>**,
then register it in the builder. Suggested batches, one per run:

| MODULE | TOPIC | SUBJECT |
|---|---|---|
| `kitchen` | cooking and kitchen physics: heating, boiling, steam, browning heat, pressure, freezing food, microwaves | `physics.thermodynamics` |
| `weather` | everyday weather: fronts, humidity, fog, frost, hail, storms, sea breezes | `physics.fluid-dynamics` |
| `home_electrics` | household electricity: switches, sockets, chargers, heaters, earthing, static | `physics.electromagnetism` |
| `transport` | vehicles: tyres, braking distance, cornering, aerodynamics, buoyancy of boats, bicycles | `physics.classical-mechanics` |
| `sports_body` | sport and body mechanics: jumping, throwing, balance, levers in the body, impact | `physics.classical-mechanics` |
| `water_everyday` | water at home and in nature: pressure in taps, capillary action, surface tension, waves | `physics.fluid-dynamics` |
| `light_everyday` | everyday light: glare, lenses in glasses, shadows, colours of objects, screens | `physics.optics` |
| `sound_everyday` | everyday sound: noise, insulation, musical instruments, sirens, headphones | `physics.acoustics` |

## Exact file format (copy this shape)

```python
"""<One-line description>."""

SUBJECT = "physics.<subfield>"        # one of the physics subfields in the table above
SOURCES = ["<registered source id>", ...]

# (id, label, statement, aliases)
CONCEPTS = [
    ("kebab-case-id", "Two Or More Word Label", "One or two sentences in your own words.", []),
]

# (id, source, target, kind, statement, condition, exception)
RELATIONS = [
    ("short-id", "source-concept-id", "target-concept-id", "causes",
     "Source Label causes target label <how>.", "<specific condition>", "<real exception or empty string>"),
]
```

Then add the module to the builder: in `tools/build_physical_causation_curriculum.py`,
add it to the `from physical_causation import (...)` list and to `SUBFIELDS`. Change
nothing else in the builder.

## Rules (every rule is checked in review; violations are rejected)

1. **Size:** 25–40 concepts and 40–70 relations per batch.
2. **IDs:** lowercase kebab-case, unique across the whole world. Before choosing IDs,
   list existing ones:
   `grep -ho '("[a-z0-9-]*"' tools/physical_causation/*.py | sort -u`.
   You may connect to existing concepts by their exact IDs, which is encouraged
   (e.g. `gravity`, `heat-transfer`, `evaporation`, `electric-current`).
3. **Relation kinds:** use only `causes`, `enables`, `prevents`, `inhibits`,
   `prerequisite`, `transforms_to`, `predicts`, `qualifies` or `part_of`. At least
   80% must be one of the first seven. Use `prevents` or `inhibits` for anything
   that blocks or reduces; never encode a reduction as `causes`.
4. **Direction must be physically correct:** the source is the cause or enabler, the
   target is the effect. A rule of thumb: "if I change the source, the target
   changes", never the reverse.
5. **Statements:** each relation statement must contain the source concept's label
   and the target concept's label (case-insensitive), joined by the kind's verb:
   "causes", "enables", "prevents", "inhibits", "is a prerequisite for",
   "transforms into" or "predicts".
6. **Conditions:** every relation has one *specific* condition saying when it holds,
   such as "the pan is on a lit burner". Never use generic text like "under normal
   conditions". No condition string may repeat within your batch. Add an exception
   only when a real one exists.
7. **Facts:** only well-established everyday physics. No speculative, medical or
   safety-critical advice. Use typical numbers only where they are textbook values.
8. **Your own words:** never copy sentences from websites or books.
9. **Labels:** at least two words wherever possible. Avoid bare common words that
   mean other things ("Lead", "Set", "Go", "Current" — write "Electric current").
   Add aliases only for true synonyms; never add a lowercase copy of the label.
10. **Sources:** use only these registered IDs: `nasa-glenn-beginners-guide`,
    `usgs-water-science-school`, `noaa-jetstream`, `eia-energy-explained`,
    `nasa-ems-tour`, `nist-codata-2022`. Do not add sources yourself; ask if one
    is needed.
11. **Myths:** do not put myths in this file. If you notice one, list it in your
    report for review.

## Checks you must run, all passing, before you finish

```bash
cd /home/jesse/Desktop/Projects/new-complete-atom-lightcone
python3 tools/build_physical_causation_curriculum.py
python3 tools/validate_curricula.py | tail -2
python3 tools/validate_sources.py | tail -1
.venv/bin/python trainer/compile_curriculum.py --world-id physical-causation-v0
```

## Deliverable

Work on a new branch `authoring/<MODULE>`, created from `pilot-physical-causation`.
Commit only your module file and the two builder lines. Then report:
- the branch name and commit;
- counts of concepts, relations and relations by kind;
- a plain list of every relation as `source -> kind -> target | condition`, which is
  what the reviewer checks;
- anything you were unsure about.

Do not merge, push, or edit any other file.
