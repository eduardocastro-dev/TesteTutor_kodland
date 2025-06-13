import math
import random
from pygame import Rect

class MenuButton:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False
    
    def draw(self, screen):
        color = (70, 70, 120) if self.hover else (50, 50, 100)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, (200, 200, 200))
        screen.draw.text(self.text, center=self.rect.center, fontsize=32, color="white")
    
    def handle_click(self):
        return self.action if self.hover else None

class MenuParticle:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.randint(1, 3)
        self.speed_y = random.uniform(0.2, 1.0)
        self.width = width
        self.height = height
    
    def update(self):
        self.y += self.speed_y
        if self.y > self.height:
            self.y = 0
            self.x = random.randint(0, self.width)
    
    def draw(self, screen):
        screen.draw.filled_circle((int(self.x), int(self.y)), self.size, (100, 150, 200, 50))

class MenuManager:
    def __init__(self, music_object, width, height):
        self.music = music_object
        self.WIDTH = width
        self.HEIGHT = height
        self.music_enabled = True
        self.sound_enabled = True
        self.particles = [MenuParticle(self.WIDTH, self.HEIGHT) for _ in range(100)]
        
        center_x = self.WIDTH // 2
      
        button_width = 300
        button_height = 60
        button_y_start = self.HEIGHT // 2 - 100
        button_spacing = 90
        
        self.buttons = [
            MenuButton(center_x - button_width // 2, button_y_start, button_width, button_height, "START GAME", "start_game"),
            MenuButton(center_x - button_width // 2, button_y_start + button_spacing, button_width, button_height, "MUSIC: ON", "toggle_music"),
            MenuButton(center_x - button_width // 2, button_y_start + button_spacing * 2, button_width, button_height, "SOUNDS: ON", "toggle_sound"),
            MenuButton(center_x - button_width // 2, button_y_start + button_spacing * 3, button_width, button_height, "QUIT", "quit")
        ]
    
    def update(self):
        for particle in self.particles: particle.update()
        self.buttons[1].text = f"MUSIC: {'ON' if self.music_enabled else 'OFF'}"
        self.buttons[2].text = f"SOUNDS: {'ON' if self.sound_enabled else 'OFF'}"
    
    def draw(self, screen):
        screen.fill((10, 20, 40))
        for particle in self.particles: particle.draw(screen)

        screen.draw.text("ROGUELIKE ADVENTURE", center=(self.WIDTH//2, self.HEIGHT * 0.25), fontsize=60, color="white", owidth=1.5, ocolor="black")
        for button in self.buttons: button.draw(screen)
        screen.draw.text("Use the mouse to navigate the menu", center=(self.WIDTH//2, self.HEIGHT - 50), fontsize=20, color=(150, 150, 150))
    
    def on_mouse_move(self, pos):
        for button in self.buttons:
            button.hover = button.rect.collidepoint(pos)
    
    def on_mouse_down(self, pos):
        for button in self.buttons:
            action = button.handle_click()
            if action:
                if action == "toggle_music": self.toggle_music()
                elif action == "toggle_sound": self.toggle_sound()
                else: return action
        return None
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_menu_music()
        else:
            self.music.stop()
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
    
    def play_menu_music(self):
        """Toca a música do menu se estiver habilitada."""
        if self.music_enabled:
            try:
                self.music.play('menumusic.wav')
            except Exception as e:
                print(f"Erro ao tocar arquivo de música: {e}")
                try:
                    self.music.play('menumusic.wav')
                except Exception as e2:
                    print(f"Erro ao tocar arquivo de música com extensão: {e2}")