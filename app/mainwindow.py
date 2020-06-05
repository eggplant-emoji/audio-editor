from tkinter import Button, Listbox, Frame, END, OptionMenu, Toplevel

from app.exportwindow import ExportWindow
from app.actionwindow import ActionWindow
from app.fragmentwindow import FragmentWindow
from app.importwindow import ImportWindow
from app.joinwindow import JoinWindow
from app.reversewindow import ReverseWindow
from app.speedwindows import SpeedUpWindow, SlowDownWindow
from app.workspace import workspace, on_workspace_update


class MainWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.imp = Button(self, command=self.new_window0)
        self.imp["text"] = "Импортировать"
        self.imp.pack()

        self.ex = Button(self, command=self.new_window01)
        self.ex["text"] = "Экспортировать"
        self.ex.pack()

        self.join = Button(self, command=self.new_window1)
        self.join["text"] = "Склеить"
        self.join.pack()

        self.crop = Button(self, command=self.new_window2)
        self.crop["text"] = "Обрезать"
        self.crop.pack()

        self.reverse = Button(self, command=self.new_window3)
        self.reverse["text"] = "Перевернуть"
        self.reverse.pack()

        self.speed_up = Button(self, command=self.new_window4)
        self.speed_up["text"] = "Ускорить"
        self.speed_up.pack()

        self.slow_down = Button(self, command=self.new_window5)
        self.slow_down["text"] = "Замедлить"
        self.slow_down.pack()
        self.listbox = Listbox(self, width=50)
        self.listbox.pack()
        self.update_listbox()
        on_workspace_update(self.update_listbox)


    def update_listbox(self):
        self.listbox.delete(0, END)
        for file_name in workspace.keys():
            self.listbox.insert(END, file_name)

    def new_window0(self):
        self.newWindow = Toplevel(self.master)
        self.app1 = ImportWindow(self.newWindow)

    def new_window01(self):
        self.newWindow = Toplevel(self.master)
        self.app1 = ExportWindow(self.newWindow)

    def new_window1(self):
        self.newWindow = Toplevel(self.master)
        self.app1 = JoinWindow(self.newWindow)

    def new_window2(self):
        self.newWindow = Toplevel(self.master)
        self.app2 = FragmentWindow(self.newWindow)

    def new_window3(self):
        self.newWindow = Toplevel(self.master)
        self.app3 = ReverseWindow(self.newWindow)

    def new_window4(self):
        self.newWindow = Toplevel(self.master)
        self.app4 = SpeedUpWindow(self.newWindow)

    def new_window5(self):
        self.newWindow = Toplevel(self.master)
        self.app4 = SlowDownWindow(self.newWindow)