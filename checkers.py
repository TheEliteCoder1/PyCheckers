
"""
An 8x8 simple checkers game made with nothing else 
but Python and Pygame.
"""

import pygame, sys, time, random
from pygame.locals import QUIT

pygame.init()
# determines sizes of squares
boardSize = 400
uiMargin = 150
screen = pygame.display.set_mode((boardSize+uiMargin, boardSize))
pygame.display.set_caption('Checkers')
pygame.font.init()

# Board rows and columns
# abcdefgh
# 12345678

# square colors
white = (255, 255, 255)
black = (0, 0, 0)

#standard color
red = (255,0,0)
green = (0, 255, 0)

# piece colors 
yellow = (255,255,0)
blue = (0, 0, 255)

# square outline
outlineColor = red
pieceSize = 20

def Opposite(turn):
    if turn == 'yellow':
        return 'blue'
    if turn == "blue":
        return 'yellow'



# king image
king_img = pygame.transform.scale(pygame.image.load("star.png"), (pieceSize+10, pieceSize+10)).convert_alpha()

rows_cols_count = 8
squareSize = boardSize / rows_cols_count

# game vars

selected_piece = None # board location
hop = False
turn = "yellow"
total_minutes = 15
winner = None
moveable_places = None # legal places
hasChosen = True
blue_count = 0
yellow_count = 0

class Board:
    def __init__(self):
        self.matrix = self.getMatrix()
        # set square color
        for square in self.matrix:
            if square.x % 2 != 0 and square.y % 2 == 0:
                square.color = black
            if square.y % 2 != 0 and square.x % 2 == 0:
                square.color = black
            

        # set pieces
        for square in self.matrix:
            if square.color == black and square.y <= 2:
                square.occupant = Piece(blue)
            if square.color == black and 4 < square.y <= 7:
                square.occupant = Piece(yellow)

    def setDefaultSquareColor(self):
        for square in self.matrix:
            if type(square.occupant) == None:
                if square.x % 2 != 0 and square.y % 2 == 0:
                    square.color = black
                if square.y % 2 != 0 and square.x % 2 == 0:
                    square.color = black

    def getMatrix(self):
        matrix = [Square(x, y, squareSize, squareSize, white, False) for x in range(rows_cols_count) for y in range(rows_cols_count)]
        return matrix

    def update(self, screen, turn):
        global moveable_places
        global selected_piece
        


       

        # draw selected piece
        if type(selected_piece) == tuple:
            for square in board.matrix:
                if square.x % 2 != 0 and square.y % 2 == 0 and (square.x, square.y) != selected_piece:
                    square.color = black
                if square.y % 2 != 0 and square.x % 2 == 0 and (square.x, square.y) != selected_piece:
                    square.color = black
                if (square.x, square.y) == selected_piece:
                    square.color = red

        
                        
                                      
        # show moveable places
        if type(moveable_places) == list:
            for box in moveable_places:
                for square in self.matrix:
                    if (box[0], box[1]) == (square.x, square.y):
                        square.color = green

        if type(selected_piece) == None:
            for square in self.matrix:
                if square.x % 2 != 0 and square.y % 2 == 0:
                    square.color = black
                if square.y % 2 != 0 and square.x % 2 == 0:
                    square.color = black

        # draw squares              
        for square in self.matrix:
            pygame.draw.rect(screen, square.color, (square.x*squareSize+uiMargin, square.y*squareSize, square.width, square.height))
            pygame.draw.rect(screen, outlineColor, (square.x*squareSize+uiMargin, square.y*squareSize, square.width, square.height), 1)

        # draw pieces
        for square in self.matrix:
            if type(square.occupant) == Piece:
                x_pos = square.x*squareSize+uiMargin
                x_pos_2 = square.x*squareSize+uiMargin+squareSize
                center_x_pos = (x_pos + x_pos_2) / 2
                y_pos = square.y*squareSize
                y_pos_2 = square.y*squareSize+squareSize
                center_y_pos = (y_pos + y_pos_2) / 2
                pygame.draw.circle(screen, square.occupant.color, (center_x_pos, center_y_pos), pieceSize)

                # checking for kings
                if square.occupant.king:
                    rect = king_img.get_rect(center=(center_x_pos, center_y_pos))
                    screen.blit(king_img, rect)


    
            

                    
                

            
def get_moveable_places(matrix, turn, square_x, square_y, king):
    moveable_places = []
    if not king:
        # northeast
        if turn == 'yellow':
            ne_x_pos = square_x - 1
            ne_y_pos = square_y - 1
        if turn == 'blue':
            ne_x_pos = square_x - 1
            ne_y_pos = square_y + 1
        ne = (ne_x_pos, ne_y_pos)
        # northwest
        if turn == 'yellow':
            nw_x_pos = square_x + 1
            nw_y_pos = square_y - 1
        if turn == 'blue':
            nw_x_pos = square_x + 1
            nw_y_pos = square_y + 1
        nw = (nw_x_pos, nw_y_pos)
        # loop through all square positions
        for square in matrix:
            if square.x == ne[0] and square.y == ne[1]:
                if type(square.occupant) == Piece:
                    if square.occupant.color == eval(Opposite(turn)):
                        moveable_places.append(ne)              
                else:
                    moveable_places.append((square.x, square.y))
            if square.x == nw[0] and square.y == nw[1]:
                if type(square.occupant) == Piece:
                    if square.occupant.color == eval(Opposite(turn)):
                        moveable_places.append(nw)
                else:
                    moveable_places.append((square.x, square.y))
                
                
        return moveable_places
    else:
        for square in matrix:
            if square.x < 8 and square.y < 8:
                # if the next square is northeast, then add it
                if turn == yellow:
                    if matrix[matrix.index(square)+1].x == square_x - 1:
                        if matrix[matrix.index(square)+1].x == square_y - 1:
                            moveable_places.append((square.x, square.y))
                
        
        
    

class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

class Square:   
    def __init__(self, x, y, width, height, color, occupant=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.occupant = occupant

def end_game(turn):
    pass

class Label():
    def __init__(self, txt, location, size=(130,30), fg=green, bg=black, font_name="segoe print", font_size=30):
        self.bg = bg  
        self.fg = fg
        self.location = location
        self.size = size
    
        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])
    
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(topleft=self.location) 

    def draw(self, screen):
        self.rect.topleft = self.location
        screen.blit(self.surface, self.rect)

    def update(self):
        self.surface.fill(self.bg)
        self.txt_surf = self.font.render(self.txt, True, self.fg)
        self.surface.blit(self.txt_surf, self.txt_rect)

     
        
# create board
board = Board()
# timer
show_ticks = pygame.USEREVENT+1
pygame.time.set_timer(show_ticks, 1000)
change_turn = pygame.USEREVENT+2
secsPerTurn = 120
pygame.time.set_timer(change_turn, 1000*secsPerTurn)
yellow_seconds = total_minutes*60
blue_seconds = total_minutes*60
run = True
clock = pygame.time.Clock()
fps = 60

yellow_count_label = Label(f"x {yellow_count}", (5, 290), fg=green, bg=white, font_size=35)
yellow_count_label.update()

blue_count_label = Label(f"x {blue_count}", (5, 240), fg=green, bg=white, font_size=35)
blue_count_label.update()

if turn == "blue":
    label_color = blue
    turn_label_location = (20, 40)
    time_label_location = (20, 10)
    turn.capitalize()
    turn_label = Label(f"{turn}", turn_label_location, fg=label_color, bg=black)
    turn_label.update()
    time_label = Label(f"Time: {blue_seconds}s", time_label_location, fg=label_color)
    time_label.update()
if turn == "yellow":
    label_color = yellow
    turn_label_location = (20, 360)
    time_label_location = (20, 320)
    turn.capitalize()
    turn_label = Label(f"{turn}", turn_label_location, fg=label_color)
    turn_label.update()
    time_label = Label(f"Time: {yellow_seconds}s", time_label_location, fg=label_color)
    time_label.update()

isYellow = True


while run:
    clock.tick(fps)

     
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            # check for chosen piece
            for square in board.matrix:
                if type(square.occupant) == Piece:
                    if square.occupant.color == eval(turn):
                        x_pos = square.x*squareSize+uiMargin
                        x_pos_2 = square.x*squareSize+uiMargin+squareSize
                        width = x_pos_2 - x_pos
                        y_pos = square.y*squareSize
                        y_pos_2 = square.y*squareSize+squareSize
                        height = y_pos_2 - y_pos
                        if pygame.Rect(x_pos, y_pos, width, height).collidepoint(mpos):
                            selected_piece = (square.x, square.y)
                            moveable_places = get_moveable_places(board.matrix, turn, selected_piece[0], selected_piece[1], king=square.occupant.king)
            if moveable_places != None:
                # if there are moveable places availible 
                # and one of them is clicked
                # then move it there
                # otherwise choose a piece to select
                for place in moveable_places:
                    x_pos = place[0]*squareSize+uiMargin
                    x_pos_2 = place[0]*squareSize+uiMargin+squareSize
                    width = x_pos_2 - x_pos
                    y_pos = place[1]*squareSize
                    y_pos_2 = place[1]*squareSize+squareSize
                    height = y_pos_2 - y_pos
                    if pygame.Rect(x_pos, y_pos, width, height).collidepoint(mpos):
                        for square in board.matrix:
                            if (square.x, square.y) == selected_piece:
                                for sq in board.matrix:
                                    if (sq.x, sq.y) == (place[0], place[1]):
                                        # if the place is empty
                                        # then move the piece
                                        if type(sq.occupant) != Piece: 
                                            sq.occupant = square.occupant
                                            # check for kinging
                                            if sq.y == 0 and square.occupant.color == yellow:
                                                sq.occupant.king = True
                                            if sq.y == 7 and square.occupant.color == blue:
                                                sq.occupant.king = True
                                            square.occupant = None
                                            selected_piece = None
                                            moveable_places = None
                                            board.setDefaultSquareColor()
                                            isYellow = not isYellow
                                            turn = "yellow" if isYellow else "blue"
                                        else:
                                            # if the place is occupied 
                                            # by the opposite side
                                            # then kill and move forward
                                            if sq.occupant.color == eval(Opposite(turn)):
                                                if eval(Opposite(turn)) == yellow:
                                                    yellow_count += 1
                                                    yellow_count_label = Label(f"x {yellow_count}", (5, 290), fg=green, bg=white, font_size=35)
                                                    yellow_count_label.update()
                                                if eval(Opposite(turn)) == blue:
                                                    blue_count += 1
                                                    blue_count_label = Label(f"x {blue_count}", (5, 240), fg=green, bg=white, font_size=35)
                                                    blue_count_label.update()
                                                sq.occupant = square.occupant
                                                # check for kinging
                                                if sq.y == 0 and square.occupant.color == yellow:
                                                    sq.occupant.king = True
                                                if sq.y == 7 and square.occupant.color == blue:
                                                    sq.occupant.king = True
                                                square.occupant = None
                                                selected_piece = None
                                                moveable_places = None
                                                board.setDefaultSquareColor()
                                                isYellow = not isYellow
                                                turn = "yellow" if isYellow else "blue"    
     
                                    
                    else:
                        for square in board.matrix:
                            if type(square.occupant) == Piece:
                                if square.occupant.color == eval(turn):
                                    x_pos = square.x*squareSize+uiMargin
                                    x_pos_2 = square.x*squareSize+uiMargin+squareSize
                                    width = x_pos_2 - x_pos
                                    y_pos = square.y*squareSize
                                    y_pos_2 = square.y*squareSize+squareSize
                                    height = y_pos_2 - y_pos
                                    if pygame.Rect(x_pos, y_pos, width, height).collidepoint(mpos):
                                        selected_piece = (square.x, square.y)
                                        moveable_places = get_moveable_places(board.matrix, turn, selected_piece[0], selected_piece[1], king=square.occupant.king)
                                       
                
            

        if event.type == change_turn:
            isYellow = not isYellow
            turn = "yellow" if isYellow else "blue"
            
        if event.type == show_ticks:
            if turn == "blue":
                blue_seconds -= 1
                label_color = blue
                turn_label_location = (20, 40)
                time_label_location = (20, 10)
                turn.capitalize()
                turn_label = Label(f"{turn}", turn_label_location, fg=label_color)
                turn_label.update() 
                time_label = Label(f"Time: {blue_seconds}s", time_label_location, fg=label_color)
                time_label.update()

                if blue_seconds == 0:
                    pygame.time.set_timer(show_ticks, 0)
                    end_game(turn)
                    
            if turn == "yellow":
                yellow_seconds -= 1
                label_color = yellow
                turn_label_location = (20, 360)
                time_label_location = (20, 320)
                turn.capitalize()
                turn_label = Label(f"{turn}", turn_label_location, fg=label_color)
                turn_label.update()
                time_label = Label(f"Time: {yellow_seconds}s", time_label_location, fg=label_color)
                time_label.update()

                if yellow_seconds == 0:  
                    pygame.time.set_timer(show_ticks, 0)
                    end_game(turn)
                
        
    screen.fill((255,255,255))
    board.update(screen, turn)
    # draw kill count
    yellow_count_label.update()
    blue_count_label.update()
    # draw color icons beside kill count
    yellow_count_label.draw(screen)
    blue_count_label.draw(screen)
    pygame.draw.circle(screen, yellow, (20, 300), 15)
    pygame.draw.circle(screen, blue, (20, 250), 15)
    turn_label.draw(screen)
    time_label.draw(screen)

    
    pygame.display.update()
