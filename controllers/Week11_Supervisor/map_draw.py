import pygame as pg

# pip install pygame==2.0.0.dev10

"""
With this program you can draw  an occupancy grid map on the
screen with pygame. Hit the "s" key to save map.png
"""

def init():
    global screen
    pg.init()
    screen = pg.display.set_mode((200, 200))
    mainloop()


drawing = False
#this is the scale factor. By default, we'll work with a 200cm by 200cm map,
#where grid cells are 10cm by 10cm. You can change this.
w = 10
#color used to represent objects
color = (255, 255, 255)


def draw(event):
    global drawing, last_pos, w

    if event.type == pg.MOUSEMOTION:
        if (drawing):
            mouse_position = pg.mouse.get_pos()
            #get current mouse pos
            mxraw,myraw = mouse_position
            #round mouse pos to respect grid size
            mx = int(mxraw/w)*w
            my = int(myraw/w)*w
            pg.draw.rect(screen, color,pg.Rect(mx,my, w,w))
    elif event.type == pg.MOUSEBUTTONUP:
        mouse_position = (0, 0)
        drawing = False
        last_pos = None
    elif event.type == pg.MOUSEBUTTONDOWN:
        drawing = True


def mainloop():
    global screen
    loop = 1
    while loop:
        # checks every user interaction in this list
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    pg.image.save(screen, "map.png")
            draw(event)
        pg.display.flip()
    pg.quit()


init()
