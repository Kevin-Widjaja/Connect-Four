import numpy as np
import pygame
import sys

ROW_COUNT = 6 # global variables are capitalized
COLUMN_COUNT = 7
BLUE = (0, 0, 255) # blue RGB value
BLACK = (0, 0, 0) 
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (119,136,153)
LIGHT_GREY = (192,192,192)
WHITE = (255, 255, 255)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT)) # this creates a 6x7 matrix using numpy
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece # will put a piece in the board row/column

def is_valid_location(board, col):
    return (board[ROW_COUNT-1][col] == 0) # returns true if we have an empty row in the column 

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board): # prints the board in the correct orientation
    print(np.flip(board, 0))

def is_winning_move(board, piece): # to check whether someone has won
    # check horizontal lines
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if (
                board[row][column] == piece and board[row][column + 1] == piece and
                board[row][column + 2] == piece and board[row][column + 3] == piece
            ):
                return True

    # check vertical lines
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if (
                board[row][column] == piece and board[row + 1][column] == piece and
                board[row + 2][column] == piece and board[row + 3][column] == piece
            ):
                return True
    
    # check positive sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece and board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and board [r+3][c+3] == piece
            ):
                return True
    
    # check negative sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece and board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and board [r-3][c+3] == piece
            ):
                return True

def draw_board(board): # draw board using pygame
    for c in range(COLUMN_COUNT): # draw the empty circle in all spots of row/column
        for r in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT): 
        for r in range (ROW_COUNT):
            if board[r][c] == 1: # if player 1 put their piece in, make the circle red
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

            elif board[r][c] == 2: # if player 2 put their piece in, make the circle yellow
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def make_move(turn): # makes the player's turn, given player number
    posX = event.pos[0]
    column = posX//SQUARESIZE # get column value by taking lowest integer when dividing

    if is_valid_location(board, column):
        row = get_next_open_row(board, column)
        drop_piece(board, row, column, turn) # drop player 1 piece

        if is_winning_move(board, turn):
            label = myfont.render("Player " + str(turn) + " wins!", 1, GREEN)
            screen.blit(label, (40,10))                        
            global game_over
            game_over = True

def ask_to_play_again(): # menu to allow user to choose to play again or quit
    # defining the text and position of our 'play again' and 'quit' buttons
    playAgainText = exitFont.render("Play Again", 1, WHITE) 
    quitText = exitFont.render("Quit", 1, WHITE)
    playAgainTextPositionX = width/2 - SQUARESIZE * 1.5 
    playAgainTextPositionY = height/2-SQUARESIZE
    quitTextPositionX = width/2 + SQUARESIZE * 1.5
    quitTextPositionY = height/2-SQUARESIZE
    playAgainTextPosition = (playAgainTextPositionX, playAgainTextPositionY)
    quitTextPosition = (quitTextPositionX, quitTextPositionY)

    pygame.display.update()
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ( # if we click on the "Play Again" button, reset the game
                (playAgainTextPositionX - SQUARESIZE <= mouse_x <= playAgainTextPositionX + SQUARESIZE) and
                (playAgainTextPositionY - SQUARESIZE <= mouse_y <= playAgainTextPositionY + SQUARESIZE)
            ):
                global board
                board = create_board()
                draw_board(board)
                global game_over
                game_over = False
                global turn 
                turn = 0
                pygame.display.update()
                return
            elif ( # if we click on the "Quit" button, leave
                (quitTextPositionX - SQUARESIZE <= mouse_x <= quitTextPositionX + SQUARESIZE) and
                (quitTextPositionY - SQUARESIZE <= mouse_y <= quitTextPositionY + SQUARESIZE)
            ):
                sys.exit()

        if event.type == pygame.MOUSEMOTION: # track the user's mouse motion to show whose turn it is
            if ( # if we hover on the "Play Again" button, highlight the button
                (playAgainTextPositionX - SQUARESIZE <= mouse_x <= playAgainTextPositionX + SQUARESIZE) and
                (playAgainTextPositionY - SQUARESIZE <= mouse_y <= playAgainTextPositionY + SQUARESIZE)
            ):
                pygame.draw.circle(screen, LIGHT_GREY, playAgainTextPosition, SQUARESIZE)
                screen.blit(playAgainText, playAgainText.get_rect(center = playAgainTextPosition))

            elif ( # if we hover over "Quit" button, highlight the button
                (quitTextPositionX - SQUARESIZE <= mouse_x <= quitTextPositionX + SQUARESIZE) and
                (quitTextPositionY - SQUARESIZE <= mouse_y <= quitTextPositionY + SQUARESIZE)
            ):
                pygame.draw.circle(screen, LIGHT_GREY, quitTextPosition, SQUARESIZE)
                screen.blit(quitText, quitText.get_rect(center = quitTextPosition))
            
            else: # if we highlight anywhere else, don't highlight either button
                pygame.draw.circle(screen, GREY, playAgainTextPosition, SQUARESIZE)
                pygame.draw.circle(screen, GREY, quitTextPosition, SQUARESIZE)
                screen.blit(playAgainText, playAgainText.get_rect(center = playAgainTextPosition))
                screen.blit(quitText, quitText.get_rect(center = quitTextPosition))

            pygame.display.update()

board = create_board()
game_over = False # start game as false, will become true if someone gets 4 in a row
turn = 0 # track whose turn it is

pygame.init() # initialize pygame

# variables tracking screen and image details
SQUARESIZE = 100 # size of each of the square spaces 
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)
exitFont = pygame.font.SysFont("monospace", 30)

# main game loop
draw_board(board)
pygame.display.update()

while True:
    while not game_over:
        # pygame will read events (mouse clicks and movements) that we need to track to play the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # allow us to exit game
                sys.exit()

            if event.type == pygame.MOUSEMOTION: # track the user's mouse motion to show whose turn it is
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE)) # this will help delete existing circles
                posX = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE/2)), RADIUS)
                if turn == 1:
                    pygame.draw.circle(screen, YELLOW, (posX, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN: # track where the user is clicking
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                make_move(turn + 1) # player whose turn it is will make their move
                draw_board(board)
                turn += 1
                turn = turn % 2

    ask_to_play_again()