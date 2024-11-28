""" Controls the sound effects of the game """

from PySide6.QtCore import QUrl, QTimer
from PySide6.QtMultimedia import QSoundEffect

class SoundEffects():
    """ Controls the sound effects of the game """
    def __init__(self) -> None:
        """
        Description: initializes the SoundEffects class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.sounds = {
            'click': self.load_sound("./utils/sound_effects/click.wav"),
            'win': self.load_sound("./utils/sound_effects/win.wav"),
            'lose': self.load_sound("./utils/sound_effects/error.wav"),
        }

    def load_sound(self, file_path) -> QSoundEffect:
        """
        Description: loads a sound effect from the given file path
        Time Complexity:
            - O(1): All operations run in constant time
        """
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(file_path))
        sound.setVolume(1)
        sound.setLoopCount(1)
        return sound

    def play_sound(self, sound_name) -> None:
        """
        Description: plays a sound effect among the collection of sounds
        Time Complexity:
            - O(1): All operations run in constant time
        """
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
        """
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.play_sound('click')

    def play_win(self) -> None:
        """
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.play_sound('win')

    def play_lose(self) -> None:
        """
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.play_sound('lose')
