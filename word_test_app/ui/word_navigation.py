import tkinter as tk
from tkinter import messagebox

from word_test_app.ui.pronunciation import Pronunciation


class WordNavigation:
    def __init__(self, parent, gui):
        self.parent = parent
        self.gui = gui  # 传入 WordTestGUI 实例
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        self.create_button("上一个", self.previous_word).pack(side="left", padx=10)
        self.create_button("下一个", self.next_word).pack(side="left", padx=10)
        self.create_button("除去当前词", self.exclude_current_word).pack(side="left", padx=10)
        self.create_button("打乱全部", self.retry_word_list).pack(side="left", padx=10)

    def create_button(self, text, command):
        return tk.Button(
            self.parent, text=text, width=10, command=command,
            font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=2
        )

    def show_word(self):
        self.gui.show_word()


    def previous_word(self):
        if self.gui.word_test.current_index > 0:
            self.gui.word_test.current_index -= 1
            self.show_word()
            self.gui.pronunciation.start_pronounce_word()
        else:
            messagebox.showinfo("Info", "You are at the first word!")

    def next_word(self):
        if self.gui.word_test.current_index < len(self.gui.word_test.history) - 1:
            self.gui.word_test.current_index += 1
            self.show_word()
            self.gui.pronunciation.start_pronounce_word()
        else:
            messagebox.showinfo("Info", "You are at the last word!")

    def retry_word_list(self):
        self.gui.random_words = self.gui.generate_random_words()
        self.show_word()

    def exclude_current_word(self):
        if self.gui.word_test.current_index < len(self.gui.word_test.history):
            index = self.gui.word_test.history[self.gui.word_test.current_index]
            self.gui.to_exclude.add(index)
            del self.gui.word_test.history[self.gui.word_test.current_index]
            self.gui.word_test.order = [i for i in self.gui.word_test.order if i not in self.gui.to_exclude]
            if self.gui.word_test.current_index >= len(self.gui.word_test.history) and self.gui.word_test.history:
                self.gui.word_test.current_index = len(self.gui.word_test.history) - 1
            if self.gui.word_test.history:
                self.show_word()
            else:
                messagebox.showinfo("Info", "All words have been excluded!")
                self.gui.word_label.config(text="")


