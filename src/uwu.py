import customtkinter as ctk

class UwUCodeEditor(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # TODO: Add widgets for respective frames
        pass

class UwUConsole(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # TODO: Add widgets for respective frames
        pass

class UwULexer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # TODO: Add widgets for respective frames
        pass

class UwU(ctk.CTk):
    def __init__(self):
        super().__init__()
        # TODO: Init window settings and display arrange different frames        
        def close():
            self.destroy()

        self.geometry("1080x720")
        self.resizable(False, False)
        self.title("UwU IDE")

        button = ctk.CTkButton(self, text="Quit", command=close)
        button.pack()
        pass

if __name__ == "__main__":
    app = UwU()
    app.mainloop()