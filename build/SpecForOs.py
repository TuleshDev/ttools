from tkinter import messagebox


class SpecForOs:

    @staticmethod
    def MessageBox1(message, title):
        #messagebox.showinfo(title, message)
        #win32api.MessageBox(0, message, title, win32con.MB_OK | win32con.MB_ICONINFORMATION)
        print(title + ' :    ' + message)
        return
