from pydub import AudioSegment
from pydub.silence import split_on_silence


def silence_cutter(filename, split_filename="분할_", filetype="wav"):
    count = 1
    file = AudioSegment.from_file(filename, format=filetype)

    # 전체 파일에서 가장 소리가 큰 값의 dBFS를 저장(normalize 위해)
    max_dBFS = file.max_dBFS

    # split_on_silence(
    #   audio_segment : 파일,
    #   min_silence_len : 탐지하는 silence의 최소 시간,
    #   silence_thresh : silence로 정의되는 소리의 크기,
    #   keep_silence : cut된 각 파일들 뒤에 붙는 silence의 길이)
    chunks = split_on_silence(file, 300, -50, 500)

    print("분할될 파일의 개수 : ", len(chunks)-1)

    for chunk in chunks[1:]:
        # cut될 각 파일들을 max_dBFS를 사용하여 normalize한다.
        if max_dBFS >= chunk.max_dBFS:
            chunk = chunk - (chunk.max_dBFS - max_dBFS)
            # 확인용 print
            # print("분할 파일의 max_dBFS :",chunk.max_dBFS)

        # 각 파일들을 export
        chunk.export(split_filename + str(count) + '.' + filetype, format(filetype))
        count += 1


if __name__ == '__main__':

    song = AudioSegment.from_file("sample_21.wav", format="wav")
    print("파일의 dBFS값 :", song.max_dBFS)

    silence_cutter("sample_21.wav")
