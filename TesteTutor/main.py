import pgzrun
from menu import MenuManager
from game import GameManager

WIDTH = 1080
HEIGHT = 1080
TITLE = "Roguelike Adventure"

MENU = 0
GAME = 1
GAME_OVER = 2
current_state = MENU

menu_manager = MenuManager(music, WIDTH, HEIGHT)
game_manager = None

def update():
    global current_state
    if current_state == MENU:
        menu_manager.update()
    elif current_state == GAME and game_manager:
        result = game_manager.update(keyboard)
        if result == "game_over":
            current_state = GAME_OVER
            music.stop() 
            
def draw():
    screen.clear()
    if current_state == MENU:
        menu_manager.draw(screen)
    elif current_state == GAME and game_manager:
        game_manager.draw(screen)
    elif current_state == GAME_OVER:
        draw_game_over()

def draw_game_over():
    screen.fill((50, 0, 0))
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=60, color=(255, 0, 0))
    screen.draw.text("Press R to Restart or ESC to return to Menu", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=24, color="white")

def on_mouse_move(pos):
    if current_state == MENU:
        menu_manager.on_mouse_move(pos)

def on_mouse_down(pos):
    global current_state, game_manager
    if current_state == MENU:
        action = menu_manager.on_mouse_down(pos)
        if action == "start_game":
            music.stop()
            if menu_manager.music_enabled:
                music.play('gamesound')

            game_manager = GameManager(
                WIDTH, HEIGHT,
                sound_enabled=menu_manager.sound_enabled,
                sounds_object=music 
            )
            current_state = GAME
        elif action == "quit":
            exit()

def on_key_down(key):
    global current_state, game_manager, menu_manager
    if key == keys.ESCAPE and current_state in [GAME, GAME_OVER]:
        music.stop()
        menu_manager.play_menu_music()
        current_state = MENU
    elif key == keys.R and current_state == GAME_OVER:
        if menu_manager.music_enabled:

            music.play('gamesound')

        game_manager = GameManager(
            WIDTH, HEIGHT,
            sound_enabled=menu_manager.sound_enabled,
            sounds_object=music  
        )
        current_state = GAME

def on_music_end():

    if current_state == MENU and menu_manager.music_enabled:
        menu_manager.play_menu_music()
    elif current_state == GAME and menu_manager.music_enabled:

        music.play('gamesound')

menu_manager.play_menu_music()

pgzrun.go()