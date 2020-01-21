import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run Dino Run!')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
cactus_img = [pygame.image.load('Cactus0.png'), pygame.image.load('Cactus1.png'), pygame.image.load('Cactus2.png')]
cloud_img = [pygame.image.load('Cloud0.png'), pygame.image.load('Cloud1.png')]
dino_img = [pygame.image.load('Dino0.png'), pygame.image.load('Dino1.png'), pygame.image.load('Dino2.png'),
            pygame.image.load('Dino3.png'), pygame.image.load('Dino4.png')]
bat0 = pygame.image.load('Bat0.png')
bat1 = pygame.image.load('Bat1.png')
bat2 = pygame.image.load('Bat2.png')
bat3 = pygame.image.load('Bat3.png')
bat0_small = pygame.transform.scale(bat0, (120, 72))
bat1_small = pygame.transform.scale(bat1, (120, 72))
bat2_small = pygame.transform.scale(bat2, (120, 72))
bat3_small = pygame.transform.scale(bat3, (120, 72))
bat_img = [bat0_small, bat1_small, bat2_small, bat3_small]

cactus_options = [69, 449, 37, 410, 40, 420]
bat_options = [70, 250, 300, 350]

dino_img_counter = 0
bat_img_counter = 0
score_counter = 0
max_score = 0

above_cactus = False


class Object:  # Класс для всех игровых объектов
    def __init__(self, x, y, width, image, speed):
        self.x, self.y, self.width, self.speed, self.image = x, y, width, speed, image

    def move(self):  # Перемещение объекта
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):  # изменение параметров объекта
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


# Передаём параметры кактусов и персонажа
cactus_width = 20
cactus_height = 70
cactus_x = 750
cactus_y = display_height - cactus_height - 100

bat_width = 20
bat_height = 70
bat_x = 750
bat_y = display_height - cactus_height - 100

usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height * 2

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30


def create_cactus_arr(array):  # Создание кактусов
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def create_bat_arr(array):  # Создание летучих мышей
    choice = random.randrange(1, 3)
    choice1 = random.randrange(0, 30)
    choice2 = random.randrange(6, 9)
    img = pygame.image.load('Empty.png')
    width = bat_options[0]
    height = bat_options[choice]
    array.append(Object(display_width + 20 * choice1, height, width, img, choice2))


def find_cactus_radius(array):  # Поиск оптимального расстояния между кактусами
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 250)
    return radius


def find_bat_radius(array):  # Поиск оптимального расстояния между летучими мышами
    if array[0].x < display_width:
        radius = display_width
        if radius - array[0].x < 50:
            radius += 150
    else:
        radius = array[0].x

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 1000)
    return radius


def draw_cactus_array(array):  # Рисуем кактусы на экране
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_cactus_radius(array)
            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]
            cactus.return_self(radius, height, width, img)


def draw_bat_array(array):  # Рисуем летучих мышей на экране
    global bat_img_counter
    for bat in array:
        check = bat.move()
        if not check:
            choice = random.randrange(1, 3)
            radius = find_bat_radius(array)
            img = pygame.image.load('Empty.png')
            width = bat_options[0]
            height = bat_options[choice]
            bat.return_self(radius, height, width, img)
        else:
            if bat_img_counter == 15:
                bat_img_counter = 0
            display.blit(bat_img[bat_img_counter // 5], (array[0].x, array[0].y))
            bat_img_counter += 1


def run_game():  # Основная функция, запускающая игровой цикл.
    global score_counter
    global make_jump
    global max_score
    game = True
    land = pygame.image.load('Land.jpg')
    cactus_arr = []
    bat_arr = []
    create_cactus_arr(cactus_arr)
    create_bat_arr(bat_arr)
    cloud = open_random_object()
    scores = 0
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        score_counter += 1
        if score_counter == 5:
            score_counter = 0
            scores += 1
            if scores > max_score:
                max_score = scores
        display.blit(land, (0, 0))
        print_text('Score: ' + str(scores), 620, 20)
        print_text('Best: ' + str(max_score), 620, 45)
        draw_cactus_array(cactus_arr)
        draw_bat_array(bat_arr)
        move_objects(cloud)

        draw_dino()

        if check_collision(cactus_arr):
            game = False
        if check_collision(bat_arr):
            game = False

        pygame.display.update()
        clock.tick(60)
    return game_over()


def jump():  # Прыжок динозавра
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def open_random_object():  # Создание облаков и камней
    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return cloud


def move_objects(cloud):  # Перемещение облаков и камней
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)


def draw_dino():  # Отрисовка персонажа
    global dino_img_counter
    if dino_img_counter == 25:
        dino_img_counter = 0
    display.blit(dino_img[dino_img_counter // 5], (usr_x, usr_y))
    dino_img_counter += 1


def print_text(message, x, y, font_color=(255, 0, 0), font_size=30):  # Вывод текста
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():  # Постановка игры на паузу
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Пауза. Нажмите Enter, чтобы продолжить', 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(60)


def check_collision(barriers):  # Проверка на столкновение
    for barrier in barriers:
        if barrier.y == 449:  # Маленький кактус
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 23 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        elif barrier.y == 410 or barrier.y == 420:  # Другие кактусы
            if not make_jump:
                if barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x - 10 + barrier.width:
                        return True
        else:  # Летучие мыши
            if usr_y <= barrier.y + 50 and usr_y + usr_height - 15 >= barrier.y + 20:
                if barrier.x + 30 <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                    return True
    return False


def game_over():  # Завершение игры при столкновении
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Game Over. Press Enter to play again. Esc to exit', 100, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(60)
                

# Запускаем игровой цикл.
while run_game():
    pass
pygame.quit()
quit()
