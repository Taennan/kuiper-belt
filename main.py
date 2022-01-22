#
# Kuiper Belt
# v 1.0.01 (2020)
#

# First game built with Pygame

# The main module
import pygame
# Imports event handlers. Is not necessary, but did not want to be typing in pygame.<whatever> continuously
from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_RETURN,
    K_KP_ENTER,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    QUIT
)
# Allows access to randomizers
import random


# Extra functions
def make_space(lines, pre_statement="", post_statement=""):
    """Prints empty line in console with optional pre and post statements"""

    # If not an empty string, prints a value or string before empty lines
    if pre_statement == "":
        pass
    else:
        print(pre_statement)

    # Prints specified amount of empty lines
    for _ in range(lines):
        print("")

    # If not an empty string, prints a value or string before empty lines
    if post_statement == "":
        pass
    else:
        print(post_statement)


# Custom classes
class Player(pygame.sprite.Sprite):
    """Player object. Can be controlled by user"""

    def __init__(self, parent):
        super().__init__()

        # The parent surface self is added to
        self.parent = parent

        # Initialises a surface for the sprite
        self.surf = pygame.Surface((65, 25))

        self.surf.fill((255, 255, 255))  # The surface's colour. In this case, white

        self.width = self.surf.get_width()  # The surface's size
        self.height = self.surf.get_height()
        self.rect = self.surf.get_rect()

        # Sets whether self was hit by an enemy
        self.was_hit = False

        # The sprite's coordinates within parent
        self.x_coord = 0
        self.y_coord = 0

    def will_move(self, with_key):
        """Changes position of self when user gives input"""

        # How fast the player moves
        speed = 3

        if with_key[K_UP]:  # Up Arrow
            self.y_coord -= speed
        if with_key[K_DOWN]:  # Down Arrow
            self.y_coord += speed
        if with_key[K_LEFT]:  # Left Arrow
            self.x_coord -= speed
        if with_key[K_RIGHT]:  # Right Arrow
            self.x_coord += speed

        # Keeps self within parent boundaries
        self.did_move()

    def did_move(self):
        """Does any jobs after self has moved"""

        # Updates rect. This must be done to allow Pygame's collision detection methods to do their job
        self.rect = self.surf.get_rect().move(self.x_coord, self.y_coord)

        # Keeps self within scene boundaries
        parent_height = self.parent.get_height()
        parent_width = self.parent.get_width()

        if self.y_coord < 0:
            self.y_coord = 0
        if self.y_coord > parent_height - self.height:
            self.y_coord = parent_height - self.height
        if self.x_coord < 0:
            self.x_coord = 0
        if self.x_coord > parent_width - self.width:
            self.x_coord = parent_width - self.width


class Enemy(pygame.sprite.Sprite):
    """Object for enemy characters"""

    def __init__(self, parent):
        super().__init__()

        # Initialises a surface for the sprite
        self.surf = pygame.Surface((25, 15))

        self.surf.fill((255, 255, 255))  # The surface's colour. In this case, white

        self.width = self.surf.get_width()  # The surface's size
        self.height = self.surf.get_height()
        self.rect = self.surf.get_rect()

        # The sprite's coordinates within parent
        self.x_coord = parent.get_width() + self.width  # Sets x_coord off screen
        self.y_coord = random.randint(0, parent.get_height() - self.height)  # Randomizes y_coord

        # The speed at which self will travel
        self.speed = random.randint(1, 4)

    def will_move(self):
        """Moves self within game scene"""

        # Moves left
        self.x_coord -= self.speed

        self.did_move()

    def did_move(self):
        """Does any jobs after self has moved"""

        # Updates rect. This must be done to allow Pygame's collision detection methods to do their job
        self.rect = self.surf.get_rect().move(self.x_coord, self.y_coord)

        # Removes self from game if it has moved off left screen
        if self.x_coord < 0:
            self.kill()


class FontContainer:
    """This object contains strings representing fonts. Add more fonts later"""

    class SystemFonts:
        """This object contains fonts from the system. Check the app 'Fontbook' for all available fonts"""

        helvetica = "Helvetica"

    def __init__(self):

        self.sys = self.SystemFonts
fonts = FontContainer()


class SpriteLabel:
    """
    Label object used to display text in-game

        NOTE: These objects cannot be added to sprite groups
    """

    def __init__(self, text, font, size):

        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, (255, 255, 255), (0, 0, 0))

        self.rect = self.text.get_rect()
        self.pos = None

        # This is set depending on whether user can press self to call commands
        self.interaction_enabled = False

    def set_pos(self, x, y):

        self.pos = (x, y)


    def center_pos(self, parent, axis):
        """
        Calculates position of self to centre it on the specified axis within parent. Specify which axis to center
        using strings ("x", "X", "y", "Y")
        """

        if axis == "x" or "X":
            # Centers along parent's X-axis
            width = parent.get_width()
            return (width / 2) - (self.rect.width / 2)

        elif axis == "y" or "Y":
            # Centers along parent's Y-axis
            height = parent.get_height()
            return (height / 2) - (self.rect.height / 2)

        else:
            # Raises error if non-compatible arguments are called
            raise RuntimeError("Invalid argument entered in center_pos method in SpriteLabel object")


    def was_clicked(self, at_point, accept_inside=True):

        width = self.rect.width
        height = self.rect.height

        point_x = at_point[0]
        point_y = at_point[1]

        if self.interaction_enabled:
            # Passes
            if self.pos is None:
                raise RuntimeError("No positional arguments given to was_clicked() method for SpriteLabel object")

            # Runs actions
            else:

                if accept_inside:

                    if self.pos[0] <= point_x <= self.pos[0] + width:
                        if self.pos[1] <= point_y <= self.pos[1] + height:
                            # Returns Bool value to be used in event handling
                            make_space(1, post_statement="Start button pressed. Game will start")
                            return True

                else:
                    # This isn't actually working yet. It won't be used in-game though
                    pass

                    if self.pos[0] >= point_x >= self.pos[0] + width:
                        if self.pos[1] >= point_y >= self.pos[1] + height:
                            # Returns Bool value to be used in event handling
                            return True

                        else:
                            print("FAIL 1")
                    else:
                        print("FAIL 2")


# Game Class
class Game:
    """Object which encapsulates the main game"""
    test = 1

    def __init__(self):
        """Initialises pygame and runs game loop"""

        # Pygame must be initialised to access
        pygame.init()


        # Starts and stops the mainloop
        self.will_quit = False


        # Contains strings representing game layers
        self.menu_layer = "menu"
        self.game_layer = "game"
        # Sets layer that is currently shown
        self.current_layer = self.menu_layer


        # The window
        self.scene_width = 800
        self.scene_height = 500

        # NOTE: The scene colour must be filled in the game loops for animations to run properly
        self.scene = pygame.display.set_mode((self.scene_width, self.scene_height))
        pygame.display.set_caption("Kuiper Belt")


        # Instantiates a clock and sets maximum frame rate
        self.clock = pygame.time.Clock()
        self.clock.tick(50)


        # Sprites
        # Instantiates a player character
        self.player = Player(self.scene)
        # Sets player position in the centre of the scene
        self.player.x_coord = self.scene_width / 2
        self.player.y_coord = self.scene_height / 2

        # Creates a title label and start button for main menu
        self.title = SpriteLabel("KUIPER BELT", fonts.sys.helvetica, 50)
        self.start_btn = SpriteLabel("START!", fonts.sys.helvetica, 20)
        self.start_btn.interaction_enabled = True   # Allows interaction with start_btn

        # Sprite Groups
        self.all_enemies = pygame.sprite.Group()   # Contains enemy sprites only
        self.game_sprites = pygame.sprite.Group()  # Contains player and enemy sprites

        self.game_sprites.add(self.player)                  # Adds the player to game_sprites


        # Custom events. These are created so pygame can run them with the other events in the queue
        # Pygame classifies all events in integers (the last one being USEREVENT)
        # Adding 1 to the last event ensures that custom events are unique

        # Does what it says. A timer is set so ADD_ENEMY is called every 250 milliseconds
        self.ADD_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_ENEMY, 250)

        # Does what it says. Called whenever the 'start' button is pressed
        self.START_GAME = self.ADD_ENEMY + 1


        # Starts Game
        make_space(1, post_statement="Kuiper Belt opened")
        print("")
        self.start_game()


    def start_game(self):
        """Starts game. Any jobs that must be done before the gameloop starts is done here"""

        # Game loop
        print("Game Started")
        make_space(1)
        self.gameloop()


    def gameloop(self):
        """Runs the game until user terminates"""

        # Main loop
        while not self.will_quit:

            # Menu Loop
            while self.current_layer == self.menu_layer:

                # Resets player
                self.player.was_hit = False

                # Sets scene colour
                self.scene.fill((0, 0, 0))

                # Blits title and start button to scene
                self.title.set_pos(self.title.center_pos(self.scene, "x"), self.scene_height * 0.25)
                self.scene.blit(self.title.text, self.title.pos)

                self.start_btn.set_pos(self.start_btn.center_pos(self.scene, "x"), self.scene_height / 2)
                self.scene.blit(self.start_btn.text, self.start_btn.pos)

                # Checks if start button has been pressed
                self.handle_events()

                # Flips display. Must be called to render a new frame
                pygame.display.flip()


            # Does any jobs before moving to game layer

            # Removes all enemies
            for enemy in self.all_enemies:
                enemy.kill()

            # Re-sets player position
            self.player.x_coord = self.scene.get_width() / 2
            self.player.y_coord = self.scene.get_height() / 2


            # Game loop
            while self.current_layer == self.game_layer:

                # Handles events and key presses
                self.handle_events()
                self.handle_keydown()

                # Sets scene colour
                self.scene.fill((0, 0, 0))

                # Moves all enemies forward
                for enemy in self.all_enemies:
                    enemy.will_move()

                # Draws sprites in scene
                for sprite in self.game_sprites:
                    self.scene.blit(sprite.surf, (sprite.x_coord, sprite.y_coord))

                # Checks if player has collided with enemies
                self.check_collisions()

                # Flips display. Must be called to render a new frame
                pygame.display.flip()


    def check_collisions(self):
        """Does what it says"""

        # Ends loop and restarts game from main menu
        if pygame.sprite.spritecollideany(self.player, self.all_enemies):
            self.current_layer = self.menu_layer
            print("Player hit. GAME OVER")


    def handle_events(self):
        """Does what it says. This method shows one way events can be handled"""

        for event in pygame.event.get():

            # Runs regardless
            # Terminates game
            if event.type == QUIT:
                # Removes the current layer and breaks mainloop
                self.current_layer = None
                self.will_quit = True
                print("Exit button pressed. Kuiper Belt will quit")


            # Only runs when game has started
            # Runs custom "ADD_ENEMY" event
            elif event.type == self.ADD_ENEMY and self.current_layer == self.game_layer:
                # Instantiates a new enemy
                enemy = Enemy(self.scene)
                # Adds enemy to sprite groups
                self.all_enemies.add(enemy)
                self.game_sprites.add(enemy)


            # Only runs while game is still in main menu
            # Detects presses on start button in main menu
            elif event.type == MOUSEBUTTONDOWN and self.current_layer == self.menu_layer:
                pos = pygame.mouse.get_pos()
                clicked = self.start_btn.was_clicked(pos)

                # If start_btn.was_clicked() returns true, starts gameloop
                if clicked:
                    self.current_layer = self.game_layer

            # Detects whether game was started by pressing RETURN or ENTER keys
            elif event.type == K_RETURN or event.type == K_KP_ENTER and not self.current_layer == self.menu_layer:
                self.current_layer = self.game_layer
                print("Enter or Return key pressed. Game will start")


            # Handles key presses
            elif event.type == KEYDOWN:

                # Runs regardless of current layer
                if event.key == K_ESCAPE:
                    # Removes the current layer and breaks mainloop
                    self.current_layer = None
                    self.will_quit = True
                    print("Escape key pressed. Kuiper Belt will quit")

                # Only runs while game is still in main menu
                # Detects whether game was started by pressing the RETURN key
                elif event.key == K_RETURN and self.current_layer == self.menu_layer:
                    self.current_layer = self.game_layer
                    print("Enter or Return key pressed. Game will start")
                # Detects whether game was started by pressing the Numpad ENTER key
                elif event.key == K_KP_ENTER and self.current_layer == self.menu_layer:
                    self.current_layer = self.game_layer
                    print("Enter or Return key pressed. Game will start")


    def handle_keydown(self):
        """Does what it says. This method only handles key presses"""

        # Gets keys pressed
        keys_pressed = pygame.key.get_pressed()

        # Moves player
        self.player.will_move(keys_pressed)


# Instantiates game
game = Game()

# When the game's loops are broken, quits pygame
make_space(1, post_statement="Kuiper Belt terminated")
pygame.quit()
