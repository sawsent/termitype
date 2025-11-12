# 🧠 Termitype

*A minimal, extensible typing speed test for your terminal.*

---

## Overview

**Termitype** is a command-line typing speed tester inspired by [Monkeytype](https://monkeytype.com) — but built entirely for the terminal.  
It’s for people who love the command line, enjoy typing fast, and appreciate clean, thoughtful design.

The goal is to make something **simple**, **extensible**, and **pleasant to use**.  
No flashy dependencies. Just Python, a terminal, and your keyboard.

---

## 🧭 Roadmap

- [ ] Core typing engine  
- [ ] Word list loader  
- [ ] Basic CLI runner  
- [ ] WPM and accuracy tracking  
- [ ] Terminal adapters (Linux/macOS/PowerShell)  
- [ ] Persistent stats  
- [ ] Configurable themes  
- [ ] Plugin system for extensions  

---

## 🚀 Example Usage

```bash
termitype run words=100
```

You’ll see a randomized set of words appear in your terminal.  
Type them as fast and accurately as you can — when you’re done, Termitype will show your results:

```
---------------------------
Run complete!
Words: 100
Time: 72.4s
WPM: 83.1
Accuracy: 98%
---------------------------
```

---

## 🧘 Philosophy

Termitype is designed around a few guiding principles:

- **Keep it simple** — the terminal is already beautiful.  
- **Be extensible** — everything from input handling to rendering can be swapped out.  
- **No bloat** — avoid heavy frameworks or unnecessary dependencies.  
- **Just work** — run a command, type some words, get your score.

---

## 🤝 Contributing

Contributions are welcome!  
Whether it’s adding adapters, improving the typing logic, or refining the UX, all help is appreciated.  

For setup instructions and development details, see [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

---

## ⚖️ License

Licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## ❤️ Inspiration

- [Monkeytype](https://monkeytype.com) — for setting the bar high.  
- The simplicity of terminal tools that “just work.”
