import pygame
import sys
import os

pygame.init()
pygame.display.set_caption('Game')
WIDTH = 500
HEIGHT = 500
clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    if not os.path.isfile(filename):
        print(f"Файл '{filename}' не найден")
        sys.exit()
    mapp = []
    with open(filename, 'r') as mapFile:
        for i in mapFile:
            mapp.append(i.strip())
    ll = [len(i) for i in mapp]
    bord = max(ll)
    l2 = []
    for i in mapp:
        l2.append(i.ljust(bord, "."))
    return l2


field = load_level(input())
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60


def load_image(name, colorkey=None, transform=None):
    fullname = os.path.join("data/" + name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["главный экран", "это главный экран", "да-да, главный экран"]

    fon = pygame.transform.scale(pygame.image.load('data/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player_pos = x, y
                new_player = Player(x, y)
    return new_player, x, y, player_pos


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == "wall":
            walls_group.add(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        global x, y, speed
        self.check = self.rect
        self.rect.x, self.rect.y = x, y
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect = self.check

            if xc1:
                x -= 50
            if xc:
                x += 50
            if yc1:
                y -= 50
            if yc:
                y += 50


player, lx, ly, position = generate_level(field)
x, y = position
x *= tile_width
x += 15
y *= tile_height
y += 5
start_screen()
running = True
pygame.mouse.set_visible(False)
bg = pygame.Surface((WIDTH, HEIGHT))
tiles_group.draw(bg)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        xc = yc = xc1 = yc1 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 50
                xc = True
            if event.key == pygame.K_RIGHT:
                x += 50
                xc1 = True
            if event.key == pygame.K_UP:
                y -= 50
                yc = True
            if event.key == pygame.K_DOWN:
                y += 50
                yc1 = True
    screen.blit(bg, (0, 0))
    player.update()
    player_group.draw(screen)
    pygame.display.flip()
    screen.fill((255, 255, 255))
terminate()
