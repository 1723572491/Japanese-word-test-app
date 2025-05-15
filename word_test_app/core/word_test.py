
import pandas as pd
import numpy as np
from tkinter import messagebox

class WordTest:
    def __init__(self, filename=None, start=0, end='last', mode='random', myorder=None):
        self.data = pd.DataFrame()
        self.myorder = None
        self.order = []
        self.current_index = 0
        self.history = []

        self.start = start
        self.end = end
        self.myorder = myorder

        if filename:
            self.load_new_data(filename)

    def load_new_data(self, filename):
        df = pd.DataFrame()
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(filename, header=0)
                if df.shape[1] < 4:
                    raise ValueError("Excel 文件列数不足，至少应包含4列（假名、日文、意思、类型）")
            else:
                raise ValueError("仅支持 .xlsx 文件")

            df = df.iloc[:, :4]
            df.dropna(how='all', inplace=True)

            for col in df.columns[:4]:
                df = df[df[col].astype(str).str.strip() != ""]
                df = df[df[col].notna()]

            df.reset_index(drop=True, inplace=True)

            if df.empty:
                raise ValueError("过滤后没有可用的单词。请检查 Excel 文件内容是否完整。")

            self.data = df
            self.reset_indices()

        except Exception as e:
            print(f"读取文件出错: {e}")
            messagebox.showerror("错误", f"读取文件失败：{e}")
            self.data = df

    def reset_indices(self):
        self.myorder = np.arange(len(self.data))
        if len(self.data) > 0:
            np.random.shuffle(self.myorder)
        self.start = 0
        self.end = len(self.data)
        self.order = self.myorder[self.start:self.end]
        self.current_index = 0
        self.history = [self.order[0]] if len(self.order) > 0 else []
