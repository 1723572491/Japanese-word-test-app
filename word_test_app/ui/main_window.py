from tkinter import Toplevel, messagebox
from ttkbootstrap.widgets import Button, Label, Frame
from ttkbootstrap import Style
from word_test_app.core.audio import AudioPlayer
from word_test_app.ui.widgets import create_button
from word_test_app.ui.word_navigation import WordNavigation
from word_test_app.ui.word_actions import WordActions
from word_test_app.ui.pronunciation import Pronunciation
import numpy as np

class WordTestGUI(Toplevel):
    def __init__(self, master, word_test):
        super().__init__(master)  # ✅ 挂靠主窗口
        self.word_test = word_test
        self.audio_player = AudioPlayer()
        self.to_exclude = set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.pronunciation = Pronunciation(self)

        self.dynamic_style = Style()
        self.dynamic_style.configure("Dynamic.TButton", font=("Helvetica", 14, "bold"))
        self.configure_ui()
        self.random_words = self.generate_random_words()
        self.show_word()

        self.bind("<Configure>", self.on_resize)

    def configure_ui(self):
        self.title("日语单词记忆")
        self.state("zoomed")
        self.configure(padx=20, pady=20)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        content_frame = Frame(main_frame)
        content_frame.grid(row=0, column=0)

        self.word_frame = Frame(content_frame)
        self.word_frame.pack(pady=30)

        self.word_label = Label(
            self.word_frame, text="", font=("Helvetica", 36, "bold")
        )
        self.word_label.pack(side="left")

        self.pronounce_button = create_button(
            self.word_frame, "🔊", self.pronunciation.start_pronounce_word
        )
        self.pronounce_button.pack(side="left", padx=10)

        self.meaning_label = Label(
            content_frame, text="", font=("Helvetica", 18),
            wraplength=800, justify="center"
        )
        self.meaning_label.pack(pady=10)

        self.button_frame_top = Frame(content_frame)
        self.button_frame_top.pack(pady=10)

        self.button_frame_bottom = Frame(content_frame)
        self.button_frame_bottom.pack(pady=10)

        WordNavigation(self.button_frame_top, self)
        WordActions(self.button_frame_bottom, self)

    def on_resize(self, event):
        width = self.winfo_width()

        word_font_size = max(28, int(width * 0.05))
        meaning_font_size = max(14, int(width * 0.02))
        button_font_size = max(10, int(width * 0.017))
        button_width = max(10, int(width / 90))

        self.word_label.config(font=("Helvetica", word_font_size, "bold"))
        self.meaning_label.config(font=("Helvetica", meaning_font_size))

        style = Style()
        style.configure("Dynamic.TButton", font=("Helvetica", button_font_size, "bold"))

        def update_buttons(frame):
            for child in frame.winfo_children():
                if isinstance(child, Button):
                    child.config(style="Dynamic.TButton", width=button_width)

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
