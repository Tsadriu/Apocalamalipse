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

        # coins
        self.coin = pygame.image.load('Assets/Art/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 23))


    def ShowHealthBar(self, currentHp, maxHp):
        self.displaySurface.blit(self.healthBar, (20, 10)) # Posizione della health bar
        barWidth = self.healthBarMaxWidth * (currentHp / maxHp) # Calcola la lunghezza della barra (152 * 0.86) per esempio
        healthBarRectangle = pygame.Rect((52, 31), (barWidth, self.healthBarHeight))
        pygame.draw.rect(self.displaySurface, '#f2df4b', healthBarRectangle) #dc4949

        self.displaySurface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(currentHp) + "/" + str(maxHp), False, '#C64355')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.displaySurface.blit(coin_amount_surf, coin_amount_rect)
