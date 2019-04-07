import io
import speech_recognition as sr
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('api-key.json')


class SpeechToSong:

    expected_words = []
    actual_words = {}

    def __init__(self, song):
        pass
        # self.expected_words = self.get_expected_words(song)

    def get_expected_words(self, song_file):
        r = sr.Recognizer()
        song = sr.AudioFile(song_file)
        with song as source:
            audio = r.record(source)

        return r.recognize_google(audio)

    def load_from_file(self, speech_file, language="en-US"):
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types

        client = speech.SpeechClient(credentials=credentials)

        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.FLAC, language_code=language,
                                         enable_word_time_offsets=True)

        response = client.recognize(config, audio)

        for result in response.results:
            alternative = result.alternatives[0]

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time

                self.actual_words[word] = {'start_time': start_time.seconds + start_time.nanos * 1e-9,
                                           'end_time': end_time.seconds + end_time.nanos * 1e-9}

    def get_status(self):
        print(self.actual_words)


if __name__ == '__main__':
    v2c = SpeechToSong("/home/nadav/Downloads/audio/trump.wav")
    # print(v2c.expected_words)
    v2c.load_from_file("/home/nadav/Downloads/audio/test.flac", "en-US")
