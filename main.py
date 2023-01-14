import os
import sys
import pygame
import random

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 100
STEP = 50
size = WIDTH, HEIGHT = 700, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
price = 0
gravity = 1
screen_rect = (0, 0, WIDTH, HEIGHT)


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


def render_multi_line(intro_text):  # создание текста
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        if line == "ЭВЕРМОР":
            intro_rect.x = 315
        else:
            intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        if line == "ЭВЕРМОР":
            text_coord += 70
        text_coord += 10


def start_screen():  # Заставка
    intro_text = ["ЭВЕРМОР", "",
                  "Проберитесь в непреступный",
                  "замок Эвемор и найдите",
                  "секретное завещание Карла XVI,",
                  "чтобы предотвратить",
                  "государственный переворот.",
                  "",
                  "Дойдите до лестницы,",
                  "чтобы подняться на",
                  "следующий этаж.",
                  "Собирайте монеты и",
                  "остеригайтесь шипов.",
                  "Используйте клавиши навигации",
                  "(кнопки со  стрелками)"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    render_multi_line(intro_text)

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


class Particle(pygame.sprite.Sprite):  # Система частиц
    # сгенерируем частицы разного размера
    fire = [load_image("price2.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(price_group2)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity


    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect) or (150 < self.rect.x < 550):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def finish_screen(price, f):  # финальное окно
    if f:
        intro_text = ["ЭВЕРМОР", "",
                      "Поздравляем!",
                      "Вы смогли пробраться",
                      "в непреступный замок Эвемор",
                      "и найти секретное завещание",
                      "Карла XVI.",
                      "Благодаря этому страна избежит ",
                      "государственного переворота",
                      f"Вы заработали {price} дублонов ",
                      f"из 130 возможных."]
    else:
        intro_text = ["ЭВЕРМОР", "",
                      "Вы не смогли пробраться",
                      "в непреступный замок Эвемор",
                      "и найти секретное завещание ",
                      "Карла XVI.",
                      "Попробуйте еще раз."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        create_particles((random.randint(1, 100), random.randint(1, 550)))
        create_particles((random.randint(550, 700), random.randint(1, 550)))
        screen.blit(fon, (0, 0))
        price_group2.draw(screen)
        price_group2.update()
        render_multi_line(intro_text)
        pygame.display.flip()
        clock.tick(10)


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
    'price': load_image('price2.png'),
    'svitok': load_image('svitok.png')
}
player_image = load_image('hero50.png')

tile_width = tile_height = 50


class Price(pygame.sprite.Sprite):  # монеты

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


class Enemies(pygame.sprite.Sprite):  # шипы

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):  # игрок

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
price_group = pygame.sprite.Group()
price_group2 = pygame.sprite.Group()
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
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Lest('lest', x, y)
            elif level[y][x] == '^':
                Lest('svitok', x, y)
            elif level[y][x] == '%':
                Enemies('enemies', x, y)
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
        if pygame.sprite.groupcollide(player_group, enemies_group, False, False):
            screen.fill(pygame.Color(25, 25, 112))
            price_group.draw(screen)
            wall_group.draw(screen)
            lest_group.draw(screen)
            enemies_group.draw(screen)
            player_group.draw(screen)
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
