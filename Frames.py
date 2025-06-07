from customtkinter import *
from tkinter import filedialog
import pyperclip

FILETYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg"), ("Images", "*.raw"), ("Images", "*.tif"),
             ("Images", "*.tiff"), ("Images", "*.bmp"), ("Images", "*.webp")]


class UrlFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = CTkLabel(master=self, text="URL", width=100, height=30, anchor="e",
                              text_color="#0080ff", fg_color="transparent", font=("Arial", 20), padx=30, pady=5)
        self.entry = CTkEntry(master=self, width=400, height=40, corner_radius=20, text_color="black",
                              fg_color="white", placeholder_text_color="black", font=("Arial", 15))
        self.button = CTkButton(master=self, width=135, height=30, corner_radius=20, text_color="black",
                                fg_color="white", font=("Arial", 15), text="Paste Url", command=self.paste_url)
        self.clear_button = CTkButton(master=self, width=30, height=30, text="✕", corner_radius=20,
                                      text_color="black", fg_color="#bf1515", font=("Arial", 15),
                                      command=self.clear_entry)
        self.status_label = CTkLabel(master=self, text="", width=1, height=20, anchor="w", text_color="white",
                                     fg_color="transparent", font=("Arial", 14))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0, padx=3)
        self.button.grid(row=1, column=1, padx=3)
        self.clear_button.grid(row=1, column=2, padx=3)
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 0))

    def paste_url(self):
        url = pyperclip.paste()
        if isinstance(url, str):
            self.entry.delete(0, END)
            self.entry.insert(0, url)

    def clear_entry(self):
        self.entry.delete(0, 'end')

    def show_label(self, text):
        self.status_label.configure(text=text)

    def hide_label(self):
        self.status_label.configure(text="")


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
        self.clear_button = CTkButton(master=self, width=30, height=30, text="✕", corner_radius=20,
                                      text_color="black", fg_color="#bf1515", font=("Arial", 15),
                                      command=self.clear_entry)
        self.status_label = CTkLabel(master=self, text="", width=1, height=20, anchor="w", text_color="white",
                                     fg_color="transparent", font=("Arial", 14))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0, padx=3)
        self.button.grid(row=1, column=1, padx=3)
        self.clear_button.grid(row=1, column=2, padx=3)
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 0))

    def select_file(self):
        # self.entry.delete(0, END)
        file = filedialog.askopenfilename(title="Select File",
                                          parent=self,
                                          filetypes=FILETYPES)
        if file:
            self.entry.delete(0, END)
            self.entry.insert(0, file)

    def clear_entry(self):
        self.entry.delete(0, 'end')

    def show_label(self, text):
        self.status_label.configure(text=text)

    def hide_label(self):
        self.status_label.configure(text="")


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
        self.clear_button = CTkButton(master=self, width=30, height=30, text="✕", corner_radius=20,
                                      text_color="black", fg_color="#bf1515", font=("Arial", 15),
                                      command=self.clear_entry)
        self.status_label = CTkLabel(master=self, text="", width=1, height=20, anchor="w", text_color="white",
                                     fg_color="transparent", font=("Arial", 14))

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0, padx=3)
        self.button.grid(row=1, column=1, padx=3)
        self.clear_button.grid(row=1, column=2, padx=3)
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 0))

    def select_folder(self):
        # self.entry.delete(0, END)
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.entry.delete(0, END)
            self.entry.insert(0, folder)

    def clear_entry(self):
        self.entry.delete(0, 'end')

    def show_label(self, text):
        self.status_label.configure(text=text)

    def hide_label(self):
        self.status_label.configure(text="")


class ResultsFrame(CTkScrollableFrame):
    row_number = 1

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = CTkLabel(master=self, text="Results", width=400, height=30, anchor="center",
                              fg_color="transparent", font=("Arial", 20), padx=30, pady=5)

        self.label.grid(row=0, column=0)

    def add_entry(self, processing_type):
        text_var = StringVar(master=self)
        text_var.set(processing_type)
        entry = CTkEntry(master=self, width=300, fg_color="transparent", textvariable=text_var, font=("Arial", 15))
        entry.grid(column=0, row=self.row_number, sticky="w")
        self.row_number += 1

    def add_result_positive(self, name, detector):
        textbox = CTkTextbox(master=self, width=475, height=52, font=("Arial", 15), wrap="word")
        textbox.configure(yscrollcommand=None)

        textbox.insert("end", f"{name}\n")
        textbox.insert("end", "Correct", "correct_tag")
        textbox.insert("end", f" - {detector}")

        textbox.tag_config("correct_tag", foreground="#35c211")
        textbox.configure(state="disabled")
        textbox.grid(column=0, row=self.row_number, sticky="w")
        self.row_number += 1

    def add_result_negative(self, name, detector, reason):
        textbox = CTkTextbox(master=self, width=475, height=70, font=("Arial", 15), wrap="word")
        textbox.configure(yscrollcommand=None)

        textbox.insert("end", f"{name}\n")
        textbox.insert("end", "Incorrect", "incorrect_tag")
        textbox.insert("end", f" - {detector}\n{reason}")

        textbox.tag_config("incorrect_tag", foreground="red")
        textbox.configure(state="disabled")
        textbox.grid(column=0, row=self.row_number, sticky="w")
        self.row_number += 1

    def delete_entries(self):
        for widget in self.winfo_children():
            if isinstance(widget, CTkEntry) or isinstance(widget, CTkTextbox):
                widget.destroy()

        self._parent_canvas.yview_moveto(0)
        self.update_idletasks()


class DetectorSettingsFrame(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.detector_label = CTkLabel(master=self, width=100, height=30, corner_radius=20, text_color="lightgrey",
                                       font=("Arial", 15), text="Select Detector:")
        self.detector_option = CTkOptionMenu(master=self, width=125, height=30, corner_radius=20, text_color="black",
                                             font=("Arial", 15), values=["ssd", "retinaface"])
        self.detector_option.set("ssd")
        self.nose_position_label = CTkLabel(master=self, width=100, height=30, corner_radius=20, text_color="white",
                                            font=("Arial", 15), text="Nose position offset (0-1)")
        self.symmetry_label = CTkLabel(master=self, width=100, height=30, corner_radius=20, text_color="white",
                                       font=("Arial", 15), text="Symmetry (0-1)")
        self.ear_height_diff_label = CTkLabel(master=self, width=100, height=30, corner_radius=20, text_color="white",
                                              font=("Arial", 15), text="Ear Height Difference (0-1)")
        self.nose_position_entry = CTkEntry(master=self, width=50, height=20, corner_radius=20, text_color="black",
                                            fg_color="white", placeholder_text_color="black", font=("Arial", 15))
        self.symmetry_entry = CTkEntry(master=self, width=50, height=20, corner_radius=20, text_color="black",
                                       fg_color="white", placeholder_text_color="black", font=("Arial", 15))
        self.ear_height_diff_entry = CTkEntry(master=self, width=50, height=20, corner_radius=20, text_color="black",
                                              fg_color="white", placeholder_text_color="black", font=("Arial", 15))

        self.default_button = CTkButton(master=self, width=125, height=30, corner_radius=20, text_color="black",
                                        text="Restore Default", font=("Arial", 15), command=self.restore_default)

        self.nose_position_entry.insert(0, "0.05")
        self.symmetry_entry.insert(0, "0.1")
        self.ear_height_diff_entry.insert(0, "0.03")

        self.detector_label.grid(row=0, column=0, pady=(20, 30))
        self.detector_option.grid(row=0, column=1, pady=(20, 30))
        self.nose_position_label.grid(row=1, column=0, pady=(5, 5))
        self.nose_position_entry.grid(row=1, column=1, pady=(5, 5))
        self.symmetry_label.grid(row=2, column=0, pady=(5, 5))
        self.symmetry_entry.grid(row=2, column=1, pady=(5, 5))
        self.ear_height_diff_label.grid(row=3, column=0, pady=(5, 5))
        self.ear_height_diff_entry.grid(row=3, column=1, pady=(5, 5))
        self.default_button.grid(row=4, column=0, columnspan=2, pady=(20 , 5))

    def get_selected_detector(self):
        return self.detector_option.get()

    def get_options(self):
        nose_position = self.nose_position_entry.get()
        symmetry = self.symmetry_entry.get()
        ear_high_diff = self.ear_height_diff_entry.get()
        return [nose_position, symmetry, ear_high_diff]

    def restore_default(self):
        self.nose_position_entry.delete(0, END)
        self.symmetry_entry.delete(0, END)
        self.ear_height_diff_entry.delete(0, END)
        self.nose_position_entry.insert(0, "0.05")
        self.symmetry_entry.insert(0, "0.1")
        self.ear_height_diff_entry.insert(0, "0.03")
