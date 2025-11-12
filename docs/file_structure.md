```
termitype/
├── __init__.py
├── __main__.py              # Entry point (bootstraps the App)
│
├── app/
│   ├── __init__.py
│   ├── app.py               # Main App loop (state machine)
│   ├── context.py           # Global context (config, user, stats cache)
│   └── state.py             # Enum or registry for app states
│
├── views/                   # Self-contained “screens” / states
│   ├── __init__.py
│   ├── base.py              # Base View interface (render, handle_input, next_state)
│   ├── menu.py              # Main menu screen
│   ├── typing.py            # Typing session view (hooks into core engine)
│   ├── results.py           # Run summary view
│   └── settings.py          # Optional settings/config view
│
├── core/                    # Core domain logic (pure logic, no I/O)
│   ├── __init__.py
│   ├── engine.py            # Typing logic (timing, progress, input validation)
│   ├── words.py             # Word list handling and randomization
│   └── stats.py             # WPM, accuracy, streaks, etc.
│
├── storage/                 # Storage logic (to file, in memory, ...)
│   ├── base.py              # Base storage interface
│   ├── memory.py            # in-memory storage
│   └── persistent.py        # persistent file-based storage 
│
├── adapters/                # Terminal/IO implementations
│   ├── __init__.py
│   ├── base.py              # Abstract adapter interface
│   ├── linux.py
│   ├── mac.py
│   ├── powershell.py
│   └── tui.py               # (Optional) a text-based UI adapter
│
├── data/
│   ├── words.txt            # Default word list
│   └── config.toml          # Default configuration
│
├── cli/
│   ├── __init__.py
│   └── entrypoint.py        # CLI parser for `termitype` command (starts app)
│
└── utils/
    ├── __init__.py
    └── logger.py            # Optional debug logging
```
