import wave
from audiodata import AudioData
keyboard_input = input()
input_data = keyboard_input.split(' ')

a = wave.open('input_data[1]', 'rb')
d = AudioData.read(a)
if input_data[0] == 'speed_up':
    coefficient = int(input_data[2])
    d.speed_up(coefficient)

elif input_data[0] == 'slow_down':
    coefficient = int(input_data[2])
    d.speed_up(coefficient)

elif input_data[0] == 'join':
    b = wave.open('input_data[2]', 'rb')
    c = AudioData.read(b)
    c.join()

elif input_data[0] == 'reserve':
    d.reverse()

elif input_data[0] == 'crop':
    start_milis = input_data[2]
    end_milis = input_data[3]
    d.crop(start_milis, end_milis)

else:
    print('Not found')



