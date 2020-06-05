import wave
from audiodata import AudioData
keyboard_input = input()
input_data = keyboard_input.split(' ')
result = None


if input_data[0] == 'speed_up':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    coefficient = int(input_data[2])
    audiodata.speed_up(coefficient)
    result = audiodata.speed_up(coefficient)
    a.close()

elif input_data[0] == 'slow_down':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    coefficient = int(input_data[2])
    audiodata.speed_up(coefficient)
    result = audiodata.speed_up(coefficient)

elif input_data[0] == 'join':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    b = wave.open(input_data[2], 'rb')
    audiodata2 = AudioData.read(b)
    audiodata.join(audiodata2)
    result = audiodata.join(audiodata2)

elif input_data[0] == 'reverse':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    audiodata.reverse()
    result = audiodata.reverse()

elif input_data[0] == 'crop':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    start_milis = int(input_data[2])
    end_milis = int(input_data[3])
    audiodata.crop(start_milis, end_milis)
    result = audiodata.crop(start_milis, end_milis)

elif input_data[0] == 'bassboost':
    a = wave.open(input_data[1], 'rb')
    audiodata = AudioData.read(a)
    result = audiodata.bassboost()

elif input_data[0] == '-h' or input_data[0] == '--help':
    print(
        'crop file.wav start_milis end_milis -- will crop your file and return new file \n'
        'join file1.wav file2.wav -- will join two files and return \n'
        'reverse file.wav -- will return the audiofile that if played back sounds like the original \n'
        'slow_down file.wav coefficient  -- will slow down audiofile by n times \n'
        'speed_up file.wav coefficient  -- will speed up audiofile by n times \n'
        )
    exit()


else:
    print('Not found')
    exit()

output_file = wave.open('output.wav', 'wb')
result.write(output_file)




