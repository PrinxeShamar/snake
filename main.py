import pygame
import random

def food_position(game):
    while True:
        x = random.randrange(game.rows)
        y = random.randrange(game.cols)
        if len(list(filter(lambda z: z == (x,y), game.snake.body))) > 0:
            continue
        break
        
    return (x,y)

class Cube():
    def __init__(self, pos, dirn, color):
        self.pos = pos
        self.dirn = dirn
        self.color = color

    def draw(self, game):
        pygame.draw.rect(game.window, self.color, (self.pos[0]*game.box_size+1,self.pos[1]*game.box_size+1, game.box_size-1, game.box_size-1))

class Snake():
    def __init__(self):
        self.body = []
        self.turns = {}

        self.body.append(Cube((10,10), (1,0), (255,0,0)))
        self.body.append(Cube((9,10), (1,0), (255,0,0)))
        self.body.append(Cube((8,10), (1,0), (255,0,0)))
        self.body.append(Cube((7,10), (1,0), (255,0,0)))

    def draw(self, game):
        for cube in self.body:
            cube.draw(game)

    def eat(self, game):
        if self.body[0].pos == game.food.pos:
            self.grow()
            game.food = Cube(food_position(game), (0,0), (0,255,0))

    def grow(self):
        print(len(self.body))
        dirn = self.body[-1].dirn
        pos = self.body[-1].pos

        if dirn == (-1,0):
            pos = (pos[0] + 1,pos[1])
        elif dirn == (1,0):
            pos = (pos[0] - 1,pos[1])
        elif dirn == (0,1):
            pos = (pos[0],pos[1] - 1)
        elif dirn == (0,-1):
            pos = (pos[0],pos[1] + 1)

        self.body.append(Cube(pos, dirn, (255,0,0)))
    
    def check_collision(self, game):
        if self.body[0].pos[0] < 0 or self.body[0].pos[0] > game.rows or self.body[0].pos[1] < 0 or self.body[0].pos[1] > game.cols:
            self.__init__()
            return 
        
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z:z.pos,self.body[x+1:])):
                self.__init__()
                break

    def move(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.body[0].dirn[0] == 0:
                    self.body[0].dirn = (-1, 0)
                    self.turns[self.body[0].pos] = self.body[0].dirn
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.body[0].dirn[0] == 0:
                    self.body[0].dirn = (1, 0)
                    self.turns[self.body[0].pos] = self.body[0].dirn
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                if self.body[0].dirn[1] == 0:
                    self.body[0].dirn = (0, -1)
                    self.turns[self.body[0].pos] = self.body[0].dirn
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if self.body[0].dirn[1] == 0:
                    self.body[0].dirn = (0, 1)
                    self.turns[self.body[0].pos] = self.body[0].dirn

        for i, cube in enumerate(self.body):
            if cube.pos in self.turns:
                cube.dirn = self.turns[cube.pos]
                if self.body[-1] == cube:
                    print(cube.pos, self.turns)
                    self.turns.pop(cube.pos)


            cube.pos = (cube.pos[0] + cube.dirn[0], cube.pos[1] + cube.dirn[1])



class Game():
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.box_size = 25
        self.rows = self.width // self.box_size
        self.cols = self.height // self.box_size
        self.window = pygame.display.set_mode((self.width, self.height)) 

        self.snake = Snake()
        self.food = Cube(food_position(self), (0,0), (0,255,0))
    
        self.loop = True
        self.main_loop()

    def draw_grid(self):
        for i in range(self.rows):
            x = (i + 1) * self.box_size
            pygame.draw.line(self.window, (255,255,255), (x,0),(x,self.height))
        
        for i in range(self.cols):
            y = (i + 1) * self.box_size
            pygame.draw.line(self.window, (255,255,255), (0,y),(self.width,y))

    def draw_window(self):
        self.window.fill((0,0,0))
        self.draw_grid()
        self.snake.draw(self)
        self.food.draw(self)

        pygame.display.update()

    def main_loop(self):
        clock = pygame.time.Clock()

        while self.loop:
            pygame.time.delay(50)
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 

            self.snake.move()
            self.snake.eat(self)
            self.snake.check_collision(self)
            self.draw_window()

if __name__ == '__main__':
    game = Game()
