import random
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# Ayarlar
SÖZLÜK_DOSYA = "kelimeler.txt"
SKOR_DOSYA   = "scores.txt"
TAHMIN_HAKKI = 3

Builder.load_file("kelime.kv")

def load_dictionary():
    d = {}
    with open(SÖZLÜK_DOSYA, encoding="utf-8") as f:
        for line in f:
            if "-" in line:
                parts = line.strip().split("-")
                if len(parts) == 2:
                    l, r = parts
                    d[l.strip().lower()] = r.strip().lower()
    return d

def load_total_score():
    total = 0
    try:
        with open(SKOR_DOSYA, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("—")
                if len(parts) == 2:
                    total += int(parts[1].split()[0])
    except FileNotFoundError:
        open(SKOR_DOSYA, "a").close()
    return total

def save_score(score):
    with open(SKOR_DOSYA, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} — {score} puan\n")

def reset_score():
    open(SKOR_DOSYA, "w", encoding="utf-8").close()

class MainMenu(Screen):
    def reset_scores(self):
        reset_score()

class PlayScreen(Screen):
    def on_enter(self):
        self.words = list(load_dictionary().items())
        self.score = load_total_score()
        self.last_saved_score = self.score  # Skor takibi
        self.next_question()

    def next_question(self, *largs):
        src, tgt = random.choice(self.words)
        if random.choice([True, False]):
            self.q, self.a = src, tgt
        else:
            self.q, self.a = tgt, src

        self.a = self.a.strip().lower()
        self.ids.lbl_q.text = f"“{self.q}” karşılığı nedir?"
        self.ids.inp_ans.text = ""
        self.ids.lbl_score.text = f"Puan: {self.score}"
        self.attempts = TAHMIN_HAKKI
        self.ids.lbl_attempts.text = f"Hak: {self.attempts}"
        self.ids.lbl_feedback.text = ""

    def play_sound(self, sound_file):
        sound = SoundLoader.load(sound_file)
        if sound:
            sound.play()

    def check_answer(self):
       
        ans = self.ids.inp_ans.text.strip().lower()
        possible_answers = [alt.strip() for alt in self.a.split(",")]

        if not ans:
          return

        if ans in possible_answers:
            self.play_sound("dogru.wav")  #  Doğruysa ses çal
            self.score += 1
            all_answers = ", ".join(possible_answers)
            self.ids.lbl_feedback.text = f"[color=00ff00]✅ Doğru! Kabul edilen cevaplar: [b]{all_answers}[/b][/color]"
            self.ids.lbl_score.text = f"Puan: {self.score}"
            save_score(self.score)
            Clock.schedule_once(self.next_question, 2)
        else:
            self.play_sound("yanlis.wav")  #  Yanlışsa ses çal
            self.attempts -= 1
            if self.attempts > 0:
                self.ids.lbl_feedback.text = f"[color=ff0000]❌ Yanlış! Kalan hak: {self.attempts}[/color]"
                self.ids.lbl_attempts.text = f"Hak: {self.attempts}"
            else:
                self.score = max(0, self.score - 1)
                self.ids.lbl_feedback.text = f"[color=ff0000]❌ Hak bitti! Doğru cevaplar: [b]{', '.join(possible_answers)}[/b][/color]"
                self.ids.lbl_score.text = f"Puan: {self.score}"
                save_score(self.score)
                Clock.schedule_once(self.next_question, 3)


    def show_answer(self):
        self.score = max(0, self.score - 1)
        self.ids.lbl_feedback.text = f"[color=ff0000]📘 Doğru Cevap: [b]{self.a}[/b][/color]"
        self.ids.lbl_score.text = f"Puan: {self.score}"
        if self.score != self.last_saved_score:
            save_score(self.score)
            self.last_saved_score = self.score
        Clock.schedule_once(self.next_question, 3)

    def give_hint(self):
        if len(self.a) <= 2:
            hint = self.a
        else:
            hint = self.a[:2] + ("*" * (len(self.a) - 2))
        self.ids.lbl_feedback.text = f"[color=00ffff]🔎 İpucu: {hint}[/color]"

class WordListScreen(Screen):
    def on_enter(self):
        self.ids.word_list.clear_widgets()
        from kivy.uix.label import Label
        for src, tgt in sorted(load_dictionary().items()):
            self.ids.word_list.add_widget(Label(text=f"{src} → {tgt}", size_hint_y=None, height="30dp"))

class AddWordScreen(Screen):
    def add_word(self):
        src = self.ids.inp_src.text.strip().lower()
        tgt = self.ids.inp_tgt.text.strip().lower()
        if src and tgt:
            with open(SÖZLÜK_DOSYA, "a", encoding="utf-8") as f:
                f.write(f"{src}-{tgt}\n")
            self.ids.lbl_feedback.text = "✅ Eklendi!"
            self.ids.inp_src.text = self.ids.inp_tgt.text = ""
            App.get_running_app().root.get_screen("list").on_enter()
        else:
            self.ids.lbl_feedback.text = "⚠️ Eksik giriş!"

class KelimeApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(PlayScreen(name="play"))
        sm.add_widget(WordListScreen(name="list"))
        sm.add_widget(AddWordScreen(name="add"))
        return sm

if __name__ == "__main__":
    KelimeApp().run()
