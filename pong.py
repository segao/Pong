import pygame, sys
from pygame.locals import *

#Define screen update rate
FPS = 200
FPSCLOCK = pygame.time.Clock()
#Define window
WIDTH = 800
HEIGHT = 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
#Define colors
GRAY = (51,51,51)
BLACK = (0,0,0)
WHITE = (255,255,255)
THICKNESS = 10 #line thickness for borders used in game
BALL = 12 #side length of ball
PADDLEWIDTH = 10
PADDLEHEIGHT = 80
PADDLEOFFSET = 20 #paddle distance from edge of screen


def drawScreen():
    DISPLAY.fill(BLACK)
    pygame.draw.rect(DISPLAY, WHITE, (WIDTH/2-THICKNESS/2, 50, 3, HEIGHT)) #center line
    pygame.draw.rect(DISPLAY, WHITE, (0, 0, WIDTH, THICKNESS)) #top border
    pygame.draw.rect(DISPLAY, WHITE, (0, HEIGHT-THICKNESS, WIDTH, THICKNESS)) #bottom border

def drawPaddle(paddle):
    #prevents paddle from going too high
    if paddle.top < THICKNESS:
        paddle.top = THICKNESS
    #prevents paddle from going too low
    elif paddle.bottom > HEIGHT - THICKNESS:
        paddle.bottom = HEIGHT - THICKNESS
    pygame.draw.rect(DISPLAY, WHITE, paddle)

def drawBall(ball):
    #prevents ball from going too high
    if ball.top < THICKNESS:
        ball.top = THICKNESS
    #prevents ball from going too low
    elif ball.bottom > HEIGHT - THICKNESS:
        ball.bottom = HEIGHT - THICKNESS
    elif ball.left < 0:
        ball.left = 0
    elif ball.right > WIDTH:
        ball.right = WIDTH
    pygame.draw.rect(DISPLAY, WHITE, ball)

def moveBall(ball, ballXDir, ballYDir):
    ball.x += 1.1 * ballXDir
    ball.y += 1.1 * ballYDir
    return ball

def checkCollision(ball, ballXDir, ballYDir):
    #if ball hits top or bottom of screen, change direction
    if ball.top == THICKNESS or ball.bottom == (HEIGHT - THICKNESS):
        ballYDir = ballYDir * -1
    if ball.left == 0 or ball.right == WIDTH:
        ballXDir = ballXDir * -1
    return ballXDir, ballYDir

def checkHit(paddle1, paddle2, ball, ballXDir):
    #if hit by player paddle on left side
    if ballXDir == -1 and paddle1.right == ball.left and paddle1.top < ball.top  and paddle1.bottom > ball.bottom:
        return -1
    #if hit by computer paddle on right side
    elif ballXDir == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

def checkScore1(ball, score1):
    if ball.right == WIDTH:
        score1 += 1
    return score1

def checkScore2(ball, score2):
    if ball.left == 0:
        score2 += 1
    return score2
    

def displayScore (score1, score2):
    result = FONT.render("%s : %s" %(score1, score2), True, WHITE)
    resultRECT = result.get_rect()
    resultRECT.center = (WIDTH/2-4, 30)
    DISPLAY.blit(result, resultRECT)

def opponent(paddle2, ball, ballXDir):
    #if ball is moving away to the left, center computer paddle
    if ballXDir == -1:
        #if paddle is above middle of screen, move down toward center
        if paddle2.centery < HEIGHT/2:
            paddle2.y += 2
        #if paddleis below, move up
        elif paddle2.centery > HEIGHT/2:
            paddle2.y -= 2
    #if ball is moving toward paddle to the right, move toward ball
    elif ballXDir == 1:
        #if ball is below paddle, move down
        if paddle2.centery < ball.centery:
            paddle2.y += 2
        else:
            paddle2.y -= 2
    return paddle2


class Option:
    hovered = False
    def __init__(self, msg, pos): 
        self.msg = msg #text on button
        self.pos = pos #x,y coordinate of top left
        self.rect()
        self.draw()
    def draw(self):
        self.set_rend()
        DISPLAY.blit(self.rend, self.rect)
    def set_rend(self):
        self.rend = OPTIONFONT.render(self.msg, 1, self.hover())
    def rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
    def hover(self):
        if self.hovered:
            return GRAY
        else:
            return WHITE


pygame.init()
TITLEFONT = pygame.font.Font(None, 110)
SIG = pygame.font.Font(None, 14)
OPTIONFONT = pygame.font.Font(None, 40)
FONT = pygame.font.Font(None, 40)
playerNum = [Option("Single Player", (125, 375)), Option("Two Players", (475, 375)), Option("Quit", (725, 550))]
welcome = TITLEFONT.render("PONG", True, WHITE)
welcomeRect = welcome.get_rect()
welcomeRect.center = ((WIDTH/2),(HEIGHT/2))
name = SIG.render("Sharon Gao, 2016", True, WHITE)
nameRect = name.get_rect()
nameRect.x = 0
nameRect.y = 0

def menu():
    while True:
        DISPLAY.fill(BLACK)
        DISPLAY.blit(welcome, welcomeRect)
        DISPLAY.blit(name, nameRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if playerNum[0].rect.collidepoint(pygame.mouse.get_pos()):
                    game(1)
                elif playerNum[1].rect.collidepoint(pygame.mouse.get_pos()):
                    game(2)
                elif playerNum[2].rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        for option in playerNum:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def winner(player1Score, player2Score):
    while True:
        DISPLAY.fill(BLACK)
        if player1Score > player2Score:
            winner = TITLEFONT.render("Player 1 Wins!", True, WHITE)
            winnerRect = winner.get_rect()
            winnerRect.center = ((WIDTH/2),(HEIGHT/2))
        elif player2Score > player1Score:
            winner = TITLEFONT.render("Player 2 Wins!", True, WHITE)
            winnerRect = winner.get_rect()
            winnerRect.center = ((WIDTH/2),(HEIGHT/2))
        DISPLAY.blit(winner, winnerRect)
        options = [Option("Play Again", (325, 375)), Option("Quit", (725, 550))]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if options[0].rect.collidepoint(pygame.mouse.get_pos()):
                    menu()
                elif options[1].rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def game(numPlayers):
    playerY = (HEIGHT - PADDLEHEIGHT) / 2
    paddle1 = pygame.Rect(PADDLEOFFSET, playerY, PADDLEWIDTH, PADDLEHEIGHT)
    paddle2 = pygame.Rect(WIDTH-PADDLEOFFSET-PADDLEWIDTH, playerY, PADDLEWIDTH, PADDLEHEIGHT)
    score1 = 0
    score2 = 0

    ball = pygame.Rect(WIDTH/2 - BALL/2 - 3, HEIGHT/2 - BALL/2, BALL, BALL)
    ballXDir = 1 #left = -1, right = 1
    ballYDir = 1 #up = -1, down = 1

    MOVE = False
    while True:
        while MOVE is False:
            drawScreen()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball)
            displayScore(score1, score2)
            for event in pygame.event.get():
                if event.type == KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_s or event.key == pygame.K_DOWN):
                    MOVE = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
                    
        key_pressed = pygame.key.get_pressed()
        if numPlayers == 1:
            if key_pressed[K_UP] or key_pressed[K_w]:
                paddle1.y -= 2
            elif key_pressed[K_DOWN] or key_pressed[K_s]:
                paddle1.y += 2
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            paddle2 = opponent(paddle2, ball, ballXDir)
        elif numPlayers == 2:
            if key_pressed[K_UP]:
                paddle2.y -= 2
            elif key_pressed[K_DOWN]:
                paddle2.y += 2
            elif key_pressed[K_w]:
                paddle1.y -= 2
            elif key_pressed[K_s]:
                paddle1.y += 2
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
        drawScreen()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        ball = moveBall(ball, ballXDir, ballYDir)
        ballXDir, ballYDir = checkCollision(ball, ballXDir, ballYDir)
        ballXDir = ballXDir * checkHit(paddle1, paddle2, ball, ballXDir)
        score1 = checkScore1(ball, score1)
        score2 = checkScore2(ball, score2)
        displayScore(score1, score2)
        if score1 == 7 or score2 == 7:
            winner(score1, score2)
            break
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
if __name__ == '__main__':
    menu()
    
