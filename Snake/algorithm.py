# algorithm
import Snake
from settings import SIZEX, SIZEY
import astar
import time

DRAW = True
DRAW_LINES = True

snk = Snake.Snake()

snk.border_collisions = True
snk.add_end = True

snk.loadimages()

ast = astar.astar(SIZEX, SIZEY)

start_time = time.time()
timer = 0
prevscore = snk.len

while snk.run:
    # Snake
    snk.events()
    snk.loop()
    if DRAW:
        snk.delay(60)
        snk.display()

    # Modes:
    #   0 - Head, tail
    #   1 - tail, head
    #   2 - weird?
    #   3 - random
    mode = 0 #if snk.len < (SIZEX * SIZEY * 0.7) else 2

    # Parameters
    x = snk.xpos
    y = snk.ypos
    target = snk.food[0:2]

    # Mode 1: Head, Tail
    if mode == 0:
        ast.settargets((x[-1], y[-1]), target) # Head -> Food
        ast.block(x, y) # Block snake
        if ast.cal():
            # Draw open and closed cells from A*
            # for c in ast.getclosed():
            #     snk.draw_cell(c[0:2], (255, 0, 0, 60))
            # for c in ast.getopen():
            #     snk.draw_cell(c[0:2], (0, 0, 255, 60))

            path = ast.getpath()
            if DRAW and DRAW_LINES:
                for i in range(len(path) - 1):
                    snk.draw_line(path[i], path[i + 1], (255,0,255))

            ast.clear()
        else:
            # print('Error: Mode 0: Path to Head not found')
            mode = 2 # Straight to mode 2, blocking path to tail won't make it better
    
    if mode == 0:
        ast.settargets((x[0], y[0]), target) # Tail -> Food
        ast.block(x, y) # Block snake
        ast.blockl(path[1:]) # Block path to head
        if ast.cal():
            pathtail = ast.getpath()
            if DRAW and DRAW_LINES:
                for i in range(len(pathtail) - 1):
                    snk.draw_line(pathtail[i], pathtail[i + 1], (255,255,255))
            ast.clear()
        else:
            # print('Error: Mode 0: Path to Tail not found')
            mode = 1
    
    # Mode 1: Tail, Head
    # Path to tail is more important
    if mode == 1:
        ast.clear()
        ast.settargets((x[0], y[0]), target) # Tail -> Food
        ast.block(x, y) # Block snake
        # Don't block this path
        if ast.cal():
            pathtail = ast.getpath()
            if DRAW and DRAW_LINES:
                for i in range(len(pathtail) - 1):
                    snk.draw_line(pathtail[i], pathtail[i + 1], (255,255,255))
            ast.clear()
        else:
            # print('Error: Mode 1: Path to Tail not found') # Tail has no connection
            mode = 2

        ast.settargets((x[-1], y[-1]), target) # Head -> Food
        ast.block(x, y) # Block snake
        ast.blockl(pathtail[1:]) # Block path to tail
        if ast.cal():
            path = ast.getpath()
            if DRAW and DRAW_LINES:
                for i in range(len(path) - 1):
                    snk.draw_line(path[i], path[i + 1], (255,255,255))
            ast.clear()
        else:
            # print('Error: Mode 1: Path to Head not found')
            mode = 2

    # Mode 2: Head -> Tail
    # Move towards tail instead
    if mode == 2:
        # print('Initializing WEIRD?™ mode')
        ast.clear()
        ast.settargets((x[-1], y[-1]), [x[0], y[0]]) # Head to tail
        ast.block(x, y) # Block snake
        if ast.cal(True):
            path = ast.getpath()
            if DRAW and DRAW_LINES:
                for i in range(len(path) - 1):
                    snk.draw_line(path[i], path[i + 1], (255,0,0))
            ast.clear()
        else:
            break

    ast.clear()

    # Move the snake
    snk.prevkey = [0,0,0,0]
    diff = (x[-1] - path[-1][0], y[-1] - path[-1][1])
    if diff == (1, 0):
        snk.prevkey[2] = 1
    if diff == (-1, 0):
        snk.prevkey[0] = 1
    if diff == (0, 1):
        snk.prevkey[1] = 1
    if diff == (0, -1):
        snk.prevkey[3] = 1
    
    if DRAW:
        snk.disp_update()
    else:
        if prevscore != snk.len:
            print('Score:', snk.len)
        

print('Time:', time.time() - start_time)

if DRAW:
    snk.run = True
    snk.disp_update()
    while snk.run:
        snk.delay(60)
        snk.events()

    snk.exit()

print('Score: ', snk.len)





