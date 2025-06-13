import math
from pygame import Rect

class Entity:

    def __init__(self, x, y, animations, width=48, height=48):  
        self.x = x
        self.y = y
        self.speed = 2
        self.rect = Rect(x, y, width, height) 
        self.health = 100
        self.max_health = 100
        self.animations = animations
        self.status = 'idle'
        self.direction = 'down'
        self.animation_frame_index = 0
        self.animation_speed = 0.15
        self.animation_finished = False
        self.non_looping_statuses = []

    def update_animation(self):

        animation_key = f"{self.status}_{self.direction}"
        if self.status in self.animations: animation_key = self.status
        if animation_key not in self.animations: animation_key = f"idle_{self.direction}"
        
        frames = self.animations.get(animation_key, [])
        if not frames: return
        
        if self.animation_finished and self.status in self.non_looping_statuses:
            return
        
        self.animation_frame_index += self.animation_speed
        
        if self.animation_frame_index >= len(frames):
            if self.status in self.non_looping_statuses:
                self.animation_frame_index = len(frames) - 1
                self.animation_finished = True
            else:
                self.animation_frame_index = 0

    def update(self):

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.update_animation()

    def move(self, dx, dy):

        self.x += dx
        self.y += dy

    def take_damage(self, damage):

        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True
        return False

    def draw(self, screen, offset_x, offset_y):
        screen_pos_x = self.rect.x - offset_x
        screen_pos_y = self.rect.y - offset_y

        animation_key = f"{self.status}_{self.direction}"
        if self.status in self.animations: animation_key = self.status
        if animation_key not in self.animations: animation_key = f"idle_{self.direction}"
        
        frames = self.animations.get(animation_key, [])
        if not frames:
            placeholder_rect = Rect(screen_pos_x, screen_pos_y, self.rect.width, self.rect.height)
            screen.draw.filled_rect(placeholder_rect, (255, 0, 255))
            return

        image_name = frames[int(self.animation_frame_index)]
        screen.blit(image_name, (screen_pos_x, screen_pos_y))

        if self.health < self.max_health and self.health > 0:
            health_bar_rect = Rect(screen_pos_x, screen_pos_y - 8, self.rect.width, 4)
            background_rect = health_bar_rect.copy()
            health_ratio = self.health / self.max_health
            health_bar_rect.width = int(self.rect.width * health_ratio)
            screen.draw.filled_rect(background_rect, (200, 0, 0))
            if health_bar_rect.width > 0:
                screen.draw.filled_rect(health_bar_rect, (0, 255, 0))

class Player(Entity):

    def __init__(self, x, y):
        animations = {
            'idle_down':  [f'hero/idle ({i})' for i in range(1, 11)],
            'walk_down':  [f'hero/run ({i})' for i in range(1, 11)],
            'idle_up':    [f'hero/idle ({i})' for i in range(1, 11)],
            'walk_up':    [f'hero/run ({i})' for i in range(1, 11)],
            'idle_left':  [f'hero/idle ({i})' for i in range(1, 11)],
            'walk_left':  [f'hero/run_l ({i})' for i in range(1, 11)],
            'idle_right': [f'hero/idle ({i})' for i in range(1, 11)],
            'walk_right': [f'hero/run ({i})' for i in range(1, 11)],
            'attack_down': [f'hero/attack ({i})' for i in range(1, 11)],
            'attack_up':   [f'hero/attack ({i})' for i in range(1, 11)],
            'attack_left': [f'hero/attack_l({i})' for i in range(1, 11)],
            'attack_right':[f'hero/attack ({i})' for i in range(1, 11)],
            'die':         [f'hero/dead ({i})' for i in range(1, 11)]
        }

        super().__init__(x, y, animations, width=48, height=48)
        self.non_looping_statuses = ['attack', 'die']
        self.speed = 4
        self.potions = 3
        self.sword_damage = 300
        self.attack_cooldown = 0
        self.shield_active = False
        self.is_dead = False

    def update(self):

        if self.is_dead:
            super().update() 
            return
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        if self.status == 'attack' and self.animation_finished:
            self.status = 'idle'
            self.animation_finished = False  

        super().update()

    def attack(self):
        if self.attack_cooldown <= 0 and self.status != 'attack':
            self.attack_cooldown = 60
            self.status = 'attack'
            self.animation_frame_index = 0
            self.animation_finished = False
            return self.sword_damage
        return 0

    def use_potion(self):
        if self.potions > 0 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + 40)
            self.potions -= 1
            return True
        return False

    def take_damage(self, damage, is_blocking=False):
        if self.is_dead: return False
        self.shield_active = is_blocking
        if self.shield_active: damage //= 2
        is_now_dead = super().take_damage(damage)
        if is_now_dead and not self.is_dead:
            self.is_dead = True
            self.status = 'die'
            self.animation_frame_index = 0
            self.animation_finished = False
        return is_now_dead

class Enemy(Entity):

    def __init__(self, x, y):
        animations = {
            'idle_down':  [f'enemies/idle ({i})' for i in range(1, 16)],
            'walk_down':  [f'enemies/walk ({i})' for i in range(1, 11)],
            'attack_down':[f'enemies/attack ({i})' for i in range(1, 9)],
            'idle_up':    [f'enemies/idle ({i})' for i in range(1, 16)],
            'walk_up':    [f'enemies/walk ({i})' for i in range(1, 11)],
            'attack_up':  [f'enemies/attack ({i})' for i in range(1, 9)],
            'idle_left':  [f'enemies/idle ({i})' for i in range(1, 16)],
            'walk_left':  [f'enemies/walk ({i})' for i in range(1, 11)],
            'attack_left':[f'enemies/attack ({i})' for i in range(1, 9)],
            'idle_right': [f'enemies/idle ({i})' for i in range(1, 16)],
            'walk_right': [f'enemies/walk ({i})' for i in range(1, 11)],
            'attack_right':[f'enemies/attack ({i})' for i in range(1, 9)],
            'die':        [f'enemies/dead ({i})' for i in range(1, 13)]
        }

        super().__init__(x, y, animations, width=48, height=48)
        self.non_looping_statuses = ['attack', 'die']
        self.health = 50
        self.max_health = 50
        self.damage = 10
        self.speed = 1.5
        self.detection_range = 250
        self.attack_range = 60  
        self.attack_cooldown = 0
        self.is_dead = False

    def update(self, player):

        can_act = not self.is_dead and not (self.status == 'attack' and not self.animation_finished)

        if can_act:

            if self.status == 'attack' and self.animation_finished:
                self.status = 'idle'

            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

            distance = math.hypot(self.x - player.x, self.y - player.y)

            if distance < self.attack_range and self.attack_cooldown <= 0:
                self.status = 'attack'
                self.animation_frame_index = 0
                self.animation_finished = False
                self.attack_cooldown = 120
            elif distance < self.detection_range:
                self.status = 'walk'
                dx = (player.x - self.x) / distance * self.speed
                dy = (player.y - self.y) / distance * self.speed
                self.move(dx, dy)
                if abs(dx) > abs(dy): self.direction = 'right' if dx > 0 else 'left'
                else: self.direction = 'down' if dy > 0 else 'up'
            else:
                self.status = 'idle'
        
        super().update()

    def take_damage(self, damage):
        if self.is_dead: return False
        is_now_dead = super().take_damage(damage)
        if is_now_dead and not self.is_dead:
            self.is_dead = True
            self.status = 'die'
            self.animation_frame_index = 0
            self.animation_finished = False
        return is_now_dead