import math
from entities import Player, Enemy
import random
from pygame import Rect

class GameManager:
    def __init__(self, width, height, sound_enabled=True, sounds_object=None):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.WORLD_WIDTH = width * 3
        self.WORLD_HEIGHT = height * 3
        
        self.player = Player(self.WORLD_WIDTH // 15, self.WORLD_HEIGHT // 15)
        
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 180
        self.game_over_delay = -1
        
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        
        self.sound_enabled = sound_enabled
        self.sounds = sounds_object

        self.kill_count = 0

        for _ in range(5):
            self.spawn_enemy()

    def spawn_enemy(self):
        while True:
            x = random.randint(50, self.WORLD_WIDTH - 50)
            y = random.randint(50, self.WORLD_HEIGHT - 50)
            distance = math.hypot(x - self.player.x, y - self.player.y)
            if distance > self.SCREEN_WIDTH // 3:
                enemy = Enemy(x, y)
                self.enemies.append(enemy)
                break
    
    def update(self, keyboard):
        if self.game_over_delay > 0:
            self.game_over_delay -= 1
            if self.game_over_delay == 0:
                if self.sound_enabled and self.sounds:
                    try:
                        self.sounds.gameover.play()
                    except AttributeError:
                        print("Som 'gameover' não encontrado na pasta music")
                return "game_over"

        if not self.player.is_dead and self.player.status != 'attack':
            self.handle_player_input(keyboard)
        
        if self.player.status == 'attack' and not self.player.is_dead:
            self.check_player_attack()
        
        self.player.update()
        for enemy in self.enemies:
            enemy.update(self.player)
        
        self.update_camera()
        
        for enemy in self.enemies:
            if enemy.status == 'attack' and enemy.rect.colliderect(self.player.rect) and not enemy.is_dead:
                attack_frame = int(enemy.animation_frame_index)
                if attack_frame == 4:
                    if self.player.take_damage(enemy.damage, self.player.shield_active):
                        self.game_over_delay = 120
        
        enemies_before = len(self.enemies)
        self.enemies = [e for e in self.enemies if not (e.is_dead and e.animation_finished)]
        kills_this_frame = enemies_before - len(self.enemies)
        if kills_this_frame > 0:
            self.kill_count += kills_this_frame

        if not self.player.is_dead:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_delay and len(self.enemies) < 25:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
        
        return None

    def handle_player_input(self, keyboard):
        moved = False
        dx, dy = 0, 0
        if keyboard.a or keyboard.left: dx -= self.player.speed
        if keyboard.d or keyboard.right: dx += self.player.speed
        if keyboard.w or keyboard.up: dy -= self.player.speed
        if keyboard.s or keyboard.down: dy += self.player.speed
        
        if dx != 0 or dy != 0:
            if dx != 0 and dy != 0:
                dx /= math.sqrt(2)
                dy /= math.sqrt(2)
            
            self.player.move(dx, dy)
            moved = True
            if abs(dx) > abs(dy):
                self.player.direction = "right" if dx > 0 else "left"
            else:
                self.player.direction = "down" if dy > 0 else "up"

        self.player.status = 'walk' if moved else 'idle'
        
        self.player.x = max(24, min(self.WORLD_WIDTH - 24, self.player.x))
        self.player.y = max(24, min(self.WORLD_HEIGHT - 24, self.player.y))
        
        if keyboard.space: self.player_attack()
        self.player.shield_active = keyboard.lshift or keyboard.rshift
        if keyboard.e and self.player.use_potion():
            if self.sound_enabled and self.sounds:
                try:
                    self.sounds.potion.play()
                except AttributeError:
                    print("Som 'potion' não encontrado na pasta music")

    def player_attack(self):
        damage = self.player.attack()
        if damage > 0:
            if self.sound_enabled and self.sounds:
                try:
                    self.sounds.attack.play()
                except AttributeError:
                    print("Som 'attack' não encontrado na pasta music")

    def update_camera(self):
        self.camera_offset_x = self.player.x - self.SCREEN_WIDTH // 2
        self.camera_offset_y = self.player.y - self.SCREEN_HEIGHT // 2
        
        self.camera_offset_x = max(0, min(self.WORLD_WIDTH - self.SCREEN_WIDTH, self.camera_offset_x))
        self.camera_offset_y = max(0, min(self.WORLD_HEIGHT - self.SCREEN_HEIGHT, self.camera_offset_y))

    def check_player_attack(self):
        attack_frame = int(self.player.animation_frame_index)
        if attack_frame >= 4 and attack_frame <= 6:
            attack_rect = self.player.rect.copy()
            attack_distance = 20
            
            if self.player.direction == 'up':
                attack_rect.y -= attack_distance
                attack_rect.height += attack_distance
            elif self.player.direction == 'down':
                attack_rect.height += attack_distance
            elif self.player.direction == 'left':
                attack_rect.x -= attack_distance
                attack_rect.width += attack_distance
            elif self.player.direction == 'right':
                attack_rect.width += attack_distance

            for enemy in self.enemies:
                if enemy.rect.colliderect(attack_rect) and not enemy.is_dead:
                    if not hasattr(enemy, 'hit_this_attack'):
                        enemy.hit_this_attack = True
                        enemy.take_damage(self.player.sword_damage)
                        print(f"Inimigo atingido! Vida restante: {enemy.health}")
        else:
            for enemy in self.enemies:
                if hasattr(enemy, 'hit_this_attack'):
                    delattr(enemy, 'hit_this_attack')

    def draw(self, screen):
        screen.fill((50, 100, 50))
        all_entities = sorted(self.enemies + [self.player], key=lambda e: e.rect.bottom)
        for entity in all_entities:
            entity.draw(screen, self.camera_offset_x, self.camera_offset_y)
        
        if self.player.status == 'attack':
            self.draw_attack_area(screen)
            
        self.draw_hud(screen)
    
    def draw_attack_area(self, screen):
        attack_frame = int(self.player.animation_frame_index)
        if attack_frame >= 4 and attack_frame <= 6:
            attack_rect = self.player.rect.copy()
            attack_distance = 20
            
            if self.player.direction == 'up':
                attack_rect.y -= attack_distance
                attack_rect.height += attack_distance
            elif self.player.direction == 'down':
                attack_rect.height += attack_distance
            elif self.player.direction == 'left':
                attack_rect.x -= attack_distance
                attack_rect.width += attack_distance
            elif self.player.direction == 'right':
                attack_rect.width += attack_distance
            
            attack_rect.x -= self.camera_offset_x
            attack_rect.y -= self.camera_offset_y
            
            screen.draw.rect(attack_rect, (255, 0, 0))
    
    def draw_hud(self, screen):
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = self.player.health / self.player.max_health
        screen.draw.filled_rect(Rect(10, 10, health_bar_width, health_bar_height), (100, 0, 0))
        screen.draw.filled_rect(Rect(10, 10, int(health_bar_width * health_ratio), health_bar_height), (0, 255, 0))
        screen.draw.text(f"Health: {self.player.health}/{self.player.max_health}", (15, 35), color="white", fontsize=24)
        screen.draw.text(f"Potions: {self.player.potions}", (15, 60), color="white", fontsize=24)
        screen.draw.text(f"Kills: {self.kill_count}", (15, 85), color="white", fontsize=24)
        screen.draw.text("WASD/Arrows: Move | SPACE: Attack | E: Potion | L-SHIFT: Block", (10, self.SCREEN_HEIGHT - 30), fontsize=20, color="white")