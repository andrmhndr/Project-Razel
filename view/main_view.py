import customtkinter

class MainView:
    def __init__(self, master, title):
        self.master = master
        self.master.geometry("500x300")
        self.master.title(title)
        self.master.minsize(400, 300)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure((0,1), weight=1)
        
        self.dialog_box = customtkinter.CTkTextbox(master=self.master)
        self.dialog_box.grid(row=0, column=0, columnspan=3, pady=(20,0), padx=20, sticky="nsew")
        
        self.entry = customtkinter.CTkEntry(self.master, placeholder_text="write...",)
        self.entry.grid(row=1, column=0, padx=(20,10), pady=10, sticky='nsew')
        
        self.button_send = customtkinter.CTkButton(self.master, text='enter', height=25, width=50)
        self.button_send.grid(row=1, column=1, padx=(0,10), pady=10, sticky="nsew")
        
        self.button_rec = customtkinter.CTkButton(self.master, text='record', height=25, width=50)
        self.button_rec.grid(row=1, column=2, padx=(0,20), pady=10, sticky="nsew")

        self.option_window = None

    def insert_dialog(self, dialog):
        self.dialog_box.insert("insert", dialog.role + '\t: ' + dialog.content +'\n\n')
        
    def insert_dialog_list(self, dialogs):
        for dialog in dialogs:
            self.insert_dialog(dialog)
            
    def show_option(self, yes_func, no_func):
        if self.option_window is None or not self.option_window.winfo_exists():
            self.option_window = TopLevelWindow(self.master)
            self.option_window.button_yes.configure(command=yes_func)
            self.option_window.button_no.configure(command=no_func)
            self.option_window.focus()
        else:
            self.option_window.focus()
            
    def exit_top_level(self):
        self.option_window.destroy()
        self.option_window.update()
        
class TopLevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.geometry('400x100')
        self.title('Options')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        
        self.label = customtkinter.CTkLabel(self, text="Text terlalu panjang, apakah anda ingin saya membacakannya ?")
        self.label.grid(row=0, column=0, columnspan=2, padx=(0,10), pady=10, sticky="nsew")
        
        self.button_yes = customtkinter.CTkButton(self, text='Ya', height=25, width=50)
        self.button_yes.grid(row=1, column=0, padx=(20,10), pady=10, sticky="nsew")
        
        self.button_no = customtkinter.CTkButton(self, text='Tidak', height=25, width=50)
        self.button_no.grid(row=1, column=1, padx=(0,20), pady=10, sticky="nsew")