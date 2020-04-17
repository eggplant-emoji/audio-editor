import wave



a = wave.open('a.wav', 'rb')
b = wave.open('b.wav', 'wb')
audiodata = AudioData.read(a)
newaudiodata = audiodata.slow_down(10)
newaudiodata.write(b)

