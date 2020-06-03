import tkinter as tk
import wave
from tkinter import filedialog

from audiodata import AudioData


def read_audiodata():
    filename = filedialog.askopenfilename()
    a = wave.open(filename, 'rb')
    audiodata = AudioData.read(a)
    return audiodata


class General(tk.Frame):
    def __init__(self, master, filenumbers):
        super().__init__(master)
        self.body = None
        self.label = None
        self.submit = None
        self.slide = None
        self.master = master
        self.frame = tk.Frame(self.master)
        self.filenumbers = filenumbers
        self.frame.pack()
        self.buttons = []
        self.audiodatas = [None] * filenumbers
        self.create_widgets()

    def create_widgets(self):
        for i in range(self.filenumbers):
            filebutton = tk.Button(self.frame, text='Файл' + ' ' + str(i + 1), command=self.on_file_select(i))
            filebutton.pack()
            self.buttons.append(filebutton)
        self.label = tk.Label(self.frame, text="Выбрете все файлы")
        self.body = tk.Frame(self.frame)
        self.body.pack()
        self.submit = tk.Button(self.frame, text='подтвердить', state='disabled', command=self.on_submit)
        self.submit.pack()

    def on_file_select(self, button_id):
        def listener():
            self.audiodatas[button_id] = read_audiodata()
            if None not in self.audiodatas:
                self.all_files_selected()

        return listener

    def on_submit(self):
        result = self.calculate_result()
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)

    def calculate_result(self):
        pass

    def all_files_selected(self):
        self.submit['state'] = 'normal'
        self.label['text'] = ''

    def show_error(self, text):
        self.label['text'] = text
        self.submit['state'] = 'disabled'

    def close_error(self):
        self.label['text'] = ''
        self.submit['state'] = 'normal'


class SpeedWindow(General):
    def __init__(self, master, text):
        super().__init__(master, 1)
        self.l1 = tk.Label(self.body, text=text, font="Arial 13")
        self.l1.pack()
        self.edit = tk.Entry(self.body, width=20)
        self.edit.pack()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.join = tk.Button(self, command=self.new_window1)
        self.join["text"] = "Склеить"
        self.join.pack()

        self.crop = tk.Button(self, command=self.new_window2)
        self.crop["text"] = "Обрезать"
        self.crop.pack()

        self.reverse = tk.Button(self, command=self.new_window3)
        self.reverse["text"] = "Перевернуть"
        self.reverse.pack()

        self.speed_up = tk.Button(self, command=self.new_window4)
        self.speed_up["text"] = "Ускорить"
        self.speed_up.pack()

        self.slow_down = tk.Button(self, command=self.new_window5)
        self.slow_down["text"] = "Змаедлить"
        self.slow_down.pack()

    def new_window1(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app1 = JoinWindow(self.newWindow)

    def new_window2(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app2 = CropWindow(self.newWindow)

    def new_window3(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app3 = ReverseWindow(self.newWindow)

    def new_window4(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app4 = SpeedUpWindow(self.newWindow)

    def new_window5(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app4 = SlowDownWindow(self.newWindow)


class JoinWindow(General):
    def __init__(self, master):
        super().__init__(master, 2)

    def calculate_result(self):
        return self.audiodatas[0].join(self.audiodatas[1])


class CropWindow(General):
    def __init__(self, master):
        super().__init__(master, 1)

        self.slide1 = tk.Scale(self.body, from_=0, to=1, state='disabled', orient=tk.HORIZONTAL,
                               command=self.correct_use)
        self.slide1.pack()
        self.slide2 = tk.Scale(self.body, from_=0, to=1, state='disabled', orient=tk.HORIZONTAL,
                               command=self.correct_use)
        self.slide2.pack()

    def correct_use(self, _):
        if self.slide1.get() > self.slide2.get():
            self.show_error('Неправильно выбраны значения')
        else:
            self.close_error()

    def all_files_selected(self):
        self.slide1['to'] = self.audiodatas[0].duration()
        self.slide2['to'] = self.audiodatas[0].duration()
        self.slide1['state'] = 'normal'
        self.slide2['state'] = 'normal'

    def calculate_result(self):
        return self.audiodatas[0].crop(int(self.slide1.get()), int(self.slide2.get()))


class ReverseWindow(General):
    def __init__(self, master):
        super().__init__(master, 1)

    def calculate_result(self):
        return self.audiodatas[0].reverse()


class SpeedUpWindow(SpeedWindow):
    def __init__(self, master):
        super().__init__(master, "Во сколько раз ускорить:")

    def calculate_result(self):
        return self.audiodatas[0].speed_up(int(self.edit.get()))


class SlowDownWindow(SpeedWindow):
    def __init__(self, master):
        super().__init__(master, "Во сколько раз замедлить:")

    def calculate_result(self):
        return self.audiodatas[0].slow_down(int(self.edit.get()))


root = tk.Tk()
app = Application(master=root)
app.mainloop()
