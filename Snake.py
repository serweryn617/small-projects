import pygame
import random
from settings import *
import spritesheet

class Snake:
    def __init__(self):
        # Starting snake length
        self.len = ST_LEN

        # Constants/Variables
        self.SIZE_X = SIZEX * GRID
        self.SIZE_Y = SIZEY * GRID

        self.xdelta = 1
        self.ydelta = 0

        self.nextdir = 0 # 0 right, 1 up, 2 left, 3 down

        # Arrays of snake segments positions and directions
        # Start in the middle
        self.xpos = [SIZEX // 2 for _ in range(self.len)]
        self.ypos = [SIZEY // 2 for _ in range(self.len)]

        # Heading: 0 right, 1 up, 2 left, 3 down
        self.dir = [0 for _ in range(self.len)]

        self.timer = -1
        self.prevkey = [0, 0, 0, 0] # R, U, L, D
        self.keys_pressed = [0, 0, 0, 0]
        self.food = [0, 0, True, 0] # x, y, eaten, type
        self.border_collisions = False
        self.add_end = False

        self.notstart = True
        self.run = True

        pygame.init()
        self.win = pygame.display.set_mode((self.SIZE_X, self.SIZE_Y))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()


    def loadimages(self):
        sheet = spritesheet.Spritesheet(SHEET_FILE)
        self.images = sheet.images_at(
            # Left, top, width, height
            [(4*j, 4*i, 4, 4) for i in range(4) for j in range(4)],
            colorkey=(255, 255, 255)
        )
        
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (GRID, GRID))

        # Creating 4 copies of snake textures might not be optimal, but sprites are very small,
        # and it is the easiest way.
        self.snake = [[] for _ in range(4)]
        for i in range(2, 7):
            self.snake[2].append(self.images[i]) # Left - original
            self.snake[0].append(pygame.transform.flip(self.images[i], True, False)) # Right - flip x
            self.snake[1].append(pygame.transform.rotate(self.snake[0][i-2], 90)) # Up - rotate 90 deg
            self.snake[3].append(pygame.transform.rotate(self.snake[2][i-2], 90)) # Down - rotate 90 deg

        # Corner: 4,5,6,7
        self.corner = [
            self.images[7],
            pygame.transform.rotate(self.images[7], 90),
            pygame.transform.rotate(self.images[7], 180),
            pygame.transform.rotate(self.images[7], 270)
        ]

        # Starting screen
        try:
            self.start_img = pygame.image.load(START_FILE).convert()
        except pygame.error as e:
            print('Unable to load image:', START_FILE)
            raise SystemExit(e)

        self.start_img = pygame.transform.scale(self.start_img, (int(GRID * 2.5), int(GRID * 2.5)))
        self.start_img.set_colorkey((255, 255, 255), pygame.RLEACCEL)


    def starting_screen(self):
        # Some starting screen, can be moved to some other method, as it doesn't change
        self.win.fill(BG_COL)
        # pygame.draw.rect(self.win, (0, 180, 0), (self.xpos[0], self.ypos[0], GRID - 1, GRID - 1))
        siz = self.start_img.get_rect().size
        self.win.blit(self.start_img, ((self.SIZE_X - siz[0]) // 2, (self.SIZE_Y - siz[1]) // 2))
        pygame.display.update()


    # Delay between frames
    def delay(self, fr):
        self.clock.tick(fr)


    # Check for the pygame events
    def events(self):
        # Close the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                return
        
        # Check for the keypress
        keys = pygame.key.get_pressed()
        keys = [keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN]]

        if keys != self.prevkey and sum(keys):
            self.prevkey = keys


    # Waits for button input to start the game
    def start(self):
        
        # Don't wait here. Waiting in main loop allows to do something
        # else in the background.
        # while self.notstart: 

        # Wait for any button
        if self.prevkey[0]:
            self.notstart = False
        elif self.prevkey[1]:
            # Set directions
            self.dir = [1 for _ in range(self.len)]
            # Exit loop
            self.notstart = False
        elif self.prevkey[2]:
            self.dir = [2 for _ in range(self.len)]
            self.notstart = False
        elif self.prevkey[3]:
            self.dir = [3 for _ in range(self.len)]
            self.notstart = False


    # Main game loop
    def loop(self):
        # Similar situation here:
        # while self.run:

        # Update positions of segments, except the head, NEEDS AN UPDATE
        for elem in range(self.len - 1):
            self.xpos[elem] = self.xpos[elem + 1] # shift left
            self.ypos[elem] = self.ypos[elem + 1]
            self.dir[elem] = self.dir[elem + 1]
        
        # Update head position and direction and prevent from going backwards
        if self.prevkey[0] and self.dir[-1] != 2:
            self.dir[-1] = 0
            self.xdelta = 1
            self.ydelta = 0
        elif self.prevkey[1] and self.dir[-1] != 3:
            self.dir[-1] = 1
            self.xdelta = 0
            self.ydelta = -1
        elif self.prevkey[2] and self.dir[-1] != 0:
            self.dir[-1] = 2
            self.xdelta = -1
            self.ydelta = 0
        elif self.prevkey[3] and self.dir[-1] != 1:
            self.dir[-1] = 3
            self.xdelta = 0
            self.ydelta = 1

        # Move the head
        self.xpos[-1] += self.xdelta
        self.ypos[-1] += self.ydelta

        # Failure conditions
        # Snake collision
        # if (len > 4): # this isn't really necessary
        for i in range(self.len - 4):
            if (self.xpos[self.len - 1] == self.xpos[i]) and (self.ypos[self.len - 1] == self.ypos[i]):
                self.run = False

        if self.border_collisions:
            # Borders collision
            if (self.xpos[self.len - 1] >= self.SIZE_X) or (self.xpos[self.len - 1] < 0) or \
                (self.ypos[self.len - 1] >= self.SIZE_Y) or (self.ypos[self.len - 1] < 0):
                self.run = False
        else:
            # Border wrapping
            if self.xpos[-1] < 0:
                self.xpos[-1] = SIZEX - 1
            if self.xpos[-1] == SIZEX:
                self.xpos[-1] = 0

            if self.ypos[-1] < 0:
                self.ypos[-1] = SIZEY - 1
            if self.ypos[-1] == SIZEY:
                self.ypos[-1] = 0
                    
        # Eating food
        if self.xpos[self.len - 1] == self.food[0] and self.ypos[self.len - 1] == self.food[1]:
            self.food[2] = True # Deactivate food
            self.len += 1
            # Insert section at the front of the snake
            if not self.add_end:
                self.xpos.append(self.xpos[-1])
                self.ypos.append(self.ypos[-1])
                self.dir.append(self.dir[-1])
            else:
                self.xpos.insert(0, self.xpos[0])
                self.ypos.insert(0, self.ypos[0])
                self.dir.insert(0, self.dir[0])


        # Create food. NEEDS AN UPDATE
        while self.food[2]:
            if self.food[2]:
                self.food[2] = False
                self.food[0] = int(random.random() * SIZEX)
                self.food[1] = int(random.random() * SIZEY)
                self.food[3] = random.randint(0,1)
            for x in range(self.len):
                if self.food[0] == self.xpos[x] and self.food[1] == self.ypos[x]:
                    self.food[2] = True


    # Draw the game
    def display(self):

        # Clear the window
        self.win.fill(BG_COL)

        # Draw food
        if not self.food[2]:
            self.win.blit(self.images[self.food[3]], (self.food[0] * GRID, self.food[1] * GRID))

        for elem in range(self.len):
            pos = (self.xpos[elem] * GRID, self.ypos[elem] * GRID)
            
            # Head
            if elem == self.len - 1:
                # Check if food is close and change to open mouth image
                closed = 1
                if abs(self.xpos[elem] - self.food[0]) <= 1 and \
                    abs(self.ypos[elem] - self.food[1]) <= 1:
                    closed = 0

                self.win.blit(self.snake[self.dir[-1]][closed], pos)

            elif elem == 0: # Tail
                self.win.blit(self.snake[self.dir[1]][4], pos)
                
            # Corners
            # This doesn't work for 'fat' corners, but it draws circle there anyways
            elif self.dir[elem] != self.dir[elem + 1]:
                # Dir: 0 right, 1 up, 2 left, 3 down
                if (self.dir[elem] == 0 and self.dir[elem + 1] == 3) or \
                    (self.dir[elem] == 1 and self.dir[elem + 1] == 2):
                    self.win.blit(self.corner[0], pos)
                if (self.dir[elem] == 0 and self.dir[elem + 1] == 1) or \
                    (self.dir[elem] == 3 and self.dir[elem + 1] == 2):
                    self.win.blit(self.corner[3], pos)

                if (self.dir[elem] == 3 and self.dir[elem + 1] == 0) or \
                    (self.dir[elem] == 2 and self.dir[elem + 1] == 1):
                    self.win.blit(self.corner[2], pos)
                if (self.dir[elem] == 1 and self.dir[elem + 1] == 0) or \
                    (self.dir[elem] == 2 and self.dir[elem + 1] == 3):
                    self.win.blit(self.corner[1], pos)
            
            # Fat sections (check if 2 are on top of each other)
            elif elem < self.len - 2 and self.xpos[elem] == self.xpos[elem + 1] and \
                self.ypos[elem] == self.ypos[elem + 1]:
                self.win.blit(self.images[5], pos)
            
            # Straight sections
            else:
                self.win.blit(self.snake[self.dir[elem]][2], pos)

        # pygame.display.update()

    def disp_update(self):
        pygame.display.update()


    def exit(self):
        pygame.quit()


    # Additional draw methods
    def draw_cell(self, pos, col):
        s = pygame.Surface((GRID, GRID), pygame.SRCALPHA)
        s.fill(col)
        self.win.blit(s, (pos[0] * GRID, pos[1] * GRID))

    def draw_line(self, a, b, col):
        pygame.draw.line(self.win, col, (a[0]*GRID+GRID//2, a[1]*GRID+GRID//2), (b[0]*GRID+GRID//2, b[1]*GRID+GRID//2), 2)

    def draw_circle(self, pos, col, r):
        pygame.draw.circle(self.win, col, (pos[0]*GRID+GRID//2, pos[1]*GRID+GRID//2), r)