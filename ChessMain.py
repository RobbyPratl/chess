import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 # dimension == 8x8
SQ_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR","bN","bB","bQ","bK","bp","wp","wR","wN","wB","wQ","wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
    #can acess an image by saying 'IMAGES['wp']'


def main():
    p.init()
    p.display.set_caption('PyChess')
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = () # keeps track of last user click / it is a tuple
    playerClicks = [] #keeps track of clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #gives x and y
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = ()
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #resets clicks
                    playerClicks = []

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # <-- not an empty tile
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()