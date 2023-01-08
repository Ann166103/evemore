import os
import sys
import random
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
STEP = 50
size = WIDTH, HEIGHT = 700, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
price = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # прозрачный цвет
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


def start_screen():  # Заставка
    intro_text = ["ЭВЕМОР", "",
                  "Проберитесь в непреступный",
                  "замок Эвемор.",
                  "",
                  "Дойдите до лестницы,",
                  "чтобы подняться на",
                  "следующий этаж"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        if line == "ЭВЕМОР":
            intro_rect.x = 315
        else:
            intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        if line == "ЭВЕМОР":
            text_coord += 70
        text_coord += 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(price):
    fon = pygame.transform.scale(load_image('fon4.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                finish_screen(price, False)
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen(price, f):
    if f:
        intro_text = ["ЭВЕМОР", "",
                      "Поздравляем!",
                      "Вы смогли пробраться",
                      "в непреступный замок Эвемор",
                      f"И заработали {price} монет."]
    else:
        intro_text = ["ЭВЕМОР", "",
                      "Вы не смогли пробраться",
                      "в непреступный замок Эвемор",
                      f"Попробуйте еще раз."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        if line == "ЭВЕМОР":
            intro_rect.x = 315
        else:
            intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        if line == "ЭВЕМОР":
            text_coord += 70
        text_coord += 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # return  # начинаем игру
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('wall3.png'),
    'enemies': load_image('enemis.png'),
    'lest': load_image('lest5.png'),
    'price': load_image('price2.png')
}
player_image = load_image('hero50.png')

tile_width = tile_height = 50


class Price(pygame.sprite.Sprite):  # пустое пространство

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(price_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):  # стены

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lest(pygame.sprite.Sprite):  # лестница

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(lest_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemies(pygame.sprite.Sprite):  # враги

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
price_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
lest_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Price('price', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '@':
                # Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Lest('lest', x, y)
            elif level[y][x] == '%':
                Enemies('enemies', x, y)
                # AnimatedSprite(load_image("dragon8x2.png"), 8, 2, x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


start_screen()


def osnov(player, price):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                    if player.rect.x < 0:
                        player.rect.x = 0
                    if pygame.sprite.groupcollide(player_group, wall_group, False, False):
                        player.rect.x += STEP
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                    if player.rect.x > WIDTH - STEP:
                        player.rect.x = WIDTH - STEP
                    if pygame.sprite.groupcollide(player_group, wall_group, False, False):
                        player.rect.x -= STEP
                if event.key == pygame.K_UP:
                    player.rect.y -= STEP
                    if player.rect.y < 0:
                        player.rect.y = 0
                    if pygame.sprite.groupcollide(player_group, wall_group, False, False):
                        player.rect.y += STEP
                if event.key == pygame.K_DOWN:
                    player.rect.y += STEP
                    if player.rect.y > HEIGHT - STEP:
                        player.rect.y = HEIGHT - STEP
                    if pygame.sprite.groupcollide(player_group, wall_group, False, False):
                        player.rect.y -= STEP
        if pygame.sprite.groupcollide(player_group, price_group, False, True):
            price += 10
        if pygame.sprite.groupcollide(player_group, enemies_group, True, False):
            return (1, price)
        if not pygame.sprite.groupcollide(player_group, lest_group, False, False):
            screen.fill(pygame.Color(25, 25, 112))
            price_group.draw(screen)
            wall_group.draw(screen)
            lest_group.draw(screen)
            enemies_group.draw(screen)
            player_group.draw(screen)
        else:
            price_group.empty()
            wall_group.empty()
            lest_group.empty()
            enemies_group.empty()
            player_group.empty()
            return (2, price)

        pygame.display.flip()
        clock.tick(FPS)


def level1(price):
    player, level_x, level_y = generate_level(load_level('level1.txt'))
    a = osnov(player, price)
    if a[0] == 1:
        game_over_screen(a[1])
    if a[0] == 2:
        level2(a[1])
    terminate()


def level2(price):
    player, level_x, level_y = generate_level(load_level('level2.txt'))
    a = osnov(player, price)
    if a[0] == 1:
        game_over_screen(a[1])
    if a[0] == 2:
        level3(a[1])
    terminate()


def level3(price):
    player, level_x, level_y = generate_level(load_level('level3.txt'))
    a = osnov(player, price)
    if a[0] == 1:
        game_over_screen(a[1])
    if a[0] == 2:
        finish_screen(a[1], True)
    terminate()


level1(price)