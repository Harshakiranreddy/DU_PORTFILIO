"""
Author: Harsha Kiran Reddy
Date: June 3 2023
"""
from tkinter import *
from tkinter import ttk, filedialog


class FileSelectionWindow:
    def __init__(self, file_type, dialogue):
        self.win = None
        self.file_type = file_type
        self.filename = ''
        self.dialogue = dialogue

    def select_file(self):
        # Create an instance of tkinter frame
        self.win = Tk()
        # Set the geometry of tkinter frame
        self.win.geometry("700x350")
        # Add a Label widget
        label = Label(self.win, text=self.dialogue, font='Georgia 13')
        label.pack(pady=10)
        # Create a Button
        ttk.Button(self.win, text="Browse", command=self.open_file).pack(pady=20)
        self.win.mainloop()
        return self.filename

    def open_file(self):
        self.filename = filedialog.askopenfilename(title='Open a file',
                                                   initialdir='.', filetypes=[(self.file_type, '*.' + self.file_type)])
        self.close()

    def close(self):
        self.win.destroy()
