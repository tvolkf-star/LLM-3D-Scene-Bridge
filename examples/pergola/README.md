# Pergola / Ribbon Seat | Command 000035

**Original ChatGPT-to-3ds Max command** supplied by the project author. This is a reproducible **procedural modeling example**, not a prebuilt 3D asset.

- [Original bridge command (JSON)](command_000035.json)
- [Extracted Python/pymxs source](MAF035_Pergola.py)
- Target environment: Autodesk 3ds Max 2024, Python/pymxs
- Geometry: 73 varying spline profiles across a 9000-unit length, rectangular renderable spline sections converted to Editable Poly, attached into one object where attachment succeeds, plus a separate base platform.
- Materials: warm timber and grey platform.

## Important safety warning

**The original code calls `rt.resetMaxFile(rt.Name("noPrompt"))`. Running it resets the current 3ds Max scene without prompting to save. Save your work and run in a disposable/empty scene.** The original command is preserved unchanged for reproducibility.

## Modeling method

The varying profiles are calculated explicitly from `math.sin` and smoothstep-style interpolation. This is **not** the Path Constraint → Auto Key → Snapshot method described in [the separate modeling lesson](../../docs/MAXBRIDGE_SNAPSHOT_MODELING_RU.md).

The example demonstrates ChatGPT generating native editable 3D geometry through the bridge. Execution success and visual correctness should be checked separately using the bridge's result, scene state and viewport capture.
