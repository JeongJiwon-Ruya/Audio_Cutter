from pydub import AudioSegment
from pydub.silence import split_on_silence


def silence_cutter(filename, split_filename="분할_", filetype="wav"):
    count = 1
    file = AudioSegment.from_file(filename, format=filetype)

    # 전체 파일에서 가장 소리가 큰 값의 dBFS를 저장(normalize 위해)
    max_dBFS = file.max_dBFS
    print("파일의 dBFS값 :", max_dBFS)
    
    # split_on_silence(
    #   audio_segment : 파일,
    #   min_silence_len : 탐지하는 silence의 최소 시간,
    #   silence_thresh : silence로 정의되는 소리의 크기,
    #   keep_silence : cut된 각 파일들 뒤에 붙는 silence의 길이)
    chunks = split_on_silence(file, 400, -50, 500)

    print("분할될 파일의 개수 : ", len(chunks))

    for chunk in chunks[0:]:
        # cut될 각 파일들을 max_dBFS를 사용하여 normalize한다.
        if max_dBFS >= chunk.max_dBFS:
            chunk = chunk - (chunk.max_dBFS - max_dBFS)
            # 확인용 print
            # print("분할 파일의 max_dBFS :",chunk.max_dBFS)

        # 각 파일들을 export
        chunk.export(split_filename + str(count) + '.' + filetype, format(filetype))
        count += 1

        
def manual_normalize(filename, divide1, divide2, filetype="wav"):
    print("manual_normalizing...")
    count = 1
    file = AudioSegment.from_file(filename, format=filetype)
    max_dBFS = file.max_dBFS
    
    chunks = split_on_silence(file, 500, -50, 500)

    sum = AudioSegment.empty()

    for chunk in chunks[int(divide1)-1: int(divide2)]:
        sum = sum + chunk

    sum = sum - (sum.max_dBFS - max_dBFS)
    sum.export("분할_"+divide1+'~'+divide2+'.'+filetype, format(filetype))

    
if __name__ == '__main__':

    print("파일 제목을 입력하세요. (확장자 없이, ex. sample.wav -> sample 입력)")
    fileName = input()
    print("확장자를 입력하세요. (. 없이, ex. wav, mp3)")
    ext = input()

    print("파일명 :", fileName+"."+ext+"\n")
    
    print("작업을 선택하세요.\n1.파일 분할\n2.나눠서 저장된 음성 합치기")
    choice = input()

    if(choice == "1"):
        silence_cutter(fileName + "." + ext)
    elif(choice == "2"):
        print("시작파일번호를 입력하세요.")
        div1 = input()
        print("마지막파일번호를 입력하세요.")
        div2 = input()
        manual_normalize(fileName + "." + ext, div1, div2)
    else :
        exit()
