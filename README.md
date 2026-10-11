# LLM–3D Scene Bridge / TASY MaxBridge

**A working experiment in direct 3D modeling from natural-language descriptions using ChatGPT and Autodesk 3ds Max 2024.**

**[⬇ СКАЧАТЬ ПОЛНЫЙ КОМПЛЕКТ / DOWNLOAD COMPLETE RELEASE ZIP](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/TASY_MaxBridge_v0.6.1_PORTABLE_COMPLETE.zip)**

**В архиве:** портативный мост 0.6.1, README, русская инструкция установки, примеры моделирования (табуретки, пергола, «Маргарита»), исходные команды, изображения, лицензия и учебная документация.

[Русская инструкция по установке](docs/INSTALL_RU.md) · [Полный текст исследования](RESEARCH_RU.md) · [English README](README_EN.md) · [Все файлы релиза](../../releases/tag/v0.6.1-portable)

## Что исследуем

Можно ли дать универсальной языковой модели возможность **не только писать код для 3ds Max, но и непосредственно моделировать в работающей программе**, получать состояние сцены и изображение viewport, анализировать результат и выполнять следующую итерацию?

Здесь исследуется реальный замкнутый процесс **ChatGPT → 3ds Max → обратная связь → ChatGPT**, а не генерация иллюстраций по тексту.

![Рендер сцены с Маргаритой](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_archviz.png)

**Рендер сцены Джипити.** Генеративная архитектурная визуализация, выполненная на основе реального viewport созданной в 3ds Max сцены. Это не штатный рендер 3ds Max.

![Сцена Маргарита в Autodesk 3ds Max](https://github.com/tvolkf-star/LLM-3D-Scene-Bridge/releases/download/v0.6.1-portable/margarita_viewport.png)

**Сцена, смоделированная Джипити при помощи моста.** Реальная редактируемая геометрия в Autodesk 3ds Max 2024.

---

No autonomous agent framework.  
No specialized 3D model.  
No text-to-3D generator.  
No custom modeling environment.  
No manual copy-paste of generated code into 3ds Max during the working loop.

The system connects ChatGPT to a locally running Autodesk 3ds Max through **Google Drive as a third-party synchronized transport layer** and an approximately **8 KB Python/pymxs bridge**.

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

Google Drive contains no modeling logic. The bridge contains no modeling intelligence and no predefined commands such as “make a chair”, “make a facade”, or “make a building”. It transports executable operations to 3ds Max and returns observable results.

**The modeling decisions remain on the general-purpose LLM side. The geometry remains on the 3ds Max side.**

The output is ordinary **native, editable Autodesk 3ds Max geometry**.

## Research question

The experiment began as a practical test:

> **Can a general-purpose language model work directly as a modeler inside a professional 3D environment?**

It was not a test of whether an LLM can write a 3ds Max script for a human to copy and run. The goal was to close the loop: task → modeling operation → actual scene → viewport → evaluation → next modeling operation.

## What was demonstrated

### 01 — Control object: stool

A simple stool was used as a controlled modeling task. The process included professional correction of the modeling method, creation of native geometry, and export of the construction logic as an autonomous Python/pymxs scene program.

![Stool reproduced in 3ds Max](media/GPT_Stool_clean_max.png)

[Stool source scripts](examples/stools/)

### 02 — Transfer of a professional modeling method

The architect then explained a reusable professional technique rather than supplying an object to copy: one source profile/object, a rule of spatial or parametric change, repeated sampled states, and cleanup into usable native geometry.

ChatGPT applied the learned logic to a new task: a large slatted urban-furniture / shade-seat module.

![Independent MAF result](media/MAF_000035_single.png)

The result was then duplicated, rotated and placed in a larger spatial composition in 3ds Max.

![MAF pair](media/MAF_000035_pair.png)

![MAF grounded composition](media/MAF_000035_grounded.png)

The intermediate failures are part of the experiment: professional feedback changed the **modeling method**, not merely a list of coordinates.

[Original MAF command 000035 and Python source](examples/pergola/) · [Spline modeling method](docs/MAXBRIDGE_SPLINE_MODELING_RU.md) · [Snapshot method](docs/MAXBRIDGE_SNAPSHOT_MODELING_RU.md)

**Technical distinction:** Command `000035` generates 73 changing spline profiles procedurally. The separately documented Path Constraint → Auto Key → Snapshot workflow is a different technique. **Command `000035` resets the active 3ds Max scene without a save prompt.**

### 03 — Executable scene representation

The stool experiment produced a second research question: does the scene itself have to be transmitted as a traditional scene file?

The modeled object was represented as an autonomous Python/pymxs program. A separate clean instance of 3ds Max, without the bridge and without the source scene, reconstructed the editable object from that program.

> **An ordinary scene stores a state of the world. An executable scene can store the rules by which that state is produced.**

Or, more simply:

> **The scene itself can be transmitted as a program.**

[Executable stool scripts](examples/stools/) · [Margarita scene reconstruction scripts](examples/margarita/)

## Read the research

- [Full research draft — Russian](RESEARCH_RU.md)
- [Setup and reproduction](docs/SETUP.md)
- [Professional modeling-method transfer](docs/MODELING_METHOD.md)
- [Transport/file protocol](protocol/FILES.md)
- [Detailed Russian installation guide for 0.6.1 PORTABLE](docs/INSTALL_RU.md)

## Repository contents

- [`TASY_MaxBridge_061_PORTABLE.py`](TASY_MaxBridge_061_PORTABLE.py) — working portable Python/pymxs bridge for Autodesk 3ds Max 2024.
- `bridge/` — compact bridge research sources and related files.
- `examples/01_stool/` — original stool construction research.
- `examples/02_method_transfer_maf/` — original modeling-method transfer experiment.
- [`examples/stools/`](examples/stools/) — packaged stool scripts.
- [`examples/pergola/`](examples/pergola/) — original command `000035` and executable Python.
- [`examples/margarita/`](examples/margarita/) — reconstructible sculptural scene scripts.
- `media/` — original viewport evidence from the experiment.
- `docs/` — setup, installation and modeling-method documentation.
- `protocol/` — transport contract and command examples.

## Status

This repository documents an ongoing practical experiment. It makes no claim that this is the first LLM-to-3ds-Max integration. The focus is the demonstrated combination of a general-purpose ChatGPT model, a deliberately minimal transport bridge, a third-party synchronized storage layer, native editable 3ds Max geometry, visual/state feedback, professional method transfer, and executable scene representation.

**Verification note:** a successful script execution does not by itself establish the geometric quality of the result. Viewport captures are best-effort and not guaranteed for every command.

**Security:** `execute_python` runs arbitrary Python inside 3ds Max with the process's permissions. Only use trusted commands; save existing scenes before experiments.

**Author:** Tasy Volkova · **License:** [Apache-2.0](LICENSE) · [NOTICE](NOTICE) · [CITATION.cff](CITATION.cff) · [tasy.pro](https://tasy.pro/)
