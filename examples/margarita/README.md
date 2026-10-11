# MARGARITA | Architectural Scene Demonstration

**Author: Tasy Volkova.**

Four sculptural lounge chairs, each combining original spline rods and oversized rectangular-section spline copies, arranged around a 95 cm table. The concept explores an architectural scene with sculptural seating visually inspired by recycled corrugated cardboard and pizza boxes.

The 3D modeling was performed in Autodesk 3ds Max 2024 by ChatGPT through TASY MaxBridge. This is technically significant to the experiment: the scene geometry was created and revised through the LLM-to-3ds-Max connection rather than modeled manually by the architect.

- `MARGARITA_v4_12KB.py`: **11,530 bytes**, reconstructs the complete editable scene from Python text. No `.max` file or MaxBridge is needed to run this standalone example.
- `MARGARITA_v4_FULL_SOURCE.py`: commented source of the same example.
- `../../assets/margarita_viewport.png`: real Autodesk 3ds Max viewport showing the scene.
- `../../assets/margarita_archviz.png`: architectural visualization based on that scene's viewport, generated using an image model. **Not a native 3ds Max render.**

## Run

1. Save your work and open a new empty scene in **3ds Max 2024**.
2. Choose **Scripting > Run Script** and select `MARGARITA_v4_12KB.py`.
3. Inspect the editable objects, and save your own `.max` if desired.

The full source was independently run in 3ds Max and visually verified. The compact script was syntax-checked but not separately tested in Max. Its geometry differs from the earlier exploratory version because the rectangular-section angle is fixed.
