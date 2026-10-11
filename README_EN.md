# LLM–3D Scene Bridge / TASY MaxBridge

**A working experiment in direct 3D modeling from natural-language descriptions using ChatGPT and Autodesk 3ds Max 2024.**

**[⬇ DOWNLOAD COMPLETE PACKAGE: bridge, examples, documentation and images](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/TASY_MaxBridge_v0.6.1_PORTABLE_COMPLETE.zip)**

[Русский README](README.md) · [Quick start (Russian)](START_HERE_RU.md) · [Full research (Russian)](RESEARCH_RU.md) · [Releases](../../releases/tag/v0.6.1-portable)

## What we are investigating

Can a general-purpose language model work **directly as a modeler inside a professional 3D application**, rather than simply generating scripts for a person to copy and run?

The experiment studies a closed loop: **ChatGPT → Autodesk 3ds Max → observable scene and viewport → ChatGPT → next iteration**.

![Margarita scene visualization](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_archviz.png)

**Scene visualization by ChatGPT.** Generative architectural visualization based on the actual 3ds Max viewport. **Not a native 3ds Max render.**

![Margarita scene in 3ds Max](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_viewport.png)

**Scene modeled by ChatGPT using MaxBridge.** Native, editable geometry inside Autodesk 3ds Max 2024.

## How to start

1. **Download the complete ZIP** above and extract it.
2. Open **3ds Max 2024 → Scripting → Run Script**, select `TASY_MaxBridge_061_PORTABLE.py`. The bridge creates its working files alongside the script.
3. **Synchronize the bridge folder using Google Drive for desktop**, keeping it locally accessible and bidirectionally synced.
4. **Give ChatGPT access to that Google Drive folder**, provide the project documentation, and ask it to study the examples and file protocol.
5. **Describe the modeling task.** Once access and synchronization are working, ChatGPT can send operations and inspect results.

[Detailed installation and troubleshooting (Russian)](START_HERE_RU.md) · [Technical setup documentation](docs/INSTALL_RU.md)

## Closed modeling loop

```text
Natural-language task
        ↓
     ChatGPT
        ↓
   Google Drive
        ↓ local sync
~8 KB Python/pymxs bridge
        ↓
Autodesk 3ds Max 2024
        ↓
native editable geometry
        ↓
result + scene state + viewport
        ↓
   Google Drive
        ↓
     ChatGPT
        ↺ next iteration
```

No autonomous agent framework.  
No specialized 3D model.  
No text-to-3D generator.  
No custom modeling environment.  
No manual copy-paste of generated code into 3ds Max during the working loop.

Google Drive is a third-party synchronized **transport layer**. It contains no modeling logic. The bridge contains no modeling intelligence and no predefined high-level instructions such as “make a chair” or “make a facade”. It executes operations inside 3ds Max and returns observable results.

**The modeling decisions remain on the general-purpose LLM side. The geometry remains on the 3ds Max side.**

## Research question

> **Can a general-purpose language model work directly as a modeler inside a professional 3D environment?**

The goal was not to test whether ChatGPT could write a script for a human to copy. The goal was to close the loop: task → modeling operation → actual scene → viewport → evaluation → next operation.

## What was demonstrated

### 01 — Control object: stool

A simple stool served as a controlled modeling task. The experiment involved professional correction of the modeling method, creation of native geometry, and a standalone Python/pymxs representation of the object.

![Stool reproduced in 3ds Max](media/GPT_Stool_clean_max.png)

[Source scripts](examples/stools/)

### 02 — Transfer of a professional modeling method

The architect taught a **reusable modeling principle**, not merely a set of coordinates: define a source profile, specify how it changes spatially or parametrically, sample repeated states, and clean up the resulting editable geometry.

ChatGPT applied this principle to a new urban-furniture / shade-seat construction.

![Independent MAF result](media/MAF_000035_single.png)

The construction was subsequently duplicated, rotated, and arranged in a larger spatial composition.

![MAF pair](media/MAF_000035_pair.png)

![MAF grounded composition](media/MAF_000035_grounded.png)

Intermediate failures matter: professional feedback changed the **modeling method**, not merely object coordinates.

[Original command 000035 and executable source](examples/pergola/) · [Spline modeling method](docs/MAXBRIDGE_SPLINE_MODELING_RU.md) · [Snapshot method](docs/MAXBRIDGE_SNAPSHOT_MODELING_RU.md)

**Technical distinction:** command `000035` procedurally creates 73 varying spline profiles. It is **not** the separate Path Constraint → Auto Key → Snapshot technique. **The original command resets the active 3ds Max scene without a save prompt.**

### 03 — Executable scene representation

The stool experiment raised a second question: must a modeled scene be transmitted as a traditional native scene file?

The object was represented as a self-contained Python/pymxs program. In a separate clean 3ds Max instance, without the bridge or original scene, that program reconstructed editable geometry.

> **An ordinary scene stores a state of the world. An executable scene can store the rules by which that state is produced.**

> **The scene itself can be transmitted as a program.**

[Stool scripts](examples/stools/) · [Margarita scene scripts](examples/margarita/)

## Research and source files

- [Full research draft (Russian)](RESEARCH_RU.md)
- [Setup and reproduction](docs/SETUP.md)
- [Professional modeling-method transfer](docs/MODELING_METHOD.md)
- [Transport and file protocol](protocol/FILES.md)
- [Installation and troubleshooting (Russian)](docs/INSTALL_RU.md)
- [Portable bridge source](TASY_MaxBridge_061_PORTABLE.py)
- [Stool examples](examples/stools/), [pergola](examples/pergola/), [Margarita](examples/margarita/)

## Status and limitations

This is an ongoing practical experiment, not a claim to be the first LLM-to-3ds-Max integration. It demonstrates the combination of a general-purpose language model, a minimal transport bridge, third-party file synchronization, native editable geometry, observable feedback, professional method transfer, and executable scene representation.

Successful code execution does **not** establish geometric correctness. Viewport capture is best-effort. ChatGPT requires instructions, examples and professional feedback to model effectively.

**Security:** `execute_python` runs arbitrary Python with the privileges of 3ds Max. Trust the command source and save your scene before running unfamiliar scripts.

**Author:** Tasy Volkova · **License:** [Apache-2.0](LICENSE) · [NOTICE](NOTICE) · [CITATION.cff](CITATION.cff) · [tasy.pro](https://tasy.pro/)
