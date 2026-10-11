# TASY MaxBridge 0.6.1 PORTABLE

**Direct ChatGPT ↔ Autodesk 3ds Max 2024 modeling through Python/pymxs and a synchronized folder.**

![Margarita architectural visualization](assets/margarita_archviz.png)

**MARGARITA · Architectural Visualization.** Four sculptural chairs and a table modeled by ChatGPT in a live 3ds Max session through TASY MaxBridge, under the art direction of **Tasy Volkova**. The image above is a generative architectural visualization based on the actual 3ds Max viewport, not a native Max renderer output.

![Actual 3ds Max viewport](assets/margarita_viewport.png)

*Actual editable geometry in Autodesk 3ds Max 2024.* [Explore the scene and download the 11,530-byte reconstruction script](examples/margarita/).

## What the bridge does

ChatGPT writes a JSON command containing Python/pymxs. TASY MaxBridge reads it from its local folder, executes it inside the running 3ds Max, and returns `result.json`, `scene.json`, status and, when possible, `viewport.png`. Google Drive is one possible synchronized **file transport**; the bridge does not use its API and does not require an agent framework.

**Important: ChatGPT does not automatically know how to model professionally.** A working connection is not a modeling skill. Teach the model about dimensions, spline sections, constructive logic, modifiers, grouping and visual verification. The human architect or art director remains responsible for decisions and acceptance.

## Quick installation

1. Download `TASY_MaxBridge_061_PORTABLE.py` from this repository.
2. Create a **dedicated writable local folder** and place the `.py` inside it. The bridge stores all its files beside the script. **No fixed drive letter is required.**
3. Start **Autodesk 3ds Max 2024**, choose **Scripting → Run Script**, and select the bridge `.py`.
4. Verify `TASY MaxBridge 0.6.1 PORTABLE running` and the `ROOT:` path in the Python Listener. `library/`, `bridge_status.json`, and `scene.json` should appear.
5. Optionally synchronize **that folder** with Google Drive or another bidirectional file transport that your ChatGPT environment can read and write.
6. Create `command.json` in the same folder:

```json
{"id":"test-ping-001","action":"ping"}
```

7. Check that `result.json` has matching `command_id`, `status: ok`, and `pong`. For each new command use a **new ID**.
8. Try a first object:

```json
{"id":"test-teapot-002","action":"execute_python","code":"o=rt.Teapot(radius=250); o.name='Bridge_Test_Teapot'; rt.select(o); rt.execute('max tool zoomextents all')"}
```

Check the geometry **in Max**, not just the response code. For complete installation, troubleshooting and synchronization instructions see [the Russian installation guide](docs/INSTALL_RU.md).

## Learn to model: training examples

- [Stools](examples/stools/): basic dimensions, geometry, construction and grouping.
- [Pergola](examples/pergola/): planned architectural exercise in repeated elements and assembly; verified source pending.
- [Margarita](examples/margarita/): spline cross-sections, iterative scene building and artistic use of unexpected geometry. The **entire reproducible scene fits into 11,530 bytes of Python text**, without transferring a native `.max` file.

The original live modeling loop required MaxBridge. The final standalone Margarita script is a separate portability demonstration and **runs without the bridge**.

## Safety and limitations

**SECURITY WARNING:** `execute_python` executes arbitrary Python with the permissions of the 3ds Max process. Use only trusted command sources. Never expose a writable bridge folder publicly. Keep one bridge instance per working folder and save scenes before running unfamiliar code.

`status: ok` confirms execution, **not geometry quality**. Always verify the matching command ID, actual viewport and object positions. The bridge does not provide automatic modeling expertise or guarantee successful screenshots.

## License and attribution

Apache License 2.0. Copyright © 2026 **Tasy Volkova**. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [CITATION.cff](CITATION.cff).

Suggested attribution: `Based on TASY MaxBridge / LLM-3D-Scene-Bridge — https://github.com/tvolkf-star/LLM-3D-Scene-Bridge (Apache-2.0).`

Apache 2.0 requires preservation of applicable notices on redistribution, but does not require downstream users to publish all changes or display an author link in their app interface.

Project: [tasy.pro](https://tasy.pro/) · [TasyTools](https://github.com/tvolkf-star/TasyTools)
