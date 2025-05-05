import pygame

Font = None

def rects(canvas,numx,numy):
    for i in range(numy):
        for j in range(numx):
            pygame.draw.rect(canvas, (255, 0, 0), pygame.Rect(30 * j, 30 * i, 30, 30), 1)
            Font.render_to(canvas,(30 * j + 10, 30 * i + 15), '123',(0,255,255),(255,255,255),0)

if __name__ == '__main__':
    pygame.init()
    size = width,height = 600, 800
    pygame.display.set_caption("test")
    canvas = pygame.display.set_mode(size)
    Font =  pygame.freetype.Font("./simhei.ttf", size=10)
    exit = False
    while not exit:
        canvas.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
        rects(canvas,20,25)
        pygame.display.update()

