from customtkinter import *
from constants.path import *
from PIL import Image


class WelcomeWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x600+600+100")
        self.title('Welcome')
        self.configure(fg_color = '#16161E')
        self.resizable(False, False)
        self.iconbitmap(f'{ICON_WHITE_ASSET}')

        self.bgImage = CTkImage(dark_image = Image.open(f'{WELCOME_BG_ASSET}'), size = (600, 600))
        self.bgLabel = CTkLabel(master = self, image = self.bgImage, 
                                text = '', bg_color  = 'transparent')
        self.bgLabel.place(x = 0, y = 0)

        self.welcomeText = CTkLabel(master = self, anchor = 'center', text = 'Welcome to', 
                                    text_color = '#FFFFFF', bg_color  = 'transparent', font = ('JetBrains Mono', 40))
        self.welcomeText.place(x = 179, y = 94)

        self.uwuImage = CTkImage(dark_image = Image.open(f'{LOGO_WHITE_ASSET}'), size = (118, 41))
        self.uwuLabel = CTkLabel(master = self, text = '', fg_color = 'transparent',
                                 image = self.uwuImage)
        self.uwuLabel.place(x = 242, y = 167)

        self.versionText = CTkLabel(master = self, anchor = 'center', text = 'Version 0.1.0', 
                                    text_color = '#FFFFFF', fg_color = 'transparent', font = ('JetBrains Mono', 14))
        self.versionText.place(x = 246, y = 229)

        self.firstDesc = CTkLabel(master = self, anchor = 'center', text = 'UwU++ is a whimsical and delightful', 
                                    text_color = '#FFFFFF', fg_color = 'transparent', font = ('JetBrains Mono', 17))
        self.firstDesc.place(x = 123, y = 271)
        
        self.secondDesc = CTkLabel(master = self, anchor = 'center', text = 'programming language that brings the charm of', 
                                    text_color = '#FFFFFF', fg_color = 'transparent', font = ('JetBrains Mono', 17))
        self.secondDesc.place(x = 70, y = 299)
        
        self.thirdDesc = CTkLabel(master = self, anchor = 'center', text = 'cuteness to the world of coding.', 
                                    text_color = '#FFFFFF', fg_color = 'transparent', font = ('JetBrains Mono', 17))
        self.thirdDesc.place(x = 138, y = 327)

        self.devLogsLabel = CTkLabel(master = self, anchor = 'center', text = 'Developer Logs', 
                                    text_color = '#FFFFFF', fg_color = 'transparent', font = ('JetBrains Mono', 15))
        self.devLogsLabel.place(x = 235, y = 376)

        self.firstLog = CTkLabel(master = self, anchor = 'center', text = '• Importing and Saving *.uwu files', 
                                    text_color = '#FFFFFF', bg_color  = 'transparent', font = ('JetBrains Mono', 15))
        self.firstLog.place(x = 144, y = 403)

        self.secondLog = CTkLabel(master = self, anchor = 'center', text = '• Display logs on console view', 
                                    text_color = '#FFFFFF', bg_color  = 'transparent', font = ('JetBrains Mono', 15))
        self.secondLog.place(x = 163, y = 430)

        self.thirdLog = CTkLabel(master = self, anchor = 'center', text = '• Token highlighting', 
                                    text_color = '#FFFFFF', bg_color  = 'transparent', font = ('JetBrains Mono', 15))
        self.thirdLog.place(x = 209, y = 457)

        self.fourthLog = CTkLabel(master = self, anchor = 'center', text = '• Lexical Analyzer', 
                                    text_color = '#FFFFFF', bg_color  = 'transparent', font = ('JetBrains Mono', 15))
        self.fourthLog.place(x = 217, y = 484)