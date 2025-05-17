import threading
from tkinter import messagebox
from Frames import *
from InputProcessing import *
from pathlib import Path


EXTENSIONS = ["png", "jpg", "jpeg", "raw", "tif", "tiff", "bmp", "webp"]
set_appearance_mode("system")
set_default_color_theme("green")

PROCESSING_URL_MESSAGE = "Url results:"
PROCESSING_FILE_MESSAGE = "File results:"
INCORRECT_FILE_EXTENSION_MESSAGE = "Incorrect file extension"
TYPE_ERROR_MESSAGE = "Unable to detect facial landmarks"
NOSE_EYE_THRESHOLD_MESSAGE = "Please provide valid value for nose position offset"
CHEEK_SYMMETRY_THRESHOLD_MESSAGE = "Please provide valid value for symmetry"
EAR_HEIGHT_DIFFERENCE_THRESHOLD_MESSAGE = "Please provide valid value for ear height difference"


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1550x550")
        self.title("Face detection app ")
        self.grid_rowconfigure(0, weight=0, minsize=135)
        self.grid_columnconfigure(0, weight=0, minsize=450)

        self.url_frame = UrlFrame(master=self)
        self.file_frame = FileFrame(master=self)
        self.folder_frame = FolderFrame(master=self)
        self.results_frame = ResultsFrame(master=self, width=475)
        self.settings_frame = DetectorSettingsFrame(master=self, fg_color="transparent")

        self.process_button = CTkButton(master=self, width=150, height=45, corner_radius=20, text_color="black",
                                        font=("Arial", 15), text="Process input", command=self.start_processing)
        self.clear_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                      font=("Arial", 15), text="Clear all results", command=self.clear_inputs)

        self.url_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.file_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.folder_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=30, sticky="nsew")
        self.settings_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=20)
        self.results_frame.grid(row=0, column=3, rowspan=4,columnspan=2, padx=20, pady=30, sticky="nsew")

        self.process_button.grid(row=2, column=2, padx=20, pady=30)
        self.clear_button.grid(row=4, column=3, padx=(75,0), pady=0)

    def start_processing(self):
        threading.Thread(target=self.process_input).start()

    def process_input(self):
        url_path = self.url_frame.entry.get().strip()
        file_path = self.file_frame.entry.get().strip()
        folder_path = self.folder_frame.entry.get().strip()
        detector = self.settings_frame.get_selected_detector()
        options = self.settings_frame.get_options()
        self.validate_options(options)
        self.disable_processing()
        self.show_status(url_path, file_path, folder_path)
        try:
            if url_path != "" and file_path == "" and folder_path == "":
                path = url_path
                self.results_frame.add_entry(PROCESSING_URL_MESSAGE)
                face_quality = process_url(path, detector, options)
                self.determine_results(path, face_quality, detector)
            elif url_path == "" and file_path != "" and folder_path == "":
                self.results_frame.add_entry(PROCESSING_FILE_MESSAGE)
                path = file_path
                face_quality = process_file(path, detector, options)
                self.determine_results(path, face_quality, detector)
            elif url_path == "" and file_path == "" and folder_path != "":
                self.results_frame.add_entry(f"Folder {self.extract_name(folder_path)} results:")
                main_path = folder_path
                files = os.listdir(main_path)
                all_files = files
                for file in all_files:
                    path = main_path + '/' + file
                    file_extension = file.split(".")[-1]
                    if file_extension in EXTENSIONS:
                        try:
                            face_quality = process_file(path, detector, options)
                            self.determine_results(path, face_quality, detector)
                        except ValueError as e:
                            self.after(0, lambda p=path, d=detector, msg=e: self.results_frame.add_result_negative(self.extract_name(p), d, msg))
                        except TypeError:
                            self.after(0, lambda p=path, d=detector, msg=TYPE_ERROR_MESSAGE: self.results_frame.add_result_negative(self.extract_name(p), d, msg))
                    else:
                        self.after(0, lambda p=path, d=detector, msg=INCORRECT_FILE_EXTENSION_MESSAGE: self.results_frame.add_result_negative(self.extract_name(p), d, msg))

            elif url_path == "" and file_path == "" and folder_path == "":
                messagebox.showinfo(title="No sources provided", message="One source must be provided")

            else:
                messagebox.showinfo(title="Too many sources provided", message="Please provide only one source")

        except ConnectionError as e:
            self.after(0, lambda p=path, d=detector, msg=e: self.results_frame.add_result_negative(self.extract_name(p), d, msg))
        except ValueError as e:
            self.after(0, lambda p=path, d=detector, msg=e: self.results_frame.add_result_negative(self.extract_name(p), d, msg))
        except TypeError:
            self.after(0, lambda p=path, d=detector, msg=TYPE_ERROR_MESSAGE: self.results_frame.add_result_negative(self.extract_name(p), d, msg))

        finally:
            self.hide_status()
            self.enable_processing()

    def determine_results(self, path, quality, detector):
        if quality:
            self.after(0, lambda p=path, d=detector: self.results_frame.add_result_positive(self.extract_name(p), d))
        else:
            self.after(0, lambda p=path, d=detector, msg="Low Quality": self.results_frame.add_result_negative(self.extract_name(p), d, msg))

    def clear_inputs(self):
        self.results_frame.delete_entries()
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

    def validate_options(self, options):
        try:
            nose_eye_threshold = float(options[0])
            cheek_threshold = float(options[1])
            ear_high_difference_threshold = float(options[2])
            if 0 > nose_eye_threshold or nose_eye_threshold > 1:
                messagebox.showinfo(title="Invalid value", message=NOSE_EYE_THRESHOLD_MESSAGE)
            if 0 > cheek_threshold or cheek_threshold > 1:
                messagebox.showinfo(title="Invalid value", message=CHEEK_SYMMETRY_THRESHOLD_MESSAGE)
            if 0 > ear_high_difference_threshold or ear_high_difference_threshold > 1:
                messagebox.showinfo(title="Invalid value", message=EAR_HEIGHT_DIFFERENCE_THRESHOLD_MESSAGE)
        except ValueError:
            messagebox.showinfo(title="Invalid value", message="Please provide valid value for one of the options")

    def disable_processing(self):
        self.process_button.configure(state="disabled")
        self.clear_button.configure(state="disabled")
        self.clear_button.configure(corner_radius=20)
        self.clear_button.update_idletasks()

    def enable_processing(self):
        self.process_button.configure(state="normal")
        self.clear_button.configure(state="normal")
        self.clear_button.configure(corner_radius=20)
        self.clear_button.update_idletasks()


app = App()
app.mainloop()
