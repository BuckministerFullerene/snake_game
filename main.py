import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirn_x=1, dirn_y=0, color='black'):
        # dir set to 1 so snake starts moving automatically
        self.pos = start
        self.dirn_x = 1
        self. dirn_y = 0
        self.color = color

    def move(self, dirn_x, dirn_y):
        self.dirn_x = dirn_x
        self.dirn_y = dirn_y
        self.pos = (self.pos[0] + self.dirn_x, self.pos[1] + self.dirn_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        # i for row
        i = self.pos[0]
        # j for column
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        # draw eyes
        if eyes:
            centre = dis//2
            radius = 3
            circle_middle = (i*dis+centre-radius, j*dis+8)
            circle_middle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, "white", circle_middle, radius)
            pygame.draw.circle(surface, "white", circle_middle2, radius)


class Snake(object):
    body = []
    # created a dictionary for turns
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # starting position of the cube
        self.head = Cube(pos)
        # append the body to the head
        self.body.append(self.head)
        # direction and keep track of direction
        self.dirn_x = 0
        self.dirn_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirn_x = -1
                    self.dirn_y = 0
                    # to remember where the first cube turned so others can follow
                    # head position set as key
                    self.turns[self.head.pos[:]] = [self.dirn_x, self.dirn_y]

                # adding elif to make sure not more than one key is pressed at once
                elif keys[pygame.K_RIGHT]:
                    self.dirn_x = 1
                    self.dirn_y = 0
                    self.turns[self.head.pos[:]] = [self.dirn_x, self.dirn_y]

                elif keys[pygame.K_UP]:
                    self.dirn_x = 0
                    self.dirn_y = -1
                    self.turns[self.head.pos[:]] = [self.dirn_x, self.dirn_y]

                elif keys[pygame.K_DOWN]:
                    self.dirn_x = 0
                    self.dirn_y = 1
                    self.turns[self.head.pos[:]] = [self.dirn_x, self.dirn_y]

        # get index (i) and cube object (c) in the self.body
        for i, c in enumerate(self.body):
            # take that cube object position and add to turn list
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                # move in direction x, y
                c.move(turn[0], turn[1])
                # after last cube body in turn remove the turn from list
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                # border checking
                # if reached the left side of the screen then start from the right
                if c.dirn_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirn_x == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                # for moving down the screen
                elif c.dirn_y == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirn_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                # if not going to edge of screen then continue in same direction as before
                else:
                    c.move(c.dirn_x, c.dirn_y)

    def reset(self, pos):
        # setting a new head
        self.head = Cube(pos)
        # clearing self.body which is a class variable
        self.body = []
        # setting a head
        self.body.append(self.head)
        self.turns = {}
        self.dirn_x = 0
        self.dirn_y = 1

    def add_cube(self):
        # first figure out the location of the tail
        # to add snack to the end of the tail
        # last element in the list
        tail = self.body[-1]
        dx, dy = tail.dirn_x, tail.dirn_y

        # to check direction of movement of cube in order to add the snack
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirn_x = dx
        self.body[-1].dirn_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            # check if first cube and draw eyes
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    # space between the grids
    size_btwn = w // rows

    x = 0
    y = 0
    i = 1
    for i in range(rows):
        x = x + size_btwn
        y = y + size_btwn
        # pygame function to draw line every iteration of loop
        pygame.draw.line(surface, "#808080", (x,0), (x,w))
        pygame.draw.line(surface, "#808080", (0,y), (w,y))


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill("#808080")
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # to prevent snack from appearing on snake, lambda is a function
        # can also be done using for loop
        # check positions of x,y
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# main loop
def main():
    global width, rows, s, snack
    # working on grid design so dirn_x and dirn_y are grid position
    # not based on the pixels position
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake("black", (10, 10))
    snack = Cube(random_snack(rows, s), color="black")
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # delay 50 ms so programs doesn't run fast
        pygame.time.delay(50)
        clock.tick(10)
        # to check if a key has been pressed
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color="black")

        # looping through every cube in the body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You lost!', 'Play again...')
                # reset to default position
                s.reset((10, 10))
                # end the loop
                break

        redraw_window(win)

    pass


main()

