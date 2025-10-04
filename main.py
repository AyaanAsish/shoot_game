"""
Ayaan Asish
A space invaders remodel with a battlefield theme.
2025-06-13
ICD2O
Image credits to flaticon
"""

# imports
import pygame
import random
import sys
import time
import Player

# constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# setting up pygame
pygame.init()
pygame.font.init()

# setting up screen and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont("Sans Serif", 50)
medFont = pygame.font.SysFont("Sans Serif", 40)
largeFont = pygame.font.SysFont("Sans Serif", 90)
fpsClock = pygame.time.Clock()

# background
spaceBG = pygame.transform.scale(pygame.image.load("Images/BG.png"), (WIDTH, HEIGHT))


# function to blit an image to screen
def move(x, y, img):
    screen.blit(img, (x, y))


# function to create a custom object of player class
def createPlayer():
    return Player.Player(375, 500, 0, 0,
                         pygame.transform.rotate(
                             pygame.transform.scale(pygame.image.load("Images/Player.png"), (100, 100)), 90),
                         100, True, False)


def createEnemy(dx):
    return Player.Player(random.randint(0, 770), random.randint(20, 180), 4, dx,
                         pygame.transform.scale(pygame.image.load("Images/Enemy.png"), (50, 50)), 50, False, False)


def createCoin():
    return Player.Player(random.randint(0, 770), random.randint(20, 180), 4, 50,
                         pygame.transform.scale(pygame.image.load("Images/Coin.png"), (50, 50)), 50, False, False)


def createMissile(x, y):
    return Player.Player(x, y, 0, -10,
                         pygame.transform.scale(pygame.image.load("Images/Missile.png"), (30, 30)), 30, False, True)


def createSMissile(x, y):
    return Player.Player(x, y, 0, -10,
                         pygame.transform.scale(pygame.image.load("Images/SMissile.png"), (40, 40)), 40, False, True)


def createMine(x, y):
    return Player.Player(x, y, 0, 10, pygame.transform.scale(pygame.image.load("Images/Mine.png"), (40, 40)), 40,
                         False, False)


# main game function
def game():
    global mine
    mine = -1
    ply = createPlayer()
    splBonus = createCoin()
    missile = [createMissile(ply.x + (ply.dim // 4), ply.y + (ply.dim // 2)) for _ in
               range(3)]  # learned from treehouse
    sMissile = [createSMissile(ply.x + (ply.dim // 4), ply.y + (ply.dim // 2)) for _ in range(1)]
    numSM = 1
    score = 0
    rounds = 1
    nextM = 0
    cTime = sMTime = lTime = mTime = time.time()
    running = True
    win = False
    numEny = 7
    enyDx = 50
    eny = [createEnemy(enyDx) for _ in range(numEny)]

    # main loop
    while running:
        # blit background and info/stats to screen
        screen.blit(spaceBG, (0, 0))
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 50))
        screen.blit(font.render(f"Special Missiles: {numSM}", True, (255, 255, 255)), (10, 90))
        screen.blit(font.render(f"ROUND {rounds}", True, (255, 255, 255)), (10, 10))

        # process key clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    ply.dx = 6
                elif event.key == pygame.K_a:
                    ply.dx = -6
                elif event.key == pygame.K_SPACE and time.time() - cTime > 0.5:
                    for i in range(len(missile)):
                        c = (nextM + i) % len(missile)
                        if missile[c].state == "rd":
                            missile[c].x = ply.x + (ply.dim // 4)
                            missile[c].y = ply.y + (ply.dim // 2)
                            missile[c].state = "fr"
                            nextM = (c + 1) % len(missile)
                            break
                    cTime = time.time()
                elif event.key == pygame.K_f and numSM > 0 and time.time() - sMTime > 0.5:
                    for sm in sMissile:
                        if sm.state == "rd":
                            sm.x = ply.x + (ply.dim // 4)
                            sm.y = ply.y + (ply.dim // 2)
                            sm.state = "fr"
                            numSM -= 1
                            sMTime = time.time()
                            break
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_d, pygame.K_a):
                    ply.dx = 0

        # process mine after it is added in round 4
        if mine != -1:
            if mine.y > 525:
                mine.y = 525

            if Player.Player.collisionR(mine, ply):
                running = False
                break

            if time.time() - mTime > 3:
                mine = createMine(random.randint(0, 700), random.randint(0, 100))
                mTime = time.time()

            mine.moveTickY()
            move(mine.x, mine.y, mine.img)

        ply.moveTickX()  # move player
        # move coin to get special missile
        splBonus.moveTickX()
        if splBonus.checkBoundaryX(WIDTH) != -1:
            splBonus.moveTickY()
            splBonus.dx *= -1

        # process enemy movement and collisions
        newEnemies = []
        for e in eny:
            e.moveTickX()
            if e.checkBoundaryX(WIDTH) != -1:
                e.x = e.checkBoundaryX(WIDTH)
                e.moveTickY()
                e.dx *= -1

            for m in missile:
                if Player.Player.collisionR(e, m):
                    e.setRand()
                    m.state = "rd"
                    m.x = ply.x + (ply.dim // 4)
                    m.y = ply.y + (ply.dim // 2)
                    score += 1

                if Player.Player.collisionR(splBonus, m):
                    if numSM < 10:
                        numSM += 1
                    splBonus.setRand()
                    if len(sMissile) < numSM:
                        sMissile.append(createMissile(ply.x + (ply.dim // 4), ply.y + (ply.dim // 2)))

            for sm in sMissile:
                if Player.Player.collisionS(e, sm):
                    e.setRand()
                    score += 1

                if Player.Player.collisionR(splBonus, sm):
                    if numSM < 10:
                        numSM += 1
                    splBonus.setRand()
                    if len(sMissile) < numSM:
                        sMissile.append(createMissile(ply.x + (ply.dim // 4), ply.y + (ply.dim // 2)))

            move(e.x, e.y, e.img)
            if e.y > ply.y - (ply.dim // 2):
                running = False
                break

            newEnemies.append(e)

        eny = newEnemies

        # process boundaries for player
        if ply.checkBoundaryX(WIDTH) != -1:
            ply.x = ply.checkBoundaryX(WIDTH)

        # missile and special missile processing
        for m in missile:
            if m.state == "fr":
                move(m.x, m.y, m.img)
                m.moveTickY()
                if m.y < 0:
                    m.state = "rd"
                    m.x = ply.x + (ply.dim // 4)
                    m.y = ply.y + (ply.dim // 2)

        for sm in sMissile:
            if sm.state == "fr":
                move(sm.x, sm.y, sm.img)
                sm.moveTickY()
                if sm.y < 0:
                    sm.state = "rd"
                    sm.x = ply.x + (ply.dim // 4)
                    sm.y = ply.y + (ply.dim // 2)

        # blit player and bonus coin to screen
        move(ply.x, ply.y, ply.img)
        move(splBonus.x, splBonus.y, splBonus.img)

        fpsClock.tick(FPS)
        pygame.display.update()

        # process rounds
        if time.time() - lTime > 10:
            rounds += 1
            lTime = time.time()
            screen.blit(spaceBG, (0, 0))
            screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render(f"Special Missiles: {numSM}", True, (255, 255, 255)), (10, 50))
            screen.blit(font.render(f"ROUND: {rounds}", True, (255, 255, 255)), (250, 400))
            pygame.display.update()
            time.sleep(1)

            if rounds == 10:
                win = True
                break
            elif rounds > 3:
                mine = createMine(random.randint(0, 700), random.randint(0, 100))

            numEny += 1
            enyDx += 20
            eny.clear()
            for _ in range(numEny):
                eny.append(createEnemy(enyDx))

    return score, win, ply


# function to show win/gameover upon game end, option to play again too
def showEndScreen(score, win, ply):
    while True:
        screen.blit(spaceBG, (0, 0))
        move(ply.x, ply.y, ply.img)
        mouse = pygame.mouse.get_pos()

        if win:
            screen.blit(largeFont.render(f"SCORE: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(largeFont.render("YOU WIN", True, (255, 255, 255)), (275, 400))
        else:
            screen.blit(font.render(f"SCORE: {score}", True, (255, 255, 255)), (10, 10))
            screen.blit(font.render("GAME OVER", True, (255, 255, 255)), (300, 400))

        #  learned how to make buttons from geeks for geeks
        color = (200, 200, 250) if (300 < mouse[0] < 500 and 300 < mouse[1] < 350) else (200, 200, 230)
        pygame.draw.rect(screen, color, [300, 300, 200, 50])
        screen.blit(medFont.render("New Game", True, (255, 255, 255)), (325, 315))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and 300 < mouse[0] < 500 and 300 < mouse[1] < 350:
                main()

        pygame.display.update()
        fpsClock.tick(FPS)


# function processes the gameloop followed by the endscreen
def main():
    score, win, ply = game()
    showEndScreen(score, win, ply)


main()
