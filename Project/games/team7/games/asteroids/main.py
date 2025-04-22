import pygame, sys
from assets import GameDataLink
import math
import csv
import random
import time
from pygame.locals import *

pygame.init()

"""
Asteroids Game Project

Contributors: Dylan G. and Vendula P.

Collaboration Note:
All contributors worked on all aspects of the game, but the primary division of tasks was as follows:
- Dylan G. focused primarily on the Game class.
- Vendula P. focused on the Player, Projectile, and Obstacle classes.
"""

# Create a 1000x800 window 
WIDTH, HEIGHT = 1000, 800
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASTEROIDS")

# Define constants in the program
FPS = 80
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
BLACK = (0, 0, 0)


class Game:
    
    def __init__(self, csv_path = None):
        self.game_data = GameDataLink.get_data()
        self.game_data["neededPoints"] = 1
        self.game_data["text"] = "This is a game based on ASTEROIDS. The user must attempt to shoot the word they are searching for to win!"

        self.linguistic_data = None
        self.word_search = None
        self.word_definition = None
        self.player_input = {"right": False, "left": False, "up": False, "down": False, "space": False}
        
        self.player = Player()
        self.obstacles = set()
        self.projectiles = set()
        self.obstacle_timer = time.time() # Timer to control obstacle spawning intervals
        self.game_state = "menu"

        if csv_path:
            # Load noun linguistic data from CSV file into a dictionary
            self.linguistic_data = self.load_data(csv_path)


    def draw_window(self):
        # Clear screen with black background
        DISPLAYSURF.fill(BLACK) 


    def load_data(self, csv_path):
        # Load noun linguistic data from the csv file into a dictionary
        linguistic_data = {}
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if not self.word_search:
                    # Assuming first word in the file is the one to search
                    self.word_search = row['noun']
                    self.word_definition = row['definition']

                # Use noun as key, store entire row
                linguistic_data[row['noun']] = row
        
        return linguistic_data
    

    def get_random_word(self):
        # Select a random word from the linguistic data
        return random.choice(list(self.linguistic_data.keys()))


    def outside_window(self, coords):
        # Check if coordinates are outside the window with a buffer zone
        buffer = 50
        if isinstance(coords[0], list):
            # Calculate the average position (center) of all points (when handling asteroids)
            avg_x = sum(point[0] for point in coords) / len(coords)
            avg_y = sum(point[1] for point in coords) / len(coords)
            x, y = avg_x, avg_y
        else:  
            # Single point (when handling projectiles)
            x, y = coords
        
        # Check if calculated (x,y) coordinates fall outside the game window (including buffer)
        return (x < -buffer or x > WIDTH+buffer or y < -buffer or y > HEIGHT+buffer)
    

    def check_input(self, key, value):
        if key == pygame.K_w or key == pygame.K_UP:
            # W or up arrow on keyboard enable forward movement
            self.player_input["up"] = value
        elif key == pygame.K_a or key == pygame.K_LEFT:
            # A or left arrow on keyboard enable left turning movement
            self.player_input["left"] = value
        elif key == pygame.K_s or key == pygame.K_DOWN:
            # S or down arrow on keyboard enable backward movement
            self.player_input["down"] = value
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            # D or right arrow on keyboard enable left turning movement
            self.player_input["right"] = value
        elif key == pygame.K_SPACE:
            # Space bar enables spaceship ability (shooting projectiles)
            self.player_input["space"] = value


    def line_segments_intersect(self, line1, line2):
        # Extract coordinates of the line segments
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]
        
        # Calculate denominators
        den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        
        # If denominator is zero, lines are parallel, so they aren't intersecting
        if den == 0:
            return False
        
        # Compute parametric values for intersection point
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
        
        # Check if intersection point lies within both line segments
        return 0 <= ua <= 1 and 0 <= ub <= 1
    

    def point_in_polygon(self, point, polygon):
        # Check if a point is inside a polygon using the ray casting algorithm.
        # This algorithm works by drawing a horizontal ray from the given point 
        # and counting how many times it intersects the polygon's edges. 
        # If the number of intersections is odd, the point is inside; if even, the point is outside.
        x, y = point
        n = len(polygon)
        inside = False
        
        # Initialize by starting with the first vertex
        p1x, p1y = polygon[0] 
        
        # Loop through all edges
        for i in range(n + 1):
            p2x, p2y = polygon[i % n] # Make sure to wrap around to the first point

            # Check if horizontal ray from (x,y) intersects the edge (p1,p2)
            if y > min(p1y, p2y): # Point is above lower endpoint
                if y <= max(p1y, p2y): # Point is below higher endpoint
                    if x <= max(p1x, p2x): # Point is to the left of the rightmost endpoint
                        if p1y != p2y: # Avoid division by zero (vertical line segment)
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters: # Check if intersection is to the right of the point
                            inside = not inside # Flip the inside status
            
            # Move to the next edges
            p1x, p1y = p2x, p2y
        
        return inside


    def player_collision(self):
        '''
        Handle collision between player and obstacle (asteroid)
        '''

        # Get player's polygon coordinates
        player_coords = self.player.get_coordinates()
    
        for obstacle in self.obstacles:
            obstacle_coords = obstacle.get_coordinates()
            obstacle_coords.append(obstacle_coords[0])  # Close the polygon

            # Iterate over each edge of the player's shape
            for i in range(len(player_coords)):
                player_segment = [player_coords[i], player_coords[(i+1) % len(player_coords)]]
                
                # Iterate over each edge of the obstacle
                for j in range(len(obstacle_coords)-1):
                    obs_segment = [obstacle_coords[j], obstacle_coords[j+1]]
                    
                    # Check if the player's edge intersects with the obstacle's edges
                    if self.line_segments_intersect(player_segment, obs_segment):
                        # Set game state to loss if collision detected
                        self.game_state = "loss"
                        return True 
        return False
        


    def projectile_collision(self):
        '''
        Handle collisions between projectiles and obstacles
        '''
        remove_obstacles = set() # Store obstacle to be removed
        remove_projectiles = set() # Store projectiles to be removed
        new_obstacles = [] # Store new obstacles created from splitting larger asteroids

        for projectile in self.projectiles:
            # Get projectile's position
            projectile_pos = projectile.get_coordinates()
            collision_detected = False

            for obstacle in self.obstacles:
                obstacle_coords = obstacle.get_coordinates()
                obstacle_coords.append(obstacle_coords[0]) # Close polygon

                # Check if projectile is inside the obstacle
                if self.point_in_polygon(projectile_pos, obstacle_coords):
                    
                    texts = None
                    if obstacle.size == "large":
                        # Check if obstacle contains the target word for a win condition
                        if obstacle.text == self.word_search:
                            self.game_state = "win"
                            self.game_data["earnedPoints"] += 1
                            return 
                        
                        # Split large obstacles into 2-4 pieces
                        num_pieces = random.randint(2,4)

                        # If linguistic data is available, assign the definition to the new pieces
                        if self.linguistic_data:
                            texts = [self.linguistic_data[obstacle.text]['definition'] for _ in range(num_pieces)]
                    
                    elif obstacle.size == "medium":
                        # Split medium obstacle into 1-3 pieces
                        num_pieces = random.randint(1,3)

                    else: 
                        # Small obstacles do not split further
                        num_pieces = 0

                    # Generate smaller obstacles from the split
                    split_asteroids = obstacle.split(num_pieces,texts)
                    new_obstacles.extend(split_asteroids)

                    # Mark the obstacle and projectile for removal
                    remove_obstacles.add(obstacle)
                    remove_projectiles.add(projectile)
                    collision_detected = True
                    break # Exit inner loop, projectile can only hit one obstacle

            if collision_detected:
                break # Exit outer loop if collision is found to avoid multiple removals

        # Remove destroyed obstacles and projectiles 
        for obstacle in remove_obstacles:
            self.obstacles.remove(obstacle)
        
        for projectile in remove_projectiles:
            self.projectiles.remove(projectile)

        # Add new obstacles resulting from splits
        for new_obstacle in new_obstacles:
            self.obstacles.add(new_obstacle)            


    def draw_menu(self, title, subtitle, button_texts, button_actions, game_won=None):
        '''
        General method to draw menus (Main or End Game) with customizable title, subtitle, and button actions.
        '''
        # Menu dimensions and position
        menu_width = 400
        menu_height = 300
        menu_x = (WIDTH // 2) - (menu_width // 2)
        menu_y = (HEIGHT // 2) - (menu_height // 2)
        
        # Draw menu background with grey rectangle and white border
        pygame.draw.rect(DISPLAYSURF, GREY, [menu_x, menu_y, menu_width, menu_height])
        pygame.draw.rect(DISPLAYSURF, WHITE, [menu_x, menu_y, menu_width, menu_height], 3)
        
        # Draw the title and subtitle
        title_font = pygame.font.SysFont("Times New Roman", 35)
        title_text = title_font.render(title, True, WHITE)
        subtitle_text = title_font.render(subtitle, True, (255, 150, 50))
        
        # Position the title and subtitle text on the screen
        title_rect = title_text.get_rect(center=(WIDTH // 2, menu_y + 50))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, menu_y + 90))
        
        # Draw the title and subtitle on the screen
        DISPLAYSURF.blit(title_text, title_rect)
        DISPLAYSURF.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        button_font = pygame.font.SysFont('Sans', 20)
        button_height = 50
        button_width = 200
        button_y_start = menu_y + 150 # Set starting vertical position for buttons
        
        # Loop through buttons and draw them
        for i, text in enumerate(button_texts):
            button = pygame.Rect(menu_x + 100, button_y_start + (i * 70), button_width, button_height) # Define the button's position and size
            pygame.draw.rect(DISPLAYSURF, (0, 100, 0) if i == 0 else (150, 0, 0), button)  # Green for Start, Red for Quit
            pygame.draw.rect(DISPLAYSURF, WHITE, button, 2) # White border around the button
            
            button_text = button_font.render(text, True, WHITE)
            button_rect = button_text.get_rect(center=button.center)
            DISPLAYSURF.blit(button_text, button_rect)
        
        # Handle button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if mouse_click[0]:  # Left mouse click
            # Check if either of the butons are clicked
            for i, button in enumerate([pygame.Rect(menu_x + 100, menu_y + 150, button_width, button_height),
                                        pygame.Rect(menu_x + 100, menu_y + 220, button_width, button_height)]):
                if button.collidepoint(mouse_pos): # If mouse within the button's area
                    # Execute the appropriate action for the button clicked
                    if button_actions[i] == "start":
                        return "start"
                    elif button_actions[i] == "quit":
                        # Handle end game scenario
                        if self.game_data["earnedPoints"] >= self.game_data["neededPoints"]:
                            self.game_data["rewardText"] = "Well done! Here is a tip: 'zhavvorsa' in Dothraki means 'dragon'"
                        GameDataLink.send_data(self.game_data)
                        pygame.quit()
                        sys.exit()  # Exit the game
        
        # Return to the main menu if no action was taken
        return "menu" if game_won is None else ("win" if game_won else "loss")


    def main_menu(self):
        # Call the draw_menu method to draw the main menu
        return self.draw_menu("Linguistic Asteroids", "(in Dothraki!)", ["Start", "Quit"], ["start", "quit"])
    

    def end_game(self, game_won=True):
        # Set the title based on whether the game was won or lost
        title = "YOU WIN" if game_won else "YOU LOSE"
        
        # Set the subtitle based on whether the player won; if they won, show the word search and definition
        subtitle = f"{self.word_search} : {self.word_definition}" if game_won else ""

        # Call the draw_menu method to draw the end game menu
        return self.draw_menu(title, subtitle, ["Play Again", "Quit"], ["start", "quit"], game_won)


    def draw_search_word(self):
        word_font = pygame.font.SysFont("Arial", 30)
        
        # Render the text to display the current search word
        word_surface = word_font.render(f"searching for: {self.word_search}", True, WHITE)

        # Position the word at the top-right of the screen with a margin of 10 pixels
        word_rect = word_surface.get_rect()
        word_rect.topright = (WIDTH - 10, 10)

        DISPLAYSURF.blit(word_surface, word_rect)


    def loop(self):
        projectile_timer = 0 # Timer to control shooting intervals (prevent ontinuous shooting)
        obstacle_wait = 2 # Initial time to wait before spawning obstacles
        clock = pygame.time.Clock() # Clock object to manage FPS

        # Main game event loop
        while True:
            # Control frame rate by limiting the game loop to FPS
            clock.tick(FPS)

            self.handle_events() # Handle user inputs and events
            self.draw_window() # Draw the game window

            if self.game_state == "menu":
                self.handle_menu()
            elif self.game_state in {"win", "loss"}:
                self.handle_end_game()
            else:
                self.draw_search_word()
                projectile_timer, obstacle_wait = self.update_gameplay(projectile_timer, obstacle_wait)

            pygame.display.update()  # Update the display
    

    def handle_events(self):
        # Handle all events (keyboard presses/releases, quit)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and self.game_state == "play":
                # Process key down (pressed) events and game state is "play"
                self.check_input(event.key, True)
            
            elif event.type == KEYUP and self.game_state == "play":
                # Process key up (unpressed) events and game state is "play"
                self.check_input(event.key, False)

    
    def handle_menu(self):
        # Handle game menu logic
        if self.main_menu() == "start":
            self.start_new_game()
    

    def handle_end_game(self):
        # Handles win/loss screen logic
        if self.end_game(self.game_state == "win") == "start":
            self.player_input = {"right": False, "left": False, "up": False, "down": False, "space": False}
            self.start_new_game()
        

    def start_new_game(self):
        # Reset game state and start a new game
        self.game_state = "play"
        self.player = Player()
        self.obstacles = set()
        self.projectiles = set()
        self.obstacle_timer = time.time()
    

    def update_gameplay(self, projectile_timer, obstacle_wait):
        '''
        Update all gameplay mechanics (movement, shooting, collisions)
        '''
        # Calculate player rotation based on left and right input
        angle_dif = self.player_input["right"] - self.player_input["left"] 
        self.player.update_orientation(angle_dif)

        # Update player's position if "up" key pressed
        if self.player_input["up"]:    
            self.player.update_xy()
        # Update player's position if "down" key pressed
        if self.player_input["down"]:
            self.player.update_xy(False)

        # Shoot projectile if the "space" key is processed (at most once every 0.25 seconds)
        if self.player_input["space"] and time.time() - projectile_timer >= 0.25:
            self.projectiles.add(self.player.shoot()) # Create and add new projectile
            projectile_timer = time.time() 

        # Spawn a new obstacle if the obstacle timer exceeds the wait time
        if time.time() - self.obstacle_timer > obstacle_wait:
            text = self.get_random_word() if self.linguistic_data else None # Get random word if linguistic data is available
            self.obstacles.add(Obstacle(text)) # Create and add new obstacle
            self.obstacle_timer = time.time()
            obstacle_wait = random.randrange(1,2) # Randomaly set next obstacle wait time
        
        # Remove off-screen obstacles and projectiles
        self.obstacles = {o for o in self.obstacles if not self.outside_window(o.get_coordinates())}
        self.projectiles = {p for p in self.projectiles if not self.outside_window(p.get_coordinates())}

        # Draw game objects
        for obj in self.obstacles | self.projectiles | {self.player}:
            obj.draw()

        # Check for projectile collisions with player and obstacles
        self.player_collision()

        # Check for projectile collisions with projectile and obstacles
        self.projectile_collision()

        return projectile_timer, obstacle_wait



class Player:
    SPEED = 3 # Movement spped of the player
    points = [(0, -25), (-20, 25), (20, 25)] # Triangle shape points

    def __init__(self):
        self.x = 0 # Player x position relative to screen center
        self.y = 0 # Player y position relative to screen center
        self.orientation = 0 # Angle of rotation (0 degrees points up)

        
    def shoot(self):
        # Create projectile at front of the player's ship
        coordinates = self.get_coordinates()
        front_x, front_y = coordinates[0][0], coordinates[0][1] # Front tip of the triangle
        return Projectile(front_x, front_y, self.orientation) # Fire projectile in player's direction


    def get_coordinates(self):
        # Calculate coordinates of player's triangular shape based on its orientation.
        center_x, center_y = WIDTH // 2 + self.x, HEIGHT // 2 + self.y # Convert to screen coordinates
        rotated_points = [self.__rotate_point(point) for point in self.points] # Rotate shape based on orientation 

        return [[center_x + rotated_points[0][0], center_y + rotated_points[0][1]], 
            [center_x + rotated_points[1][0], center_y + rotated_points[1][1]], 
            [center_x + rotated_points[2][0], center_y + rotated_points[2][1]]]


    def update_xy(self, move_up=True):
        # Move player in the direction it is facing.
        x_dif = self.SPEED * math.cos(math.radians(self.orientation - 90))
        y_dif = self.SPEED * math.sin(math.radians(self.orientation - 90))

        if move_up:
            self.x += x_dif
            self.y += y_dif
        else:
            self.x -= x_dif
            self.y -= y_dif


    def update_orientation(self, angle_dif):
        # Rotate player by given angle difference.
        self.orientation = (self.orientation + self.SPEED * angle_dif) % 360


    def draw(self):
        # Draw player's ship on the screen.
        coordinates = self.get_coordinates()
        pygame.draw.polygon(DISPLAYSURF, WHITE, coordinates, 5)


    def __rotate_point(self, point):
        # Rotate a point around the player's center based on it's orientation.
        rad = math.radians(self.orientation)
        x, y = point 
        new_x = x * math.cos(rad) - y * math.sin(rad)
        new_y = x * math.sin(rad) + y * math.cos(rad)
        return new_x, new_y



class Projectile:
    SPEED = 5 # Speed of the projectile

    def __init__(self, x, y, orientation):
        # Initialize projectile at the given position and direction
        self.x = x
        self.y = y
        self.orientation = orientation # Direction in which projectile is moving

    def update(self):
        # Move the projectile in its set direction
        self.x += self.SPEED * math.cos(math.radians(self.orientation - 90))
        self.y += self.SPEED * math.sin(math.radians(self.orientation - 90))

    def get_coordinates(self):
        # Return projectile's current coordinates.
        return [self.x, self.y]

    def draw(self):
        # Update and draw the projectile as a small circle.
        self.update() # Move projectile before drawing
        pygame.draw.circle(DISPLAYSURF, WHITE, (self.x, self.y), 4)



class Obstacle:
    SPEED = 2 # Speed of the obstacle

    def __init__(self, text = None, size = "large", x = None, y = None, orientation = None):
        self.text = text
        self.size = size # Size of the obstacle (large, medium, small)
        self.points = self.__generate_points() # Generate shape of the obstacle

        # If no position is given, generate random trajectory
        if x is None or y is None or orientation is None: 
            self.x, self.y, self.orientation = self.__generate_trajectory()
        else:
            self.x = x
            self.y = y
            self.orientation = orientation


    def update(self):
        self.x += self.SPEED * math.cos(math.radians(self.orientation - 90))
        self.y += self.SPEED * math.sin(math.radians(self.orientation - 90))


    def split(self,num_pieces=2,texts=None):
        # Split large or medium asteroids into smaller pieces
        if self.size == "small":
            # Small obstacles don't split further
            return []
        
        new_size = "medium" if self.size == "large" else "small"
        new_asteroids = []

        for i in range(num_pieces):
            # Create new asteroids traveling in new direction from a slight offset position
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)

            # Generate new direction for the obstacle, so they do not overlap when moving
            new_orientation = (self.orientation + random.randint(-45, 45)) % 360

            new_asteroid = Obstacle(
                text = texts[i] if texts else None,
                size = new_size,
                x = self.x + offset_x,
                y = self.y + offset_y,
                orientation = new_orientation
            )

            # Speed up the smaller asteroids slightly
            if new_size == "medium":
                new_asteroid.SPEED = self.SPEED * 1.2
            else:
                new_asteroid.SPEED = self.SPEED * 1.5

            new_asteroids.append(new_asteroid)
        
        return new_asteroids


    def get_coordinates(self):
        # Return the coordinates of the obstacle shape.
        return [[self.x + p[0], self.y + p[1]] for p in self.points]
    

    def draw(self):
        # Update and draw the obstacle, possibly with text
        self.update()
        coordinates = self.get_coordinates()
        pygame.draw.polygon(DISPLAYSURF, WHITE, coordinates, 3)
        
        # Only add text to larger asteroids (large or medium)
        if self.text:
            font = pygame.font.SysFont('Arial', 25).render(self.text, True, (255,0,0))
            # Define offset for larger and medium obstacles
            offset = 10 if self.size == "large" else 5
            DISPLAYSURF.blit(font,(coordinates[0][0] + offset, coordinates[0][1] + offset))


    def __generate_points(self):
        # Generate a random obstacle shape for the obstacle using predefined x and y coordinate ranges
        scale = 1.0
        if self.size == "medium":
            scale = 0.5
        if self.size == "small":
            scale = 0.25
        
        # Define possible x and y coordinate ranges for the obstacle shape
        x_ranges = [(-55*scale, -45*scale), (20*scale, 30*scale), (30*scale, 40*scale), 
                    (35*scale, 45*scale), (-35*scale, -25*scale), (-65*scale, -55*scale), (-55*scale, -45*scale)]
        y_ranges = [(-55*scale, -45*scale), (-45*scale, -35*scale), (-30*scale, -20*scale), 
                    (5*scale, 15*scale), (20*scale, 30*scale), (10*scale, 20*scale), (-15*scale, -5*scale)]
        
        # Generate points using the ranges 
        points = []
        for x_range, y_range in zip(x_ranges, y_ranges):
            # Convert range endpoints to integers to work with randint
            x_min, x_max = int(x_range[0]), int(x_range[1])
            y_min, y_max = int(y_range[0]), int(y_range[1])
            
            # Randomly select point with the range (ensure non-zero range)
            x_point = random.randint(x_min, x_max) if x_min != x_max else x_min
            y_point = random.randint(y_min, y_max) if y_min != y_max else y_min
            
            points.append((x_point, y_point))
        
        return points
    

    def __generate_trajectory(self):
        # NOTE: Pygame coordinate system:
        # - The origin (0,0) at top-left corner of screen
        # - 0° points right, 90° points down, 180° left, 270° up.

        # Randomly select an orientation (angle in degrees)
        orientation = random.randint(0, 359)

        # Determine the opposite direction (180° from the chosen orientation)
        opposite = (orientation + 180) % 360

        # Generate random starting angle slightly offset from opposite direction 
        start_angle = (random.randint(opposite - 10, opposite + 10)) % 360

        # Set spawn distance beyond the screen boundaries
        spawn_distance = max(WIDTH, HEIGHT) // 2

        # Calculate spawn position with -90 degree offset to handle Pygame's angle system
        spawn_x = WIDTH // 2 + spawn_distance * math.cos(math.radians(start_angle-90))
        spawn_y = HEIGHT // 2 + spawn_distance * math.sin(math.radians(start_angle-90))
        
        return spawn_x, spawn_y, orientation


def main():
    # Initialize and start game loop using specified CSV file for game assets.
    game = Game('games/asteroids/game_assets/dothraki.csv')
    game.loop()


if __name__ == "__main__":
    main()