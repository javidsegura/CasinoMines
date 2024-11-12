""" Controls the sound effects of the game """

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtMultimedia import QSoundEffect

class SoundEffects():
    """ Controls the sound effects of the game """
    def __init__(self) -> None:
        self.sounds = {
            'click': self.load_sound("CasinoMines/utils/sound_effects/click.wav"),
            'win': self.load_sound("CasinoMines/utils/sound_effects/win.wav"),
            'lose': self.load_sound("CasinoMines/utils/sound_effects/error.wav"),
            # Add more sound effects here
        }

    def load_sound(self, file_path) -> QSoundEffect:
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(file_path))
        sound.setVolume(1)
        sound.setLoopCount(1)
        return sound

    def play_sound(self, sound_name) -> None:
        """ Plays a sound effect among the collection of sounds"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if sound.isLoaded():
                sound.play()
                QTimer.singleShot(100, lambda: None)
            else:
                raise Exception(f"Sound effect '{sound_name}' not loaded properly")
        else:
            raise Exception(f"Sound effect '{sound_name}' not found")

    def play_click(self) -> None:
        self.play_sound('click')

    def play_win(self) -> None:
        self.play_sound('win')

    def play_lose(self) -> None:
        self.play_sound('lose')