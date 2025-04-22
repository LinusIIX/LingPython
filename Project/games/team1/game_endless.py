# contributors:
# All of use (basegame)
# Eilo (transformation into endless mode and all resulting adjustments needed)
# Max (base implementation of buttons)
# Nikolas (refactoring)

import math
from enum import Enum
from random import randint, choice
from typing import TypedDict
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
from pygame.font import Font

import settings
from resources import ASSETS, save_highscore

class Enemy(TypedDict):
    word: str
    start_pos: pg.Vector2
    time_alive: float
    color: int

class GameState(Enum):
    PLAYING = 0
    PAUSE = 1
    GAME_OVER = 2

class Button:
    def __init__(self, text, center_x, center_y, box = True, underline = False, topleft = False):
        font: Font = ASSETS["FONTS"]["monospace"]
        self.text = text
        text_render = font.render(text, 1, settings.COLORS_CHOICES["BLACK"])
        if topleft:
            self.rect = text_render.get_rect(topleft=(0,0))
        else:
            self.rect = text_render.get_rect(center=(center_x, center_y))
        border_width = 2
        self.rect_border = pg.Rect(self.rect.left-border_width,
                                   self.rect.top-border_width,
                                   self.rect.width+2*border_width,
                                   self.rect.height+2*border_width)
        self.box = box
        self.underline = underline

    def draw(self, surface: pg.Surface, input = ""):
        if self.underline:
            font: Font = ASSETS["FONTS"]["monospaceUL"]
        else:
            font: Font = ASSETS["FONTS"]["monospace"]
        if self.box:
            overlap = find_overlap(input, self.text)
            button_font_start = font.render(self.text[:overlap],
                                            1,
                                            settings.COLORS_CHOICES["DARK_GRAY"])
            button_font_end = font.render(self.text[overlap:],
                                            1,
                                            settings.COLORS_CHOICES["LIGHT_GRAY"])
            start_width = button_font_start.get_width()
            end_width = button_font_end.get_width()
            button_rect_start = button_font_start.get_rect(center=(self.rect.left + start_width/2,self.rect.centery))
            button_rect_end = button_font_end.get_rect(center=(self.rect.left+start_width+end_width/2,self.rect.centery))
            pg.draw.rect(surface, settings.COLORS_CHOICES["BLACK"], self.rect_border)
            pg.draw.rect(surface, settings.COLORS_CHOICES["WHITE"], self.rect)
            surface.blit(button_font_start, button_rect_start)
            surface.blit(button_font_end, button_rect_end)
        else:
            text_font = font.render(self.text, 1, settings.COLORS_CHOICES["BLACK"])
            text_rect = text_font.get_rect(center=(self.rect.center))
            surface.blit(text_font, text_rect)

class Game:
    def __init__(self, gameData):
        self.screen = pg.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pg.display.set_caption("Words Tower Defense")
        self.clock = pg.time.Clock()
        self.shots_surface = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
        self.state: GameState
        self.state_change(GameState.PLAYING)
        self.quit = pg.USEREVENT + 1
        self.screen_center = pg.Vector2(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2)
        self.offset = 0.05*settings.SCREEN_WIDTH
        self.buttons: list[Button] = []
        self.game_surface = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
        self.blur_surface = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
        self.blur_surface.set_alpha(100)
        self.blur_surface.fill(settings.COLORS_CHOICES["DARK_GRAY"])
        self.current_wordlist = list(filter(lambda x: settings.CHANGABLE_VARIABLES["word_length_min"]<=len(x)<=settings.CHANGABLE_VARIABLES["word_length_max"], ASSETS["WORDLISTS"][settings.CHANGABLE_VARIABLES["active_wordlist"]]))
        self.gameData = gameData

        # Init game vars
        self.active_enemies: list[Enemy] = []
        self.shots: list[list[Enemy, float]] = []    # [enemy to shoot, time bolt is flying]
        self.difficulty: int = settings.CHANGABLE_VARIABLES["DIFFICULTY"]
        self.attack_text = ""
        self.pause_text = ""
        self.score = 0
        self.last_rotation = 0
        self.last_summon = 0
        self.death_enemy = ""
        self.score_text = Button(f"Score: {self.score}", 0, 0, False, topleft=True)
        self.start_time = 0

    def load_default_states(self):
        self.active_enemies = []
        self.shots = []
        self.difficulty = settings.CHANGABLE_VARIABLES["DIFFICULTY"]
        self.attack_text = ""
        self.pause_text = ""
        self.score = 0
        self.last_rotation = 0
        self.last_summon = 0
        self.death_enemy = ""
        self.score_text = Button(f"Score: {self.score}", 0, 0, False, topleft=True)
        self.start_time = 0

    def run(self):
        while True:
            d_time = self.clock.tick(settings.FPS) / 1000

            if self.handle_events():
                break
            self.update(d_time)
            self.draw()

            pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for e in events:
            match e.type:
                case pg.QUIT:
                    pg.event.post(pg.event.Event(self.quit))

                case self.quit:
                    return True
                
                case pg.KEYDOWN:
                    self.typing(e.key)

                case pg.MOUSEBUTTONDOWN:
                    self.click(pg.mouse.get_pos())

    def typing(self, key):
        keyname = pg.key.name(key)
        match self.state:
            case GameState.PLAYING:
                match key:
                    case pg.K_ESCAPE:
                        self.state_change(GameState.PAUSE)
                    case pg.K_RETURN:
                        self.attack_text = ""
                    case pg.K_SPACE:
                        self.attack_text = (self.attack_text + " ")[-15:]
                    case pg.K_BACKSPACE:
                        self.attack_text = self.attack_text[:-1]
                    case _ if len(keyname) == 1:
                        self.attack_text = (self.attack_text + keyname)[-15:]
                try:
                    channel = pg.mixer.find_channel()
                    channel.set_volume(settings.CHANGABLE_VARIABLES["SOUND"])
                    channel.play(ASSETS["SOUNDS"]["KEYBOARD"][keyname])
                except:
                    pass
                self.shoot()

            case GameState.PAUSE:
                match key:
                    case pg.K_ESCAPE:
                        self.state_change(GameState.PLAYING)
                    case pg.K_RETURN:
                        for button in self.buttons:
                            if self.pause_text[-len(button.text):].upper() == button.text:
                                self.activate_button(button)
                    case pg.K_SPACE:
                        self.pause_text = (self.pause_text + " ")[-15:]
                    case pg.K_BACKSPACE:
                        self.pause_text = self.pause_text[:-1]
                    case _ if len(keyname) == 1:
                        self.pause_text = (self.pause_text + keyname)[-15:]

            case GameState.GAME_OVER:
                match key:
                    case pg.K_ESCAPE:
                        pg.event.post(pg.event.Event(self.quit))
                    case pg.K_RETURN:
                        for button in self.buttons:
                            if self.pause_text[-len(button.text):].upper() == button.text:
                                self.activate_button(button)
                    case pg.K_SPACE:
                        self.pause_text = (self.pause_text + " ")[-15:]
                    case pg.K_BACKSPACE:
                        self.pause_text = self.pause_text[:-1]
                    case _ if len(keyname) == 1:
                        self.pause_text = (self.pause_text + keyname)[-15:]

    def click(self, pos: tuple[int, int]):
        for button in self.buttons:
            if pg.Rect.collidepoint(button.rect_border, pos):
                self.activate_button(button)

    def activate_button(self, button: Button):
        self.pause_text = ""
        match button.text:
            case "CONTINUE":
                self.state_change(GameState.PLAYING)
            case "QUIT":
                pg.event.post(pg.event.Event(self.quit))
            case "TRY AGAIN":
                self.load_default_states()
                self.state_change(GameState.PLAYING)

    def update(self, d_time: float):
        if self.state == GameState.PLAYING:
            self.start_time += d_time
            self.move_bolts(d_time)
            collision, active_enemies = self.update_enemies(d_time)
            if collision:
                self.death_enemy = active_enemies[0]
                self.state_change(GameState.GAME_OVER)
                return
            self.summon_enemy()

    def move_bolts(self, d_time: float):
        shot_removal = []
        for shot in self.shots:
            shot[1] += d_time/settings.SHOT_FLIGHT_RATE
            if shot[0]["time_alive"] + shot[1] > 1:
                shot_removal.append(shot)
        for shot in shot_removal:
            self.shots.remove(shot)
            self.active_enemies.remove(shot[0])

    def update_enemies(self, d_time: float):
        for enemy in self.active_enemies:
            enemy["time_alive"] += d_time/10
            if enemy["time_alive"] >= 1:
                return True, [enemy]
        return False, self.active_enemies

    def summon_enemy(self):
        summoning_chance = settings.BASE_SUMMONING_CHANCE - self.difficulty - self.score - self.last_summon
        if not (randint(0, pg.math.clamp(summoning_chance, 20, settings.BASE_SUMMONING_CHANCE)) and self.active_enemies): # summon
            self.last_summon = 0
            # choose one corner randomly
            x = randint(0,1) * settings.SCREEN_WIDTH
            y = randint(0,1) * settings.SCREEN_HEIGHT
            # randomize along the connected edges
            if randint(0,1):
                x = randint(0,settings.SCREEN_WIDTH)
            else:
                y = randint(0,settings.SCREEN_HEIGHT)
            word = choice(self.current_wordlist)
            new_enemy: Enemy = {
                "word": word,
                "start_pos": pg.Vector2(x,y),
                "time_alive": 0,
                "color": randint(0,2)
            }
            self.active_enemies.append(new_enemy)
        else: # don't summon
            self.last_summon += 1

    def shoot(self):
        for enemy in self.active_enemies:
            if enemy in [shot[0] for shot in self.shots]:
                continue # disable shooting the same word twice
            if enemy["word"].lower() == self.attack_text[-len(enemy["word"]):].lower():
                channel = pg.mixer.find_channel()
                channel.set_volume(settings.CHANGABLE_VARIABLES["SOUND"])
                channel.play(ASSETS["SOUNDS"]["kill"])
                self.attack_text = ""
                self.score += 1
                self.gameData["earnedPoints"] = max(self.gameData["earnedPoints"], self.score*2)
                self.score_text = Button(f"Score: {self.score}", 0, 0, False, topleft=True)
                self.shots.append([enemy, 0])
                self.last_rotation = math.degrees( # convert relative coordinates into a rotation
                    math.atan2(enemy["start_pos"].x - self.screen_center.x, enemy["start_pos"].y - self.screen_center.y))
                break

    def state_change(self, new_state: GameState):
        self.buttons = []
        match new_state:
            case GameState.PLAYING:
                ...
            
            case GameState.PAUSE:
                self.game_surface.blit(self.blur_surface)
                self.game_surface = pg.transform.box_blur(self.game_surface, 5)
                new_buttons = ["GAME PAUSED", "CONTINUE", "QUIT"]
                height = get_height(new_buttons[0], "monospace")
                self.buttons += [Button(button, self.screen_center.x, self.offset+height/2+n*height*1.5, False, True) for n,button in enumerate(new_buttons[:1])]
                self.buttons += [Button(button, self.screen_center.x, self.offset+height/2+n*height*1.5) for n,button in enumerate(new_buttons[1:],1)]
            
            case GameState.GAME_OVER:
                save_highscore("endless", self.score)
                self.game_surface.blit(self.blur_surface)
                self.game_surface = pg.transform.box_blur(self.game_surface, 5)
                new_buttons = ["GAME OVER", f"FINAL SCORE: {self.score}", f"AT {round(self.score*60/self.start_time,1)} WORDS PER MINUTE", "TRY AGAIN", "QUIT"]
                text_settings = [True, False, False]
                height = get_height(new_buttons[0], "monospace")
                self.buttons += [Button(button, self.screen_center.x, self.offset+height/2+n*height*1.5, False, underline) for n,(button,underline) in enumerate(zip(new_buttons[:-2],text_settings))]
                self.buttons += [Button(button, self.screen_center.x, self.offset+height/2+n*height*1.5) for n,button in enumerate(new_buttons[-2:],3)]

        self.state = new_state

    def draw(self):
        match self.state:
            case GameState.PLAYING:
                self.load_game_surface()
                self.screen.blit(self.game_surface)

            case GameState.PAUSE:
                self.screen.blit(self.game_surface)
                for button in self.buttons:
                    button.draw(self.screen, self.pause_text)

            case GameState.GAME_OVER:
                self.screen.blit(self.game_surface)
                for button in self.buttons:
                    button.draw(self.screen, self.pause_text)

    def load_game_surface(self):
        self.game_surface.blit(ASSETS["IMAGES"]["background"])

        # draw shots
        self.shots_surface.fill((*settings.COLORS_CHOICES["BLACK"], 0))
        for shot in self.shots:
            bolt: pg.Surface = ASSETS["IMAGES"]["bolt"]
            bolt_rotation = math.degrees( # convert relative coordinates into a rotation
                    math.atan2(shot[0]["start_pos"].x - self.screen_center.x, shot[0]["start_pos"].y - self.screen_center.y)) - 90
            rotated_bolt = pg.transform.rotate(bolt, bolt_rotation)
            bolt_rect = rotated_bolt.get_rect(center=self.screen_center.lerp(shot[0]["start_pos"], shot[1]))
            self.shots_surface.blit(rotated_bolt, bolt_rect)
        self.game_surface.blit(self.shots_surface)

        # draw ballista
        rotated_ballista = pg.transform.rotate(ASSETS["IMAGES"]["ballista"], self.last_rotation)
        self.game_surface.blit(rotated_ballista,
                            rotated_ballista.get_rect(center=self.screen_center))
        
        # draw enemies
        font: Font = ASSETS["FONTS"]["monospace"]
        for enemy in reversed(self.active_enemies):
            # reverse this list to give the closest enemy the highest priority so that it is drawn over the others
            current_pos = enemy["start_pos"].lerp(self.screen_center, enemy["time_alive"]*0.9)
            overlap = find_overlap(self.attack_text, enemy["word"])
            enemy_font_start = font.render(enemy["word"][:overlap],
                                            1,
                                            settings.ENEMY_COLORS[enemy["color"]+3])
            enemy_font_end = font.render(enemy["word"][overlap:],
                                            1,
                                            settings.ENEMY_COLORS[(enemy["color"]+3) if enemy in [shot[0] for shot in self.shots] else enemy["color"]])
            start_width = enemy_font_start.get_width()
            end_width = enemy_font_end.get_width()
            enemy_rect_start = enemy_font_start.get_rect(center=(round(current_pos.x-end_width/2),round(current_pos.y)))
            enemy_rect_end = enemy_font_end.get_rect(center=(round(current_pos.x+start_width/2),round(current_pos.y)))
            color = [255-color for color in settings.ENEMY_COLORS[enemy["color"]]] # complementary background color
            left = enemy_rect_start.left
            right = enemy_rect_end.right
            top = enemy_rect_start.top
            bottom = enemy_rect_start.bottom
            pg.draw.rect(self.game_surface, color, pg.Rect(left-5, top, right-left+10, bottom-top))
            self.game_surface.blit(enemy_font_start, enemy_rect_start)
            self.game_surface.blit(enemy_font_end, enemy_rect_end)
        if settings.CHANGABLE_VARIABLES["stats"]:
            self.score_text.draw(self.game_surface)
            wpm_font = font.render(f"WPM: ",1,settings.COLORS_CHOICES["BLACK"])
            wpm_rect = wpm_font.get_rect(topright=(self.screen_center.x, 0))
            wpm_value_font = font.render(f"{round(self.score*60/self.start_time,1)}",1,settings.COLORS_CHOICES["BLACK"])
            wpm_value_rect = wpm_font.get_rect(topleft=wpm_rect.topright)
            self.game_surface.blit(wpm_font, wpm_rect)
            self.game_surface.blit(wpm_value_font, wpm_value_rect)

def find_overlap(input: str, word: str):
    for i in range(min(len(input), len(word)), 0, -1):
        if input[-i:].lower() == word[:i].lower():
            return i
    return 0

def get_height(word, font_name):
    font: Font = ASSETS["FONTS"][font_name]
    return font.render(word, 1, settings.COLORS_CHOICES["BLACK"]).get_height()