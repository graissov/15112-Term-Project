#Gani Raissov term project
#graissov

#importing libraries
from copy import copy
import pygame
from pygame.locals import *
from math import *
import random

#Initializing main variables
color= (50,70,100)
radiusOfFood = 10
gameScreen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)#(screenWidth,screenHeight))
screenHeight = pygame.display.get_surface().get_height()
screenWidth =  pygame.display.get_surface().get_width()
foodSize = 150
numberOfPythons = 20
pygame.init()
vector = pygame.math.Vector2()
playerSkin = 'red.png'
quiGame = False
 

#class to that defines sections of the snake
class section:
    def __init__(self, parent_screen,horizontalPosition,verticalPosition,width,height,skin):
        #setting horizontal and vertical positions of a section
        self.horizontalPosition = horizontalPosition
        self.verticalPosition = verticalPosition
        #width and height of the section
        self.width = width
        self.height = height
        self.rectangle = Rect(horizontalPosition,verticalPosition,width,height)
        #defining a screen
        self.parent_screen = parent_screen
        #specifying the file that contains a section image
        self.section = pygame.image.load(skin)
        #creating image of a scetion on a screen
        self.image = pygame.transform.scale(self.section,(self.rectangle.width,self.rectangle.height))
          
    #function to show the section on the screen at the specific (x,y) location
    def show(self,x,y):
        self.image = pygame.transform.scale(self.section,(self.rectangle.width,self.rectangle.height))
        self.parent_screen.blit(self.image,(x,y))   
        
#class to that defines the head of the python
class Python:
    def __init__(self, parent_screen,horizontalPosition,verticalPosition,width,height,file):
        #best selection list will be used to get the most effective path to food
        self.bestSelection = [[],[]]
        #file that contains an image of a skin
        self.skin = file
        #Identifying if a snake grew or not
        self.startGrowth = False
        self.horizontalPosition = horizontalPosition
        self.verticalPosition = verticalPosition
        self.snakeGrew = True
        self.width = width
        self.height = height
        self.path = 0
        #rectangle that contains the python's head
        self.rectangle = pygame.Rect(horizontalPosition,verticalPosition,width,height)
        self.parent_screen = gameScreen
        #load the image of the python
        self.section = pygame.image.load(file)
        self.length = 0
        self.newsections = 3
        self.growth = 0
        self.image = pygame.transform.scale(self.section,(width,height))
        self.currentSections = []
        self.sections = []
        self.movement = []

    #function calcultes the grwoth of the python as it etas food
    def grow(self,growth):
        self.length+=growth
        self.growth+=growth
        if self.growth>=25:
            self.newsections = self.growth//25
            self.growth = self.growth - self.newsections*25
            self.snakeGrew = True

    #function shows the image of python on the screen
    def show(self,x,y):
        self.image = pygame.transform.scale(self.section,(self.rectangle.width,self.rectangle.height))
        gameScreen.blit(self.image,(x,y))      
        
#class defines the food objects
class food:
    def __init__(self, horizontalPosition,verticalPosition,width):
        file = "circle (" +str(random.randint(1,13))+").png"
        self.width = width
        self.rectangle = pygame.Rect(horizontalPosition,verticalPosition,width,width)
        self.food = pygame.image.load(file)
        self.foodImage = pygame.transform.scale(self.food,(width,width))

#putting the food image on the screen
    def show(self,screen,x,y):
        screen.blit( pygame.transform.scale(self.food,(self.width,self.width)),(x,y))        

#class that is responsible for most of the in-game processes
class Game:
    def __init__(self):
        self.MapRect = Rect(-2*screenWidth, -2*screenHeight, 4*screenWidth, 4*screenHeight)
        self.horizontalMovement = 0
        self.verticalMovement = 0
        self.pause = False
        self.radius = random.randint(10,50)
        self.startWidth = 30
        self.exit = False
        self.screen = gameScreen
        pygame.display.set_caption('Python in Python')
        self.screen.fill((5,70,100))  
        self.foodItems = []
        self.clock = pygame.time.Clock()
        self.movementStep = 5
        self.movementStepBots = 4
        self.movement = []
        self.separation = 20
        self.sections = []
        self.currentSections = []
        self.startGrowth = False
        self.counter = 0
        self.vector = [0,0]
        self.width = 30
        self.height = self.width
        self.startposX = 0
        self.startposY = 0
        self.mainpython = Python(self.screen,self.startposX,self.startposY,self.startWidth,self.startWidth,playerSkin)
        self.inflationFactor = 0
        self.allPythons = []
        self.backToMenuButton = button("red.png",self.screen,500,20,50,50,"Pause","black")

    #function to create food objects
    def createFood(self,numberOfFood=foodSize):    
        for i in range(numberOfFood):
            radiusOfFood = random.randint(5,10)
            positionOfFood = [random.randint(self.MapRect.left+200,self.MapRect.right-200),
            random.randint(self.MapRect.top+200,self.MapRect.bottom-200)]
            f = food(positionOfFood[0],positionOfFood[1],radiusOfFood)
            self.foodItems.append(f) 

    #function to create pythons
    def createPythons(self,number = numberOfPythons):        
        for python in range(number):
            horizaontalPositionOfPython = random.randint(self.MapRect.left+100,self.MapRect.right-100)
            verticalPositionOfPython = random.randint(self.MapRect.top,self.MapRect.y+self.MapRect.h)
            file = "circle (" +str(random.randint(1,13))+").png"
            f = Python(gameScreen,horizaontalPositionOfPython,verticalPositionOfPython,self.width,self.width,file)
            f.newsections = random.randint(0,10)
            f.snakeGrew = True
            self.allPythons.append(f) 

    #function to show all objects        
    def showAllObjects(self):  
        #vector to calculate the offset from camera
        self.vector[0] = self.mainpython.rectangle.center[0] - screenWidth//2
        self.vector[1] = self.mainpython.rectangle.center[1] - screenHeight//2 
        self.screen.fill(color)
        #putting the image of main player python in the center
        self.horizontalPositionShift = self.mainpython.rectangle.x - self.vector[0]
        self.verticalPositionShift = self.mainpython.rectangle.y - self.vector[1]
        self.MapRectBorder = Rect(-2*screenWidth-self.vector[0], -2*screenHeight-self.vector[1], 4*screenWidth, 4*screenHeight)
        self.text = pygame.font.SysFont("impact",30).render('Score: '+str(self.mainpython.length),True,'black')
        pygame.draw.rect(gameScreen, 'red', self.MapRectBorder, width=5)


        for f in self.foodItems:
            #adjusting the position of food relative to player
            horizontalCorrection = f.rectangle.x - self.vector[0]
            VerticalCorrection = f.rectangle.y - self.vector[1]
            f.show(self.screen,horizontalCorrection,VerticalCorrection)
        for pythons in self.allPythons:
            #adjusting position of pythons relative to pythons
            horizontalCorrection = pythons.rectangle.x - self.vector[0]
            VerticalCorrection = pythons.rectangle.y - self.vector[1]
            pythons.show(horizontalCorrection,VerticalCorrection)
        gameScreen.blit(self.text,(0,0))  
        self.showNewSections()

        self.mainpython.show(self.horizontalPositionShift,self.verticalPositionShift)
        
#chowing sections of the pythons
    def showNewSections(self):
        for onepython in self.allPythons:
            for i in range(len(onepython.currentSections)):
                #loop through each section of each python
                #show the image with respect to correction relative to player
                horizontalCorrection = onepython.currentSections[i].rectangle.x - self.vector[0]
                verticalCorrection = onepython.currentSections[i].rectangle.y - self.vector[1]
                onepython.currentSections[i].show(horizontalCorrection,verticalCorrection)
        #do the same for the main player
        for i in range(len(self.mainpython.currentSections)):
            horizontalCorrection = self.mainpython.currentSections[i].rectangle.x - self.vector[0]
            verticalCorrection = self.mainpython.currentSections[i].rectangle.y - self.vector[1]
            self.mainpython.currentSections[i].show(horizontalCorrection,verticalCorrection)   

#function to add new sections
    def addSections(self):
        # Checking for Snake growth
        for onepython in self.allPythons:
            if onepython.snakeGrew == True:
                onepython.snakeGrew = False
                #get the number of sections to add
                for i in range(onepython.newsections):
                    #spawn a new section at the position of the last section
                    if len(onepython.currentSections) != 0:
                        horizontalPosition = onepython.currentSections[0].rectangle.x
                        verticalPosition = onepython.currentSections[0].rectangle.y
                        #create a new section and add it to the list of exctions
                        skin = onepython.skin
                        newSection = section(self.screen,horizontalPosition,verticalPosition,self.width,self.width,skin)
                        onepython.sections.append(newSection)
                    #if list of sections is empty, spawn the section at the position of the head of the snake
                    else:
                        horizontalPosition = onepython.rectangle.x
                        verticalPosition = onepython.rectangle.y
                        newSection = section(self.screen,horizontalPosition,verticalPosition,self.width,self.height,onepython.skin)
                        #create a new section and add it to the list of exctions
                        onepython.sections.append(newSection)
                        onepython.currentSections.append(newSection)
                #loop through new sections and append them to current sections(all sections to display)
                for s in onepython.sections:
                    onepython.currentSections.append(s)
                onepython.sections = []
                #increase width of the python

                onepython.rectangle.w += 0.1
                onepython.rectangle.h += 0.1
                for i in range(len(onepython.currentSections)):
                    onepython.currentSections[i].rectangle.w = onepython.rectangle.w
                    onepython.currentSections[i].rectangle.h = onepython.rectangle.h

        # Doing the same for mainpython 
        if self.mainpython.snakeGrew == True:
            self.mainpython.snakeGrew = False
            for i in range(self.mainpython.newsections):
                if len(self.mainpython.currentSections) != 0:
                    horizontalPosition = self.mainpython.currentSections[0].rectangle.x
                    verticalPosition = self.mainpython.currentSections[0].rectangle.y
                    newSection = section(self.screen,horizontalPosition,verticalPosition,self.width,self.width,playerSkin)
                    self.mainpython.sections.append(newSection)
                else:
                    horizontalPosition = self.mainpython.rectangle.x
                    verticalPosition = self.mainpython.rectangle.y
                    newSection = section(self.screen,horizontalPosition,verticalPosition,self.width,self.height,playerSkin)
                    self.mainpython.sections.append(newSection)
                    self.mainpython.currentSections.append(newSection)
            for s in self.mainpython.sections:
                self.mainpython.currentSections.append(s)
            self.mainpython.sections = []
            self.mainpython.rectangle.w += 0.1
            self.mainpython.rectangle.h += 0.1
            for i in range(len(self.mainpython.currentSections)):
                self.mainpython.currentSections[i].rectangle.w = self.mainpython.rectangle.w
                self.mainpython.currentSections[i].rectangle.h = self.mainpython.rectangle.h

#Function that handles collisions,movement
    def action(self):
        distance = 4 
        for f in self.foodItems:
            if f.rectangle.colliderect(self.mainpython.rectangle):
                #start grwoth
                self.startGrowth = True
                #call grow function from the python
                self.mainpython.grow(f.width)
                #remove food that python collided with
                self.foodItems.remove(f)
                #spawn a new food
                radiusOfFood =  random.randint(5,10)
                horizaontalPositionOfFood = random.randint(self.MapRect.x,self.MapRect.x+self.MapRect.w)
                verticalPositionOfFood = random.randint(self.MapRect.y,self.MapRect.y+self.MapRect.h)
                f = food(horizaontalPositionOfFood,verticalPositionOfFood,radiusOfFood)
                self.foodItems.append(f)  
                self.addSections()
        #get the mouse position
        mousePosition = pygame.mouse.get_pos()
        mouseHorizontalPos = mousePosition[0]
        mouseVerticalPos = mousePosition[1]
        #calculate the distance from the python to the center of the screen
        horizontalDistance = mouseHorizontalPos - screenWidth//2
        verticalDistance = mouseVerticalPos - screenHeight//2
        #calculate the direction of movement 
        atan = atan2(horizontalDistance,verticalDistance)
        #components of direction
        self.horizontalMovement = sin(atan)*self.movementStep
        self.verticalMovement = cos(atan)*self.movementStep
        self.mainpython.rectangle.x+=self.horizontalMovement
        self.mainpython.rectangle.y+=self.verticalMovement
        #save position of the head of python in the list
        self.mainpython.movement += [[self.mainpython.rectangle.x,self.mainpython.rectangle.y]]  
        #spawn the sections with certain distance from each other
        if len(self.mainpython.movement)>=(len(self.mainpython.currentSections))*distance and len(self.mainpython.currentSections)!=0:
            for i in range(len(self.mainpython.currentSections)):  
                #print(len(self.mainpython.movement),len(self.mainpython.currentSections)) 
                self.mainpython.currentSections[i].rectangle.x = self.mainpython.movement[-distance*i][0]
                self.mainpython.currentSections[i].rectangle.y = self.mainpython.movement[-distance*i][1] 

        #do the same for all other pythons
        for onepython in self.allPythons:
            for f in self.foodItems:
                if f.rectangle.colliderect(onepython.rectangle):
                    self.startGrowth = True
                    onepython.grow(f.width)
                    self.foodItems.remove(f)
                    radiusOfFood =  random.randint(5,10)
                    positionOfFood = [random.randint(self.MapRect.x,self.MapRect.x+self.MapRect.w),random.randint(self.MapRect.y,self.MapRect.y+self.MapRect.h)]
                    f = food(positionOfFood[0],positionOfFood[1],radiusOfFood)
                    self.foodItems.append(f)  
                    self.addSections()
            onepython.movement += [[onepython.rectangle.x,onepython.rectangle.y]]  
            if len(onepython.currentSections)==1:
                onepython.currentSections[0].rectangle.x = onepython.movement[0]
                onepython.currentSections[0].rectangle.y = onepython.movement[1] 
            if len(onepython.movement)>=(len(onepython.currentSections))*distance and len(onepython.currentSections)!=0:
                for i in range(len(onepython.currentSections)):                              
                        onepython.currentSections[i].rectangle.x = onepython.movement[-distance*i][0]
                        onepython.currentSections[i].rectangle.y = onepython.movement[-distance*i][1] 
            #get the position of nearest food and python
            nearestSection = self.checkDistanceToSections(onepython)
            #calculate distance to food
            if onepython.bestSelection[0] == []:
                onepython.bestSelection = self.bestStrategy(onepython)
            horizontalDistanceSection = nearestSection.rectangle.x - onepython.rectangle.x
            verticalDistanceSection = nearestSection.rectangle.y - onepython.rectangle.y
            if horizontalDistanceSection<=0 and verticalDistanceSection<=0:
                for i in  onepython.bestSelection[0]:
                    if i.rectangle.x - onepython.rectangle.x <= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y <= verticalDistanceSection:
                        onepython.bestSelection[0].remove(i)
            elif horizontalDistanceSection>=0 and verticalDistanceSection<=0:
                for i in  onepython.bestSelection[0]:
                    if i.rectangle.x - onepython.rectangle.x >= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y <= verticalDistanceSection:
                        onepython.bestSelection[0].remove(i)
            elif horizontalDistanceSection>=0 and verticalDistanceSection>=0:
                for i in onepython.bestSelection[0]:
                    if i.rectangle.x - onepython.rectangle.x >= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y >= verticalDistanceSection:
                        onepython.bestSelection[0].remove(i)
            elif horizontalDistanceSection<=0 and verticalDistanceSection>=0:
                for i in onepython.bestSelection[0]:
                    if i.rectangle.x - onepython.rectangle.x <= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y >= verticalDistanceSection:
                        onepython.bestSelection[0].remove(i)

            otherFood = copy(self.foodItems)
            if horizontalDistanceSection<=0 and verticalDistanceSection<=0:
                for i in otherFood:
                    if i.rectangle.x - onepython.rectangle.x <= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y <= verticalDistanceSection:
                        otherFood.remove(i)
            elif horizontalDistanceSection>=0 and verticalDistanceSection<=0:
                for i in otherFood:
                    if i.rectangle.x - onepython.rectangle.x >= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y <= verticalDistanceSection:
                        otherFood.remove(i)
            elif horizontalDistanceSection>=0 and verticalDistanceSection>=0:
                for i in otherFood:
                    if i.rectangle.x - onepython.rectangle.x >= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y >= verticalDistanceSection:
                        otherFood.remove(i)
            elif horizontalDistanceSection<=0 and verticalDistanceSection>=0:
                for i in otherFood:
                    if i.rectangle.x - onepython.rectangle.x <= horizontalDistanceSection or i.rectangle.y - onepython.rectangle.y >= verticalDistanceSection:
                        otherFood.remove(i)
            if onepython.bestSelection[0] == []:
                onepython.bestSelection = self.bestStrategy(onepython)
            horizontalDistanceFood = onepython.bestSelection[0][0].rectangle.x - onepython.rectangle.x
            verticalDistanceFood = onepython.bestSelection[0][0].rectangle.y - onepython.rectangle.y
            if onepython.bestSelection[0][0] not in otherFood:
                onepython.bestSelection = self.bestStrategy(onepython)

            if (onepython.rectangle.x<self.MapRect.left or 
            onepython.rectangle.x>self.MapRect.right or 
            onepython.rectangle.y<self.MapRect.top or
            onepython.rectangle.y>self.MapRect.bottom):
                self.pythonDied(onepython)


            angle = atan2(horizontalDistanceFood,verticalDistanceFood)
            movx = sin(angle)
            movy = cos(angle)
            horizontalMovement = movx*self.movementStepBots
            verticalMovement = movy*self.movementStepBots
            onepython.rectangle.x+=horizontalMovement
            onepython.rectangle.y+=verticalMovement
        self.collisionOfSankes()
        self.collisionMainPython()
        if (self.mainpython.rectangle.x<self.MapRect.left or 
            self.mainpython.rectangle.x>self.MapRect.right or 
            self.mainpython.rectangle.y<self.MapRect.top or
            self.mainpython.rectangle.y>self.MapRect.bottom):
            self.pythonDied(self.mainpython)
            self.exit = True
            deathScreen()   


#check if a certain snake collided with other snake
    def collisionOfSankes(self):
        pythons = self.allPythons + [self.mainpython]
        for i in range(len(pythons)):
            for j in range(len(pythons[i].currentSections)):
                for onepython in (pythons[:i]+pythons[i+1:]):
                    if onepython.rectangle.colliderect(pythons[i].currentSections[j].rectangle) or onepython.rectangle.colliderect(pythons[i].rectangle):
                        self.pythonDied(onepython)

#check if the main python collided with another python
    def collisionMainPython(self):        
        for a in range(len(self.allPythons)):
             for b in range(len(self.allPythons[a].currentSections)):
                if self.mainpython.rectangle.colliderect(self.allPythons[a].currentSections[b].rectangle) or self.mainpython.rectangle.colliderect(self.allPythons[a].rectangle):
                    self.pythonDied(self.mainpython)
                    self.exit = True
                    deathScreen()

#function to determine the most efficient movement path
    def bestStrategy(self,python):
        copyOfFoodItems = copy(self.foodItems)
        nearestFoodList = []
        strategies = []
        for i in range(2):
            nearestFood = self.checkDistance(python,copyOfFoodItems)[0]
            nearestFoodList.append(nearestFood)
            copyOfFoodItems.remove(nearestFood)
        for k in range(len(nearestFoodList)):
            best = self.bestStrategyHelper(2,[nearestFoodList[k].rectangle.x,nearestFoodList[k].rectangle.y],copyOfFoodItems)
            strategies.append(best)
        best = strategies[1]
        for i in range(len(strategies)):
            if strategies[i][1]<best[1]:
                best = strategies[i]
        return best
            
#helper function to determine the most efficient movement path
    def bestStrategyHelper(self,depth,foodCoordinates,copyOfFoodItems):
        if depth==0:
            return [[],0]
        else:
            nearestFood = self.checkDistanceTest(foodCoordinates,copyOfFoodItems)
            copyOfFoodItems.remove(nearestFood[0])
            foodCoordinates = [nearestFood[0].rectangle.x,nearestFood[0].rectangle.y]
            return [[nearestFood[0]] + self.bestStrategyHelper(depth-1,[nearestFood[0].rectangle.x,nearestFood[0].rectangle.y],copyOfFoodItems)[0],
            nearestFood[1]+
            self.bestStrategyHelper(depth-1,[nearestFood[0].rectangle.x,nearestFood[0].rectangle.y],copyOfFoodItems)[1]]
                        
#function handle python death
    def pythonDied(self,python):
        #create fodd insted of python
        if python in self.allPythons:
            for section in python.currentSections:
                horizontalPosition = section.rectangle.x
                verticalPosition = section.rectangle.y
                radius = 25
                newFood = food(horizontalPosition,verticalPosition,radius)
                self.foodItems.append(newFood)
            #remove python
            self.allPythons.remove(python)
            file = "circle (" +str(random.randint(1,13))+").png"
            positionOfPython = [random.randint(self.MapRect.left+100,self.MapRect.right-100),
            random.randint(self.MapRect.top+100,self.MapRect.bottom-100)]
            f = Python(gameScreen,positionOfPython[0],positionOfPython[1],self.width,self.width,file)
            f.newsections = random.randint(0,10)
            f.snakeGrew = True
            self.addSections()
            self.allPythons.append(f) 

#function to check distance to objects in a list(in this case, distance to food)
    def checkDistance(self,python,searchList):
        mindist = 100000000
        if len(searchList)!=0:
            for i in searchList:
                #calculate the distance
                dx = i.rectangle.x - python.rectangle.x
                dy = i.rectangle.y - python.rectangle.y
                dist = (dx**2+dy**2)**(1/2)
                #find the minimum distance
                if dist < mindist:
                    mindist = dist
                    target = i
            return (target,mindist)

#this function works similarly to the one mentioned above but takes coordiates instead of an object
    def checkDistanceTest(self,coordinates,searchList):
        mindist = 100000000
        if len(searchList)!=0:
            for i in searchList:
                #calculate the distance
                dx = i.rectangle.x - coordinates[0]
                dy = i.rectangle.y - coordinates[1]
                dist = (dx**2+dy**2)**(1/2)
                #find the minimum distance
                if dist < mindist:
                    mindist = dist
                    target = i
            return (target,mindist)

#function to check the distance to sections
    def checkDistanceToSections(self,python):
        mindist = 10000000
        pythons = self.allPythons + [self.mainpython]
        pythons.remove(python)
        if len(pythons)!=0:
            for i in pythons:
                if len(i.currentSections)==0:
                    dx = i.rectangle.x - python.rectangle.x
                    dy = i.rectangle.y - python.rectangle.y
                    dist = (dx**2+dy**2)**(1/2)
                    #find the minimum distance
                    if dist < mindist:
                        mindist = dist
                        nearestSection = i
                else:
                    allSections = copy(i.currentSections) + [i]
                    for j in allSections:
                        dx = j.rectangle.x - python.rectangle.x
                        dy = j.rectangle.y - python.rectangle.y
                        dist = (dx**2+dy**2)**(1/2)
                        if dist < mindist:
                            mindist = dist
                            nearestSection = j
            return nearestSection
        
#function to run the main game 
    def runGame(self):
        self.mainpython = Python(self.screen,self.startposX,self.startposY,self.startWidth,self.startWidth,playerSkin)
        self.createFood()
        self.createPythons()
        #main event loop        
        while self.exit == False and self.pause == False:
            self.clock.tick(60)
            for event in pygame.event.get():
                #check if window close button is clicked
                if event.type == QUIT:
                    #stop running the program
                    self.exit = True
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause = True
                        showPauseMenu()
            if self.pause == False:
                self.action()            
                self.showAllObjects() 
                pygame.display.update()

#defining a button class used to create buttons
class button:
    def __init__(self, picture,parentScreen,horizontalPosition,verticalPosition,width,height,buttonText,textColor):
        self.picture = picture
        self.horizontalPosition = horizontalPosition
        self.verticalPosition = verticalPosition
        self.rectangle = Rect(horizontalPosition,verticalPosition,width,height)
        self.buttonText = pygame.font.SysFont("impact",30).render(buttonText,True,textColor)
        self.parentScreen = parentScreen
        if picture != None:
            self.buttonPic = pygame.image.load(picture)
            self.image = pygame.transform.scale(self.buttonPic,(width,height))

    #function to show the button
    def show(self):
        if self.picture != None:
            gameScreen.blit(self.image,(self.rectangle.x,self.rectangle.y))   
        self.parentScreen.blit(self.buttonText,(self.rectangle.x,self.rectangle.y))

    #checking if the button is pressed
    def isButtonPressed(self,horizontalPosition,verticalPosition):
        if horizontalPosition in range(self.rectangle.left, self.rectangle.right):
            if verticalPosition in range(self.rectangle.top,self.rectangle.bottom):
                return True

#Function that shows the skin selection menu            
def ShowSkinSelectionWindow():
    k=0
    Skin = button('DD.png',gameScreen,screenWidth//2-100,screenHeight//2-100,200,200,"","black")
    file = 'DD.png'
    while True:
        listOfSkins = ['DD.png','SR.png','circle (1).png','circle (2).png','circle (3).png','circle (4).png','circle (5).png','circle (6).png','circle (7).png','circle (8).png','circle (9).png']
        screen = gameScreen
        screen.fill((5,7,100)) 
        pygame.display.set_caption('Skin Selection')
        textTitle = pygame.font.SysFont("impact",30).render('Select your skin',True,'black')
        gameScreen.blit(textTitle,(screenWidth//2-textTitle.get_rect().width//2,100))  
        mousePosition = pygame.mouse.get_pos() 
        mouseHorizontalPos = mousePosition[0]
        mouseVerticalPos = mousePosition[1]
        rightButton = button("arrow1.png",gameScreen,screenWidth//2+100,screenHeight//2-25,50,50,"","black")
        rightButton.show()
        leftButton = button("arrow2.png",gameScreen,screenWidth//2-150,screenHeight//2-25,50,50,"","black")
        leftButton.show()
        textConfirm = pygame.font.SysFont("impact",30).render('Confirm Selection',True,'black')   
        #gameScreen.blit(text,(screenWidth//2-textResume.get_rect().width//2,100))  
        Confirm = button(None,gameScreen,screenWidth//2-textConfirm.get_rect().width//2,screenHeight//2+150,textConfirm.get_rect().width,textConfirm.get_rect().height,'Confirm Selection',"black")
        Confirm.show()
        Skin.show()
        #main event loop        
        for event in pygame.event.get():
                #check if window close button is clicked
                if event.type == QUIT:
                    #stop running the program
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rightButton.isButtonPressed(mouseHorizontalPos,mouseVerticalPos) and k<len(listOfSkins)-1:
                        k+=1
                        file = listOfSkins[k]
                        Skin = button(file,gameScreen,screenWidth//2-100,screenHeight//2-100,200,200,"","black")
                        Skin.show()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if leftButton.isButtonPressed(mouseHorizontalPos,mouseVerticalPos) and k>0:
                        k-=1
                        file = listOfSkins[k]
                        Skin = button(file,gameScreen,screenWidth//2-100,screenHeight//2-100,200,200,"","black")
                        Skin.show()
                    if Confirm.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                        game.mainpython.section = pygame.image.load(file)
                        global playerSkin
                        playerSkin = file
                        menu()   
        pygame.display.update()    

#Function that shows the pause menu            
def showPauseMenu():
    quitGame = False
    while game.pause:
        screen = gameScreen
        screen.fill((5,7,100)) 
        pygame.display.set_caption('Pause')
        exit = False
        text = pygame.font.SysFont("impact",30).render('Game Paused',True,'white')
        gameScreen.blit(text,(screenWidth//2-text.get_rect().width//2,100))  
        mousePosition = pygame.mouse.get_pos() 
        mouseHorizontalPos = mousePosition[0]
        mouseVerticalPos = mousePosition[1]
        textResume = pygame.font.SysFont("impact",30).render('Resume',True,'black')   
        Resume = button(None,gameScreen,screenWidth//2-textResume.get_rect().width//2,200,textResume.get_rect().width,textResume.get_rect().height,'Resume',"black")
        Resume.show()
        textMenu = pygame.font.SysFont("impact",30).render('Quit To Menu',True,'black')   
        Menu = button(None,gameScreen,screenWidth//2-textMenu.get_rect().width//2,300,textMenu.get_rect().width,textMenu.get_rect().height,'Quit to menu',"black")
        Menu.show()
        #main event loop        
        for event in pygame.event.get():
                #check if window close button is clicked
                if event.type == QUIT or quitGame == True:
                    #stop running the program
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Resume.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                        game.pause = False 
                    if Menu.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                        game.foodItems.clear()
                        game.allPythons.clear()
                        game.mainpython.currentSections.clear()
                        menu()
        pygame.display.update()    

#function to show the death screen
def deathScreen():
    run = True
    quitGame = False
    while run:
        pygame.display.set_caption('Game Over')
        gameScreen.fill((5,70,100))  
        text = pygame.font.SysFont("impact",30).render('Game Over! You collided with another python or border. Score: '+str(game.mainpython.length),True,'White')
        gameScreen.blit(text,(screenWidth//2-text.get_rect().width//2,100))
        mousePosition = pygame.mouse.get_pos() 
        mouseHorizontalPos = mousePosition[0]
        mouseVerticalPos = mousePosition[1]
        textMenu = pygame.font.SysFont("impact",30).render('Back to Menu',True,'black')
        gameButton = button(None,gameScreen,screenWidth//2-textMenu.get_rect().width//2,200,textMenu.get_rect().width,textMenu.get_rect().height,'Back to menu',"black")
        gameButton.show()
        textExit = pygame.font.SysFont("impact",30).render('Quit',True,'black')   
        Quit = button(None,gameScreen,screenWidth//2-textExit.get_rect().width//2,300,textExit.get_rect().width,textExit.get_rect().height,'Quit',"black")
        Quit.show()
        for event in pygame.event.get():
            if event.type == QUIT or quitGame == True:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameButton.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                    game.foodItems.clear()
                    game.allPythons.clear()
                    game.mainpython.currentSections.clear()
                    menu()
                if Quit.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                    quitGame = True

            pygame.display.update()

    
#Function to open main menu
def menu():
    #loop
    run = True
    quitGame = False
    while run:
        pygame.display.set_caption('Game Menu')
        gameScreen.fill((5,70,100))  
        mousePosition = pygame.mouse.get_pos() 
        mouseHorizontalPos = mousePosition[0]
        mouseVerticalPos = mousePosition[1]
        #button to play
        gameButton = button(None,gameScreen,screenWidth//2-25,100,50,50,"Play","black")
        gameButton.show()
        #button to select a skin
        skinChoiceButton = button(None,gameScreen,screenWidth//2-75,200,200,50,"Choose Skin","black")
        skinChoiceButton.show()
        textExit = pygame.font.SysFont("impact",30).render('Quit',True,'black')   
        Quit = button(None,gameScreen,screenWidth//2-textExit.get_rect().width//2,300,textExit.get_rect().width,textExit.get_rect().height,'Quit',"black")
        Quit.show()
        for event in pygame.event.get():
            if event.type == QUIT or quitGame == True:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameButton.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                    game.pause = False
                    game.exit = False
                    game.runGame()
                if skinChoiceButton.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                    ShowSkinSelectionWindow()
                if Quit.isButtonPressed(mouseHorizontalPos,mouseVerticalPos):
                    quitGame = True
            pygame.display.update()
game = Game()
menu()





        