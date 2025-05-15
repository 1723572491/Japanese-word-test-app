import threading
from word_test_app.core.audio import AudioPlayer

class Pronunciation:
    def __init__(self, main_window):
        self.main_window = main_window
        self.audio_player = AudioPlayer()

    def start_pronounce_word(self):
        threading.Thread(target=self.pronounce_word).start()

    def pronounce_word(self):
        current_index = self.main_window.word_test.history[self.main_window.word_test.current_index]
        kana = self.main_window.word_test.data.iloc[current_index, 0]
        kanji = self.main_window.word_test.data.iloc[current_index, 1]
        tts_input = f"{kanji}"
        url = self.audio_player.get_audio_url(tts_input)
        if url:
            audio_file = self.audio_player.cache_audio(url, kanji)
            if audio_file:
                self.audio_player.play_audio(audio_file)
        else:
            self.main_window.show_error("发音失败")