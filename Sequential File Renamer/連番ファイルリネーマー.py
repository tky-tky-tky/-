import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("連番リネーム")

        # テキストボックス
        self.entry = tk.Entry(root, justify='center', font=("Arial", 16))
        self.entry.insert(0, "001")
        self.entry.pack(pady=10)

        # 操作ボタンをフレームでまとめる
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        # ◀ ボタン（左に0を追加）
        tk.Button(button_frame, text="◀", command=self.add_leading_zero).grid(row=0, column=0, padx=5)

        # ▶ ボタン（左の桁を削除）
        tk.Button(button_frame, text="▶", command=self.remove_leading_digit).grid(row=0, column=1, padx=5)

        # ▲ ボタン（+1）
        tk.Button(button_frame, text="▲", command=self.increment_number).grid(row=0, column=2, padx=5)

        # ▼ ボタン（-1）
        tk.Button(button_frame, text="▼", command=self.decrement_number).grid(row=0, column=3, padx=5)

        # リセットボタン
        tk.Button(button_frame, text="Reset", command=self.reset_number).grid(row=0, column=4, padx=5)

        # 画像をドラッグアンドドロップできる領域
        self.drop_label = tk.Label(root, text="Drop image here", bg="lightgray", height=5, width=30)
        self.drop_label.pack(pady=10)

        # ドロップイベントの設定
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)

    # ◀: 先頭に0を追加
    def add_leading_zero(self):
        text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "0" + text)

    # ▶: 左の桁を削除（1桁は残す）
    def remove_leading_digit(self):
        text = self.entry.get()
        if len(text) > 1:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text[1:])

    # ▲: +1
    def increment_number(self):
        text = self.entry.get()
        width = len(text)
        try:
            num = int(text)
            num += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{num:0{width}d}")
        except ValueError:
            pass

    # ▼: -1（0未満にはしない）
    def decrement_number(self):
        text = self.entry.get()
        width = len(text)
        try:
            num = int(text)
            if num > 0:
                num -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"{num:0{width}d}")
        except ValueError:
            pass

    # Reset: 001に戻す
    def reset_number(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "001")

    def on_drop(self, event):
        file_path_with_braces = event.data
        file_path = file_path_with_braces[1:-1]
        file_paths = file_path.split("} {")
        print("File dropped:", file_paths)

        #行数とカウントを保存
        current_number_str = self.entry.get()
        width = len(current_number_str)
        current_number = int(current_number_str)

        for file_path in file_paths:
            if os.path.isfile(file_path):
                # ファイルをリネーム
                new_name = f"{current_number:0{width}d}{os.path.splitext(file_path)[1]}"
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                print("ファイルが次の名前に変更されました:", new_path)

                # テキストボックスの数字を1進める
                current_number += 1

        # カウンターの新しい値でエントリを更新
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{current_number:0{width}d}")

if __name__ == "__main__":
    # アプリの起動
    root = TkinterDnD.Tk()
    app = SimpleApp(root)
    root.mainloop()
