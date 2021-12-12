#   tictactoe.py
#
#   Created by Angus Lin, 2021.11.30
#
#   History
#   2021.12.7   completed version 1 with minimax
#   2021.12.8   add alpha-beta

import pygame
import logging

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ALPHABETA = True
PLUSINF = 10000
MINUSINF = -10000

#   Recursion counter
GRecurCount = 0
GNodes = 0

def drawBoard(win, board, msg):
    win.fill(WHITE)
    w, h = pygame.display.get_surface().get_size()
    pygame.draw.line(win, BLACK, (1, h * 0.33), (w, h * 0.33))
    pygame.draw.line(win, BLACK, (1, h * 0.66), (w, h * 0.66))
    pygame.draw.line(win, BLACK, (w * 0.33, 1), (w * 0.33, h))
    pygame.draw.line(win, BLACK, (w * 0.66, 1), (w * 0.66, h))
    for i, v in enumerate(board):
        y = i // 3
        x = i % 3
        if v == 1:
            pygame.draw.circle(
                win, BLACK, (w/6+x*w*0.33, h/6+y*h*0.33), h * 0.1)
            pygame.draw.circle(
                win, WHITE, (w/6+x*w*0.33, h/6+y*h*0.33), h * 0.1 - 2)
        elif v == -1:
            pygame.draw.line(win, BLACK, (w*0.1+x*w*0.33, h*0.1+y*h*0.33),
                                ((x+1)*w*0.33-w*0.1, (y+1)*h*0.33-h*0.1), 2)
            pygame.draw.line(win, BLACK, (w*0.1+x*w*0.33, (y+1) *
                                h*0.33-h*0.1), ((x+1)*w*0.33-w*0.1, h*0.1+y*h*0.33), 2)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(msg, True, BLACK, WHITE)
    textRect = text.get_rect()
    w, h = pygame.display.get_surface().get_size()
    textRect.center = (w//2, h//2)
    win.blit(text, textRect)

    pygame.display.flip()

#   return 0 - game in progress
#          1 - this player win
#          2 - the other player win
#          3 - draw
def boardStatus(board, player):
    dcube = [sum(board[0:3]),
             sum(board[3:6]),
             sum(board[6:9]),
             board[0]+board[3]+board[6],
             board[1]+board[4]+board[7],
             board[2]+board[5]+board[8],
             board[0]+board[4]+board[8],
             board[2]+board[4]+board[6]]
    if 3 * player in dcube:
        return 1
    elif -3 * player in dcube:
        return 2
    elif not(0 in board):
        return 3
    else:
        return 0    

#   return available move of board
def boardAvail(board):
    res = []
    for c,i in enumerate(board):
        if i == 0:
            res.append(c)
    return res

#   return the best move of player
#   minmax : 1 = max, -1 = min
def minimax(board, player, minmax, alpha = MINUSINF, beta = PLUSINF):
    global GRecurCount
    global GNodes
    GRecurCount = GRecurCount + 1
    bs = boardStatus(board, player)
    score = MINUSINF * minmax
    if bs == 3:
        GNodes = GNodes + 1
        return 0
    elif bs == 1:
        GNodes = GNodes + 1
        return (len(boardAvail(board)) + 1) * minmax 
    elif bs == 2:
        GNodes = GNodes + 1
        return (-len(boardAvail(board)) - 1) * minmax 
    else:
        avail = boardAvail(board)
        for i in avail:
            nboard = board.copy()
            nboard[i] = player
            s = minimax(nboard, -1 * player, minmax * -1, alpha, beta)
            if (minmax == 1):
                score = max(s, score)
                if ALPHABETA:
                    alpha = max(s,alpha)
                    if alpha >= beta:
                        break
            elif (minmax == -1):
                score = min(s, score)
                if ALPHABETA:
                    beta = min(s,beta)
                    if alpha >= beta:
                        break
        return score

def nextMove(board, player):
    avail = boardAvail(board)
    maxscore = -10000
    maxmove = 0
    for i in avail:
        nboard = board.copy()
        nboard[i] = player
        s = minimax(nboard,player*-1,-1, MINUSINF, PLUSINF)
        if s > maxscore:
            maxscore = s
            maxmove = i
    print(maxmove, maxscore)
    return maxmove

def main():
    global GRecurCount
    global GNodes
    pygame.init()
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    board = [0,0,0,0,0,0,0,0,0]
    msg = ''
    win = pygame.display.set_mode((300, 300))
    win.fill(WHITE)
    pygame.display.set_caption("Tic Tac Toe")
    drawBoard(win, board, msg)
    w, h = pygame.display.get_surface().get_size()
    run = True
    while run:
        bs = boardStatus(board, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if bs != 0:
                    GRecurCount = 0
                    GNodes = 0
                    board = [0,0,0,0,0,0,0,0,0]
                    msg = ''
                else:
                    (mx, my) = pygame.mouse.get_pos()
                    x = int(mx / (w / 3))
                    y = int(my / (h / 3))
                    if board[y * 3 + x] == 0:                   
                        board[y * 3 + x] = -1
                        bs = boardStatus(board, -1)
                        if bs == 0:
                            board[nextMove(board,1)] = 1
                        bs = boardStatus(board, 1)
                        if bs != 0:
                            if bs == 1:
                                msg = "I win, click to play again"
                            elif bs == 2:
                                msg = "You win, click to play again"
                            else:
                                msg = "Draw, click to play again"
                    if msg:
                        logging.debug(f'Total recursion : {GRecurCount} / Total Nodes : {GNodes}')
            drawBoard(win, board, msg)

    pygame.quit()


if __name__ == "__main__":
    main()
