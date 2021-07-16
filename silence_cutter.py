from pydub import AudioSegment
from pydub.silence import split_on_silence


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def silence_cutter(filename, split_filename="분할_", filetype="wav"):
    count = 1
    file = AudioSegment.from_file(filename + ".wav", format=filetype)
    # normalize
    file = match_target_amplitude(file, -20.0)

    # split_on_silence(audio_segment, min_silence_len, silence_thresh, keep_silence)
    chunks = split_on_silence(file, 300, -50, 500)
    print("분할될 파일의 개수 : ", len(chunks))

    for chunk in chunks[0:]:
        chunk.export(split_filename + str(count) + '.' + filetype, format(filetype))
        count += 1


if __name__ == '__main__':
    silence_cutter("sample")
