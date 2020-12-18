import pygame
import os
import sys

WIDTH, HEIGHT = 1280, 770


def generate_level(level):
    new_player, x, y, player_x, player_y = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player_x, player_y = x, y
    new_player = Player(player_x, player_y)
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.type = tile_type


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        collided_sprite = pygame.sprite.spritecollideany(self, tiles_group)
        if collided_sprite and collided_sprite.type == 'wall':
            self.rect.x -= x
            self.rect.y -= y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [
        "ЗАСТАВКА",
        "",
        "Правила игры",
        "Если в правилах несколько строк,",
        "приходится выводить их построчно"
    ]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.target = player

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if obj.rect.x < -2:
            obj.rect.x += width
        elif obj.rect.x + tile_width > width - 2:
            obj.rect.x -= width
        if obj.rect.y < 0:
            obj.rect.y += height
        elif obj.rect.y + tile_height > height:
            obj.rect.y -= height

    # позиционировать камеру на объекте target
    def update(self):
        self.dx = -(self.target.rect.x + self.target.rect.w // 2 - width // 2)
        self.dy = -(self.target.rect.y + self.target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mario.png')

    tile_width = tile_height = 50

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    pygame.display.set_caption('Персонаж')

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_screen()
    pygame.quit()
    level = load_level('map.txt')  # input('Введите название текстового файла с картой уровня: ')
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    player = generate_level(level)
    camera = Camera()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -tile_height)
                if event.key == pygame.K_DOWN:
                    player.move(0, tile_height)
                if event.key == pygame.K_RIGHT:
                    player.move(tile_width, 0)
                if event.key == pygame.K_LEFT:
                    player.move(-tile_width, 0)

        keys = pygame.key.get_pressed()
        screen.fill(pygame.Color('black'))
        # изменяем ракурс камеры
        camera.update()
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        pygame.display.flip()
