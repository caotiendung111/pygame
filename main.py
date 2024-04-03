import pygame, sys, random
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()
#ham tao ong
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #chọn 1 chiều cao ngẫu nhiên ở List pipe_height
    bottom_pipe = pipe_green.get_rect(midtop=(500, random_pipe_pos*1.2))
    top_pipe = pipe_green.get_rect(midtop=(500, random_pipe_pos - 650))
    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_green,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_green,False,True)
            screen.blit(flip_pipe, pipe)
def check_vacham(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            hit_sound.play()
            return False
    return True
def rotate_bird(bird1):
    new_bird  = pygame.transform.rotozoom(bird1,-bird_move*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(gamestate):
    if gamestate == "main game":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if gamestate == "game over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)

screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)
#tạo biến cho game
gravity = 0.25
bird_move = 0 #lúc đầu chưa di chuyển
game_active = True
score = 0
high_score = 0
#chèn background
background = pygame.image.load('background-night.png').convert()
background = pygame.transform.scale2x(background)
#chèn sàn
floor = pygame.image.load('floor.png').convert()  #.convert làm cho pygame nhận biết va chạm nhanh hơn
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo chim
bird_up = pygame.transform.scale2x(pygame.image.load("yellowbird-upflap.png")).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load("yellowbird-midflap.png")).convert_alpha()
bird_down = pygame.transform.scale2x(pygame.image.load("yellowbird-downflap.png")).convert_alpha()
bird_list = [bird_down,bird_mid,bird_up] #0,1,2
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('yellowbird-midflap.png').convert_alpha() #phía trên rotozoom taoj ra 1 lớp màu đen, dùng corvert_alpha để làm đẹp
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100,384))
#tao timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
#tạo ống
pipe_green = pygame.image.load('pipe-green.png').convert()
pipe_green = pygame.transform.scale2x(pipe_green)
pipe_list = []
#tạo timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,1200) #sau 1,2s th sẽ xh ống mới
# tạo ống ngẫu nhie
pipe_height = [250,300,400]
#Tao man hinh ket thuc
game_over_surface  = pygame.transform.scale2x(pygame.image.load("message.png")).convert_alpha()
game_over_surface_rect = game_over_surface.get_rect(center = (216,384))
#chen am thanh
flap_sound = pygame.mixer.Sound("sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sfx_hit.wav")
score_sound = pygame.mixer.Sound("sfx_point.wav")
score_sound_coutdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_move = 0
                bird_move = -11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear() #xóa nhung cái ống
                bird_rect.center = (100,384)
                bird_move = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()
    screen.blit(background, (0, 0))
    if game_active:
        #chim
        bird_move += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_move
        screen.blit(rotated_bird,bird_rect)
        game_active = check_vacham(pipe_list)
        #Ông
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display("main game")
        score_sound_coutdown -= 1
        if score_sound_coutdown <= 0:
            score_sound.play()
            score_sound_coutdown = 100
    else:
        screen.blit(game_over_surface,game_over_surface_rect)
        high_score = update_score(score,high_score)
        score_display("game over")
    #sàn di chuyển liên tục
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)