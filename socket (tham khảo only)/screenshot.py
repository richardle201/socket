import tkinter as tk
from io import BytesIO
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from utils import receive_data


class Screenshot:
    def __init__(self, client):
        self.ss_window = tk.Tk()
        # setting window size
        self.ss_window.title = 'Screenshot'
        width = 670
        height = 500
        screenwidth = self.ss_window.winfo_screenwidth()
        screenheight = self.ss_window.winfo_screenheight()
        align_str = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.ss_window.geometry(align_str)

        canvas_w, canvas_h = (width - 140, height)
        self.canvas = tk.Canvas(self.ss_window, width=canvas_w, height=canvas_h)
        self.canvas.pack(side='left')

        self.image = Screenshot.receive_screenshot_image(client)
        new_w, new_h = Screenshot.resize_image(self.image, canvas_w, canvas_h)
        image_mod = self.image.resize((new_w, new_h), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(master=self.ss_window, image=image_mod)
        self.image_canvas = self.canvas.create_image(0, 0, anchor='nw', image=image_tk)
        self.canvas.itemconfig(self.image_canvas, image=image_tk)

        button_ss = tk.Button(master=self.ss_window, text='Screenshot', command=lambda: self.screenshot(client))
        button_ss.place(x=width - 120, y=100, width=100, height=100)

        button_s = tk.Button(master=self.ss_window, text='Save', command=self.save)
        button_s.place(x=width - 120, y=220, width=100, height=50)
        self.ss_window.mainloop()

    @staticmethod
    def resize_image(image, new_w, new_h):
        rat = image.width / image.height
        if image.width > image.height:
            new_h = new_w / rat
        else:
            new_w = rat * new_h
        return int(new_w), int(new_h)

    @staticmethod
    def receive_screenshot_image(client):
        client.send_command('screenshot')
        image_bytes = receive_data(client, 65356)
        stream = BytesIO(image_bytes)
        image = Image.open(stream).convert('RGB')
        return image

    def save(self):
        files = [
            ('PNG Files', '*.png'),
            ('JPG Files', '*.jpg'),
            ('JPEG Files', '*.jpeg'),
            ('Bitmap Files', '*.bmp'),
        ]
        file = asksaveasfilename(filetypes=files, defaultextension=files)
        if file:
            self.image.save(file)

    def screenshot(self, client):
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.image = Screenshot.receive_screenshot_image(client)
        new_w, new_h = Screenshot.resize_image(self.image, canvas_w, canvas_h)
        image_mod = self.image.resize((new_w, new_h), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(master=self.ss_window, image=image_mod)
        self.canvas.itemconfig(self.image_canvas, image=image_tk)
        self.ss_window.mainloop()
