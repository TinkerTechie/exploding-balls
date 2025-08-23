import pygame
import random
import math
## initializing pygame
pygame.init()

## ball size and display

width = 800
height = 600
ball_radius = 20

## colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

## create display
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

## define the ball using oops

class Ball:
    def __init__(self,color) :
        self.x = random.randint(ball_radius,width-ball_radius)
        self.y = random.randint(ball_radius,height-ball_radius)
        self.velocity_x = random.randint(1,3) * 2
        self.velocity_y = random.randint(1,3) * -2
        self.color = color
    ## setting up for velocity
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        ## bouncing off the walls
        if self.x <= ball_radius or self.x >= width - ball_radius:
            self.velocity_x *= -1
            self.x = max(ball_radius,min(width-ball_radius,self.x))
        if self.y <= ball_radius or self.y >= width - ball_radius:
            self.velocity_y *= -1
            self.y = max(ball_radius,min(width-ball_radius,self.y))
    ## drawing the ball
    def draw(self):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),ball_radius)
    
    ## handing the collision of ball to ball
    def check_collision(self,other_ball):
        dx = self.x - other_ball.x
        dy = self.y - other_ball.y
        distance = math.sqrt(dx**2+dy**2)
        if distance < 2 * ball_radius:
            normal_vector = pygame.math.Vector2(dx,dy).normalize()
            relative_velocity = pygame.math.Vector2(self.velocity_x,self.velocity_y) - pygame.math.Vector2(other_ball.velocity_x,other_ball.velocity_y)
            velocity_along_normal = relative_velocity.dot(normal_vector)
            if velocity_along_normal < 0:
                return
            impulse = 2*velocity_along_normal / (2*ball_radius)
            self.velocity_x -= impulse * normal_vector.x
            self.velocity_y -= impulse * normal_vector.y
            other_ball.velocity_x += impulse * normal_vector.x
            other_ball.velocity_y += impulse * normal_vector.y
            # Reposition to avoid overlap
            overlap = 2 * ball_radius - distance
            self.x += normal_vector.x * overlap / 2
            self.y += normal_vector.y * overlap / 2
            other_ball.x -= normal_vector.x * overlap / 2
            other_ball.y -= normal_vector.y * overlap / 2
    
balls = [Ball(red), Ball(green), Ball(blue)]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and collision
    for ball in balls:
        ball.move()
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].check_collision(balls[j])

    screen.fill(white)
    for ball in balls:
        ball.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
        