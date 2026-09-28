# File contract

`command.json` — input command from the remote side.

`result.json` — command ID, status, returned results/error and whether viewport capture succeeded.

`scene.json` — lightweight post-command scene snapshot: object names/classes/transforms/bounding boxes.

`viewport.png` — active viewport capture after command processing.

`bridge_status.json` — current bridge identity/version/state.

`bridge_state.json` — last consumed command ID and status; prevents replay.

All files live in `E:\TASY_MaxBridge`. The `library\` subfolder stores reusable `.py` modelling scripts.
