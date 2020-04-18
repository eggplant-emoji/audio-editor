import wave
from audiodata import AudioData
keyboard_input = input()
input_data = keyboard_input.split(' ')
output_file = wave.open('output.wav', 'wb')
result = None

a = wave.open(input_data[1], 'rb')
audiodata = AudioData.read(a)

if input_data[0] == 'speed_up':
    coefficient = int(input_data[2])
    audiodata.speed_up(coefficient)
    result = audiodata.speed_up(coefficient)

elif input_data[0] == 'slow_down':
    coefficient = int(input_data[2])
    audiodata.speed_up(coefficient)
    result = audiodata.speed_up(coefficient)

elif input_data[0] == 'join':
    b = wave.open(input_data[2], 'rb')
    audiodata2 = AudioData.read(b)
    audiodata.join(audiodata2)
    result = audiodata.join(audiodata2)

elif input_data[0] == 'reverse':
    audiodata.reverse()
    result = audiodata.reverse()

elif input_data[0] == 'crop':
    start_milis = int(input_data[2])
    end_milis = int(input_data[3])
    audiodata.crop(start_milis, end_milis)
    result = audiodata.crop(start_milis, end_milis)

else:
    print('Not found')
    exit()

result.write(output_file)




