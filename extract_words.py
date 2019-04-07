import io
from pydub import AudioSegment
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('api-key.json')

class WordsExtractor:

    words = {}

    def __init__(self, song, words):
        self.words_list = words
        self.get_expected_words(song)

    def get_expected_words(self, audio_file):
        response = self.transcribe_audio_file(audio_file)
        audio_file = AudioSegment.from_wav(audio_file)
        for result in response.results:
            alternative = result.alternatives[0]

            for word_info in alternative.words:
                word = word_info.word
                if word in self.words_list:
                    start_time = word_info.start_time
                    end_time = word_info.end_time

                    start = start_time * 1000
                    end = end_time * 1000
                    print("split at [ {}:{}] ms".format(start, end))
                    self.words[word] = audio_file[start:end]

    def transcribe_audio_file(self, speech_file_path, language="en-US"):
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types

        client = speech.SpeechClient(credentials=credentials)

        with io.open(speech_file_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.FLAC, language_code=language,
                                         enable_word_time_offsets=True)

        response = client.recognize(config, audio)
        return response

    def exports_words(self):
        for word, audio_chunk in self.words_list.iteritems():
            audio_chunk.export("{}.wav".format(word), format="wav")

if __name__ == '__main__':
    words = ["china", "when", "was", "wall"]
    v2c = WordsExtractor("/home/nadav/Downloads/audio/trump.flac", words)
    v2c.exports_words()
    # v2c.load_from_file("/home/nadav/Downloads/audio/test.flac", "en-US")
