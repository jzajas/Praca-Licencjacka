from customtkinter import *
from Services import *
from tkinter import filedialog
import pyperclip


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
        self.entry.insert(0, "Folder Path")
        file = filedialog.askopenfile(title="Select File",
                                      filetypes=[("Images", "*.png"), ("Images", "*.jpg")])
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
        self.entry.insert(0, "Folder Path")
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.entry.delete(0, END)
            self.entry.insert(0, folder)


# TODO to delete
# class TestFrame(CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#
#         self.label = CTkLabel(master=self, text="Folder", width=100, height=30, anchor="e",
#                               fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
#         self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20,
#                               placeholder_text="Folder Path", font=("Arial", 15))
#
#         self.label.grid(row=0, column=0)
#         self.entry.grid(row=1, column=0)


# class MiddleFrame(CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#         # TODO add progress bar?
#
#         self.button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
#                                 font=("Arial", 15), text="Process input")
#         self.button.grid(row=3, column=0)

