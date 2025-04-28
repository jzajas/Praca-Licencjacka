from customtkinter import *
from tkinter import filedialog
import pyperclip

FILETYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg"), ("Images", "*.raw"), ("Images", "*.tif"),
             ("Images", "*.tiff"), ("Images", "*.bmp"), ("Images", "*.webp"), ("Images", "*.avif")]


class UrlFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="URL", width=100, height=30, anchor="e",
                              text_color="#0080ff", fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text_color="black",
                              font=("Arial", 15))
        self.button = CTkButton(master=self, width=135, height=30, corner_radius=20, text_color="black",
                                fg_color="white", font=("Arial", 15), text="Paste Url", command=self.paste_url)

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0, padx=3)
        self.button.grid(row=1, column=1,  padx=3)

    def paste_url(self):
        url = pyperclip.paste()
        if isinstance(url, str):
            self.entry.delete(0, END)
            self.entry.insert(0, url)


class FileFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="File Path", width=100, height=30, anchor="e", text_color="#0080ff",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text_color="black",
                              font=("Arial", 15))
        self.button = CTkButton(master=self, width=135, height=30, corner_radius=20, text_color="black",
                                fg_color="white", font=("Arial", 15), text="Browse Files", command=self.select_file)

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0, padx=3)
        self.button.grid(row=1, column=1,  padx=3)

    def select_file(self):
        self.entry.delete(0, END)
        file = filedialog.askopenfilename(title="Select File",
                                                parent=self,
                                                filetypes=FILETYPES)
        if file:
            self.entry.delete(0, END)
            self.entry.insert(0, file)


class FolderFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="Folder Path", width=100, height=30, anchor="e", text_color="#0080ff",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text_color="black",
                              font=("Arial", 15))
        self.button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                fg_color="white", font=("Arial", 15), text="Browse Folders", command=self.select_folder)

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0,  padx=3)
        self.button.grid(row=1, column=1, padx=3)

    def select_folder(self):
        self.entry.delete(0, END)
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.entry.delete(0, END)
            self.entry.insert(0, folder)


class ResultsFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="Results", width=200, height=30, anchor="center",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.correct_frame = ResultsDisplayingFrame(master=self, text="Correct", height=400, width=230)
        self.incorrect_frame = ResultsDisplayingFrame(master=self, text="Incorrect", height=400, width=230)

        self.correct_frame.grid(row=0, column=0, rowspan=10, padx=20, pady=30, sticky="nsew")
        self.incorrect_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=30, sticky="nsew")
        self.label.grid(row=0, column=0)


class ResultsDisplayingFrame(CTkScrollableFrame):
    row_number = 1

    def __init__(self, master, text, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text=text, width=200, height=30, anchor="center",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)

        self.label.grid(row=0, column=0)

    def add_result(self, entry_text, error=None):
        text_var = StringVar(master=self)
        text_var.set(entry_text)
        entry = CTkEntry(master=self, width=200, fg_color="transparent", textvariable=text_var, font=("Arial", 15))
        entry.grid(column=0, row=self.row_number, sticky="w")
        self.row_number += 1

        if error is not None:
            entry_tool_tip = CreateToolTip(entry, error)

    def delete_entries(self):
        for widget in self.winfo_children():
            if isinstance(widget, CTkEntry):
                widget.destroy()


# TODO spytać promotora czy kod z StackOverflow może być
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.wait_time = 500
        self.wrap_length = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = CTkToplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = CTkLabel(self.tw, text=self.text, justify='left', wraplength=self.wrap_length)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
