from customtkinter import *
from Frames import *
from Services import *

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
        self.url_frame.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

        self.file_frame = FileFrame(master=self)
        self.file_frame.grid(row=1, column=0, padx=20, pady=30, sticky="nsew")

        self.folder_frame = FolderFrame(master=self)
        self.folder_frame.grid(row=2, column=0, padx=20, pady=30, sticky="nsew")

        # TODO to delete
        self.new_frame = TestFrame(master=self)
        self.new_frame.grid(row=0, column=1)

        self.switch_var = StringVar(value="on")
        self.mode_switch = CTkSwitch(self, text="Dark / Light Mode Switch", command=self.change_appearance,
                                     variable=self.switch_var, onvalue="light", offvalue="dark")
        self.mode_switch.grid(row=3, column=0, padx=20, pady=30, sticky="nsew")

        self.middle_frame = MiddleFrame(master=self)
        self.middle_frame.grid(row=1, column=1, padx=20, pady=30, sticky="nsew")

        self.process_button = CTkButton(master=self, width=100, height=30, corner_radius=20, text_color="black",
                                        font=("Arial", 15), text="Process input", command=self.process_input)
        self.process_button.grid(row=2, column=1, padx=20, pady=30, sticky="nsew")

    # TODO add button that clears all fields and inserts base values there
    def change_appearance(self):
        mode = self.switch_var.get()
        if mode == "dark":
            set_appearance_mode("dark")
        elif mode == "light":
            set_appearance_mode("light")

    def process_input(self):
        url_path = self.url_frame.entry.get()
        print(url_path)

    # TODO might be useful
    # if __name__ == '__main__':
    #     root = tk.Tk()
    #     app = Application(root)
    #     app.mainloop()


app = App()
app.mainloop()

# # TODO tabview dobre do pokazywania co jest dobre a co złe
# TODO Frame dobre do oddzielenia sekcji gdzie są pokazywane wyniki
# TODO ProgressBarr dobry do pokazywania ile czasu jeszcze przy opcji Folder do przetwarzania
# TODO switch do zmieniania pomiędzy light i dark mode
# tabview = CTkTabview(master=window)
# tabview.grid()
#
# tabview.add("tab 1")  # add tab at the end
# tabview.add("tab 2")  # add tab at the end
# tabview.set("tab 2")  # set currently visible tab
#
# button2 = CTkButton(master=tabview.tab("tab 1"))
# button2.grid()
