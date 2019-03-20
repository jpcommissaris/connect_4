import pygame
from board import Board
import numpy as np

LIGHT_BLUE = (155,205,250)
WHITE = (255,255,255)

pygame.init()

# Set up the screen [width, height]
length = 606
width = 570
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
            m = pygame.mouse.get_pos()
            #resets
            if (250 < m[0] < 356) and (520 < m[1] < 550):
                b.winner = 0
                b.board = np.zeros((b.rows, b.cols))
                b.player = 1
            # does move and checks for a winner
            if b.winner == 0:
                b.doMove(event)

    # --- repaints screen ---
    screen.fill(LIGHT_BLUE)

    # --- new drawings ---
    b.drawBoard(screen)
    b.drawTexts(screen)
    b.newGameButton(screen)
    # Updates screen with new drawings
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
