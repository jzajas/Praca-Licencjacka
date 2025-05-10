from tkinter import messagebox
from Frames import *
from InputProcessing import *
from pathlib import Path


EXTENSIONS = ["png", "jpg", "jpeg", "raw", "tif", "tiff", "bmp", "webp"]
set_appearance_mode("system")
set_default_color_theme("green")
INCORRECT_FILE_EXTENSION_MESSAGE = "Incorrect file extension"
TYPE_ERROR_MESSAGE = "Unable to detect facial landmarks"


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x550")
        self.title("Face detection app ")
        self.grid_rowconfigure(0, weight=0, minsize=135)
        self.grid_columnconfigure(0, weight=0, minsize=450)

        self.url_frame = UrlFrame(master=self)
        self.file_frame = FileFrame(master=self)
        self.folder_frame = FolderFrame(master=self)
        self.results_frame = ResultsFrame(master=self, width=500)
        self.settings_frame = DetectorSettingsFrame(master=self, fg_color="transparent")

        self.switch_var = StringVar(value="on")
        self.process_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                        font=("Arial", 15), text="Process input", command=self.process_input)
        self.clear_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                      font=("Arial", 15), text="Clear all results", command=self.clear_inputs)

        self.url_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.file_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.folder_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.settings_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.results_frame.grid(row=0, column=3, rowspan=4, padx=20, pady=30, sticky="nsew")

        self.process_button.grid(row=2, column=2, padx=20, pady=30, sticky="nsew")
        self.clear_button.grid(row=3, column=2, padx=0, pady=0)

    def process_input(self):
        url_path = self.url_frame.entry.get().strip()
        file_path = self.file_frame.entry.get().strip()
        folder_path = self.folder_frame.entry.get().strip()
        detector = self.settings_frame.get_selected_detector()
        self.show_status(url_path, file_path, folder_path)
        try:
            if url_path != "" and file_path == "" and folder_path == "":
                path = url_path
                face_quality = process_url(path, detector)
                self.determine_results(path, face_quality)
            elif url_path == "" and file_path != "" and folder_path == "":
                path = file_path
                face_quality = process_file(path, detector)
                self.determine_results(path, face_quality)
            elif url_path == "" and file_path == "" and folder_path != "":
                main_path = folder_path
                files = os.listdir(main_path)
                all_files = files
                print(all_files)
                for file in all_files:
                    print("Processing: " + file)
                    path = main_path + '/' + file
                    file_extension = file.split(".")[-1]
                    if file_extension in EXTENSIONS:
                        try:
                            print(file_extension)
                            face_quality = process_file(path, detector)
                            self.determine_results(path, face_quality)
                        except ValueError as e:
                            self.results_frame.incorrect_frame.add_result(self.extract_name(path), e)
                        except TypeError as e:
                            self.results_frame.incorrect_frame.add_result(self.extract_name(path), TYPE_ERROR_MESSAGE)
                    else:
                        self.results_frame.incorrect_frame.add_result(self.extract_name(path), INCORRECT_FILE_EXTENSION_MESSAGE)

            elif url_path == "" and file_path == "" and folder_path == "":
                messagebox.showinfo(title="No sources provided", message="One source must be provided")

            else:
                messagebox.showinfo(title="Too many sources provided", message="Please provide only one source")

        except ConnectionError as e:
            self.results_frame.incorrect_frame.add_result(path, e)
        except ValueError as e:
            self.results_frame.incorrect_frame.add_result(self.extract_name(path), e)
        except TypeError as e:
            self.results_frame.incorrect_frame.add_result(self.extract_name(path), TYPE_ERROR_MESSAGE)

        finally:
            self.hide_status()

    def determine_results(self, path, quality):
        if quality:
            self.results_frame.correct_frame.add_result(self.extract_name(path))
        else:
            self.results_frame.incorrect_frame.add_result(self.extract_name(path), "Low Quality")

    def clear_inputs(self):
        self.results_frame.incorrect_frame.delete_entries()
        self.results_frame.correct_frame.delete_entries()
        self.hide_status()

    def extract_name(self, path):
        return Path(path).name

    def show_status(self, url_path, file_path, folder_path):
        if url_path != "":
            self.url_frame.show_label("Processing: ")
        elif file_path != "":
            self.file_frame.show_label("Processing: " + file_path)
        elif folder_path != "":
            self.folder_frame.show_label("Processing: " + folder_path)
        self.update()

    def hide_status(self):
        self.url_frame.hide_label()
        self.file_frame.hide_label()
        self.folder_frame.hide_label()

# TODO might be useful
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = Application(root)
#     app.mainloop()


app = App()
app.mainloop()
