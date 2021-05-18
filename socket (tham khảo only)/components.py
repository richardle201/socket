import tkinter as tk
import tkinter.font as tkFont


class Text:
    def __init__(self, root, text, has_scroll_bar=False):
        self.text = tk.Text(root)
        self.text["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.text["font"] = ft
        self.text["fg"] = "#000000"
        self.text.bind("<Button-1>", lambda event: self.delete_default())
        self.text.bind("<FocusIn>", lambda event: self.delete_default())
        self.text.bind("<FocusOut>", lambda event: self.add_default())
        self.text.insert(1.0, text)
        if has_scroll_bar:
            scroll_bar = tk.Scrollbar(self.text)
            scroll_bar.config(command=self.text.yview)
            self.text.config(yscrollcommand=scroll_bar.set)
        self.default_text = text
        self.initial = True

    def delete_default(self):
        if self.initial:
            self.initial = False
            self.text.delete(1.0, tk.END)

    def add_default(self):
        if not self.initial and self.get(1.0, tk.END) == '\n':
            self.initial = True
            self.text.insert(1.0, self.default_text)

    def place(self, x, y, w, h):
        return self.text.place(x=x, y=y, w=w, h=h)

    def get(self, beg, end):
        return self.text.get(beg, end)

    def insert(self, index, text):
        return self.text.insert(index, text)

    def clear(self):
        return self.text.delete(1.0, tk.END)


class Entry:
    def __init__(self, root, text, *args, **kwargs):
        self.text = tk.Entry(root, *args, **kwargs)
        self.text.bind("<Button-1>", lambda event: self.delete_default())
        self.text.bind("<FocusIn>", lambda event: self.delete_default())
        self.text.bind("<FocusOut>", lambda event: self.add_default())
        self.text.insert(0, text)

        self.default_text = text
        self.initial = True

    def focus_set(self):
        self.text.focus_set()

    def delete_default(self):
        if self.initial:
            self.initial = False
            self.text.delete(0, tk.END)

    def add_default(self):
        if not self.initial and len(self.get()) == 0:
            self.initial = True
            self.text.insert(0, self.default_text)

    def clear(self):
        return self.text.delete(0, tk.END)

    def insert(self, index, text):
        return self.text.insert(index, text)

    def place(self, x, y, width, height):
        return self.text.place(x=x, y=y, w=width, h=height)

    def get(self):
        return self.text.get()
