from pydub import AudioSegment


def get_audio_segment(file_path, output_path, duration_from, duration_to, audio_type="mp3"):
    audio = AudioSegment.from_file(file_path)
    segment = audio[duration_from:duration_to]
    segment.export(output_path, format=audio_type)


if __name__ == '__main__':
    audio_path = '../data/test.mp3'
    new_audio_path = "../data/audio_test.mp3"
    get_audio_segment(audio_path, new_audio_path, 10000, 40000)
