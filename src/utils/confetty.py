from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QBrush
import random

class ConfettiParticle:
    def __init__(self, x, y):
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.gravity = 0.5
        
    def start_animation(self):
        self.show()
        self.particles = []
        for _ in range(100):
            x = random.uniform(0, self.width())
            y = 0  # Start from top of screen
            self.particles.append(ConfettiParticle(x, y))
        
        self.timer.start(16)
        
    def update_particles(self):
        for particle in self.particles:
            particle.vy += self.gravity
            particle.x += particle.vx
            particle.y += particle.vy
            particle.rotation += particle.rotation_speed
            
        # Remove particles that are off screen
        self.particles = [p for p in self.particles if p.y < self.height() + 50]
        
        if not self.particles:
            self.timer.stop()
            self.hide()
            
        self.update()
        
    def paintEvent(self, event):
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