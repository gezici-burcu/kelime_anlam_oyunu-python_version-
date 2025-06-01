# 🧠 Word Meaning Game (Python Version)

This project is a **Python-based console + Kivy** application that helps users learn word meanings by guessing.

## 🎯 Purpose

The goal is to guess the meaning of randomly shown words. The app gives audio feedback for correct/incorrect answers. Scores are saved in a `scores.txt` file.

---

## 🛠️ Technologies Used

- 🐍 Python 3  
- 🎛️ Kivy (for GUI)  
- 🔊 Audio playback (WAV format)  
- 📄 File operations (word list, score recording)

---

## 📂 File Structure

```plaintext
kelime_anlam_oyunu-python_version/
├── main.py             # Main application file
├── kelime.kv           # Kivy UI definition
├── scores.txt          # Stores user scores
├── dogru.wav           # Sound for correct answers
├── yanlis.wav          # Sound for wrong answers
