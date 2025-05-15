
import tkinter as tk
from tkinter import filedialog
from core.word_test import WordTest
from ui.main_window import WordTestGUI

def open_word_test():
    filename = filedialog.askopenfilename(title="选择单词表", filetypes=[("Excel Files", "*.xlsx")])
    if filename:
        initial_window.destroy()
        test = WordTest(filename=filename)
        app = WordTestGUI(test)
        app.mainloop()

if __name__ == "__main__":
    initial_window = tk.Tk()
    initial_window.title("选择单词表")
    initial_window.geometry("400x200")

    start_button = tk.Button(initial_window, text="选择单词表", command=open_word_test, width=30)
    start_button.pack(pady=50)

    initial_window.mainloop()
