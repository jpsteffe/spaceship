# Python imports
import math
import random
import sys
from abc import ABCMeta, abstractmethod

# Library imports
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

# Set constants
WIDTH = 600
HEIGHT = 600

# Initialize pygame
pygame.init()

# Setup the pygame window
mainClock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceship')

# Setup pygame constants
FONT_LARGE = pygame.font.SysFont(None, 36)
FONT_SMALL = pygame.font.SysFont(None, 20)

# Load game assets
menu = pygame.image.load('mainmenu.png').convert()
pausebg = pygame.image.load('pausebg.png').convert()

background = pygame.image.load('stars.gif').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bombpic = pygame.image.load('bomb.jpg').convert()
bombpic = pygame.transform.scale(bombpic, (20, 20))
bombpic.set_colorkey(THECOLORS['white'])

playerpic = pygame.image.load('spaceship.png').convert()
playerpic = pygame.transform.scale(playerpic, (30, 30))
playerpic.set_colorkey(THECOLORS['white'])

rockpic = pygame.image.load('rock.png').convert()
rockpic.set_colorkey(THECOLORS['white'])

explosion = pygame.image.load('explosion.jpg')
explosion = pygame.transform.scale(explosion, (60, 60))
explosion.set_colorkey(THECOLORS['white'])


def exit_game():
    # Cleanup resources and quit the game
    sys.exit()


class State:
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass  # Return next state or self to stay on current state


class MainMenuState(State):
    def __init__(self):
        self.play_rect = pygame.Rect(window.get_rect().centerx - 55,
                                     window.get_rect().centery - 90,
                                     125, 55)
        self.options_rect = pygame.Rect(window.get_rect().centerx - 75,
                                        window.get_rect().centery - 20,
                                        167, 55)
        self.highscores_rect = pygame.Rect(window.get_rect().centerx - 110,
                                           window.get_rect().centery + 45,
                                           250, 55)
        self.quit_rect = pygame.Rect(window.get_rect().centerx - 45,
                                     window.get_rect().centery + 105,
                                     105, 45)

    def draw(self):
        # Draw the background image to erase the previous screen
        window.blit(menu, (0, 0))

        # If the mouse is in a menu option rectangle then draw a line around it
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.play_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.play_rect, 2)

        if self.options_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.options_rect, 2)

        if self.highscores_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.highscores_rect, 2)

        if self.quit_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.quit_rect, 2)

        pygame.display.update()

    def handle_event(self, event):
        # Handle window close events
        if event.type == QUIT:
            exit_game()

        # Pressing escape also closes the game
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit_game()

        if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if self.play_rect.collidepoint(mouse_x, mouse_y):
                return GameState()

            if self.options_rect.collidepoint(mouse_x, mouse_y):
                return self

            if self.highscores_rect.collidepoint(mouse_x, mouse_y):
                return self

            if self.quit_rect.collidepoint(mouse_x, mouse_y):
                exit_game()
        return self


class GameState(State):
    def __init__(self):
        self.game_over = False
        self.score = 1

        self.player = pygame.Rect(window.get_rect().centerx, window.get_rect().centery, 30, 30)
        self.speed = 6
        self.moveleft = False
        self.moveright = False
        self.moveup = False
        self.movedown = False

        self.bombs = []

        self.rocks = []
        self.num_rocks = 5
        self.spawn_rect = pygame.Rect(0, -40, WIDTH, 40)
        for i in range(self.num_rocks):
            self.rocks.append(self.spawn_rock())

    def spawn_rock(self):
        rocksize = random.randint(20, 40)
        rockx = random.randint(self.spawn_rect.left, self.spawn_rect.right)
        rocky = random.randint(self.spawn_rect.top, self.spawn_rect.bottom)
        x_dist = self.player.centerx - rockx
        y_dist = self.player.centery - rocky
        total_dist = math.sqrt((x_dist ** 2) + (y_dist ** 2))
        return {'rect': pygame.Rect(rockx, rocky, rocksize, rocksize),
                'xspeed': x_dist / total_dist,
                'yspeed': y_dist / total_dist,
                'pic': pygame.transform.scale(rockpic, (rocksize, rocksize))}

    def spawn_bomb(self):
        mousex, mousey = pygame.mouse.get_pos()
        x_dist = mousex - self.player.centerx
        y_dist = mousey - self.player.centery
        total_dist = math.sqrt((x_dist ** 2) + (y_dist ** 2))
        return {'rect': pygame.Rect(self.player.centerx, self.player.centery, 15, 15),
                'xspeed': x_dist / total_dist,
                'yspeed': y_dist / total_dist,
                'pic': bombpic,
                'exploded': False,
                'explosion_counter': 10}

    def draw(self):
        # Draw the background
        window.fill(THECOLORS['black'])
        window.blit(background, (0, 0))

        # Move the player
        if self.moveleft:
            self.player.left -= self.speed
        if self.moveup:
            self.player.top -= self.speed
        if self.movedown:
            self.player.bottom += self.speed
        if self.moveright:
            self.player.right += self.speed
        self.player.clamp_ip(window.get_rect())

        # Rotate the player
        mousex, mousey = pygame.mouse.get_pos()

        # Subtract player x from mouse x to match atan2 expected inputs
        player_angle_x = mousex - self.player.centerx
        player_angle_y = self.player.centery - mousey

        # Subtract 135 degrees to offset the angle of the spaceship in the image
        rotation = math.degrees(math.atan2(player_angle_y, player_angle_x)) - 135

        player_rotated = pygame.transform.rotate(playerpic, rotation)
        window.blit(player_rotated, self.player)

        # Move the bombs
        self.bombs = [bomb for bomb in self.bombs
                      if bomb['rect'].colliderect(window.get_rect()) and bomb['explosion_counter'] > 0]
        for bomb in self.bombs:
            if bomb['exploded']:
                bomb['explosion_counter'] -= 1
                window.blit(explosion, bomb['rect'])
            else:
                bomb['rect'].centerx += bomb['xspeed'] * self.speed
                bomb['rect'].centery += bomb['yspeed'] * self.speed
                window.blit(bomb['pic'], bomb['rect'])

                # Remove a rock from the list if it was hit and start the explosion counter
                rock_index = bomb['rect'].collidelist([r['rect'] for r in self.rocks])
                if rock_index != -1:
                    self.rocks.pop(rock_index)
                    self.rocks.append(self.spawn_rock())
                    bomb['exploded'] = True

        # Move the rocks
        self.rocks = [rock for rock in self.rocks
                      if rock['rect'].collidelist([window.get_rect(), self.spawn_rect]) != -1]
        for i in range(self.num_rocks - len(self.rocks)):
            self.rocks.append(self.spawn_rock())
            self.score += 1
        for rock in self.rocks:
            rock['rect'].centerx += rock['xspeed'] * self.speed
            rock['rect'].centery += rock['yspeed'] * self.speed

            window.blit(rock['pic'], rock['rect'])

        # Check for player collision
        if self.player.collidelist([rock['rect'] for rock in self.rocks]) != -1:
            self.game_over = True
            pygame.event.post(pygame.event.Event(USEREVENT, {}))

        # Every 50 points increase the number of rocks by 5
        if self.score % 50 == 0:
            self.num_rocks += 5
            self.score += 1

        # Draw the score
        window.blit(FONT_SMALL.render(str(self.score), True, THECOLORS['red'], THECOLORS['black']), (350, 25))

        pygame.display.update()
        mainClock.tick(40)

    def handle_event(self, event):
        # Handle window close events
        if event.type == QUIT:
            exit_game()

        if self.game_over:
            return GameOverState(self.score)

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                self.moveright = False
                self.moveleft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                self.moveright = True
                self.moveleft = False
            if event.key == K_UP or event.key == ord('w'):
                self.movedown = False
                self.moveup = True
            if event.key == K_DOWN or event.key == ord('s'):
                self.moveup = False
                self.movedown = True
            if event.key == K_ESCAPE:
                return PauseState(self)
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord('a'):
                self.moveleft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                self.moveright = False
            if event.key == K_UP or event.key == ord('w'):
                self.moveup = False
            if event.key == K_DOWN or event.key == ord('s'):
                self.movedown = False
        if event.type == MOUSEBUTTONUP:
            if len(self.bombs) < 5:
                self.bombs.append(self.spawn_bomb())
        return self


class GameOverState(State):
    def __init__(self, score):
        self.score = score

    def draw(self):
        game_over_text = FONT_LARGE.render('Game Over', True, THECOLORS['red'], THECOLORS['black'])
        text_rect = game_over_text.get_rect()
        text_rect.centerx = window.get_rect().centerx
        text_rect.centery = window.get_rect().centery
        window.blit(game_over_text, text_rect)

        score_text = FONT_LARGE.render('Your Score: ' + str(self.score), True, THECOLORS['red'], THECOLORS['black'])
        score_rect = score_text.get_rect()
        score_rect.centerx = window.get_rect().centerx
        score_rect.top = text_rect.bottom + 4
        window.blit(score_text, score_rect)

        continue_text = FONT_LARGE.render('Press SPACE to continue...', True, THECOLORS['red'], THECOLORS['black'])
        continue_rect = continue_text.get_rect()
        continue_rect.centerx = window.get_rect().centerx
        continue_rect.top = score_rect.bottom + 4
        window.blit(continue_text, continue_rect)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == QUIT:
            exit_game()

        if event.type == KEYUP and event.key == K_SPACE:
            return MainMenuState()

        return self


class PauseState(State):
    def __init__(self, prev_state):
        self.prev_state = prev_state
        self.resume_rect = pygame.Rect(window.get_rect().centerx - 50, window.get_rect().centery - 40, 96, 23)
        self.main_menu_rect = pygame.Rect(window.get_rect().centerx - 60, window.get_rect().centery + 5, 125, 25)
        self.quit_rect = pygame.Rect(window.get_rect().centerx - 30, window.get_rect().centery + 55, 55, 23)

    def draw(self):
        window.blit(pausebg, (window.get_rect().centerx - 100, window.get_rect().centery - 150))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.resume_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.resume_rect, 2)

        if self.main_menu_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.main_menu_rect, 2)

        if self.quit_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(window, THECOLORS['red'], self.quit_rect, 2)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == QUIT:
            exit_game()

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return self.prev_state

        if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if self.resume_rect.collidepoint(mouse_x, mouse_y):
                return self.prev_state

            if self.main_menu_rect.collidepoint(mouse_x, mouse_y):
                return MainMenuState()

            if self.quit_rect.collidepoint(mouse_x, mouse_y):
                exit_game()
        return self


def main():
    state = MainMenuState()
    while True:
        state.draw()
        for event in pygame.event.get():
            state = state.handle_event(event)


if __name__ == '__main__':
    main()
