# Direct Modeling in Autodesk 3ds Max via ChatGPT and an Executable Representation of a 3D Scene

[Русская версия](RESEARCH_RU.md) · [Repository overview](README.md)

**Project author: Tasy Volkova**

## 1. Background

Modern language models can generate and analyze program code, work with visual information, and execute sequences of related operations. Professional 3D modeling systems, in turn, provide programmatic interfaces for direct control of scenes and geometry.

This makes it possible to ask a practical question: **does work in a professional 3D environment require a specialized AI system, or is it sufficient to give a general-purpose language model a direct control channel to an existing professional tool?**

The experiment used **Autodesk 3ds Max 2024** and **ChatGPT GPT-5.6 Sol in Instant mode**. Work was performed through the ordinary ChatGPT user interface, without a separate API workflow, autonomous agent framework, specialized text-to-3D model, or custom geometry editor.

A key condition was to preserve the standard modeling environment. Operations had to produce ordinary native 3ds Max objects that remained editable with the application's standard tools.

The research question was not:

**“Can an LLM write a script for 3ds Max?”**

The question was:

**“Can a general-purpose language model directly control native modeling operations in a professional 3D environment, receive feedback from the scene, and iteratively modify the result?”**

A second question emerged during the work: **can the resulting scene exist not only as a binary scene file, but also as an executable textual representation accessible to both 3ds Max and a language model?**

---

## 2. Experimental system

As part of the research, **Tasy Volkova developed a minimal bidirectional software bridge** between the ChatGPT interface and a locally running Autodesk 3ds Max 2024.

Data transfer was organized through a synchronized Google Drive directory:

**ChatGPT → Google Drive → local synchronization → Python/pymxs → Autodesk 3ds Max**

The return channel was:

**3ds Max → execution result + scene state + viewport image → Google Drive → ChatGPT**

Google Drive acts only as a transport layer. It does not participate in modeling and contains no special geometric logic.

The bridge is deliberately minimal as well. It is approximately 8 KB of Python/pymxs code. It contains no library of predefined high-level commands such as “create a house”, “create a chair”, or “build a facade”. The bridge receives operations produced by the LLM, executes them through the native 3ds Max Python/pymxs interface, and returns observable results.

The modeling logic is therefore not hidden inside the bridge. **The LLM forms operations; 3ds Max creates and stores the geometry; the bridge provides the bidirectional channel between them.**

![Experimental loop](media/architecture.png)

The working loop was:

**task → modeling operations → execution in 3ds Max → scene state and viewport → professional evaluation → next local task.**

The last step matters. The experiment did not show that the LLM autonomously and reliably maintains the entire project and its context. Project context, evaluation criteria, and the direction of the next iteration remain with the human. The model solves the next modeling problem within that loop.

---

## 3. From the first object to native modeling

Initial tests used simple geometry to verify the bidirectional loop. Task complexity was then increased progressively.

One early architectural test was a shopping-center scene generated from a textual description and consisting of **69 separate native 3ds Max objects**. The geometry was created directly inside the professional environment and remained available for standard editing.

The first controlled object-modeling test used an IKEA FROSTA stool as a constructive reference. The stool was not intended as a design showcase. Its purpose was to test the complete loop: construct an object, inspect the actual result in Max, receive professional correction of the method, and rebuild the geometry.

![GPT Stool No. 1 in Autodesk 3ds Max](media/GPT_Stool_clean_max.png)

*Native editable geometry in Autodesk 3ds Max.*

During modeling, an independent variant of the bent support geometry emerged. Tasy Volkova evaluated the result and deliberately retained it as a separate design variant named **GPT Stool No. 1**.

The significant result was not only the object but the change in working method. After professional correction, the LLM moved from direct polygon construction to a method more appropriate to the task:

**SplineShape → rectangular section → Editable Poly → relative instance transformations.**

In other words, the finished model was not manually repaired. What was corrected was **the modeling method used by the LLM to solve the task**.

[Python/pymxs source](examples/01_stool/GPT_FROSTA_Instant_000027.py)

---

## 4. Transfer of a professional modeling method

The next stage tested a more demanding hypothesis: can a language model adopt not the coordinates of a particular object, but the principle of a professional modeling method and apply it to a new geometric task?

Tasy Volkova demonstrated a professional working principle used for repeated spatial systems: a source profile or object moves along a path while its parameters change, and a sequence of states is materialized as geometry. In 3ds Max, such a workflow can be implemented, among other ways, with Path Constraint, Animation, and Snapshot.

Her examples explained the **principle** rather than supplying geometry to copy.

The LLM then received a new task: an elongated small architectural form with an integrated seat and canopy. The model did not literally reproduce the demonstrated Path Constraint + Animation + Snapshot sequence. Instead, it transferred the principle of a changing profile and sampled states into a procedural construction of the new form.

![Single MAF module](media/MAF_000035_single.png)

*First spatial form.*

![Paired MAF modules](media/MAF_000035_pair.png)

*Testing the form as a paired composition.*

![Grounded MAF composition](media/MAF_000035_grounded.png)

*Further test of spatial organization.*

The first iterations revealed errors in form and ergonomics. Professional feedback addressed the profile, transitions, lamella section, and construction method. After the method was corrected, subsequent iterations produced a substantially different result.

This stage supports a narrower and more testable conclusion than “teaching a model to model in general”: **Tasy Volkova transferred a professional construction principle through explanation and examples; the LLM interpreted that principle and applied it to a new task through a different procedural implementation.**

[Source example](examples/02_method_transfer_maf/MAF_RibbonSeat_000035.py) · [Modeling method](docs/MODELING_METHOD.md)

---

## 5. From an individual object to a scene: MARGARITA

The next stage increased not only geometric complexity but also the scale of the task.

### Object

The **MARGARITA** chair was developed as a more demanding object with a repeated corrugated-cardboard structure, a metal support frame, and fastening details.

Its name came from the initial idea of using recycled pizza boxes: corrugated cardboard → pizza boxes → Margherita → **MARGARITA**.

![MARGARITA chair concept](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_chair_concept.jpg)

*Visualization of the intended material and product character. This is a separate image-generation visualization, not a native 3ds Max render.*

### Scene

Once the chair geometry had been developed, the task was expanded into a scene composition. Through the bridge, the LLM created a table, placed four chairs, and assembled the composition in Autodesk 3ds Max 2024.

![MARGARITA viewport in Autodesk 3ds Max](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_viewport.png)

*Actual Autodesk 3ds Max 2024 viewport. The geometry is native and editable.*

After the scene geometry was completed, it was used as the basis for a separate architectural visualization produced with image generation.

![MARGARITA architectural visualization](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_archviz.png)

*Presentation outcome based on the completed scene. It is not evidence of native 3ds Max rendering.*

This stage matters because it moves the experiment **from an individual model to a scene** containing multiple related objects, instances, constructive details, and compositional relationships.

---

## 6. Executable scene representation

Working through Python/pymxs raised an additional question.

If the construction of native geometry can be expressed as a sequence of executable operations, must the binary .max file remain the only carrier of the result?

Autonomous Python/pymxs representations of the created geometry were prepared to test this.

The principle was first tested with GPT Stool No. 1. Its script was run in a separate Autodesk 3ds Max instance that was not connected to the bridge, did not contain the source scene, and had not participated in the modeling process. Execution rebuilt the object as ordinary editable geometry.

The same principle was then applied to the substantially more complex MARGARITA scene.

The full reconstruction source is **14,552 bytes**. The repository also contains a compact **11,530-byte** version.

[MARGARITA full source](examples/margarita/MARGARITA_v4_FULL_SOURCE.py) · [Compact version](examples/margarita/MARGARITA_v4_12KB.py)

The full version was run separately and visually verified in Autodesk 3ds Max 2024. The compact version was syntax-checked, but is not claimed here as a separately verified complete reconstruction.

Two claims must be kept distinct.

The experiment **does not mean that a binary .max file is “compressed into 14 KB of text.”** The executable representation is not a serialization of every internal datum in a 3ds Max file.

The verified result is different: **a native geometric scene can be reconstructed from a compact textual description of the procedure used to build it.**

Such text can simultaneously be:

- executed by a professional DCC system;
- read by a human;
- analyzed programmatically;
- read by an LLM as ordinary source code;
- modified and executed again to produce new native geometry.

This is what makes the executable representation interesting as an additional means of transferring and continuing work on a scene.

---

## 7. Reproducibility and evidence

The research is built around observable results rather than requiring trust in a description of the process.

The repository contains:

- source code of the bidirectional bridge;
- the exchange protocol;
- executable Python/pymxs examples;
- intermediate and final viewport images;
- examples of native geometry;
- materials from the professional-method-transfer experiment;
- the full executable representation of the MARGARITA scene;
- the compact version of that representation;
- images that distinguish actual 3ds Max geometry from subsequent presentation-oriented image generation.

The minimal executable-representation test remains simple:

**empty Autodesk 3ds Max 2024 + Python/pymxs file → reconstructed editable geometry.**

For MARGARITA, the full reconstruction source was tested separately. Compatibility with other versions of 3ds Max or with other DCC applications was not tested in this research.

---

## 8. Conclusions

The experiment showed that a general-purpose language model can be incorporated directly into a professional 3D-modeling loop.

In the implemented system, the LLM is not limited to supplying code for manual transfer by the user. It receives a task in natural language, forms construction operations, transmits them through a minimal bridge to 3ds Max, receives the actual scene state and viewport, and uses that feedback in the next iteration.

At the same time, **3ds Max remains 3ds Max**. No intermediate “AI geometry” is created that later requires conversion. The result consists of standard editable objects in a professional DCC system.

The experiment also demonstrated transfer of a professional modeling principle. Tasy Volkova explained a professional method for solving a class of tasks rather than supplying finished geometry to copy. The LLM interpreted that principle and applied it to a new form, without necessarily using the same literal sequence of commands.

The progression from a simple object to MARGARITA and then to a composition of multiple objects showed that the same loop can be applied to increasingly complex tasks. It also exposed an important boundary: **the human more reliably maintains project context and evaluation criteria; the LLM is effective as a modeler solving the next local task within that context.**

A further result was the executable textual representation of a scene.

It does not replace .max as a universal container for all Autodesk 3ds Max data, nor is it a textual copy of the binary file. Its role is different: **to describe a sufficient sequence of operations to reconstruct the tested native geometry.**

Text therefore performs two functions in the experimental system.

**In one direction, text is the language used to control the modeling process: the LLM forms operations that are executed in 3ds Max.**

**In the other direction, the geometric construction of the scene can be expressed as executable text that an LLM can read, analyze, and modify, and that 3ds Max can turn back into native geometry.**

The bidirectional interface therefore connects not only a language model and a modeling application. It connects two representations of the same process: **a native editable 3D scene and its executable textual description.**
