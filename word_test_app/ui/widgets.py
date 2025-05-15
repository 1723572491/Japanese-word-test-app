import tkinter as tk

def create_button(parent, text, command):
    return tk.Button(
        parent, text=text, width=10, command=command,
        font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white",
        activebackground="#45a049", relief="raised", bd=2
    )