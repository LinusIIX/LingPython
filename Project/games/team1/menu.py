# contributors:
# Nikolas (custom word list loading, refactoring)
# Max (rest of the main menu)

from enum import Enum
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
from pygame.font import Font

import settings
from resources import ASSETS, load_wordlist
from game_endless import Game as Endless
from game_roguelike import Game as Roguelike
from game_sandbox import Game as Sandbox

class GameState(Enum):
    MODE_SELECT = 0
    SETTINGS = 1
    WORDLIST = 2
    HIGHSCORE = 3
    CREDITS = 4
    MENU = 5
    DISCLAIMER = 6

class Button:
    def __init__(self, text: str, left, top, right, bottom, box = True, underline = False):
        self.text = text
        self.rect = pg.Rect(left, top, right-left, bottom-top)
        border_width = 2
        self.rect_border = pg.Rect(left-border_width,
                                   top-border_width,
                                   right-left+2*border_width,
                                   bottom-top+2*border_width)
        self.center = (left+right)/2, (top+bottom)/2
        self.box = box
        self.underline = underline

    def draw(self, surface: pg.Surface, input = "", text_color = settings.COLORS_CHOICES["BLACK"]):
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
            button_rect_start = button_font_start.get_rect(center=(self.rect.left + start_width/2,self.center[1]))
            button_rect_end = button_font_end.get_rect(center=(self.rect.left+start_width+end_width/2,self.center[1]))
            pg.draw.rect(surface, settings.COLORS_CHOICES["BLACK"], self.rect_border)
            pg.draw.rect(surface, settings.COLORS_CHOICES["WHITE"], self.rect)
            surface.blit(button_font_start, button_rect_start)
            surface.blit(button_font_end, button_rect_end)
        else:
            text_font = font.render(self.text,1,text_color)
            text_rect = text_font.get_rect(center=(self.rect.left + text_font.get_width()/2,self.center[1]))
            surface.blit(text_font, text_rect)

class Checkbox:
    def __init__(self, text: str, left, top, right, bottom, initial_value):
        self.text = text
        self.text_rect = pg.Rect(left, top, right-left, bottom-top)
        self.border_width = 2
        self.rect_border = pg.Rect(left-self.border_width,
                                   top-self.border_width,
                                   right-left+6*self.border_width+bottom-top,
                                   bottom-top+2*self.border_width)
        self.text_rect_border = pg.Rect(left-self.border_width,
                                   top-self.border_width,
                                   right-left+2*self.border_width,
                                   bottom-top+2*self.border_width)
        left = right + 4*self.border_width
        self.checkbox_rect = pg.Rect(left, top, bottom-top, bottom-top)
        self.checkbox_rect_border = pg.Rect(left-self.border_width,
                                            top-self.border_width,
                                            bottom-top+2*self.border_width,
                                            bottom-top+2*self.border_width)
        self.checked = initial_value

    def draw(self, surface: pg.Surface, input = ""):
        font: Font = ASSETS["FONTS"]["monospace"]
        overlap = find_overlap(input, self.text)
        button_font_start = font.render(self.text[:overlap],
                                        1,
                                        settings.COLORS_CHOICES["DARK_GRAY"])
        button_font_end = font.render(self.text[overlap:],
                                        1,
                                        settings.COLORS_CHOICES["LIGHT_GRAY"])
        start_width = button_font_start.get_width()
        end_width = button_font_end.get_width()
        button_rect_start = button_font_start.get_rect(center=(self.text_rect.left + start_width/2,self.text_rect.centery))
        button_rect_end = button_font_end.get_rect(center=(self.text_rect.left+start_width+end_width/2,self.text_rect.centery))
        pg.draw.rect(surface, settings.COLORS_CHOICES["BLACK"], self.text_rect_border)
        pg.draw.rect(surface, settings.COLORS_CHOICES["WHITE"], self.text_rect)
        pg.draw.rect(surface, settings.COLORS_CHOICES["BLACK"], self.checkbox_rect_border)
        pg.draw.rect(surface, settings.COLORS_CHOICES["WHITE"], self.checkbox_rect)
        if self.checked:
            pg.draw.line(surface, settings.COLORS_CHOICES["BLACK"],
                         (self.checkbox_rect.left+self.border_width*2, self.checkbox_rect.top+self.border_width*2),
                         (self.checkbox_rect.right-self.border_width*2, self.checkbox_rect.bottom-self.border_width*2), 5)
            pg.draw.line(surface, settings.COLORS_CHOICES["BLACK"],
                         (self.checkbox_rect.right-self.border_width*2, self.checkbox_rect.top+self.border_width*2),
                         (self.checkbox_rect.left+self.border_width*2, self.checkbox_rect.bottom-self.border_width*2), 5)
        surface.blit(button_font_start, button_rect_start)
        surface.blit(button_font_end, button_rect_end)

class Slider:
    def __init__(self, text: str, left, top, right, bottom, initial_value):
        font: Font = ASSETS["FONTS"]["monospace"]
        self.text = text
        self.text_rect = pg.Rect(left, top, right-left, bottom-top)
        self.border_width = 2
        self.rect_border = pg.Rect(right+4*self.border_width,
                                   (bottom+top)/2-3*self.border_width,
                                   right-left,
                                   self.border_width*6)
        slider_value_coords = pg.math.lerp(self.rect_border.left, self.rect_border.right, initial_value/100)
        self.slider_blob_rect = pg.Rect(
            slider_value_coords-4*self.border_width,
            self.rect_border.centery-4*self.border_width,
            8*self.border_width,
            8*self.border_width)
        self.slider_blob_rect_inner = pg.Rect(
            slider_value_coords-3*self.border_width,
            self.rect_border.centery-3*self.border_width,
            6*self.border_width,
            6*self.border_width)
        self.value = initial_value
        self.value_rect = font.render(str(self.value), 1, settings.COLORS_CHOICES["BLACK"]).get_rect(topleft=(self.rect_border.right+4*self.border_width, top))

    def draw(self, surface: pg.Surface, input = ""):
        font: Font = ASSETS["FONTS"]["monospace"]
        text_font = font.render(self.text, 1, settings.COLORS_CHOICES["BLACK"])
        value_font = font.render(str(self.value) + "%", 1, settings.COLORS_CHOICES["BLACK"])
        font_rect = text_font.get_rect(topleft=self.text_rect.topleft)
        surface.blit(text_font, font_rect)
        surface.blit(value_font, self.value_rect)
        pg.draw.rect(surface, settings.COLORS_CHOICES["LIGHT_GRAY"],
                     pg.Rect(self.rect_border.left,
                     self.rect_border.centery-self.border_width,
                     self.rect_border.width,
                     self.border_width*2),
                     border_radius=self.border_width)
        pg.draw.rect(surface, settings.COLORS_CHOICES["BLACK"], self.slider_blob_rect)
        pg.draw.rect(surface, settings.COLORS_CHOICES["WHITE"], self.slider_blob_rect_inner)

    def update_value(self, mouse_x):
        self.value = pg.math.clamp(round((mouse_x-self.rect_border.x)*100 / (self.rect_border.width)), 0, 100)
        slider_value_coords = pg.math.lerp(self.rect_border.left, self.rect_border.right, self.value/100)
        self.slider_blob_rect.left = slider_value_coords-4*self.border_width
        self.slider_blob_rect_inner.left = slider_value_coords-3*self.border_width

class Menu:
    def __init__(self, gamedata):
        self.screen = pg.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pg.display.set_caption("Words Tower Defense")
        self.clock = pg.time.Clock()

        # Init vars
        self.ui_surface = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
        self.background_surface: pg.Surface = load_background()
        try:
            import assets
            self.state = GameState.DISCLAIMER
        except:
            self.state = GameState.MENU
        self.quit = pg.USEREVENT + 1
        self.play_endless = pg.USEREVENT + 2
        self.play_roguelike = pg.USEREVENT + 3
        self.play_sandbox = pg.USEREVENT + 4
        self.screen_center = pg.Vector2(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2)
        self.text_input = ""
        self.button_texts = ["PLAY", "SETTINGS", "EDIT WORDS", "HIGHSCORES", "CREDITS"]
        width, height = get_largest(self.button_texts)
        self.offset = 0.05*settings.SCREEN_WIDTH
        self.buttons = [Button(button, self.offset, self.offset+n*height*1.5, self.offset+width, self.offset+n*height*1.5+height) for n,button in enumerate(self.button_texts, 1)]
        self.buttons.append(Button("Words TD - Type or Die", self.offset, self.offset, self.offset+get_largest(["Words TD - Type or Die"])[0], self.offset+height, False, True))
        self.word_list = "MIT-10000"
        self.rainbow = [0,0,255]
        self.rainbow_index = 0
        self.track_mouse_pos: bool | Slider = False
        disclaimer_message = "Thank you for trying our game: Words TD - Type or Die!\n\nYour goal is to type the incoming words before they reach you. This trains typing quickly on a computer and can be loaded with custom word lists to train your vocabulary.\n\nTo unlock the Dothraki hint you must hit a score of 50 in Endless mode, 100 in Roguelike mode or 200 in Sandbox mode. We spent a lot of time developing the Roguelike mode, so we highly recommend trying it out.\n\nFor more information refer to the README.md on the same file level as this game (should be GameEngineInterface/games/Words TD/README.md or something similar).\n\nGood luck and have fun wish you the developers Max, Nikolas and Eilo :)\n\nPress any key to continue..."
        font: Font = ASSETS["FONTS"]["monospace"]
        self.disclaimer_font = font.render(disclaimer_message, 1, settings.COLORS_CHOICES["WHITE"], wraplength=round(settings.SCREEN_WIDTH*0.9))
        self.disclaimer_rect = self.disclaimer_font.get_rect(center=self.screen_center)
        self.gameData = gamedata

    def draw(self):
        self.screen.blit(self.background_surface)
        self.ui_surface.fill((*settings.COLORS_CHOICES["BLACK"], 0))

        match self.state:
            case GameState.MENU:
                for button in self.buttons:
                    button.draw(self.ui_surface, self.text_input)

            case GameState.MODE_SELECT:
                for button in self.buttons:
                    button.draw(self.ui_surface, self.text_input)

            case GameState.SETTINGS:
                for button in self.buttons:
                    button.draw(self.ui_surface, self.text_input)

            case GameState.WORDLIST:
                for button in self.buttons:
                    button.draw(self.ui_surface, self.text_input)

            case GameState.HIGHSCORE:
                for button in self.buttons:
                    button.draw(self.ui_surface, self.text_input)

            case GameState.CREDITS:
                self.update_rainbow()
                for button in self.buttons[:len(self.button_texts)+1]:
                    button.draw(self.ui_surface, self.text_input)
                for button in self.buttons[len(self.button_texts)+1:]:
                    button.draw(self.ui_surface, self.text_input, self.rainbow)

            case GameState.DISCLAIMER:
                self.screen.fill(settings.COLORS_CHOICES["BLACK"])
                self.screen.blit(self.disclaimer_font, self.disclaimer_rect)
                return

        self.screen.blit(self.ui_surface)

    def run(self):
        while True:
            self.clock.tick(settings.FPS)

            if self.handle_events():
                break
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
                
                case self.play_endless:
                    Endless(self.gameData).run()
                    self.state_change(GameState.MENU)
                
                case self.play_roguelike:
                    Roguelike(self.gameData).run()
                    self.state_change(GameState.MENU)
                
                case self.play_sandbox:
                    Sandbox(self.gameData).run()
                    self.state_change(GameState.MENU)
                
                case pg.KEYDOWN:
                    self.typing(e.key)

                case pg.MOUSEBUTTONDOWN:
                    self.click(pg.mouse.get_pos())

                case pg.MOUSEBUTTONUP:
                    if self.track_mouse_pos:
                        settings.CHANGABLE_VARIABLES[self.track_mouse_pos.text] = self.track_mouse_pos.value
                        self.track_mouse_pos = False

        if self.track_mouse_pos:
            mouse_pos_x = pg.mouse.get_pos()[0]
            self.track_mouse_pos.update_value(mouse_pos_x)
    
    def click(self, pos: tuple[int, int]):
        if self.state == GameState.DISCLAIMER:
            self.state_change(GameState.MENU)
            return
        for n,button in enumerate(self.buttons):
            if pg.Rect.collidepoint(button.rect_border, pos):
                self.activate_button(button, n)

    def typing(self, key):
        keyname = pg.key.name(key)
        if self.state == GameState.DISCLAIMER:
            self.state_change(GameState.MENU)
            return
        match key:
            case pg.K_ESCAPE:
                if self.state == GameState.MENU:
                    pg.event.post(pg.event.Event(self.quit))
                else:
                    self.state_change(GameState.MENU)

            case pg.K_SPACE:
                self.text_input = (self.text_input + " ")[-15:]

            case pg.K_BACKSPACE:
                self.text_input = self.text_input[:-1]

            case pg.K_RETURN:
                for n,button in enumerate(self.buttons):
                    if self.text_input[-len(button.text):].upper() == button.text:
                        self.activate_button(button, n)

            case _ if len(keyname) == 1:
                self.text_input = (self.text_input + keyname)[-15:]

    def activate_button(self, button: Button | Checkbox | Slider, button_number: int):
        self.text_input = ""
        if button_number < len(self.button_texts):
            self.state_change(GameState(button_number))
        else:
            match button.text:
                case "ENDLESS":
                    pg.event.post(pg.event.Event(self.play_endless))
                case "ROGUELIKE":
                    pg.event.post(pg.event.Event(self.play_roguelike))
                case "SANDBOX":
                    pg.event.post(pg.event.Event(self.play_sandbox))
                case "SHOW STATS":
                    button.checked = not button.checked
                    settings.CHANGABLE_VARIABLES["stats"] = button.checked
                case "SOUND":
                    self.track_mouse_pos = button
                case "DIFFICULTY":
                    self.track_mouse_pos = button
                case "LOAD DEFAULT":
                    self.word_list = "MIT-10000"
                    settings.CHANGABLE_VARIABLES["active_wordlist"] = "MIT-10000"
                    self.state_change(GameState.WORDLIST)
                case "LOAD CUSTOM":
                    self.word_list = load_wordlist()
                    settings.CHANGABLE_VARIABLES["active_wordlist"] = self.word_list
                    self.state_change(GameState.WORDLIST)

    def state_change(self, new_state: GameState):
        self.buttons = self.buttons[:len(self.button_texts)+1]
        match new_state:
            case GameState.MODE_SELECT:
                new_buttons = ["ENDLESS", "ROGUELIKE", "SANDBOX"]
                width, height = get_largest(new_buttons)
                offset_left = self.buttons[0].rect.right + self.offset
                self.buttons += [Button(button, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height) for n,button in enumerate(new_buttons,1)]
            case GameState.SETTINGS:
                new_buttons = ["SHOW STATS", "SOUND", "DIFFICULTY"]
                initial_checkbox_values = [True]
                initial_slider_values = [settings.CHANGABLE_VARIABLES["SOUND"], settings.CHANGABLE_VARIABLES["DIFFICULTY"]]
                width, height = get_largest(new_buttons)
                offset_left = self.buttons[0].rect.right + self.offset
                self.buttons += [Checkbox(checkbox, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height, initial_value) for n,(checkbox, initial_value) in enumerate(zip(new_buttons[:1],initial_checkbox_values),1)]
                self.buttons += [Slider(slider, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height, initial_value) for n,(slider, initial_value) in enumerate(zip(new_buttons[1:], initial_slider_values),2)]
            case GameState.WORDLIST:
                new_buttons = ["LOAD DEFAULT", "LOAD CUSTOM", f"ACTIVE: {self.word_list}"]
                width, height = get_largest(new_buttons)
                offset_left = self.buttons[0].rect.right + self.offset
                self.buttons += [Button(button, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height) for n,button in enumerate(new_buttons[:-1],1)]
                self.buttons += [Button(button, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height, False) for n,button in enumerate(new_buttons[-1:], len(new_buttons))]
            case GameState.HIGHSCORE:
                headers = ["Endless:", "Roguelike:"]
                highscores: dict[str, dict[str, int]] = ASSETS["HIGHSCORES"]
                highscores_endless = highscores["endless"]
                entries = [f"{(user+':').ljust(10)} {score}" for user, score in sorted(highscores_endless.items(), key=lambda item: item[1], reverse=True)]
                width, height = get_largest([headers[0], *entries])
                offset_left = self.buttons[0].rect.right + self.offset
                self.buttons.append(Button(headers[0], offset_left, self.offset+height*1.5, offset_left+width, self.offset+height*2.5, False, True))
                self.buttons += [Button(button, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height, False) for n,button in enumerate(entries,2)]
                highscores_roguelike = ASSETS["HIGHSCORES"]["roguelike"]
                print(highscores_roguelike)
                entries = [f"{(user+':').ljust(10)} {score}" for user, score in sorted(highscores_roguelike.items(), key=lambda item: item[1], reverse=True)]
                width, height = get_largest([headers[1], *entries])
                offset_left = self.buttons[-1].rect.right + self.offset*2
                self.buttons.append(Button(headers[1], offset_left, self.offset+height*1.5, offset_left+width, self.offset+height*2.5, False, True))
                self.buttons += [Button(button, offset_left, self.offset+n*height*1.5, offset_left+width, self.offset+n*height*1.5+height, False) for n,button in enumerate(entries,2)]
            case GameState.CREDITS:
                infos = [
                    ["Max Morscher", "Coding roguelike mode", "Highscore tracking", "UI design", "Bugfixing"],
                    ["Nikolas Heise", "Coding sandbox mode", "Custom wordlist loading", "Sound design", "Refactoring, planning"],
                    ["Eilo de Vito", "Coding endless mode", "Framework connection", "Custom artworks", "Testing"],
                ]
                widths = get_widths(infos)
                max_widths = max(widths[0]), max(widths[1]), max(widths[2])
                height = get_height(infos[0][0], "monospace")
                offset_top = self.offset + 1.5 * height
                offset_left = self.buttons[0].rect.right + self.offset
                for max_width,width,info in zip(max_widths, widths, infos):
                    for n,entry in enumerate(zip(info, width)):
                        self.buttons.append(Button(entry[0], offset_left+max_width/2-entry[1]/2, offset_top+n*height*1.5, offset_left+max_width/2+entry[1]/2, offset_top+n*height*1.5+height, False))
                    offset_left += max_width
                    offset_top = self.buttons[-1].rect.bottom + 0.5*height
                button_index = len(self.button_texts)+1
                for i in range(len(infos)):
                    self.buttons[button_index].underline = True
                    button_index += len(infos[i])
        self.state = new_state

    def update_rainbow(self):
        speed = 5
        match self.rainbow_index:
            case 0: new_value = self.rainbow[0] + speed
            case 1: new_value = self.rainbow[2] - speed
            case 2: new_value = self.rainbow[1] + speed
            case 3: new_value = self.rainbow[0] - speed
            case 4: new_value = self.rainbow[2] + speed
            case 5: new_value = self.rainbow[1] - speed
        if new_value < 0 or new_value > 255:
            self.rainbow_index = (self.rainbow_index + 1)%6
            self.update_rainbow()
        else:
            match self.rainbow_index:
                case 0 | 3: self.rainbow[0] = new_value
                case 2 | 5: self.rainbow[1] = new_value
                case 1 | 4: self.rainbow[2] = new_value

def find_overlap(input: str, word: str):
    for i in range(min(len(input), len(word)), 0, -1):
        if input[-i:].lower() == word[:i].lower():
            return i
    return 0

def get_largest(words):
    buttons: list[pg.Surface] = []
    for word in words:
        font: Font = ASSETS["FONTS"]["monospace"]
        buttons.append(font.render(word, 1, settings.COLORS_CHOICES["BLACK"]))
    try: return max(button.get_width() for button in buttons), max(button.get_height() for button in buttons)
    except: return 0,0

def get_widths(words):
    font: Font = ASSETS["FONTS"]["monospace"]
    return [[font.render(entry, 1, settings.COLORS_CHOICES["BLACK"]).get_width() for entry in dev] for dev in words]

def get_height(word, font_name):
    font: Font = ASSETS["FONTS"][font_name]
    return font.render(word, 1, settings.COLORS_CHOICES["BLACK"]).get_height()

def load_background():
    images: dict[str, pg.Surface] = ASSETS["IMAGES"]
    background = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    background.blit(images["background"])
    center = (settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2)
    background.blit(images["ballista"], images["ballista"].get_rect(center=center))
    blur = pg.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pg.SRCALPHA)
    blur.set_alpha(100)
    blur.fill(settings.COLORS_CHOICES["DARK_GRAY"])
    background.blit(blur)
    return pg.transform.gaussian_blur(background, 5)