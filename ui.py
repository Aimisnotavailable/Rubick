import pygame

pygame.init()
w, h = 1000, 800
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Rubick")
black, white, dark_blue, navy, green = (0, 0, 0), (255, 255, 255), (0, 0, 80), (0, 0, 128), (0, 100, 0)
font = pygame.font.Font(None, 24)

def rr(s, c, r, rad): pygame.draw.rect(s, c, r, 0, border_radius=rad) 
def txt(s, t, c, p): s.blit(font.render(t, True, c), p) 
def btn(s, r, c, t, tc): rr(s, c, r, 8); tx = r.x + (r.width - font.size(t)[0]) // 2; ty = r.y + (r.height - font.size(t)[1]) // 2; txt(s, t, tc, (tx, ty)) 

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(w - 80, 10, 70, 30).contains(e.pos): print("Menu")
            if pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 40).contains(e.pos): print("Scan")

    screen.fill(dark_blue)
    pygame.draw.rect(screen, navy, (0, 0, w, 50))
    txt(screen, "Notifications", white, (w - 200, 17))
    btn(screen, pygame.Rect(w - 80, 10, 70, 30), green, "Menu", white)

    rr(screen, navy, pygame.Rect(20, 70, w - 40, h - 100), 15)
    txt(screen, "Status", white, (40, 90))
    pygame.draw.circle(screen, green, (w // 2, h // 2 - 50), 30)
    txt(screen, " ------------p r o m p t------------", white, (w // 2 - 100, h // 2 - 10))

    btn(screen, pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 40), green, "RUN SMART SCAN", white)

    y = 150
    for s in ["Protection", "Model"]: txt(screen, s, white, (40, y)); y += 55

   
    pygame.display.flip()

pygame.quit()