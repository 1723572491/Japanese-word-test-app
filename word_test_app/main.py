from ttkbootstrap import Window
from ttkbootstrap.widgets import Button
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from core.word_test import WordTest
from ui.main_window import WordTestGUI

def open_word_test():
    filename = filedialog.askopenfilename(
        title="选择单词表",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if filename:
        initial_window.withdraw()
        test = WordTest(filename=filename)
        app = WordTestGUI(initial_window, test)  # ❗传入 initial_window 作为 master
        app.mainloop()
    else:
        Messagebox.show_info("请先选择一个文件")

if __name__ == "__main__":
    # 初始化主窗口
    initial_window = Window(themename="flatly")  # 可换成 minty/superhero 等
    initial_window.title("选择单词表")
    initial_window.geometry("400x200")
    initial_window.resizable(False, False)

    # 创建圆角按钮
    start_button = Button(
        initial_window,
        text="选择单词表",
        width=25,
        padding=10,
        command=open_word_test
    )
    start_button.pack(pady=60)

    initial_window.mainloop()
