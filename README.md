# 🐍 Snake Game (Python + Pygame)

A classic Snake game built with Python and Pygame, featuring multiple map sizes, pixel art sprites, sounds, and a highscore system.

---

## 🎮 Features

* Smooth snake movement with input buffering
* 3 map sizes (6x6, 9x9, 12x12)
* Pixel art graphics (snake, apple, grass)
* Sound effects (eat, death, movement, menu clicks)
* Persistent highscore saving (`highscore.json`)
* Simple menu system + game over screen

---

## 🖥️ Requirements

You need:

* Python 3.x
* pygame

Install pygame:

```bash
pip install pygame
```

---

## 📁 Project Structure

Make sure your folder looks like this:

```
Snake/
├── Snake.py
├── highscore.json
├── assets/
│   ├── Snake_Apple.png
│   ├── Snake_Body.png
│   ├── Snake_Grass.png
│   ├── Snake_Head.png
│   ├── Snake_Tail.png
│   ├── Snake_Turn.png
│   └── sounds/
│       ├── Apple_Eat_Sound.wav
│       ├── Snake_Died_Sound.wav
│       ├── Menu_Select_Sound.wav
│       └── Movement_sound (2).wav
```

---

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Run the game:

```bash
python Snake.py
```

---

## 🎮 Controls

### Menu:

* **ENTER** → Start game
* **X** → Quit

### In Game:

* **W / A / S / D** → Move snake

### Game Over:

* **ENTER** → Restart
* **ESC** → Back to menu
* **X** → Quit

---

## 💾 Highscores

Highscores are saved automatically in:

```
highscore.json
```

If the file is missing, it will be created automatically.

---

## ⚠️ Notes

* Make sure the `assets/` folder is in the same directory as `Snake.py`
* If sounds or images don’t load, check file paths
* Game runs best in fullscreen resolution

---

## 🚀 Author

Made by **Awack**

---

If you want, I can also:

* make it look like a **Steam-quality README**
* add badges (Python version, status, etc.)
* or write a short GitHub bio/description for your repo

Just say 👍
