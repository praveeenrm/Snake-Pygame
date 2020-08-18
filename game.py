# Sounds from www.bensound.com
import pygame
import random
from os import path

# SETTINGS
TITLE = "Snake"
WIDTH = 600
HEIGHT = 600
FPS = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
SNAKE_GREEN = (34, 139, 34)
APPLE_COLOR = (255, 8, 0)

SNAKE_SIZE = 20
APPLE_SIZE = 20

TILE_SIZE = 20

# Get assets/Sound/Image Folder
game_folder = path.dirname(__file__)
assets_folder = path.join(game_folder, 'assets')
sounds_folder = path.join(assets_folder, 'sounds')

font_file = path.join(assets_folder, '04B_19.ttf')
eat_music = path.join(sounds_folder, 'eat.wav')
hit_music = path.join(sounds_folder, 'hit.wav')
bg_music = path.join(sounds_folder, 'happy.ogg')
snake_icon = path.join(assets_folder, 'snake_icon.png')

# GAME
class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		pygame.display.set_icon(pygame.image.load(snake_icon))
		self.clock = pygame.time.Clock()
		self.eat_sound =  pygame.mixer.Sound(eat_music)
		self.hit_sound = pygame.mixer.Sound(hit_music)
		# self.bg_sound = pygame.mixer.Sound(bg_music)
		self.running = True
		self.font_name = font_file

	def new(self):
		self.playing = True
		self.lead_x = 300
		self.lead_y = 300
		self.lead_x_pos = 0
		self.lead_y_pos = 0
		self.rand_apple_x = 100
		self.rand_apple_y = 100
		self.snake_list = []
		self.snake_length = 1
		self.score = 0
		self.speed = 20
		self.run()

	def run(self):
		# self.bg_sound.play(-1)
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.draw()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.lead_x_pos = -self.speed
					self.lead_y_pos = 0
				if event.key == pygame.K_RIGHT:
					self.lead_x_pos = self.speed
					self.lead_y_pos = 0
				if event.key == pygame.K_UP:
					self.lead_y_pos = -self.speed
					self.lead_x_pos = 0
				if event.key == pygame.K_DOWN:
					self.lead_y_pos = self.speed
					self.lead_x_pos = 0

		self.lead_x += self.lead_x_pos
		self.lead_y += self.lead_y_pos

		self.snake_head = []
		self.snake_head.append(self.lead_x)
		self.snake_head.append(self.lead_y)
		self.snake_list.append(self.snake_head)

		# Check if snake hits the boundaries
		if self.lead_x + 20 > WIDTH or self.lead_x < 0 or self.lead_y + 20 > HEIGHT or self.lead_y < 0:
			self.hit_sound.play()
			self.playing = False

		# Add snake length only when it eats apple else remove all the snake_list
		if len(self.snake_list) > self.snake_length:
			del self.snake_list[0]

		# Check if snake hits snake
		for i in self.snake_list[1:]:
			if self.snake_list[0] == i:
				self.hit_sound.play()
				self.playing = False

	def draw(self):
		self.screen.fill(DARKGREY)
		self.draw_apple(self.rand_apple_x, self.rand_apple_y)
		self.draw_snake(self.snake_list)
		self.random_apple()
		self.draw_grid()
		pygame.display.flip()

	def draw_grid(self):
		for x in range(0, WIDTH, TILE_SIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILE_SIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw_apple(self, x, y):
		pygame.draw.rect(self.screen, APPLE_COLOR, [x, y, SNAKE_SIZE, SNAKE_SIZE])
		self.apple = pygame.draw.rect(self.screen, RED, [x, y, SNAKE_SIZE, SNAKE_SIZE])

	def draw_snake(self, li):
		for xandy in li:
			pygame.draw.rect(self.screen, SNAKE_GREEN, [xandy[0], xandy[1], SNAKE_SIZE, SNAKE_SIZE])
			self.snake = pygame.draw.rect(self.screen, GREEN, [xandy[0], xandy[1], SNAKE_SIZE, SNAKE_SIZE])

	def random_apple(self):
		# If snake eats apple
		if self.snake == self.apple:
			self.eat_sound.play()
			self.rand_apple_x = random.randrange(0, WIDTH-20, 20)
			self.rand_apple_y = random.randrange(0, HEIGHT-20, 20)
			self.snake_length += 1
			self.score += 1

	def show_start_page(self):
		self.screen.fill(LIGHTGREY)
		self.draw_text("Snake", 40, WHITE, WIDTH/2, HEIGHT/4)
		self.draw_text("Arrows to move", 25, WHITE, WIDTH/2, HEIGHT/3)
		self.draw_text('Press "SPACE" to play', 25, WHITE, WIDTH/2, HEIGHT/2)
		pygame.display.flip()
		self.wait_for_key()

	def wait_for_key(self):
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.waiting = False
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.waiting = False
					if event.key == pygame.K_p:
						# self.bg_sound.stop()
						self.waiting = False
						self.running = True

	def show_game_over(self):
		if not self.running:
			return
		self.screen.fill(LIGHTGREY)
		self.draw_text("GAMEOVER", 40, WHITE, WIDTH/2, HEIGHT/4)
		self.draw_text(f"Your Score: {self.score}", 30, WHITE, WIDTH/2, HEIGHT/3)
		self.draw_text('Press "p" key to play again', 25, WHITE, WIDTH/2, HEIGHT/2)
		pygame.display.flip()
		self.wait_for_key()

	def draw_text(self, text, size, color, x, y):
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

g = Game()
bg_sound = pygame.mixer.Sound(bg_music)
bg_sound.play(-1)
g.show_start_page()
while g.running:
	g.new()
	g.show_game_over()
bg_sound.stop()
pygame.quit()
