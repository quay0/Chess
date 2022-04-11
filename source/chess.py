#Goose Chess
#Open source project - for more information see https://github.com/quay0/chess/
#This is a development build meaning it may contain bugs - if you find any go to https://github.com/quay0/chess/issues/new/

draw_selected = False #Draw selected: show where piece is moving from
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Hiding the greetings from the pygame comminity message

import pygame
pygame.init()

from copy import deepcopy

#Coordinates of selected square to move from
mx = 0
my = 0

#Window Setup
screen = 512+128
window = pygame.display.set_mode((screen, screen))
pygame.display.set_caption("Chess")
window.fill((255, 255, 255))

#Icon setup
icon = pygame.image.load("wk.ico")
pygame.display.set_icon(icon)

#Sound setup
sound = pygame.mixer.Sound("sound.wav")

#Images setup
_wq = pygame.image.load("wq.png")
_wk = pygame.image.load("wk.png")
_wr = pygame.image.load("wr.png")
_wb = pygame.image.load("wb.png")
_wn = pygame.image.load("wn.png")
_wp = pygame.image.load("wp.png")

_bq = pygame.image.load("bq.png")
_bk = pygame.image.load("bk.png")
_br = pygame.image.load("br.png")
_bb = pygame.image.load("bb.png")
_bn = pygame.image.load("bn.png")
_bp = pygame.image.load("bp.png")

#Piece numbers
wp = 10
wn = 20
wb = 30
wr = 40
wq = 50
wk = 60

bp = -10
bn = -20
bb = -30
br = -40
bq = -50
bk = -60

def check_win():
    no_wk = True
    no_bk = True
    global chessboard
    #Goes through every square on the board and checks if the white and black kings are still there
    scanx = 0
    scany = 0
    while scanx < 8:
        while scany < 8:
            if chessboard[scanx][scany] == wk:
                no_wk = False
            if chessboard[scanx][scany] == bk:
                no_bk = False
            scany += 1
        scanx += 1
        scany = 0
    #If there isn't a white king or a black king
    if no_wk == True or no_bk == True:
        #Resets the board
        turn = 1 #1 for white, 0 for black
        selected = False
        skip = False
        legal = False
        mx = 0
        my = 0
        chessboard = [[br,bn,bb,bq,bk,bb,bn,br],
                [bp,bp,bp,bp,bp,bp,bp,bp],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [wp,wp,wp,wp,wp,wp,wp,wp],
                [wr,wn,wb,wq,wk,wb,wn,wr]]


#Setting colors for board
light = (255, 255, 255)
medium = (211, 228, 171)
dark = (167, 201, 87)

#Setting starting poition
#Unlike on a normal chess board (where it would be 1-8), this board records positions as 0-7
chessboard = [[br,bn,bb,bq,bk,bb,bn,br],
        [bp,bp,bp,bp,bp,bp,bp,bp],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [wp,wp,wp,wp,wp,wp,wp,wp],
        [wr,wn,wb,wq,wk,wb,wn,wr]]
boardLength = 8
square_size = 64

#Drawing squares
def draw_board():
    count = 0
    for i in range(1,boardLength+1):
        for z in range(1,boardLength+1):
            if count % 2 == 0:
                pygame.draw.rect(window, light,[square_size*z,square_size*i,square_size,square_size])
            else:
                pygame.draw.rect(window, dark, [square_size*z,square_size*i,square_size,square_size])
            count +=1
        count -= 1
    if draw_selected == True:
        if mx < 8 and my < 8:
            pygame.draw.rect(window, medium, [(square_size*my)+64,(square_size*mx)+64,square_size,square_size])

#Putting the images of the pieces onto the screen to show their positions to the user
def draw_pieces():
    #Goes through every square on the board
    row = 0
    column = 0
    while row < 8:
        while column < 8:
            current = chessboard[column][row]
            if current != 1:
                #Drawing pieces
                if current == bn:
                    window.blit(_bn, (((64 * row) + 74), ((64 * column) + 74)))
                if current == bb:
                    window.blit(_bb, (((64 * row) + 74), ((64 * column) + 74)))
                if current == bk:
                    window.blit(_bk, (((64 * row) + 74), ((64 * column) + 74)))
                if current == bq:
                    window.blit(_bq, (((64 * row) + 74), ((64 * column) + 74)))
                if current == br:
                    window.blit(_br, (((64 * row) + 74), ((64 * column) + 74)))
                if current == bp:
                    window.blit(_bp, (((64 * row) + 74), ((64 * column) + 74)))

                if current == wn:
                    window.blit(_wn, (((64 * row) + 74), ((64 * column) + 74)))
                if current == wb:
                    window.blit(_wb, (((64 * row) + 74), ((64 * column) + 74)))
                if current == wk:
                    window.blit(_wk, (((64 * row) + 74), ((64 * column) + 74)))
                if current == wq:
                    window.blit(_wq, (((64 * row) + 74), ((64 * column) + 74)))
                if current == wr:
                    window.blit(_wr, (((64 * row) + 74), ((64 * column) + 74)))
                if current == wp:
                    window.blit(_wp, (((64 * row) + 74), ((64 * column) + 74)))
            column += 1
        row += 1
        column = 0

#Font setup
font = pygame.font.SysFont(None, 22)

turn = 1 #1 for white, 0 for black
selected = False
skip = False
legal = False

def draw_turn():
    pygame.draw.rect(window, (255, 255, 255), (0,0,512+128,64))
    #Drawing text
    label = font.render("Goose Chess", 1, (0,0,0))
    window.blit(label, (480, 32))
    if turn == 1:
        label = font.render("White", 1, (0, 0, 0))
        window.blit(label, (128, 32))
    else:
        label = font.render("Black", 1, (0, 0, 0))
        window.blit(label, (128, 32))
    label = font.render("New", 1, dark)
    window.blit(label, (64, 32))

if __name__ == "__main__":
    #Main loop
    loop = True

    while loop:
        pygame.time.delay(2)
        draw_board()
        draw_pieces()
        draw_turn()
        check_win()
                           
        for event in pygame.event.get():
            #Allowing window to close
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #If mouse clicks on "New"
                cx, cy = pygame.mouse.get_pos()
                if cx > 32 and cx < 94 and cy > 0 and cy < 64:
                    #Resets the board
                    turn = 1 #1 for white, 0 for black
                    selected = False
                    skip = False
                    legal = False
                    mx = 0
                    my = 0
                    chessboard = [[br,bn,bb,bq,bk,bb,bn,br],
                            [bp,bp,bp,bp,bp,bp,bp,bp],
                            [1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1],
                            [wp,wp,wp,wp,wp,wp,wp,wp],
                            [wr,wn,wb,wq,wk,wb,wn,wr]]

                #Moving pieces
                if selected == False:
                    if skip == False:
                        #Getting mouse coordinates
                        my, mx = pygame.mouse.get_pos()
                        #Converting mouse coordinates to chessboard coordinates
                        mx = mx / 64 - 1
                        my = my / 64 - 1
                        mx = int(mx)
                        my = int(my)
                        #If clicked on a square with a piece
                        if mx > -1 and mx < 8 and my > -1 and my < 8:
                            if chessboard[mx][my] != 1:
                                #Current is the piece selected
                                current = chessboard[mx][my]
                                selected = True
                                draw_selected = True
                        else:
                            skip = True
                    else:
                        skip = False
                else:
                    #Getting mouse coordinates
                    new_my, new_mx = pygame.mouse.get_pos()
                    #Converting mouse coordinates to chessboard coordinates
                    new_mx = new_mx / 64 - 1
                    new_my = new_my / 64 - 1
                    new_mx = int(new_mx)
                    new_my = int(new_my)
                    legal = False
                    
                    if turn == 0:
                        #King
                        if current == bk:
                            #King side castling
                            if mx == 0 and my == 4 and new_mx == 0 and new_my == 6 and chessboard[0][5] == 1 and chessboard[0][6] == 1 and chessboard[0][7] == br:
                                legal = True
                                chessboard[0][7] = 1
                                chessboard[0][5] = br

                            #Queen side castling
                            if mx == 0 and my == 4 and new_mx == 0 and new_my == 1 and chessboard[0][1] == 1 and chessboard[0][2] == 1 and chessboard[0][3] == 1 and chessboard [0][0] == br:
                                legal = True
                                chessboard[0][0] = 1
                                chessboard[0][2] = br
                            
                            if mx == new_mx or my == new_my:
                                if mx == new_mx + 1 or mx == new_mx - 1:
                                    legal = True
                                elif my == new_my + 1 or my == new_my - 1:
                                    legal = True
                            else:
                                x = abs(new_mx - mx)
                                y = abs(new_my - my)
                                if x == y and x != 0:
                                    if mx == new_mx + 1 and my == new_my + 1:
                                        legal = True
                                    elif mx == new_mx - 1 and my == new_my - 1:
                                        legal = True
                                    elif mx == new_mx + 1 and my == new_my - 1:
                                        legal = True
                                    elif mx == new_mx - 1 and my == new_my + 1:
                                        legal = True
                        
                        #Rook
                        if current == br:
                            if mx == new_mx or my == new_my:
                                f_legal = True
                                if my != new_my:
                                    if my < new_my:
                                        p = my + 1
                                        while p < new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = my - 1
                                        while p > new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                                else:
                                    if mx < new_mx:
                                        p = mx + 1
                                        while p < new_mx:
                                            if chessboard[p][my] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = mx - 1
                                        while p > new_mx:
                                            if chessboard[p][mx] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                        
                        #Bishop
                        if current == bb:
                            x = abs(new_mx - mx)
                            y = abs(new_my - my)
                            if x == y and x != 0:
                                f_legal = True
                                if new_mx > mx and new_my > my:
                                    new_mx_ = new_mx - 1
                                    new_my_ = new_my - 1
                                    while new_mx_ > mx and new_my_ > my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ -= 1
                                        new_my_ -= 1
                                if new_mx > mx and new_my < my:
                                    new_mx_ = new_mx - 1
                                    new_my_ = new_my + 1
                                    while new_mx_ > mx and new_my_ < my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ -= 1
                                        new_my_ += 1
                                if new_mx < mx and new_my > my:
                                    new_mx_ = new_mx + 1
                                    new_my_ = new_my - 1
                                    while new_mx_ < mx and new_my_ > my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ += 1
                                        new_my_ -= 1
                                if new_mx < mx and new_my < my:
                                    new_mx_ = new_mx + 1
                                    new_my_ = new_my + 1
                                    while new_mx_ < mx and new_my_ < my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ += 1
                                        new_my_ += 1
                                if f_legal == True:
                                    legal = True
                        
                        #Queen
                        if current == bq:
                            if mx == new_mx or my == new_my:
                                f_legal = True
                                if my != new_my:
                                    if my < new_my:
                                        p = my + 1
                                        while p < new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = my - 1
                                        while p > new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                                else:
                                    if mx < new_mx:
                                        p = mx + 1
                                        while p < new_mx:
                                            if chessboard[p][my] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = mx - 1
                                        while p > new_mx:
                                            if chessboard[p][mx] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                            else:
                                x = abs(new_mx - mx)
                                y = abs(new_my - my)
                                if x == y and x != 0:
                                    f_legal = True
                                    if new_mx > mx and new_my > my:
                                        new_mx_ = new_mx - 1
                                        new_my_ = new_my - 1
                                        while new_mx_ > mx and new_my_ > my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ -= 1
                                            new_my_ -= 1
                                    if new_mx > mx and new_my < my:
                                        new_mx_ = new_mx - 1
                                        new_my_ = new_my + 1
                                        while new_mx_ > mx and new_my_ < my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ -= 1
                                            new_my_ += 1
                                    if new_mx < mx and new_my > my:
                                        new_mx_ = new_mx + 1
                                        new_my_ = new_my - 1
                                        while new_mx_ < mx and new_my_ > my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ += 1
                                            new_my_ -= 1
                                    if new_mx < mx and new_my < my:
                                        new_mx_ = new_mx + 1
                                        new_my_ = new_my + 1
                                        while new_mx_ < mx and new_my_ < my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ += 1
                                            new_my_ += 1
                                    if f_legal == True:
                                        legal = True
                            
                        #Knight
                        if current == bn:
                            if mx != new_mx or my != new_my:
                                if mx == new_mx - 1 and my == new_my + 2:
                                    legal = True
                                elif mx == new_mx + 1 and my == new_my + 2:
                                    legal = True
                                elif mx == new_mx - 2 and my == new_my + 1:
                                    legal = True
                                elif mx == new_mx + 2 and my == new_my + 1:
                                    legal = True
                                elif mx == new_mx - 2 and my == new_my - 1:
                                    legal = True
                                elif mx == new_mx + 2 and my == new_my - 1:
                                    legal = True
                                elif mx == new_mx - 1 and my == new_my - 2:
                                    legal = True
                                elif mx == new_mx + 1 and my == new_my - 2:
                                    legal = True
                        
                        #Pawn
                        if current == bp:
                            if mx < 7 and my < 0:
                                left = chessboard[mx + 1][my - 1]
                                if left != 1:
                                    if new_my == my - 1 and new_mx == mx + 1:
                                        legal =    True
                            if mx < 7 and my < 7:
                                right = chessboard[mx + 1][my + 1]
                                if right != 1:
                                    if new_my == my + 1 and new_mx == mx + 1:
                                        legal = True
                            if mx < 7:
                                piece_infront = chessboard[mx + 1][my]
                                if piece_infront == 1:
                                    if mx == new_mx - 1 and my == new_my:
                                        legal = True
                            if mx < 6:
                                piece_infront2 = chessboard[mx + 2][my]
                                if piece_infront2 == 1 and piece_infront == 1:
                                    if mx == 1:
                                        if mx == new_mx - 2 and my == new_my:
                                            legal = True

                        #Changing array to move pieces
                        if legal == True:
                            if new_mx != mx or new_my != my:
                                target = chessboard[new_mx][new_my]
                                if target == wk or target == wq or target == wb or target == wn or target == wr or target == wp or target == 1:
                                    chessboard[mx][my] = 1
                                    chessboard[new_mx][new_my] = current
                                    sound.play()
                                    turn ^= 1
                                    legal = False
                                    if current == bp and new_mx == 7:
                                        chessboard[7][new_my] = bq
                        selected = False

                    if turn == 1:

                        #King
                        if current == wk:
                            #King side castling
                            if mx == 7 and my == 4 and new_mx == 7 and new_my == 6 and chessboard[7][5] == 1 and chessboard[7][6] == 1 and chessboard[7][7] == wr:
                                legal = True
                                chessboard[7][7] = 1
                                chessboard[7][5] = wr

                            #Queen side castling
                            if mx == 7 and my == 4 and new_mx == 7 and new_my == 1 and chessboard[7][1] == 1 and chessboard[7][2] == 1 and chessboard[7][3] == 1 and chessboard [7][0] == wr:
                                legal = True
                                chessboard[7][0] = 1
                                chessboard[7][2] = wr

                            if mx == new_mx or my == new_my:
                                if mx == new_mx + 1 or mx == new_mx - 1:
                                    legal = True
                                elif my == new_my + 1 or my == new_my - 1:
                                    legal = True
                            else:
                                x = abs(new_mx - mx)
                                y = abs(new_my - my)
                                if x == y and x != 0:
                                    if mx == new_mx + 1 and my == new_my + 1:
                                        legal = True
                                    elif mx == new_mx - 1 and my == new_my - 1:
                                        legal = True
                                    elif mx == new_mx + 1 and my == new_my - 1:
                                        legal = True
                                    elif mx == new_mx - 1 and my == new_my + 1:
                                        legal = True
                        
                        #Rook
                        if current == wr:
                            if mx == new_mx or my == new_my:
                                f_legal = True
                                if my != new_my:
                                    if my < new_my:
                                        p = my + 1
                                        while p < new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = my - 1
                                        while p > new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                                else:
                                    if mx < new_mx:
                                        p = mx + 1
                                        while p < new_mx:
                                            if chessboard[p][my] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = mx - 1
                                        while p > new_mx:
                                            if chessboard[p][my] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                        
                        #Bishop
                        if current == wb:
                            x = abs(new_mx - mx)
                            y = abs(new_my - my)
                            if x == y and x != 0:
                                f_legal = True
                                if new_mx > mx and new_my > my:
                                    new_mx_ = new_mx - 1
                                    new_my_ = new_my - 1
                                    while new_mx_ > mx and new_my_ > my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ -= 1
                                        new_my_ -= 1
                                if new_mx > mx and new_my < my:
                                    new_mx_ = new_mx - 1
                                    new_my_ = new_my + 1
                                    while new_mx_ > mx and new_my_ < my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ -= 1
                                        new_my_ += 1
                                if new_mx < mx and new_my > my:
                                    new_mx_ = new_mx + 1
                                    new_my_ = new_my - 1
                                    while new_mx_ < mx and new_my_ > my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ += 1
                                        new_my_ -= 1
                                if new_mx < mx and new_my < my:
                                    new_mx_ = new_mx + 1
                                    new_my_ = new_my + 1
                                    while new_mx_ < mx and new_my_ < my:
                                        if chessboard[new_mx_][new_my_] != 1:
                                            f_legal = False
                                        new_mx_ += 1
                                        new_my_ += 1
                                if f_legal == True:
                                    legal = True
                        
                        #Queen
                        if current == wq:
                            if mx == new_mx or my == new_my:
                                f_legal = True
                                if my != new_my:
                                    if my < new_my:
                                        p = my + 1
                                        while p < new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = my - 1
                                        while p > new_my:
                                            if chessboard[mx][p] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                                else:
                                    if mx < new_mx:
                                        p = mx + 1
                                        while p < new_mx:
                                            if chessboard[p][my] != 1:
                                                f_legal = False
                                            p += 1
                                        if f_legal == True:
                                            legal = True
                                    else:
                                        p = mx - 1
                                        while p > new_mx:
                                            if chessboard[p][mx] != 1:
                                                f_legal = False
                                            p -= 1
                                        if f_legal == True:
                                            legal = True
                            else:
                                x = abs(new_mx - mx)
                                y = abs(new_my - my)
                                if x == y and x != 0:
                                    f_legal = True
                                    if new_mx > mx and new_my > my:
                                        new_mx_ = new_mx - 1
                                        new_my_ = new_my - 1
                                        while new_mx_ > mx and new_my_ > my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ -= 1
                                            new_my_ -= 1
                                    if new_mx > mx and new_my < my:
                                        new_mx_ = new_mx - 1
                                        new_my_ = new_my + 1
                                        while new_mx_ > mx and new_my_ < my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ -= 1
                                            new_my_ += 1
                                    if new_mx < mx and new_my > my:
                                        new_mx_ = new_mx + 1
                                        new_my_ = new_my - 1
                                        while new_mx_ < mx and new_my_ > my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ += 1
                                            new_my_ -= 1
                                    if new_mx < mx and new_my < my:
                                        new_mx_ = new_mx + 1
                                        new_my_ = new_my + 1
                                        while new_mx_ < mx and new_my_ < my:
                                            if chessboard[new_mx_][new_my_] != 1:
                                                f_legal = False
                                            new_mx_ += 1
                                            new_my_ += 1
                                    if f_legal == True:
                                        legal = True
                        #Knight
                        if current == wn:
                            if mx != new_mx or my != new_my:
                                if mx == new_mx - 1 and my == new_my + 2:
                                    legal = True
                                elif mx == new_mx + 1 and my == new_my + 2:
                                    legal = True
                                elif mx == new_mx - 2 and my == new_my + 1:
                                    legal = True
                                elif mx == new_mx + 2 and my == new_my + 1:
                                    legal = True
                                elif mx == new_mx - 2 and my == new_my - 1:
                                    legal = True
                                elif mx == new_mx + 2 and my == new_my - 1:
                                    legal = True
                                elif mx == new_mx - 1 and my == new_my - 2:
                                    legal = True
                                elif mx == new_mx + 1 and my == new_my - 2:
                                    legal = True
                        
                        #Pawn
                        if current == wp:
                            if mx > 0 and my > 0:
                                left = chessboard[mx - 1][my - 1]
                                if left != 1:
                                    if new_my == my - 1 and new_mx == mx - 1:
                                        legal =    True
                            if mx > 0 and my < 7:
                                right = chessboard[mx - 1][my + 1]
                                if right != 1:
                                    if new_my == my + 1 and new_mx == mx - 1:
                                        legal = True
                            if mx > 0:
                                piece_infront = chessboard[mx - 1][my]
                                if piece_infront == 1:
                                    if mx == new_mx + 1 and my == new_my:
                                        legal = True
                            if mx > 1:
                                piece_infront2 = chessboard[mx - 2][my]
                                if piece_infront2 == 1 and piece_infront == 1:
                                    if mx == 6:
                                        if mx == new_mx + 2 and my == new_my:
                                            legal = True

                        #Changing array to move pieces
                        if legal == True:
                            if new_mx != mx or new_my != my:
                                target = chessboard[new_mx][new_my]
                                if target == bk or target == bq or target == bb or target == bn or target == br or target == bp or target == 1:
                                    chessboard[mx][my] = 1
                                    chessboard[new_mx][new_my] = current
                                    sound.play()
                                    turn ^= 1
                                    legal = False
                                    if current == wp and new_mx == 0:
                                        chessboard[0][new_my] = wq
                        selected = False
        pygame.display.update()
