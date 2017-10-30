import pygame
import random



class Cell(pygame.sprite.Sprite):
    def __init__(self,y,x):
        self.ypos = y
        self.xpos = x
        self.size = 6
        self.sizes = 6
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill([255,255,255])
        self.rect = self.image.get_rect()
        self.rect.y = self.sizes * self.ypos
        self.rect.x = self.sizes * self.xpos

    def zoomIn(self):
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,(w * 2, h * 2))
        self.rect.width = w * 2
        self.rect.height = h * 2
        self.sizes = self.rect.height
        self.rect.y *= 2
        self.rect.x *= 2

    def zoomOut(self):
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,(int(w / 2), int(h / 2)))
        self.rect.width = w / 2
        self.rect.height = h / 2
        self.sizes = self.rect.height
        self.rect.y /= 2
        self.rect.x /= 2

class Display():
    def __init__(self):
        self.gridX = 200
        self.gridY = 120
        self.pauseState = False
        self.current = 0
        self.maxs = 6
        self.zoomScale = 1
        self.simulator = Simulator(self.gridY,self.gridX)
        self.display = DisplayGrid(self.gridY,self.gridX)
        self.cellGroup = self.display.getSpriteGrid()
        self.cellGrid = self.display.getGrid()
        self.flags=[0,0,0,0]

    def update(self):
        if self.pauseState == False:
            if self.current >= self.maxs:
                self.simulator.step()
                self.current = 0
            else:
                self.current += 1
        self.panUpdate()
        self.updateDisplay()

    def panUpdate(self):
        if self.flags[0] == 1:
            self.pan("down")
        if self.flags[1] == 1:
            self.pan("up")
        if self.flags[2] == 1:
            self.pan("right")
        if self.flags[3] == 1:
            self.pan("left")

    def render(self, screen):
        self.cellGroup.draw(screen)

    def handle_Events(self, events):
        for event_type in events:
            if event_type.type == pygame.KEYDOWN:
                if event_type.key == pygame.K_SPACE:
                    if self.pauseState == False:
                        self.pauseState = True
                    else:
                        self.pauseState = False
                if event_type.key == pygame.K_EQUALS:
                    self.maxs += 1
                if event_type.key == pygame.K_MINUS:
                    self.maxs -= 1
                if event_type.key == pygame.K_q:
                    self.zoom(False)
                if event_type.key == pygame.K_e:
                    self.zoom(True)
                if event_type.key == pygame.K_UP:
                    self.flags[0] = 1
                if event_type.key == pygame.K_DOWN:
                    self.flags[1] = 1
                if event_type.key == pygame.K_LEFT:
                    self.flags[2] = 1
                if event_type.key == pygame.K_RIGHT:
                    self.flags[3] = 1
            elif event_type.type == pygame.KEYUP:
                if event_type.key == pygame.K_UP:
                    self.flags[0] = 0
                if event_type.key == pygame.K_DOWN:
                    self.flags[1] = 0
                if event_type.key == pygame.K_LEFT:
                    self.flags[2] = 0
                if event_type.key == pygame.K_RIGHT:
                    self.flags[3] = 0

            if event_type.type == pygame.MOUSEBUTTONDOWN:
                self.checkClicked(event_type.pos)

    def pan(self, dir):
        for cells in self.cellGroup:
            if dir == "up":
                cells.rect.y -= 24
            if dir == "down":
                cells.rect.y += 24
            if dir == "left":
                cells.rect.x -= 24
            if dir == "right":
                cells.rect.x += 24

    def zoom(self, type):
        for cells in self.cellGroup:
            if type == True:
                cells.zoomIn()
            else:
                cells.zoomOut()


    def checkClicked(self, pos):
        for cells in self.cellGroup:
            if cells.rect.collidepoint(pos):
                if self.simulator.getGrid()[cells.ypos][cells.xpos] == 0:
                    self.simulator.getGrid()[cells.ypos][cells.xpos] = 1
                else:
                    self.simulator.getGrid()[cells.ypos][cells.xpos] = 0

    def updateDisplay(self):
        for y in range(self.gridY):
            for x in range(self.gridX):
                if self.simulator.getGrid()[y][x] == 0:
                    self.cellGrid[y][x].image.fill([255,255,255])
                else:
                    self.cellGrid[y][x].image.fill([255,0,0])

class DisplayGrid():
    def __init__(self,y ,x):
        self.gridy = y
        self.gridx = x
        self.Spritegrid = pygame.sprite.Group()
        self.grid = []
        self.createGrid()

    def createGrid(self):
        print("Creating Sprite Grid")
        for y in range(self.gridy):
            self.grid.append([])
        print("Added Initial Y Index in SpriteGrid")
        print("Populating Spritegrid with Sprites")
        for y in range(self.gridy):
            for x in range(self.gridx):
                newCell = Cell(y,x)
                self.grid[y].append(newCell)
                self.Spritegrid.add(newCell)
        print("Done Creating Sprite Grid")

    def getSpriteGrid(self):
        return self.Spritegrid

    def getGrid(self):
        return self.grid

class Simulator():
    def __init__(self, y,x):
        worldGrid= WorldGrid(y,x)
        self.grid = worldGrid.getGrid()
        self.bufferGrid = []
        self.createBuffer()
        self.generation = 0

    def createBuffer(self):
        for y in range(len(self.grid)):
            self.bufferGrid.append([])
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.bufferGrid[y].append(self.grid[y][x])

    def updateBuffer(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.bufferGrid[y][x] = self.grid[y][x]
    def updateGrid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x] = self.bufferGrid[y][x]

    def step(self):
        print("Generation: ", self.generation)
        self.generation+=1
        self.updateBuffer()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                live_n = self.getNeighbors(y,x)

                if self.grid[y][x] == 1:
                    if live_n < 2:
                        self.bufferGrid[y][x] = 0
                    elif live_n > 3:
                        self.bufferGrid[y][x] = 0
                    else:
                        self.bufferGrid[y][x] = 1
                else:
                    if live_n == 3:
                        self.bufferGrid[y][x] = 1

        self.updateGrid()

    def getGrid(self):
        return self.grid

    def getNeighbors(self, y, x):
        live_neighbors = 0

        if y == 0 and x == 0:
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x] != 0:
                live_neighbors += 1

        elif y == 0 and x == len(self.grid[0]) - 1:
            if self.grid[y+1][x] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x-1] != 0:
                live_neighbors += 1

        elif y == len(self.grid)-1 and x == len(self.grid[0])-1:
            if self.grid[y-1][x] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
            if self.grid[y-1][x-1] != 0:
                live_neighbors += 1

        elif y == len(self.grid)-1 and x == 0:
            if self.grid[y-1][x] != 0:
                live_neighbors += 1
            if self.grid[y-1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
        elif y == 0 and x > 0 and x < len(self.grid[0])-1:
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x] != 0:
                live_neighbors += 1
            if self.grid[y+1][x-1] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
        elif x == 0 and y > 0 and y < len(self.grid) -1:
            if self.grid[y-1][x] != 0:
                live_neighbors += 1
            if self.grid[y-1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x] != 0:
                live_neighbors += 1

        elif y == len(self.grid)-1 and x > 0 and x < len(self.grid[0]) -1:
            if self.grid[y-1][x] != 0:
                live_neighbors += 1
            if self.grid[y-1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
            if self.grid[y-1][x-1] != 0:
                live_neighbors += 1
        elif x == len(self.grid[0])-1 and y > 0 and y < len(self.grid)-1:
            if self.grid[y+1][x] != 0:
                live_neighbors += 1
            if self.grid[y+1][x-1] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
            if self.grid[y-1][x-1] != 0:
                live_neighbors += 1
            if self.grid[y-1][x] != 0:
                live_neighbors += 1

        else:
            if self.grid[y-1][x] != 0:
                live_neighbors += 1
            if self.grid[y-1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x+1] != 0:
                live_neighbors += 1
            if self.grid[y+1][x] != 0:
                live_neighbors += 1
            if self.grid[y+1][x-1] != 0:
                live_neighbors += 1
            if self.grid[y][x-1] != 0:
                live_neighbors += 1
            if self.grid[y-1][x-1] != 0:
                live_neighbors += 1

        return live_neighbors


class WorldGrid():
    def __init__(self, size_y, size_x):
        self.gridx = size_x
        self.gridy = size_y
        self.createGrid()
        self.seedGrid()

    def createGrid(self):
        print("Creating Grid")
        self.grid = []
        for y in range(self.gridy):
            self.grid.append([])
        for y in range(self.gridy):
            for x in range(self.gridx):
                self.grid[y].append(0)

    def seedGrid(self):
        print("Seeding Grid")
        for i in range(960):
            xrand = random.randint(0,self.gridx-1)
            yrand = random.randint(0,self.gridy-1)
            if self.grid[yrand][xrand] != 1:
                self.grid[yrand][xrand] = 1

    def getGrid(self):
        return self.grid
