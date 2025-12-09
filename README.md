# termitype
```
 ____  ____  ____  __  __  ____  ____  _  _  ____  ____          made by sawsent
(_  _)( ___)(  _ \(  \/  )(_  _)(_  _)( \/ )(  _ \( ___)
  )(   )__)  )   / )    (  _)(_   )(   \  /  )___/ )__)
 (__) (____)(_)\_)(_/\/\_)(____) (__)  (__) (__)  (____)
```

A clean, minimal, fully-terminal typing test — inspired by Monkeytype, built for people who love the terminal.

Termitype focuses on:

- a refined terminal UI
- extensibility through adapters (macOS, Linux, Windows/PowerShell)  
- portability with zero external frameworks  
- a simple, fast typing experience

---

## Features

### ✔ Minimal, beautiful terminal UI  
A clean interface built specifically for terminal environments.  
Fully adjustable **width** and **height** via settings.

### ✔ Real-time typing test  
- Randomized words  
- Accurate cursor simulation  
- Inline mistake highlighting  
- Previous, current, and next words clearly spaced  

### ✔ Settings screen with full-text search  
Settings are now searchable: type to filter options instantly.

### ✔ End-of-run results screen  
Shows:
- WPM  
- Accuracy  
- Duration  
- A diff-style view comparing typed vs expected text  

### ✔ Adapter-based architecture  
All OS-specific terminal behavior (cursor movement, color support, input handling) is abstracted.  
Termitype works equally well on:
- macOS (Terminal, iTerm2) (implemented)
- Linux (not implemented)
- Windows Terminal / PowerShell (not implemented)

### ✔ Persistent run storage  
Store:
- WPM  
- accuracy  
- date/time  
- detailed statistics  
- settings used for the run  

### ✔ Stats dashboard  
A new analytics-driven screen:
- WPM personal best
- rolling averages
- lifetime totals

---

## Roadmap

### 🔜 Windows and Linux adapters
Right now only the Macos adapter is implemented, soon other adapters will be added.

### 🔜 Color schemes  
Easy to change themes to customize the look.

---

## Philosophy

Termitype is designed to be:

- **fast** — instant, frictionless startup
- **portable** — independent of terminal quirks, without frameworks
- **extensible** — clean architecture, easy to add new screens
- **pleasant** — polished UI details without complexity

---

## Installation
```bash
pip install termitype
```

---

## Usage
Just run the termitype command to open the app!
```bash
termitype
```

## Screenshots

### Typing screen  
![typing screen](https://raw.githubusercontent.com/sawsent/termitype/main/media/run-screen.png)

### Results screen
![results screen](https://raw.githubusercontent.com/sawsent/termitype/main/media/results-screen.png)

### Settings screen (with search)
![settings search](https://raw.githubusercontent.com/sawsent/termitype/main/media/settings-screen.png)

### Profile dashboard
![profile dashboard](https://raw.githubusercontent.com/sawsent/termitype/main/media/dashboard-screen.png)
---

## License

Licensed under the **Apache License 2.0**.  
See the [`LICENSE`](LICENSE) file for details.

---

## ❤️ Inspiration

- [Monkeytype](https://monkeytype.com) — for setting the bar high.  
- The simplicity of terminal tools that “just work.”
