import os
from tkinter import font
import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

from button import Button
from Game import Game

CARD_WIDTH = 100
CARD_HEIGHT = 145
CARD_SPACING = 110 

ask_new_game = False

root = tk.Tk()
root.withdraw()
player_name = simpledialog.askstring("Player Name", "Enter your name:")

game = Game(player_name)
# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 1250
screen_height = 670
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption(f"{player_name}'s game of QJack")

def ask_another_round():
    def on_count_me_in():
        nonlocal choice
        choice = "yes"
        dialog.destroy()

    def on_leave_game():
        nonlocal choice
        choice = "no"
        dialog.destroy()

    choice = None
    dialog = tk.Tk()
    dialog.title("Play Again?")
    dialog.geometry("300x150+500+200")
    dialog.resizable(False, False)

    label = tk.Label(dialog, text="Another round?", font=("Arial", 14))
    label.pack(pady=20)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    yes_btn = tk.Button(button_frame, text="Count me in!", width=12, command=on_count_me_in)
    yes_btn.pack(side="left", padx=10)

    no_btn = tk.Button(button_frame, text="Leave game", width=12, command=on_leave_game)
    no_btn.pack(side="left", padx=10)

    dialog.mainloop()
    return choice

def ui_evaluate_winner():
    msg = ''
    if (game.dealer.is_bust): msg += f"Dealer busts with {game.dealer.score}. "
    if (game.player.is_bust): msg += f"{game.player.name} busts with {game.player.score}. "

    if game.player.is_bust:
        msg += "Dealer wins!"
    elif game.dealer.is_bust:
        msg += f"{game.player.name} wins!"
    elif game.player.score > game.dealer.score:
        msg += f"{game.player.name} wins!"
    elif game.player.score < game.dealer.score:
        msg += "Dealer wins!"
    else:
        msg += "It’s a tie!"
    return msg

def load_card_images(card_folder="ui/cards"):
    card_images = {}
    for filename in os.listdir(card_folder):
        if filename.endswith(".png"):
            key = filename.replace(".png", "") 
            image = pygame.image.load(os.path.join(card_folder, filename)).convert_alpha()
            image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
            card_images[key] = image
    return card_images

card_images = load_card_images()
logo_image = pygame.image.load("ui/cards/card_back.png").convert_alpha() 
logo_image = pygame.transform.scale(logo_image, (CARD_WIDTH // 2, CARD_HEIGHT // 2)) 

message = 'Welcome to QJack!'

font = pygame.font.SysFont(None, 36)
# Button setup
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LAVENDER = (197, 194, 242)
LIGHT_GREEN = (194, 242, 209)
LIGHT_PINK = (242, 194, 212)
TRANSPARENT_BLACK = (0, 0, 0, 128) 

button_width = 125
button_height = 40
bottom_margin = 20
button_spacing = 40  # space between buttons

message_font = pygame.font.SysFont(None, 36)
label_font = pygame.font.SysFont(None, 36)
player_card_y = screen_height - 145 - 100
dealer_card_y = screen_height - 145 - 350

# Y position (distance from bottom of screen)
y_pos = screen_height - button_height - bottom_margin

# Calculate total width of all buttons plus the spaces in between
total_width = 3 * button_width + 2 * button_spacing
start_x = (screen_width - total_width) // 2

# Create buttons
hit_button = Button(start_x, y_pos, button_width, button_height, "Hit", font, LIGHT_GREEN, DARK_GRAY, BLACK)
stay_button = Button(start_x + (button_width + button_spacing), y_pos, button_width, button_height, "Stay", font, LIGHT_PINK, DARK_GRAY, BLACK)
peek_button = Button(start_x + 2 * (button_width + button_spacing), y_pos, button_width, button_height, "Measure", font, LAVENDER, DARK_GRAY, BLACK)

buttons = [hit_button, stay_button, peek_button]

# Create Score box
score_box_width = 250
score_box_height = 50
score_box_x = screen_width - score_box_width - 20 
score_box_y = 20 

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (green table background)
    screen.fill((0, 128, 0))
    screen.blit(logo_image, (30, 20))

    message_surface = message_font.render(message, True, WHITE)
    message_rect = message_surface.get_rect(center=(screen_width // 2, 40))
    screen.blit(message_surface, message_rect)

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for btn in buttons:
        btn.draw(screen)

    pygame.draw.rect(screen, GRAY, (30, player_card_y - 60, (screen_width - 60), CARD_HEIGHT + 80), border_radius=8, width=4)

    # Draw player's label
    player_label = label_font.render(f"{game.player.name}'s Hand", True, BLACK)
    player_label_rect = player_label.get_rect(center=(screen_width // 2, player_card_y - 30))  # Position above the player's cards
    screen.blit(player_label, player_label_rect)

    # Draw player's cards
    for i, card in enumerate(game.player.hand):
        try:
            card_key = card.card_key()
            card_img = card_images[card_key]
            card_x = 50 + i * CARD_SPACING
            card_y = player_card_y
            screen.blit(card_img, (card_x, card_y))

            if card.is_quantum and card.measured_value is not None:
                note_text = f'value: {card.measured_value}'  # or card.name / card.rank / card.state etc.
                note_font = pygame.font.SysFont(None, 24)
                note_surface = note_font.render(note_text, True, WHITE)
                note_rect = note_surface.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT + 10))
                screen.blit(note_surface, note_rect)
        except KeyError:
            print(f"Missing image for: {card_key}")

    pygame.draw.rect(screen, GRAY, (30, dealer_card_y - 60, (screen_width - 60), CARD_HEIGHT + 80), border_radius=8, width=4)
    # Draw dealer's label
    dealer_label = label_font.render("Dealer's Cards", True, BLACK)
    dealer_label_rect = dealer_label.get_rect(center=(screen_width // 2, dealer_card_y - 30))  # Position above the dealer's cards
    screen.blit(dealer_label, dealer_label_rect)

    # Draw dealer's cards
    for i, card in enumerate(game.dealer.cards):
        try:
            card_key = card.card_key()  
            card_img = card_images[card_key]
            card_x = 50 + i * CARD_SPACING
            card_y = dealer_card_y
            screen.blit(card_img, (card_x, card_y))
        except KeyError:
            print(f"Missing image for: {card_key}")

            
    # Draw white rectangle (score box)
    pygame.draw.rect(screen, WHITE, (score_box_x, score_box_y, score_box_width, score_box_height), border_radius=8)

    # Render score text
    score_text = f"{game.player.name}'s score: {game.player.calculate_tentative_score()}"
    score_surface = font.render(score_text, True, BLACK)
    score_rect = score_surface.get_rect(center=(score_box_x + score_box_width // 2, score_box_y + score_box_height // 2))

    # Blit text
    screen.blit(score_surface, score_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for btn in buttons:
            if btn.is_clicked(event):
                if btn.text == "Hit":
                    game.player.add_card(game.deck.deal(1)[0])
                    message = f"{player_name} hits!"
                    # game.deck.entanglement_detected
                    if (game.player.hand[-1].is_quantum and game.player.hand[-1].entangled_group_id != None):
                        message += f" {game.player.hand[-1].name} Entanglement detected."
                    for card in game.player.hand:
                        print(card)
                    if game.player.calculate_score() > 21:
                        print("Player busts!")
                        message = ui_evaluate_winner()
                        ask_new_game = True
                        for button in buttons:
                            button.set_state("disabled")
                        # response = ask_another_round()
                elif btn.text == "Stay":
                    message = f"{player_name} stays."
                    # End player turn, run dealer turn
                    game.player.measure_hand()
                    game.player.calculate_score()

                    for card in game.dealer.cards:
                        if card.is_quantum:
                            card.measure()
                    game.dealer.calculate_score()

                    while game.dealer.isHitting():
                        new_card = game.deck.deal(1)[0]
                        if new_card.is_quantum:
                            new_card.measure()
                        game.dealer.cards.append(new_card)
                        game.dealer.calculate_score()
                        message = ui_evaluate_winner()
                    
                    game.print_game_state()
                    game.evaluate_winner()
                    for button in buttons:
                        button.set_state("disabled")
                    ask_new_game = True
                elif btn.text == "Measure":
                    if game.player.measure_used:
                        message = "No more peeking!"
                        print("No more peeking!")
                    else:
                        buttons[2].set_state("disabled")
                        game.player.measure_hand()
                        message = f"{player_name} peeked!"
                        if game.player.calculate_score() > 21:
                            print("Player busts!")
                            message = ui_evaluate_winner()
                            ask_new_game = True
                            for button in buttons:
                                button.set_state("disabled")
                            # response = ask_another_round()
                        for card in game.player.hand: print(card)

    # game = Game(player_name)

    # Update the display
    pygame.display.flip()
    # if ask_new_game == True:
    #     pygame.time.delay(300)
    #     ask_new_game = False
    #     response = ask_another_round()
    #     if response == "yes":
    #         print("Player wants another round!")
    #     elif response == "no":
    #         print("Player is done.")

# Quit Pygame
pygame.quit()
sys.exit()
