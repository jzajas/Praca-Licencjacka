from customtkinter import *
from Services import *

class UrlFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="URL", width=100, height=30, anchor="e",
                              text_color="#0080ff", fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text="URL", placeholder_text_color="black", font=("Arial",15))

        self.label.grid(row=0,column=0)
        self.entry.grid(row=1, column=0)


class FileFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="File", width=100, height=30, anchor="e", text_color="#0080ff",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text="File Path", placeholder_text_color="black", font=("Arial",15))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)


class FolderFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="Folder", width=100, height=30, anchor="e", text_color="#0080ff",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text="Folder Path", placeholder_text_color="black", font=("Arial",15))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)


# TODO to delete
class TestFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="Folder", width=100, height=30, anchor="e",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20,
                              placeholder_text="Folder Path", font=("Arial",15))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)


class MiddleFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    #     TODO add progress bar?

        self.button = CTkButton(command=process_input)



