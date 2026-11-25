import pygame
import random
from game.ship import Ship
from game.meteor import Meteor

WIDTH,HEIGHT=700,520
FPS=60
BG=(8,5,20)
ORB_INTERVAL = 6 * FPS
SHIELD_DURATION = 8 * FPS
MULTIPLIER_INTERVAL = 10 * FPS


class Laser:
    radius = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= 14

    def hits(self, meteor):
        distance_squared = (self.x - meteor.x) ** 2 + (self.y - meteor.y) ** 2
        return distance_squared <= (self.radius + meteor.radius) ** 2

    def draw(self, screen):
        pygame.draw.line(screen, (125, 251, 255), (self.x, self.y - 8), (self.x, self.y + 8), 3)


class ShieldOrb:
    radius = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y += 2.5

    def collected_by(self, ship):
        dx = self.x - ship.rect.centerx
        dy = self.y - ship.rect.centery
        return dx * dx + dy * dy <= (self.radius + 16) ** 2

    def draw(self, screen):
        center = (round(self.x), round(self.y))
        pygame.draw.circle(screen, (70, 215, 250), center, self.radius, 2)
        pygame.draw.circle(screen, (160, 245, 255), center, 4)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",26,bold=True)
        self.big_font=pygame.font.SysFont("monospace",46,bold=True)
        self.stars=[(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(1,3)) for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship=Ship(WIDTH//2,HEIGHT-80)
        self.meteors=[]
        self.lasers = []
        self.orbs = []
        self.orb_timer = 0
        self.shield_frames = 0
        self.timer=0
        self.spawn_interval=60
        self.score=0
        self.survival_frames = 0
        self.streak_frames = 0
        self.game_over=False
        self.started=False

    @property
    def multiplier(self):
        return 1 + self.streak_frames // MULTIPLIER_INTERVAL

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset()
                    self.started = True
                elif not self.started:
                    self.started = True
                else:
                    self.lasers.append(Laser(self.ship.rect.centerx, self.ship.rect.top))
        return True

    def update(self):
        if self.game_over or not self.started: return
        keys=pygame.key.get_pressed()
        self.ship.move(keys,WIDTH,HEIGHT)
        self.update_shields()
        self.timer+=1
        if self.timer>=self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer=0
            self.spawn_interval=max(20,self.spawn_interval-0.3)
        for meteor in self.meteors:
            meteor.update()
        self.update_lasers()
        remaining_meteors = []
        took_hit = False
        for meteor in self.meteors:
            if meteor.collides(self.ship.rect):
                if self.shield_frames:
                    self.shield_frames = 0
                    took_hit = True
                    continue
                self.game_over = True
            if not meteor.off_screen(HEIGHT):
                remaining_meteors.append(meteor)
        self.meteors = remaining_meteors
        if not self.game_over:
            self.survival_frames += 1
            self.streak_frames = 0 if took_hit else self.streak_frames + 1
            self.score += self.multiplier

    def update_shields(self):
        self.shield_frames = max(0, self.shield_frames - 1)
        self.orb_timer += 1
        if self.orb_timer >= ORB_INTERVAL:
            self.orbs.append(ShieldOrb(random.randint(24, WIDTH - 24), -12))
            self.orb_timer = 0

        active_orbs = []
        for orb in self.orbs:
            orb.update()
            if orb.collected_by(self.ship):
                self.shield_frames = SHIELD_DURATION
            elif orb.y <= HEIGHT + orb.radius:
                active_orbs.append(orb)
        self.orbs = active_orbs

    def update_lasers(self):
        active_lasers = []
        fragments = []
        for laser in self.lasers:
            laser.update()
            if laser.y < -laser.radius:
                continue
            for meteor in self.meteors:
                if laser.hits(meteor):
                    self.meteors.remove(meteor)
                    fragments.extend(meteor.fragments())
                    break
            else:
                active_lasers.append(laser)
        self.lasers = active_lasers
        self.meteors.extend(fragments)

    def draw(self):
        self.screen.fill(BG)
        for sx,sy,sr in self.stars:
            pygame.draw.circle(self.screen,(200,200,220),(sx,sy),sr)
        for m in self.meteors: m.draw(self.screen)
        for laser in self.lasers:
            laser.draw(self.screen)
        for orb in self.orbs:
            orb.draw(self.screen)
        self.ship.draw(self.screen)
        if self.shield_frames:
            pygame.draw.circle(self.screen, (80, 220, 250), self.ship.rect.center, 24, 2)
        hud = f"Time {self.survival_frames // FPS}s   Score {self.score}   x{self.multiplier}"
        self.screen.blit(self.font.render(hud, True, (200, 200, 240)), (10, 10))
        if not self.started:
            msg=self.font.render("Press SPACE to launch",True,(180,180,240))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2))
        if self.game_over:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            self.screen.blit(ov,(0,0))
            m=self.big_font.render("DESTROYED!",True,(220,80,60))
            outcome = f"Survived {self.survival_frames // FPS}s | Score {self.score}"
            s=self.font.render(outcome,True,(200,200,200))
            restart = self.font.render("SPACE to restart", True, (200, 200, 200))
            self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
            self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))
            self.screen.blit(restart, (WIDTH//2-restart.get_width()//2, HEIGHT//2+56))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
