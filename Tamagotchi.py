import pygame
from PIL import Image
import time
import threading
from text_render import render_text
from Button import *
import json
import sys

# Function to handle text input
def get_name():
    pygame.init()
    name_window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Enter your pet's name:")

    font = pygame.font.Font(None, 74)
    input_box = pygame.Rect(100, 200, 440, 74)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        name_window.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        name_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(name_window, color, input_box, 2)

        pygame.display.flip()

    pygame.quit()
    return text

# Get the name from the user
name = get_name()

# Reinitialize Pygame for the main program
pygame.init()

# Initialize Pygame
# Coordinates for the GIF and buttons
gif_y = 100  # Y-coordinate of the bottom of the GIF
buttons_y = 500  # Y-coordinate of the top of the buttons

# Calculate the position for the text
text_y = (gif_y + buttons_y) // 2

# Set up the display
pet = pygame.display.set_mode((600, 800), pygame.RESIZABLE)
pygame.display.set_caption('VIRTUAL PET')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load GIF frames using Pillow
idle = Image.open('idle_breathing.gif')
sleeping = Image.open('sleeping.webp')
sad_breathing = Image.open('sad_breathing.gif')
bath = Image.open('bath.webp')
#dirty = Image.open('dirty.gif')
frames = []
durations = []
new_size = (300, 300)  # Set the new size for the GIF frames

def gif(x):
    frames.clear()
    durations.clear()
    for frame in range(x.n_frames):
        x.seek(frame)
        frame_image = x.convert('RGBA')
        frame_image = frame_image.resize(new_size)  # Resize the frame
        frame_data = frame_image.tobytes()
        frame_surface = pygame.image.fromstring(frame_data, frame_image.size, 'RGBA')
        frames.append(frame_surface)
        durations.append(x.info['duration'])

gif(idle)

# Create an instance of Goober
class Goober:
    def __init__(self):
        self.name = name
        self.hunger = 0
        self.tired = False
        self.clean = True
        self.unconscious = False
        self.living = True
        self.energy = 100
        self.joy = 50
        self.dirt = 0

    #json saver
    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "tired": self.tired,
            "clean": self.clean,
            "unconscious": self.unconscious,
            "living": self.living,
            "energy": self.energy,
            "joy": self.joy,
            "dirt": self.dirt
        }
    
    def load_state_from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.name = data.get("name", "Goober")
            self.hunger = data.get("hunger", 0)
            self.tired = data.get("tired", False)
            self.clean = data.get("clean", True)
            self.unconscious = data.get("unconscious", False)
            self.living = data.get("living", True)
            self.energy = data.get("energy", 100)
            self.joy = data.get("joy", 50)
            self.dirt = data.get("dirt", 0)

    def save_state_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    def feed(self):
        self.hunger -= 10
        self.energy -= 5
        self.dirt += 5
    
    def wash(self):
        if self.dirt <= 10:
            self.dirt = 0
        else:
            self.dirt = 10

    def play(self):
        self.energy -= 10
        self.hunger += 5
        self.joy += 10
        self.dirt += 10

    def sleep(self):
        self.unconscious = True
        self.tired = False
        while self.energy < 100:
            time.sleep(1)  # Wait for 10 seconds
            self.energy += 1
        if self.energy == 100:
            self.unconscious = False
            self.energy = 100

    def start_sleep(self):
        sleep_thread = threading.Thread(target=self.sleep)
        sleep_thread.daemon = True
        sleep_thread.start()

    def idleDecay(self):
            while True:
                time.sleep(120)  # Wait for 2 minutes
                self.joy -= 12
                self.hunger += 1
                self.energy -= 1


    def get_state(self):
        return (f"Name: {self.name}\n"
            f"Hunger: {100 - self.hunger}%\n"
            f"Tired: {self.tired}\n"
            f"Clean: {self.clean}\n"
            f"Energy: {self.energy}\n"
            f"Joy: {self.joy}")

goober = Goober()

# Create buttons
buttons = [
    Button('Feed', goober.feed),
    Button('Wash', goober.wash),
    Button('Play', goober.play),
    Button('Sleep', goober.start_sleep)
]

# Start the hunger thread
decay_thread = threading.Thread(target=goober.idleDecay)
decay_thread.daemon = True  # Ensure the thread exits when the main program does
decay_thread.start()

# Main game loop
running = True
frame_index = 0
clock = pygame.time.Clock()
frame_time = 0
is_sleeping_gif = False  # Flag to track if the sleeping GIF is being displayed

while running:
    goober.load_state_from_json('goober_state.json')
    pet.fill((0, 0, 0))  # Clear the screen with a black color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                goober.feed()
            elif event.key == pygame.K_w:
                goober.wash()
            elif event.key == pygame.K_p:
                goober.play()
            elif event.key == pygame.K_s:
                goober.start_sleep()
        elif event.type == pygame.VIDEORESIZE:
            pet = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        for button in buttons:
            button.is_clicked(event)

    # Update game state
    if goober.energy <= 30:
        goober.tired = True
    elif goober.energy <= -1:
        goober.living = False
    if -50 >= goober.hunger >= 100:
        goober.living = False
    if goober.unconscious and not is_sleeping_gif:
        gif(sleeping)
        is_sleeping_gif = True
    if goober.energy == 100 and is_sleeping_gif:
        goober.unconscious = False
        gif(idle)
        is_sleeping_gif = False
    if goober.joy <= 10:
        gif(sad_breathing)
    if goober.hunger >= 50:
        gif(sad_breathing)
    if goober.dirt >= 50:
        goober.clean = False
    elif goober.dirt <= 50:
        goober.clean = True
    '''if goober.clean == False:
        gif(dirty)'''

    # Render Goober's state
    render_text(goober.get_state(), 36, (255, 255, 255), ('center', text_y))

    # Clear the screen
    pet.fill(WHITE)

    # Calculate positions to center the GIF and buttons
    screen_width, screen_height = pet.get_size()
    gif_x = (screen_width - new_size[0]) // 2
    gif_y = (screen_height - new_size[1]) // 2 - 100  # Adjust the y position as needed

    button_width = 100
    button_height = 50
    button_spacing = 20
    total_button_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
    button_start_x = (screen_width - total_button_width) // 2
    button_y = screen_height - button_height - 50  # Adjust the y position as needed

    # Draw the current frame of the GIF
    pet.blit(frames[frame_index], (gif_x, gif_y))

    # Draw Goober's state
    render_text(goober.get_state(), 36, (0, 0, 0), ('center', 500))

    # Draw buttons
    for i, button in enumerate(buttons):
        button_x = button_start_x + i * (button_width + button_spacing)
        button.draw(pet, button_x, button_y, button_width, button_height)
    
    goober.save_state_to_json('goober_state.json')

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    frame_time += clock.tick(30)  # Adjust the frame rate as needed
    if frame_time >= durations[frame_index]:
        frame_time = 0
        frame_index = (frame_index + 1) % len(frames)

# Quit Pygame
pygame.quit()