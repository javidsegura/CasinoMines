from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QBrush
import random

# O(1):Every operation runs in constant time
class ConfettiParticle:
    def __init__(self, x:float, y:float) -> None:
        """
        Description: initializes the ConfettiParticle class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-10, -5)
        self.size = random.randint(5, 15)
        self.color = random.choice([
            QColor("#FFD700"),  # Gold
            QColor("#FF6B6B"),  # Red
            QColor("#4ECDC4"),  # Turquoise
            QColor("#45B7D1"),  # Blue
            QColor("#96CEB4"),  # Green
            QColor("#FFEEAD"),  # Yellow
        ])
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)

class ConfettiEffect(QWidget):
    def __init__(self, parent:QWidget=None) -> None:
        """
        Description: initializes the ConfettiEffect class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.gravity = 0.5

    # O(n): as for a loop iterating n times. Note this is asymtotical growth and not fixed to the 100 values set there
    def start_animation(self) -> None:
        """
        Description: starts the animation
        Time Complexity:
            - O(n): as for a loop iterating n times. Note this is asymtotical growth and not fixed to the 100 values set there
        """
        self.show()
        self.particles = []
        for _ in range(100):
            x = random.uniform(0, self.width())
            y = 0  # Start from top of screen
            self.particles.append(ConfettiParticle(x, y))
        
        self.timer.start(16)

    # O(n):where n is the number of particles   
    def update_particles(self) -> None:
        """
        Description: updates the particles
        Time Complexity:
            - O(n):where n is the number of particles (again, note this is asymptotic growth, 
            ignoring the fact that self.particles is an arr of fixed size 100)
        """
        for particle in self.particles:
            particle.vy += self.gravity
            particle.x += particle.vx
            particle.y += particle.vy
            particle.rotation += particle.rotation_speed
            
        # Remove particles that are off screen; O(n) too
        self.particles = [p for p in self.particles if p.y < self.height() + 50]
        
        if not self.particles:
            self.timer.stop()
            self.hide()
            
        self.update()
        
    def paintEvent(self, event) -> None:
        """
        Description: paints the particles
        Time Complexity:
            - O(n):where n is the number of particles (again, note this is asymptotic growth, 
            ignoring the fact that self.particles is an arr of fixed size 100)
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for particle in self.particles:
            painter.save()
            painter.translate(particle.x, particle.y)
            painter.rotate(particle.rotation)
            
            painter.setBrush(QBrush(particle.color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(-particle.size/2, -particle.size/2, 
                           particle.size, particle.size)
            
            painter.restore()