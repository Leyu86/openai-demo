from component.openai import openai

MODEL = "whisper-1"


def whisper(audio_path: str, model: str = MODEL):
    try:
        audio_file = open(audio_path, "rb")
        response = openai.Audio.transcribe(model=model, file=audio_file)
        print(response)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    path = "D:/audio/audio_test.mp3"
    whisper(path)
