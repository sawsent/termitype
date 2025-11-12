# Termitype Project Structure

This document explains the purpose of each folder and file in the Termitype project.

---

## Root

- `__main__.py` — Entry point; bootstraps the persistent app loop.  
- `__init__.py` — Marks `termitype` as a Python package.

---

## app/

- `app.py` — Main application loop (state machine handling persistent session).  
- `context.py` — Holds global context: configuration, user info, cached stats.  
- `state.py` — Defines available app states and transitions between them.

---

## views/  *(self-contained “screens” for the app)*

- `base.py` — Base interface for all views (`render`, `handle_input`, `next_state`).  
- `menu.py` — Main menu screen for navigation and commands.  
- `typing.py` — Typing session screen; hooks into the core engine.  
- `results.py` — Displays run summary (WPM, accuracy, stats).  
- `settings.py` — Optional settings/config screen.

---

## core/  *(pure logic, independent of terminal)*

- `engine.py` — Handles the typing logic: timing, input validation, progress tracking.  
- `words.py` — Loads and randomizes word lists for typing sessions.  
- `stats.py` — Calculates WPM, accuracy, streaks, and other metrics.  

---

## storage/ *(Handles storage I/O interface and implementations)*

- `base.py` - Base interface for all storage (`add`, `get`)
- `memory.py` - In-memory persistence
- `persistent.py` - Persistent storage

---

## adapters/  *(terminal I/O implementations)*

- `base.py` — Abstract adapter interface for rendering and input.  
- `linux.py` — Linux terminal adapter.  
- `mac.py` — macOS terminal adapter.  
- `powershell.py` — Windows PowerShell adapter.  

---

## data/

- `words.txt` — Default word list for sessions.  
- `config.toml` — Default configuration and settings.

---

## cli/

- `entrypoint.py` — Handles parsing `termitype` command-line arguments and starts the app.

---

## utils/

- `timer.py` — Lightweight timer abstraction for measuring session durations.  
- `logger.py` — Optional logging utility for debugging.  
- `theme.py` — Optional color schemes and visual styling.

---

## tests/

- `test_engine.py` — Unit tests for the typing engine.  
- `test_views.py` — Tests for view logic and transitions.  
- `test_storage.py` — Tests for saving and loading runs.  
- `test_app_loop.py` — Tests for the main application loop and state transitions.

---

### Notes

- Core engine and utils are **framework-independent** and fully testable.  
- Adapters isolate terminal or platform-specific behavior.  
- Views are modular and can be added/removed without touching core logic.  
- The app loop drives a **persistent session**, switching between views/states seamlessly.

