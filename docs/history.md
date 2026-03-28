All 7 tasks complete. Here's a summary:

---

### ✅ Done

| Task | Result |
|------|--------|
| Install schemdraw | Installed into active conda env |
| Schematic script | spice_to_schematic.py — parses V/R/D elements, renders LED symbols |
| `test2.spice` | test2.spice — two parallel LED branches off the same 3.3 V rail |
| `led_test2.gc` | led_test2.gc — sweeps 0→3.3 V, prints `v(2) v(3) i(D1) i(D2)`, no errors |
| Schematic images | test.png · test2.png — both verified visually |
| README | README.md — covers simulation workflow, when to regenerate images, adding new circuits, and GnuCap vs. SPICE syntax gotchas |

To regenerate a schematic after editing a netlist:
```bash
python spice_to_schematic.py <name>.spice
```
<!-- ------ -->
---