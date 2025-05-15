
import os
import requests
import pygame
import tempfile

pygame.mixer.init()

class AudioPlayer:
    def __init__(self):
        self.audio_cache = {}
        self.temp_dir = tempfile.gettempdir()

    def get_audio_url(self, word):
        encoded_word = requests.utils.quote(word)
        return f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_word}&tl=ja&client=gtx"

    def cache_audio(self, audio_url, word):
        audio_file = os.path.join(self.temp_dir, f"{word}.mp3")
        if word in self.audio_cache:
            return self.audio_cache[word]
        try:
            response = requests.get(audio_url)
            if response.status_code == 200:
                with open(audio_file, "wb") as f:
                    f.write(response.content)
                self.audio_cache[word] = audio_file
                return audio_file
        except Exception as e:
            print('Cache audio error:', e)
        return None

    def play_audio(self, audio_file):
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        except Exception as e:
            print('Play audio error:', e)
