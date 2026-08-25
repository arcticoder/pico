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
