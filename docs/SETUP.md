# Setup — 3ds Max 2024

## Requirements

- Autodesk 3ds Max 2024 with `pymxs` and PySide2.
- A local folder at `E:\TASY_MaxBridge`.
- Optional: sync that folder with a cloud transport such as Google Drive. The bridge itself does not depend on the Google Drive API.

## Folder layout

```text
E:\TASY_MaxBridge\
  command.json
  result.json
  scene.json
  viewport.png
  bridge_status.json
  bridge_state.json
  library\
```

The bridge intentionally writes JSON directly and does **not** create `.tmp` files in the synchronized root.

## Start

Run `TASY_MaxBridge_061_PERSONAL.py` in 3ds Max. It does not reset the current scene. It starts a Qt timer that checks `command.json` every 1000 ms.

Expected Listener output:

```text
TASY MaxBridge 0.6.1 PERSONAL running
ROOT: E:\TASY_MaxBridge
LIB:  E:\TASY_MaxBridge\library
```

## Command consumption

Every command needs a unique `id`. The bridge marks the ID consumed **before** scene mutation. Therefore a command that fails halfway is not executed again every second.

`execute_python` uses the field **`code`**. Its scope exposes `rt`, `os`, `json`, `ROOT`, `LIB` and Python builtins.

## Supported actions

The compact bridge supports `ping`, `execute_python`, `library_list`, `library_save`, `library_run`, plus small convenience actions `create_box`, `move`, `scale`, `rotate`, `delete`, and `rename`.

`library_run` exposes a `params` dictionary to the saved script.

## First test

Write this to `command.json`:

```json
{"id":"test-001","action":"ping"}
```

Check `result.json`. It should report `status: ok` and contain `pong` in `results`. The bridge also refreshes `scene.json` and attempts to save `viewport.png`.

Then test real Max execution:

```json
{
  "id":"test-002",
  "action":"execute_python",
  "code":"o=rt.Teapot(radius=250); o.name='Bridge_Test_Teapot'; rt.select(o); rt.execute('max tool zoomextents all')"
}
```

## Re-running the bridge

The script attempts to stop older bridge instances stored under the known bridge global names before creating the current one. If Max has been restarted, simply run the bridge again.

## Troubleshooting

**Nothing happens:** confirm the local root is exactly `E:\TASY_MaxBridge`, `command.json` contains valid JSON, and its `id` differs from `bridge_state.json:last_command_id`.

**Python command is empty:** use `code`, not a made-up field name. The compact 0.6.1 reads `code` for `execute_python`.

**A failed command keeps coming back:** it should not on this build; the command ID is consumed before mutation. Check that the running bridge is actually this compact 0.6.1 file.

**Viewport is not updated:** check `result.json:viewport_saved`; viewport capture is best-effort and does not invalidate successful geometry execution.

**Wrong bridge copy is running:** compare the Listener startup line and keep one canonical bridge file. Do not mix this release candidate with earlier experimental expanded copies.
