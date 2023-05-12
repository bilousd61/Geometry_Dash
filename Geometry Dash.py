import pygame
import sys
import json


class Geometry_Dash():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1300, 600))
		self.screen_rect = self.screen.get_rect()
		pygame.display.set_caption('Geometry Dash')
		self.FPS = 60

		self.start_pos = 480
		self.rect_player = pygame.Rect(420, self.start_pos, 135, 135)
		self.player_y = float(self.rect_player.y)

		self.player_image = pygame.image.load('images/0001.bmp')
		self.spike_image = pygame.image.load('images/spike.bmp')
		self.spike_image.set_colorkey((255, 255, 255))
		self.wall_image = pygame.image.load('images/wall.bmp')


		self.speed_gravity = 1
		self.speed_jump = -18
		self.on_ground = False
		self.jump_active = False
		self.speed_player_y = 0
		self.speed = 9

		self.curent_map = "stereo_madnes.json"
		self.update_map()

		self.font = pygame.font.Font(None, 30)

		self.clock = pygame.time.Clock()
	def run_game(self):
		while True:
			self._update_screen()
			self._check_events()
			self._check_collide()
			self._gravity()
			self._jump_update()
			self.clock.tick(self.FPS)
	def _update_screen(self):
		self.screen.fill((145, 145, 230))


		self.hit_box = pygame.Rect(
			(self.rect_player.x, self.player_y, 94, 94))
		self.rect_player.y = self.player_y
		self.screen.blit(self.player_image, self.player_image.get_rect(center = self.hit_box.center))
		pygame.draw.rect(self.screen, (255, 0, 0), self.hit_box, 2)
		pygame.draw.rect(self.screen, (255, 9, 0), self.player_image.get_rect(center = self.hit_box.center), 2)

		self._draw_and_move_map()
		self._draw_progres_bar()
		self._draw_debug_items()

		pygame.display.flip()
	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit()
				elif event.key == pygame.K_r:
					self.dead()
				elif event.key == pygame.K_1:
					self.update_map("stereo_madnes.json")
				elif event.key == pygame.K_2:
					self.update_map("polargeist.json")
				elif event.key == pygame.K_SPACE:
					self.jump_active = True
					self._check_collide_orbs()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.jump_active = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.jump_active = True
				self._check_collide_orbs()
			elif event.type == pygame.MOUSEBUTTONUP:
				self.jump_active = False
	def _check_collide(self):
		for wall in self.walls:
			if self.hit_box.colliderect(wall):
				self._collide(wall)
				break
			else:
				self.on_ground = False
		for spike in self.spikes_hitbox:
			if self.hit_box.colliderect(spike):
				self.dead()
				break
		for portal in self.portals["speed4"]:
		    if self.hit_box.colliderect(portal):
		        self.speed = 18
	def _collide(self, wall):
		if self.speed_gravity > 0:
			if self.hit_box.bottom < wall.y:
				if self.speed_player_y > 0:
					self.speed_player_y = 0
				self.on_ground = True
			elif self.hit_box.bottom - 30 < wall.y:
				if self.speed_player_y > 0:
					self.speed_player_y = 0
				self.on_ground = True
				self.player_y = wall.y - self.hit_box.width + 1
			elif self.hit_box.y > wall.y:
				self.dead()
		elif self.speed_gravity < 0:
			if self.hit_box.y < wall.bottom:
				if self.speed_player_y < 0:
					self.speed_player_y = 0
				self.on_ground = True
			elif self.hit_box.y + 30 < wall.bottom:
				if self.speed_player_y < 0:
					self.speed_player_y = 0
				self.on_ground = True
				self.player_y = wall.y + self.hit_box.width
			elif self.hit_box.y > wall.y:
				self.dead()
	def _check_collide_orbs(self):
		for orb in self.orbs['normal']:
			if self.hit_box.colliderect(orb):
				self.jump()
				break
		for orb in self.orbs["gravity"]:
			if self.hit_box.colliderect(orb):
				self.speed_player_y = 0
				self.speed_gravity = -self.speed_gravity
				self.speed_jump = -self.speed_jump
				self.player_image = pygame.transform.rotate(self.player_image, 180)
				break
	def _jump_update(self):
		if self.jump_active:
			if self.on_ground == True:
				self.jump()
	def _gravity(self):
		if self.player_y < -1000 or self.player_y > 1000:
			self.dead()
		self.player_y += self.speed_player_y
		if self.on_ground == False:
			if self.speed_player_y < 20 or self.speed_player_y > 20:
				self.speed_player_y += self.speed_gravity
	def _draw_and_move_map(self):
		self.procced += self.speed
		for spike in self.spikes:
			self.screen.blit(self.spike_image, spike)
			spike.x -= self.speed
		for spike in self.spikes_hitbox:
			#pygame.draw.rect(self.screen, (255, 0 ,0), spike)
			spike.x -= self.speed
		for wall in self.walls:
			self.screen.blit(self.wall_image, wall)
			wall.x -= self.speed
		for portal in self.portals["speed4"]:
			pygame.draw.rect(self.screen, (255, 100, 0), portal)
			portal.x -= self.speed
		for orb in self.orbs["normal"]:
			pygame.draw.circle(self.screen, (255, 255, 0), orb.center, 35)
			orb.x -= self.speed
		for orb in self.orbs["gravity"]:
			pygame.draw.circle(self.screen, (0, 0, 255), orb.center, 35)
			orb.x -= self.speed
	def _draw_progres_bar(self):
		self.procced_procent = self.procced/self.level_length
		if self.procced_procent >= 1:
			self.dead()
		pygame.draw.rect(self.screen, (0, 255, 0), (400, 15, 600 * self.procced_procent, 20))
		pygame.draw.rect(self.screen, (0, 0, 0), (400, 12, 600, 26), 5)
		self.procced_procent *= 100
		text = self.font.render(f"{round(self.procced_procent, 2)}%", True, (0, 0, 0))
		text_rect = text.get_rect()
		self.screen.blit(text, (1010, 15, text_rect.width, text_rect.height))
	def _draw_debug_items(self):
		debug_items = {
			"on_ground": self.on_ground,
			"jump_active": self.jump_active,
			"hit_box.y": self.hit_box.y,
			"speed_gravity": self.speed_gravity
		}

		y = 10
		for key, item in debug_items.items():
			image = self.font.render(f"{key}: {item}", True, (0, 0, 0))
			image_rect = image.get_rect()
			image_rect.x = 10
			image_rect.y = y
			y += image_rect.height + 5
			self.screen.blit(image, image_rect)
	def update_map(self, map = 0):
		if map != 0:
			self.curent_map = map

		with open(f'maps/{self.curent_map}') as f:
			self.map = json.load(f)
		self.clear()

		width = 76
		height = 69

		x = 0
		y = 0
		for row in self.map:
			row = ''.join(row.split())
			for wall in row:
				if wall == 's':
					self.spikes.append(pygame.Rect((x, y, width, height)))
					self.spikes_hitbox.append(
						pygame.Rect((x + 22, y + 22, width - 44, height - 44)))
				elif wall == 'w':
					self.walls.append(pygame.Rect((x, y, width, height)))
				elif wall == '4':
					self.portals["speed4"].append(
						pygame.Rect((x, y, width, height*3)))
				elif wall == 'o':
					self.orbs["normal"].append(
						pygame.Rect((x - 20, y - 20, width + 40, height + 40)))
				elif wall == 'g':
					self.orbs["gravity"].append(
						pygame.Rect((x - 20, y - 20, width + 40, height + 40)))
				x += width
				if x > self.level_length:
					self.level_length = x
			x = 0
			y += height
	def jump(self):
		self.speed_player_y = self.speed_jump
		self.on_ground = False
	def dead(self):
		self.update_map()
		self.on_ground = False
	def clear(self):
		self.rect_player.y = self.start_pos
		self.player_y = float(self.start_pos)
		self.speed_player_y = 0
		self.speed_gravity = 1
		self.speed_jump = -18
		self.speed = 9
		self.procced = 0
		self.level_length = 0
		self.spikes = []
		self.spikes_hitbox = []
		self.walls = []
		self.portals = {
			"speed4": []
		}
		self.orbs = {
			"normal": [],
			"gravity": []
		}
if __name__ == "__main__":
	game = Geometry_Dash()
	game.run_game()