
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import numpy as np
from word_test_app.core.audio import AudioPlayer
from word_test_app.core.word_test import WordTest
from word_test_app.ui.widgets import create_button
from word_test_app.ui.word_navigation import WordNavigation
from word_test_app.ui.word_actions import WordActions
from word_test_app.ui.pronunciation import Pronunciation


class WordTestGUI(tk.Tk):
    def __init__(self, word_test):
        super().__init__()
        self.word_test = word_test
        self.audio_player = AudioPlayer()
        self.to_exclude = set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.pronunciation = Pronunciation(self)

        self.configure_ui()
        self.random_words = self.generate_random_words()
        self.show_word()

        # 绑定窗口变化事件用于自适应字体
        self.bind("<Configure>", self.on_resize)

    def configure_ui(self):
        self.title("日语单词记忆")
        self.state("zoomed")
        self.config(bg="#eaeaea")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = tk.Frame(self, bg="#eaeaea")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(main_frame, bg="#eaeaea")
        content_frame.grid(row=0, column=0)

        self.word_frame = tk.Frame(content_frame, bg="#eaeaea")
        self.word_frame.pack(pady=30)

        self.word_label = tk.Label(
            self.word_frame, text="", font=("Helvetica", 36, "bold"),
            bg="#eaeaea", fg="#222"
        )
        self.word_label.pack(side="left")

        self.pronounce_button = create_button(
            self.word_frame, "🔊", self.pronunciation.start_pronounce_word
        )
        self.pronounce_button.pack(side="left", padx=10)

        self.meaning_label = tk.Label(
            content_frame, text="", font=("Helvetica", 18),
            fg="#444", bg="#eaeaea", wraplength=800, justify="center"
        )
        self.meaning_label.pack(pady=10)

        self.button_frame_top = tk.Frame(content_frame, bg="#eaeaea")
        self.button_frame_top.pack(pady=10)

        self.button_frame_bottom = tk.Frame(content_frame, bg="#eaeaea")
        self.button_frame_bottom.pack(pady=10)

        WordNavigation(self.button_frame_top, self)
        WordActions(self.button_frame_bottom, self)

    def on_resize(self, event):
        width = self.winfo_width()
        word_font_size = max(20, int(width * 0.04))
        meaning_font_size = max(12, int(width * 0.018))
        button_font_size = max(10, int(width * 0.015))
        button_width = max(8, int(width * 0.01))

        self.word_label.config(font=("Helvetica", word_font_size, "bold"))
        self.meaning_label.config(font=("Helvetica", meaning_font_size))

        self.pronounce_button.config(
            font=("Helvetica", button_font_size, "bold"),
            width=button_width
        )

        def update_buttons(frame):
            for child in frame.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(font=("Helvetica", button_font_size, "bold"), width=button_width)

        update_buttons(self.button_frame_top)
        update_buttons(self.button_frame_bottom)

    def generate_random_words(self):
        filtered_order = [i for i in self.word_test.order if i not in self.to_exclude]
        np.random.shuffle(filtered_order)
        self.word_test.history = filtered_order
        self.word_test.current_index = 0
        self.pronunciation.start_pronounce_word()
        return iter(self.word_test.history)

    def generate_review_shuffle(self):
        if not self.word_test.history:
            return iter([])
        current_index = self.word_test.current_index + 1
        reviewed = self.word_test.history[:current_index]
        remaining = self.word_test.history[current_index:]
        np.random.shuffle(reviewed)
        new_history = reviewed + remaining
        self.word_test.history = new_history
        self.word_test.current_index = 0
        self.show_word()
        self.pronunciation.start_pronounce_word()
        return iter(new_history)

    def show_word(self):
        if self.word_test.history and self.word_test.current_index < len(self.word_test.history):
            current_index = self.word_test.history[self.word_test.current_index]
            kana = self.word_test.data.iloc[current_index, 0]
            self.word_label.config(text=f"{self.word_test.current_index + 1}. {kana}")
            self.meaning_label.config(text="")
        elif not self.word_test.history:
            self.word_label.config(text="")
            self.meaning_label.config(text="")
            messagebox.showwarning("没有可用词汇", "单词列表为空，或所有词汇已被排除。")
        else:
            messagebox.showinfo("完成", "你已浏览完所有单词！")

    def on_closing(self):
        def after_close_save():
            self.destroy()
        if messagebox.askyesno("保存", "是否保存当前单词表为新文件？"):
            WordActions.save_word_list(callback=after_close_save)
        else:
            self.destroy()
