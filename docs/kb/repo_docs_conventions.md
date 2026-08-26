# KB: pico repo docs conventions

Audience: future LLM sessions working in this repo (or the sibling `lab/`
repo). Process/structural notes — not useful to the end user, who already
knows this stuff first-hand.

## `docs/history.md` is append-only, not corrected retroactively

Same convention as the sibling `lab/` repo's `docs/kb/repo_docs_conventions.md`
documents for `lab/docs/history.md`: past session entries describe the repo
as it was at the time (including now-removed things like the Wokwi
`diagram.json` workflow, the electrogravitics/Biefeld-Brown framing, and
flat top-level circuit folders) and are not edited when current-state docs
change. When cleaning up references to something removed from the current
repo (2026-08-24: Wokwi, `docs/related/Valone2008/`, `biefeld_brown_lifter`),
only touch `README.md` and per-circuit docs — leave `docs/history.md` as-is.

## Inventory "Slide Switch" row corrected (2026-08-25) — it's a standard SPDT part, not an unmarked mystery switch

`docs/inventory.md`'s Slide Switch row previously described the 3-pin
switch as "1P2T" with one floating outer pin and one active pin — a
hypothesis from an ad hoc probe that lacked a solid GND reference (see
the sibling `lab/` repo's `docs/kb/repo_docs_conventions.md` entry on
`switch_pin_identifier`'s GND-reference bug, and the follow-up entry
documenting that whole circuit's deletion). The manufacturer's own page
(SunFounder Thales kit, `components/slide_switch.html`) describes this
part as a standard 3-pin slide switch: pin 2 (middle) is the fixed
contact, and it connects to pin 1 or pin 3 depending on slide direction —
ordinary SPDT behavior, not an oddball part needing per-unit
reverse-engineering. The row is now written from that reference instead
of the old ad hoc probe result. If a similar "no printed markings, so we
probed it and got a weird result" situation comes up for another
inventory part, check whether the manufacturer/kit vendor already
documents the part before building a whole Pico probe circuit to
characterize it from scratch.

## Category-subdirectory taxonomy (introduced 2026-08-24)

Circuits moved from flat top-level folders into category subdirectories,
mirroring the sibling `lab/` repo's `power_supplies/` / `measurement_tools/`
grouping convention:

| Category | Contains |
|---|---|
| `leds/` | Any circuit whose primary output is an LED (including PWM-driven) |
| `buttons/` | Any circuit whose primary input is a pushbutton/switch, polled or interrupt-driven |
| `measurement_tools/` | ADC/sensor readout, calibration, IMU, HV-divider — anything whose job is *measuring* something |
| `displays/` | Anything whose job is showing output to a human (LCD, etc.) |
| `micropico/`, `lib/`, `tools/`, `docs/` | Unchanged top-level utility dirs — not circuits, don't get a category |

When adding a new circuit folder, pick the category by the circuit's
primary purpose using the table above; if it doesn't fit cleanly (e.g. a
circuit that both senses and displays), prefer `measurement_tools/` since
that's this repo's more distinctive niche relative to `leds/`/`buttons/`/
`displays/`, which are closer to generic Pico-tutorial material. Moving a
folder touches more than the folder itself: every relative link inside the
moved folder's own README/breadboard needs an extra `../`, and every
repo-root-relative `ngspice -b <old-path>` / `mpremote cp <old-path>`
command in that folder's own README and in the top-level `README.md`
needs the new prefix. Grep the old bare folder name across the whole repo
before considering a move done.
