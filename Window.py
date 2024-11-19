# TODO ProgressBarr dobry do pokazywania ile czasu jeszcze przy opcji Folder do przetwarzania
# TODO przetwarzanie File i Folder inputów
# TODO Ustawienia co do przetwarzania twarzy
# TODO minmaxowanie ustawień co do wykrywania twarzy

from customtkinter import *
from tkinter import messagebox
from Frames import *
from InputProcessing import *

set_appearance_mode("system")
set_default_color_theme("green")


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x500")
        # TODO Change name
        self.title("Face quality checking app ")
        self.grid_rowconfigure(0, weight=0, minsize=135)
        self.grid_columnconfigure(0, weight=0, minsize=450)

        self.url_frame = UrlFrame(master=self)
        self.file_frame = FileFrame(master=self)
        self.folder_frame = FolderFrame(master=self)
        self.results_frame = ResultsFrame(master=self, width=500)

        self.switch_var = StringVar(value="on")
        self.mode_switch = CTkSwitch(self, text="Dark / Light Mode Switch", command=self.change_appearance,
                                     variable=self.switch_var, onvalue="light", offvalue="dark")

        self.process_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                        font=("Arial", 15), text="Process input", command=self.process_input)
        self.clear_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                      font=("Arial", 15), text="Clear all entries", command=self.clear_inputs)

        self.url_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.file_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.folder_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.results_frame.grid(row=0, column=3, rowspan=4, padx=20, pady=30, sticky="nsew")

        self.mode_switch.grid(row=3, column=0, padx=20, pady=30, sticky="nsew")
        self.process_button.grid(row=2, column=2, padx=20, pady=30, sticky="nsew")
        self.clear_button.grid(row=3, column=2, padx=0, pady=0)

    def change_appearance(self):
        mode = self.switch_var.get()
        if mode == "dark":
            set_appearance_mode("dark")

        elif mode == "light":
            set_appearance_mode("light")

    def clear_inputs(self):
        self.url_frame.entry.delete(0, END)
        self.file_frame.entry.delete(0, END)
        self.folder_frame.entry.delete(0, END)
        self.results_frame.incorrect_frame.delete_entries()
        self.results_frame.correct_frame.delete_entries()

    def process_input(self):
        url_path = self.url_frame.entry.get().strip()
        file_path = self.file_frame.entry.get().strip()
        folder_path = self.folder_frame.entry.get().strip()

        try:
            if url_path != "" and file_path == "" and folder_path == "":
                path = url_path
                face_quality = process_url(path)
            elif url_path == "" and file_path != "" and folder_path == "":
                path = file_path
                face_quality = process_file(path)
            elif url_path == "" and file_path == "" and folder_path != "":
                path = folder_path
                # TODO change file processing
                # face_quality = process_url(path)
            elif url_path == "" and file_path == "" and folder_path == "":
                messagebox.showinfo(title="No sources provided", message="One source must be provided")

            else:
                messagebox.showinfo(title="Too many sources provided", message="Please provide only one source")

            self.results_frame.correct_frame.add_result(path)

        except ConnectionError as e:
            self.results_frame.incorrect_frame.add_result(path, e)

        except ValueError as e:
            self.results_frame.incorrect_frame.add_result(path, e)

        except TypeError as e:
            self.results_frame.incorrect_frame.add_result(path, "Incorrect face position")


# TODO might be useful
    # if __name__ == '__main__':
    #     root = tk.Tk()
    #     app = Application(root)
    #     app.mainloop()


app = App()
app.mainloop()
