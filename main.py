import pygame
from board import Board
import sys
import random
import math

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()

# Set up the screen [width, height]
length = 600
width = 600
size = (length, width)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Four in a Row")

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()




b = Board()

# --- game loop ---
while not done:
    b.pressed = False
    # --- Events loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            # does move and checks for a winner
            b.doMove(event)
        if event.type == pygame.MOUSEMOTION:
            b.highlight(screen, event)
    # --- scene logic ---


    # --- repaints screen ---
    screen.fill((255,255,255))

    # --- new drawings ---
    b.drawBoard(screen)

    # Updates screen with new drawings
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
