import pygame
import numpy as np
from fourier import fourier


# Window size
SIZE_X = 1500
SIZE_Y = 800

# Window elements: x, y, w, h
INPUT_RECT = 50, 50, 700, 700
PLOT_X = 800, 50, 650, 200
PLOT_Y = 800, 300, 650, 200
START = 800, 550, 100, 100

# Animation time
ANIM_TIME = 360 # frames

# Number of Fourier coefficients to calculate
COEFFICIENTS = 10


def to_screen_pos(pos):
    x = pos[0] + INPUT_RECT[0] + INPUT_RECT[2] / 2
    y = -pos[1] + INPUT_RECT[1] + INPUT_RECT[3] / 2
    return x, y


recdata = []
def reconstruct(a, b, a2, b2, frame, r=0, pos=(0,0)):
    # pygame.draw.circle(win, (255,0,0), to_screen_pos(pos), abs(b[r]), 1)
    endpos = [
        pos[0] + np.cos(2*np.pi*(r+1)*frame/ANIM_TIME)*a[r] + np.sin(2*np.pi*(r+1)*frame/ANIM_TIME)*b[r],
        pos[1]
    ]
    pygame.draw.line(win, (0,0,255), to_screen_pos(pos), to_screen_pos(endpos))
    
    endpos2 = [
        endpos[0],
        endpos[1] + np.cos(2*np.pi*(r+1)*frame/ANIM_TIME)*a2[r] + np.sin(2*np.pi*(r+1)*frame/ANIM_TIME)*b2[r]
    ]
    pygame.draw.line(win, (0,0,255), to_screen_pos(endpos), to_screen_pos(endpos2))

    r += 1
    if r < len(a):
        reconstruct(a, b, a2, b2, frame, r, endpos2)
    else:
        recdata.append(endpos2)


def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


datax = []
datay = []
capture_pos = False

ak, bk, ak2, bk2 = [], [], [], []
mean_val = [0, 0]

anim = False
frame = 0

pygame.init()
win = pygame.display.set_mode((SIZE_X, SIZE_Y))
pygame.display.set_caption('Gravity')
clock = pygame.time.Clock()

run = True
while run:
    # 60hz refresh
    clock.tick(60)

    # close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # LMB down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            # Inside drawing rectangle
            if INPUT_RECT[0] < event.pos[0] < INPUT_RECT[0] + INPUT_RECT[2] and INPUT_RECT[1] < event.pos[1] < INPUT_RECT[1] + INPUT_RECT[3]:
                datax.append(event.pos[0] - INPUT_RECT[0] - INPUT_RECT[2] / 2)
                datay.append(-event.pos[1] + INPUT_RECT[1] + INPUT_RECT[3] / 2)
                capture_pos = True

            # Inside start button
            if START[0] < event.pos[0] < START[0] + START[2] and START[1] < event.pos[1] < START[1] + START[3]:
                ak, bk, mean_val[0] = fourier(datax, COEFFICIENTS)
                ak2, bk2, mean_val[1] = fourier(datay, COEFFICIENTS)
                recdata = []
                anim = True

        # LMB up
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            capture_pos = False
    
    # clear canvas
    win.fill((0,0,0))
    
    # ====================================================================================================
    # Capturing position
    # ====================================================================================================

    if capture_pos:
        pos = pygame.mouse.get_pos()
        x = pos[0] - INPUT_RECT[0] - INPUT_RECT[2] / 2
        y = -pos[1] + INPUT_RECT[1] + INPUT_RECT[3] / 2
        if dist((x, y), (datax[-1], datay[-1])) > 5:
            datax.append(x)
            datay.append(y)

    # ====================================================================================================
    # Plotting
    # ====================================================================================================

    # x plot
    midplotx = PLOT_X[1] + PLOT_X[3] / 2
    pygame.draw.line(win, (120,120,120), (PLOT_X[0], midplotx), (PLOT_X[0] + PLOT_X[2], midplotx))
    pygame.draw.rect(win, (255,255,255), pygame.Rect(PLOT_X), 1)

    # y plot
    midploty = PLOT_Y[1] + PLOT_Y[3] / 2
    pygame.draw.line(win, (120,120,120), (PLOT_Y[0], midploty), (PLOT_Y[0] + PLOT_Y[2], midploty))
    pygame.draw.rect(win, (255,255,255), pygame.Rect(PLOT_Y), 1)

    # input rectangle
    mid = INPUT_RECT[0] + INPUT_RECT[2] / 2, INPUT_RECT[1] + INPUT_RECT[3] / 2
    pygame.draw.line(win, (120,120,120), (INPUT_RECT[0], mid[1]), (INPUT_RECT[0] + INPUT_RECT[2], mid[1]))
    pygame.draw.line(win, (120,120,120), (mid[0], INPUT_RECT[1]), (mid[0], INPUT_RECT[1] + INPUT_RECT[3]))
    pygame.draw.rect(win, (255,255,255), pygame.Rect(INPUT_RECT), 1)

    # display current data
    prevxposx = PLOT_X[0]
    prevxposy = PLOT_Y[0]
    for p in range(1, len(datax)):
        # draw lines inside input rect
        pygame.draw.line(
            win,
            (255,255,0),
            (datax[p-1] + mid[0], -datay[p-1] + mid[1]),
            (datax[p] + mid[0], -datay[p] + mid[1])
        )

        # draw x plot
        xpos = PLOT_X[0] + PLOT_X[2] / (len(datax) - 1) * (p)
        scale = PLOT_X[3] / INPUT_RECT[2]
        pygame.draw.line(
            win,
            (255,0,0),
            (prevxposx, midplotx - datax[p-1] * scale),
            (xpos, midplotx - datax[p] * scale)
        )
        prevxposx = xpos

        # draw y plot
        xpos = PLOT_Y[0] + PLOT_Y[2] / (len(datay) - 1) * (p)
        scale = PLOT_Y[3] / INPUT_RECT[3]
        pygame.draw.line(
            win,
            (0,255,0),
            (prevxposy, midploty - datay[p-1] * scale),
            (xpos, midploty - datay[p] * scale)
        )
        prevxposy = xpos

    # ====================================================================================================
    # Buttons
    # ====================================================================================================

    # start button
    pygame.draw.rect(win, (0,200,0), pygame.Rect(START))

    # ====================================================================================================
    # Display fourier animation
    # ====================================================================================================

    if anim:
        # Animation time
        frame += 1
        if frame == ANIM_TIME:
            frame = 0
            anim = False

        # recdata = []
        reconstruct(ak, bk, ak2, bk2, frame, pos=mean_val)

    for p in range(1, len(recdata)):
        pygame.draw.line(
            win,
            (255,0,0),
            to_screen_pos((recdata[p-1][0], recdata[p-1][1])),
            to_screen_pos((recdata[p][0], recdata[p][1]))
        )

    # ====================================================================================================
    # Update display; End of the loop
    # ====================================================================================================
    
    # update frame
    pygame.display.update()

# end of the loop
pygame.quit()































