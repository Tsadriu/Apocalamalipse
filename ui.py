import pygame


class UI:
    def __init__(self, surface):
        # setup
        self.displaySurface = surface

        # health
        self.healthBar = pygame.image.load('Assets/Art/ui/healthBar.png').convert_alpha()
        self.healthBarMaxWidth = 154
        self.font = pygame.font.Font('Assets/Art/ui/AGoblinAppears-o2aV.ttf', 15)
        self.healthBarHeight = 18

    def ShowHealthBar(self, currentHp, maxHp):
        self.displaySurface.blit(self.healthBar, (20, 10)) # Posizione della health bar
        barWidth = self.healthBarMaxWidth * (currentHp / maxHp) # Calcola la lunghezza della barra (152 * 0.86) per esempio
        healthBarRectangle = pygame.Rect((52, 31), (barWidth, self.healthBarHeight))
        pygame.draw.rect(self.displaySurface, '#F2DF4B', healthBarRectangle)
        hpText = self.font.render(str(currentHp) + "/" + str(maxHp), False, '#C64355')
        hpRectangle = hpText.get_rect(midleft=(75, 39))
        self.displaySurface.blit(hpText, hpRectangle)
