
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from core.audio import AudioPlayer
from core.word_test import WordTest
import numpy as np

class WordTestGUI(tk.Tk):
    def __init__(self, word_test):
        super().__init__()
        self.word_test = word_test
        self.audio_player = AudioPlayer()
        self.to_exclude = set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.configure_ui()
        self.random_words = self.generate_random_words()
        self.show_word()

    def configure_ui(self):
        self.title("日语单词记忆")
        self.geometry("800x300")
        self.config(bg="#eaeaea")

        self.word_frame = tk.Frame(self, bg="#eaeaea")
        self.word_frame.pack(pady=30)

        self.word_label = tk.Label(self.word_frame, text="", font=("Helvetica", 32, "bold"), bg="#eaeaea", fg="#333")
        self.word_label.pack(side="left")

        self.pronounce_button = tk.Button(
            self.word_frame, text="🔊", command=self.start_pronounce_word,
            font=("Helvetica", 12), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=2, width=2
        )
        self.pronounce_button.pack(side="left", padx=10)

        self.meaning_label = tk.Label(self, text="", font=("Helvetica", 16), fg="#666", bg="#eaeaea")
        self.meaning_label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#eaeaea")
        self.button_frame.pack(pady=20)

        self.create_button("不记得", self.forgotten_word).pack(side="right", padx=10)
        self.create_button("下一个", self.next_word).pack(side="left", padx=10)
        self.create_button("上一个", self.previous_word).pack(side="left", padx=10)
        self.create_button("爬", self.exclude_current_word).pack(side="left", padx=10)
        self.create_button("重来一遍", self.retry_word_list).pack(side="left", padx=10)
        self.create_button("切换单词表", self.switch_word_list).pack(side="left", padx=10)

    def create_button(self, text, command):
        return tk.Button(
            self.button_frame, text=text, width=10, command=command,
            font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=2
        )

    def generate_random_words(self):
        filtered_order = [i for i in self.word_test.order if i not in self.to_exclude]
        np.random.shuffle(filtered_order)
        self.word_test.history = filtered_order
        self.word_test.current_index = 0
        return iter(self.word_test.history)

    def retry_word_list(self):
        self.random_words = self.generate_random_words()
        self.show_word()

    def exclude_current_word(self):
        if self.word_test.current_index < len(self.word_test.history):
            current_index = self.word_test.history[self.word_test.current_index]
            self.to_exclude.add(current_index)
            del self.word_test.history[self.word_test.current_index]
            self.word_test.order = [i for i in self.word_test.order if i not in self.to_exclude]
            if self.word_test.current_index >= len(self.word_test.history) and self.word_test.history:
                self.word_test.current_index = len(self.word_test.history) - 1
            if self.word_test.history:
                self.show_word()
            else:
                messagebox.showinfo("Info", "All words have been excluded!")
                self.word_label.config(text="")

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

    def forgotten_word(self):
        current_index = self.word_test.history[self.word_test.current_index]
        row = self.word_test.data.iloc[current_index]
        self.meaning_label.config(text=f"{row[1]};     {row[2]};     {row[3]}")

    def previous_word(self):
        if self.word_test.current_index > 0:
            self.word_test.current_index -= 1
            self.show_word()
            self.start_pronounce_word()  # 自动朗读当前单词
        else:
            messagebox.showinfo("Info", "You are at the first word!")

    def next_word(self):
        if self.word_test.current_index < len(self.word_test.history) - 1:
            self.word_test.current_index += 1
            self.show_word()
            self.start_pronounce_word()  # 自动朗读当前单词
        else:
            messagebox.showinfo("Info", "You are at the last word!")

    def switch_word_list(self):
        def after_save():
            filename = filedialog.askopenfilename(title="选择单词表", filetypes=[("Excel Files", "*.xlsx")])
            if filename:
                self.word_test = WordTest(filename=filename)
                self.random_words = self.generate_random_words()
                self.show_word()

        if messagebox.askyesno("保存", "是否保存当前单词表为新文件？"):
            self.save_word_list(callback=after_save)
        else:
            after_save()

    def save_word_list(self, callback=None):
        range_window = tk.Toplevel(self)
        range_window.title("Select Save Range")

        min_index = 1
        max_index = len(self.word_test.history)

        tk.Label(range_window, text=f"Select range to save (Valid range: {min_index} to {max_index}):").pack(pady=10)

        input_frame = tk.Frame(range_window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Start Index:").grid(row=0, column=0)
        start_entry = tk.Entry(input_frame)
        start_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="End Index:").grid(row=1, column=0)
        end_entry = tk.Entry(input_frame)
        end_entry.grid(row=1, column=1)

        def confirm_selection():
            try:
                start = int(start_entry.get())
                end = int(end_entry.get())
                if min_index <= start <= end <= max_index:
                    range_window.destroy()
                    self.perform_save(start, end, callback=callback)
                else:
                    messagebox.showerror("Error", "Please enter valid start and end indices.")
            except ValueError:
                messagebox.showerror("Error", "Please enter numeric start and end indices.")

        tk.Button(range_window, text="Save", command=confirm_selection).pack(pady=10)

    def perform_save(self, start, end, callback=None):
        save_filename = filedialog.asksaveasfilename(defaultextension=".txt", title="保存单词表",
                                                     filetypes=[("Text Files", "*.txt")])
        if save_filename:
            with open(save_filename, 'w', encoding='utf-8') as f:
                for i in range(start - 1, end):
                    index = self.word_test.history[i]
                    if index not in self.to_exclude:
                        row = self.word_test.data.iloc[index]
                        f.write(f"{row[0]} {row[2]}\n")
            if callback:
                callback()

    def start_pronounce_word(self):
        threading.Thread(target=self.pronounce_word).start()

    def pronounce_word(self):
        current_index = self.word_test.history[self.word_test.current_index]
        kana = self.word_test.data.iloc[current_index, 0]
        kanji = self.word_test.data.iloc[current_index, 1]
        tts_input = f"{kanji}"  # 同时给语音和语境
        url = self.audio_player.get_audio_url(tts_input)
        if url:
            audio_file = self.audio_player.cache_audio(url, kanji)  # 缓存时仍用 kanji 命名
            if audio_file:
                self.audio_player.play_audio(audio_file)
        else:
            self.show_error("发音失败")

    def show_error(self, message):
        self.after(0, lambda: messagebox.showerror("Error", message))

    def on_closing(self):
        def after_close_save():
            self.destroy()
        if messagebox.askyesno("保存", "是否保存当前单词表为新文件？"):
            self.save_word_list(callback=after_close_save)
        else:
            self.destroy()
