import tkinter as tk
from tkinter import messagebox as mbox
from PIL import Image, ImageTk
import shutil
import os
import glob

from generate import generate_text

def app ():

    win = tk.Tk()
    win.geometry("500x250") # サイズを指定

    # 部品を作成 --- (*2)
    # ラベルを作成
    label = tk.Label(win, text='Enter the seed texts')
    label.pack()

    # テキストボックスを作成
    text = tk.Entry(win)
    text.pack()
    text.insert(tk.END, 'Enter the seed texts') # 初期値を指定

    # テキストボックスを作成
    #text_1 = tk.Entry(win)
    #text_1.pack()
    #text_1.insert(tk.END, 'Enter the num of sentence') # 初期値を指定

    # OKボタンを押した時 --- (*3)
    def ok_click():
        # テキストボックスの内容を得る
        seed_text = text.get()
        num_of_sentence = 100

        x = 80
        y = 100
        max_sequence_len = 1082

        gen_text = generate_text(seed_text, int(num_of_sentence), max_sequence_len)

        background = "#d8d6d5"
        static1 = tk.Label(text=gen_text, foreground='#02010c', background=background)
        static1.place(x=x, y=y)

    # ボタンを作成 --- (*4)
    okButton = tk.Button(win, text='OK', command=ok_click)
    okButton.pack()

    # ウィンドウを動かす
    win.mainloop()

if __name__ == '__main__':
    app()
