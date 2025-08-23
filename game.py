import pygame
import random
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
ball_radius = 20
white = (255, 255, 255)

class Ball:
    def __init__(self, color):
        self.x = random.randint(ball_radius, width - ball_radius)
        self.y = random.randint(ball_radius, height - ball_radius)
        self.velocity_x = random.choice([-4, -3, 3, 4])
        self.velocity_y = random.choice([-4, -3, 3, 4])
        self.color = color
        self.radius = ball_radius
    
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.x <= self.radius or self.x >= width - self.radius:
            self.velocity_x *= -1
        if self.y <= self.radius or self.y >= height - self.radius:
            self.velocity_y *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < self.radius + other.radius

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)
        self.color = (255, random.randint(100, 150), 0)  # Fire-like colors
        self.velocity_x = random.uniform(-5, 5)
        self.velocity_y = random.uniform(-5, 5)
        self.lifetime = 30  # frames
    
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1
    
    def draw(self):
        if self.lifetime > 0:
            alpha = max(0, int(255 * (self.lifetime / 30)))  # fade out
            surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(surface, (int(self.x - self.radius), int(self.y - self.radius)))

balls = [Ball((255, 0, 0)), Ball((0, 255, 0)), Ball((0, 0, 255))]
particles = []
running = True

while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move and draw balls
    for ball in balls:
        ball.move()
        ball.draw()
    
    # Check for collisions and create explosions
    to_remove = []
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].check_collision(balls[j]):
                # Mark balls for removal
                to_remove.extend([balls[i], balls[j]])
                # Create explosion particles at collision point
                cx = (balls[i].x + balls[j].x) / 2
                cy = (balls[i].y + balls[j].y) / 2
                for _ in range(30):
                    particles.append(Particle(cx, cy))
    
    # Remove collided balls
    balls = [b for b in balls if b not in to_remove]

    # Update and draw particles
    particles = [p for p in particles if p.lifetime > 0]
    for particle in particles:
        particle.move()
        particle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
