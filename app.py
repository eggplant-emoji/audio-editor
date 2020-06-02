import tkinter as tk
from tkinter import filedialog
import wave
from audiodata import AudioData


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


class JoinWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.file1 = tk.Button(self.frame, text='Первый файл', command=self.get_filename1)
        self.file1.pack()
        self.file2 = tk.Button(self.frame, text='Второй файл', command=self.get_filename2)
        self.file2.pack()
        self.submit = tk.Button(self.frame, text='Склеить', command=self.on_submit)
        self.submit.pack()
        self.frame.pack()

    def get_filename1(self):
        self.filename1 = filedialog.askopenfilename()

    def get_filename2(self):
        self.filename2 = filedialog.askopenfilename()

    def on_submit(self):
        a = wave.open(self.filename1, 'rb')
        b = wave.open(self.filename2, 'rb')
        audiodata1 = AudioData.read(a)
        audiodata2 = AudioData.read(b)
        result = audiodata1.join(audiodata2)
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


class CropWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.file1 = tk.Button(self.frame, text='Файл', command=self.get_filename)
        self.file1.pack()

        self.submit = tk.Button(self.frame, text='Обрезать', command=self.on_submit)
        self.submit.pack()
        self.frame.pack()

    def get_filename(self):
        self.filename = filedialog.askopenfilename()
        self.create_slider1()
        self.create_slider2()

    def create_slider1(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        self.slide1 = tk.Scale(self.frame, from_=0, to=audiodata.duration(), orient=tk.HORIZONTAL)
        self.slide1.pack()

    def create_slider2(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        self.slide2 = tk.Scale(self.frame, from_=0, to=audiodata.duration(), orient=tk.HORIZONTAL)
        self.slide2.pack()

    def on_submit(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        result = audiodata.crop(int(self.slide1.get()), int(self.slide2.get()))
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


class ReverseWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.file1 = tk.Button(self.frame, text='Файл', command=self.get_filename)
        self.file1.pack()

        self.submit = tk.Button(self.frame, text='Перевернуть', command=self.on_submit)
        self.submit.pack()
        self.frame.pack()

    def get_filename(self):
        self.filename = filedialog.askopenfilename()

    def on_submit(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        result = audiodata.reverse()
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


class SpeedUpWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.file1 = tk.Button(self.frame, text='Файл', command=self.get_filename)
        self.file1.pack()

        self.l1 = tk.Label(self.frame, text="Во скаолько раз ускорить:", font="Arial 9")
        self.l1.pack()

        self.entry = tk.Entry(self.frame, width=20)
        self.entry.pack()

        self.submit = tk.Button(self.frame, text='Ускорить', command=self.on_submit)
        self.submit.pack()
        self.frame.pack()

    def get_filename(self):
        self.filename = filedialog.askopenfilename()

    def on_submit(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        result = audiodata.speed_up(int(self.entry.get()))
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


class SlowDownWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.file1 = tk.Button(self.frame, text='Файл', command=self.get_filename)
        self.file1.pack()

        self.l1 = tk.Label(self.frame, text="Во скаолько раз замедлить:", font="Arial 9")
        self.l1.pack()

        self.entry = tk.Entry(self.frame, width=20)
        self.entry.pack()

        self.submit = tk.Button(self.frame, text='Замедлить', command=self.on_submit)
        self.submit.pack()
        self.frame.pack()

    def get_filename(self):
        self.filename = filedialog.askopenfilename()

    def on_submit(self):
        a = wave.open(self.filename, 'rb')
        audiodata = AudioData.read(a)
        result = audiodata.slow_down(int(self.entry.get()))
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
