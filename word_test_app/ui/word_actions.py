import tkinter as tk
from tkinter import filedialog, messagebox
from word_test_app.core.word_test import WordTest

class WordActions:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.create_action_buttons()

    def create_action_buttons(self):
        self.create_button("显示词义", self.forgotten_word).pack(side="right", padx=10)
        self.create_button("切换词表", self.switch_word_list).pack(side="left", padx=10)
        self.create_button("打乱已看过", self.review_seen_words).pack(side="left", padx=10)
        self.create_button("跳转单词", self.jump_to_word).pack(side="left", padx=10)

    def create_button(self, text, command):
        return tk.Button(
            self.parent, text=text, width=10, command=command,
            font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white",
            activebackground="#45a049", relief="raised", bd=2
        )

    def forgotten_word(self):
        current_index = self.main_window.word_test.history[self.main_window.word_test.current_index]
        row = self.main_window.word_test.data.iloc[current_index]
        self.main_window.meaning_label.config(
            text=f"{row[1]};            {row[2]};            {row[3]}"
        )

    def switch_word_list(self):
        def after_save():
            filename = filedialog.askopenfilename(title="选择单词表", filetypes=[("Excel Files", "*.xlsx")])
            if filename:
                self.main_window.word_test = WordTest(filename=filename)
                self.main_window.random_words = self.main_window.generate_random_words()
                self.main_window.show_word()

        if messagebox.askyesno("保存", "是否保存当前单词表为新文件？"):
            self.save_word_list(callback=after_save)
        else:
            after_save()

    def save_word_list(self, callback=None):
        range_window = tk.Toplevel(self.main_window)
        range_window.title("Select Save Range")

        min_index = 1
        max_index = len(self.main_window.word_test.history)

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
                    messagebox.showerror("Error", "请输入有效的起始和结束索引。")
            except ValueError:
                messagebox.showerror("Error", "请输入数字索引。")

        tk.Button(range_window, text="Save", command=confirm_selection).pack(pady=10)

    def perform_save(self, start, end, callback=None):
        save_filename = filedialog.asksaveasfilename(defaultextension=".txt", title="保存单词表",
                                                     filetypes=[("Text Files", "*.txt")])
        if save_filename:
            with open(save_filename, 'w', encoding='utf-8') as f:
                for i in range(start - 1, end):
                    index = self.main_window.word_test.history[i]
                    if index not in self.main_window.to_exclude:
                        row = self.main_window.word_test.data.iloc[index]
                        f.write(f"{row[0]} {row[2]}\n")
            if callback:
                callback()

    # ✅ 新增功能：打乱当前已看过单词
    def review_seen_words(self):
        self.main_window.generate_review_shuffle()

    # ✅ 新增功能：跳转到指定单词编号
    def jump_to_word(self):
        jump_window = tk.Toplevel(self.main_window)
        jump_window.title("跳转到单词")

        tk.Label(jump_window, text="请输入要跳转的单词编号：").pack(pady=10)
        entry = tk.Entry(jump_window)
        entry.pack(pady=5)

        def confirm_jump():
            try:
                target = int(entry.get())
                if 1 <= target <= len(self.main_window.word_test.history):
                    self.main_window.word_test.current_index = target - 1
                    self.main_window.show_word()
                    self.main_window.pronunciation.start_pronounce_word()
                    jump_window.destroy()
                else:
                    messagebox.showerror("错误", "输入的编号超出范围。")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字编号。")

        tk.Button(jump_window, text="跳转", command=confirm_jump).pack(pady=10)
