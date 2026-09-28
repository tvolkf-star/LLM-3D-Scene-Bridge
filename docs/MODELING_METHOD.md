# Modelling method transferred during the experiment

The important lesson was not a catalogue of example objects. It was a reusable modelling logic for repeated architectural and urban-design systems.

## Principle

**Model one element and the law of its existence in space, rather than manually modelling many elements.**

A practical native 3ds Max workflow is:

1. Make one source profile/object. A spline is especially easy to control, but the source can be other geometry.
2. Make a path. It may be a circle or any other spline.
3. Use Animation → Constraints → Path Constraint.
4. Animate position along the path and, when useful, rotation, scale, source shape or section dimensions.
5. Use Tools → Snapshot over a frame range, with the desired number of copies and Mesh output.
6. Inspect the generated family of states.
7. Select the generated pieces and attach/collapse them into one clean Editable Poly when separate pieces are no longer useful.
8. Delete or hide the construction geometry before placing the finished object into the main scene.

## Profile first

For seating and other human-scale MAF, first solve a good source profile. Simple helper boxes can establish human dimensions. Edit the spline while its real renderable thickness is visible. Snapshot multiplies both good decisions and small defects, so a clean source curve matters more than a large number of generated slats.

## Section is design

Slats are not square by default. A rectangular section has a broad face and a thin edge, changing transparency, rhythm and visual weight with viewpoint. For facade systems, a source may also be a **closed spline** converted to poly or extruded only a few millimetres to a few centimetres before repetition.

## Workbench discipline

Generate procedural families in a clear work area, resolve the form there, combine the result into a manageable object, then move the finished object into the architectural scene. The final scene should contain the useful result, not every temporary construction object.

## Transfer test 000035

After this method was demonstrated through dialogue and examples, the LLM was asked to make a different object rather than copy the demonstrated one. It produced a long slatted urban shade/seat ribbon, merged the generated lamellae into one Editable Poly, and left no construction splines in the finished scene. The first version still had local curvature/ergonomic defects at the seat edge, but its overall form survived duplication, rotation and placement as a two-part spatial module.

This is the interesting part of the experiment: **method transfer, not visual copying.**
