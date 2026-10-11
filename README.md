# Cosmo

Cosmo is a voice assistant that runs on your Windows PC. You talk to it, it answers by voice, and it can act on the machine: open and close apps, move the mouse, type, press keys, change the volume, search the web, read the weather and play files.

It is built on [LiveKit Agents](https://github.com/livekit/agents) with Google's realtime voice model (voice "Charon"). Its behaviour is set by the prompts in `Cosmo_prompts.py`, written in Hindi and English.

## Tools

`agent.py` registers 15 tools:

| Area | Tools | File |
| --- | --- | --- |
| Web and time | `google_search`, `get_current_datetime` | `Cosmo_google_search.py` |
| Weather | `get_weather` | `Cosmo_get_whether.py` |
| Windows and files | `open`, `close`, `folder_file` | `Cosmo_window_CTRL.py` |
| Media files | `Play_file` | `Cosmo_file_opner.py` |
| Keyboard and mouse | `move_cursor_tool`, `mouse_click_tool`, `scroll_cursor_tool`, `type_text_tool`, `press_key_tool`, `press_hotkey_tool`, `control_volume_tool`, `swipe_gesture_tool` | `Cosmo_kb_mouse_CTRL.py` |

## Requirements

- Windows. Window and input control uses `pywin32`, `pyautogui` and `pynput`, so it does not work on macOS or Linux.
- Python 3.12 (the bytecode this repo used to carry was 3.12).
- A LiveKit project, plus Google and OpenWeather API keys. `.env.example` lists the variable names.

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then fill in your own keys
python agent.py console     # or: python agent.py dev
```

Say "shutdown", "quit", "exit" or "close cosmo" to stop it.

## Limits

- Windows only.
- Cosmo controls the real mouse and keyboard. Whatever it is told to type or click happens on your actual desktop, so run it where that is safe.
- It needs internet access and API keys that may be rate-limited or paid.
- No tests are included. The tools were tried by hand.

## Credits

The persona and prompts in `Cosmo_prompts.py` name Arham Khan as the assistant's designer.

## History note

Earlier versions of this repository committed a `.env` file, a `venv/` folder and `__pycache__/`. They have been removed from history. Treat any key that was in that `.env` as exposed and rotate it.
