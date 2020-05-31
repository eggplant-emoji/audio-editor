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
        self.join = tk.Button(self, command=self.new_window)
        self.join["text"] = "Склеить"
        self.join.pack()

        self.crop = tk.Button(self)
        self.crop["text"] = "Обрезать"
        self.crop.pack()
        self.reverse = tk.Button(self)
        self.reverse["text"] = "Перевернуть"
        self.reverse.pack()
        self.speed_up = tk.Button(self)
        self.speed_up["text"] = "Ускорить"
        self.speed_up.pack()
        self.slow_down = tk.Button(self)
        self.slow_down["text"] = "Змаедлить"
        self.slow_down.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = JoinWindow(self.newWindow)


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
        print(self.filename1, self.filename2)
        a = wave.open(self.filename1, 'rb')
        b = wave.open(self.filename2, 'rb')
        audiodata1 = AudioData.read(a)
        audiodata2 = AudioData.read(b)
        result = audiodata1.join(audiodata2)
        output_file = wave.open('output.wav', 'wb')
        result.write(output_file)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
