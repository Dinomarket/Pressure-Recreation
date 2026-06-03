BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (255, 0, 0)
LIME    = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER  = (192, 192, 192)
GRAY    = (128, 128, 128)
MAROON  = (128, 0, 0)
OLIVE   = (128, 128, 0)
GREEN   = (0, 128, 0)
PURPLE  = (128, 0, 128)
TEAL    = (0, 128, 128)
NAVY    = (0, 0, 128)
ORANGE = (255, 165, 0)

import pygame

class HeartbeatOverlay:
    def __init__(self):
        self.active = False

        self.start_time = 0
        self.last_beat_time = 0

        self.duration = 0
        self.beat_interval = 800  # starts slower, speeds up

        self.flash_visible = False
        self.flash_duration = 80  # quick pulse

        self.screen_shake_intensity = 0

    def start(self, duration=5000):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.last_beat_time = self.start_time
        self.duration = duration
        self.beat_interval = 800

    def update(self):
        if not self.active:
            return

        current = pygame.time.get_ticks()

        # end effect
        if current - self.start_time >= self.duration:
            self.active = False
            self.flash_visible = False
            return

        # speed up heartbeat over time (panic increases)
        progress = (current - self.start_time) / self.duration
        self.beat_interval = max(200, 800 - int(progress * 600))

        # trigger beat
        if current - self.last_beat_time >= self.beat_interval:
            self.last_beat_time = current
            self.flash_visible = True

        # turn off flash quickly (heartbeat "thump")
        if self.flash_visible and current - self.last_beat_time > self.flash_duration:
            self.flash_visible = False

    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # --- heartbeat flash (red pulse) ---
        if self.flash_visible:
            overlay.fill((255, 0, 0, 60))  # red tint
        else:
            overlay.fill((0, 0, 0, 0))

        screen.blit(overlay, (0, 0))

        # --- optional: vignette effect for panic ---
        vignette = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        vignette.fill((0, 0, 0, 0))
        pygame.draw.rect(vignette, (0, 0, 0, 80), vignette.get_rect(), border_radius=50)
        screen.blit(vignette, (0, 0))