from customtkinter import *
from Frames import *
from Services import *


set_appearance_mode("system")
set_default_color_theme("dark-blue")


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1300x500")
        # TODO Change name
        self.title("Face quality checking app ")

        self.grid_rowconfigure(0, weight=0, minsize=150)
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
        self.mode_switch = CTkSwitch(self, text="Dark / Light Mode Switch", command=self.change_appearance, variable=self.switch_var,
                                     onvalue="light", offvalue="dark")
        self.mode_switch.grid(row=3, column=0, padx=20, pady=30, sticky="nsew")

    def change_appearance(self):
        mode = self.switch_var.get()
        if mode == "dark":
            set_appearance_mode("dark")
        elif mode == "light":
            set_appearance_mode("light")

    def get_url(self):
        return 0




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
