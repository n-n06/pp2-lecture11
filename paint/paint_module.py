import pygame
from typing import Tuple
import math

width, height = 640,480


class Figure():
    layers = []
    def __init__(self, color:Tuple[int,int,int], screen : pygame.surface.Surface, draw_size : int):
        '''
        The class Figure - parent class of all of the drawable elements. Has list var layers that stores all of the object's layers to draw them in order
        Initialized with the following parameters (passed on by the user):
        - color - an RGB tuple
        - screen - pygame's main display Surface
        - draw_size - thickness of elements
        Automatically set parameters:
        - layer - a transparent layer that will be blit on the main display
        - drawn - a bool parameter. whether the current object has been drawn
        - added_to_layers - a bool parameter. whether the current object is in the Figure's class var layers

        '''
        self.color = color
        self.layer = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.screen = screen
        self.drawn = False
        self.added_to_layers = False
        self.draw_size = draw_size

    def add_to_layers(self):
        '''
        Add the current instance's layer to Figure's layers list
        layers list is then sliced to save only the last 500 layers (for the sake of optimization)
        '''
        Figure.layers.append(self)
        Figure.layers = Figure.layers[-500:]

    @classmethod
    def draw_all(cls):
        '''
        Drawing each instance's layer on the main display with no coordinate offset
        '''
        for inst in cls.layers:
            inst.screen.blit(inst.layer, (0,0))



class Circle(Figure):
    '''
    The class Circle - child class of Figure. Used to draw circles.
    Has class var enable that turns on/off the drawing circles mode
    Has adjustable thickness
    '''

    enable = False

    def __init__(self, color : Tuple[int, int, int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing as a child of the Figure class.
        Setting radius to 0, and center to None as we did not draw anythin at the point of initialization
        '''
        super().__init__(color, screen, draw_size)
        self.radius = 0
        self.center = None
    
    def change_size(self, direction : int):
        '''
        Changing the thickness of circle(affects only next circles). The thickness ranges from 5 to the radius of the circle
        '''

        if direction > 0 and self.radius > 0:
            self.draw_size = min(math.ceil(self.radius), self.draw_size + 2)
        elif direction < 0 and self.radius > 0:
            self.draw_size = max(5, self.draw_size - 2)

    
    def draw(self, mouse_pressed : bool):
        '''
        Function that draws a circle based on the current mouse position
        If the circle is drawn and is not added to the layers list of the parent class, we draw it on its layer and quit the function
        If we have already set the circle's size and its center is not None, we mark it as a drawn circle
        '''

        if self.drawn and not self.added_to_layers:
            self.draw_on_layer()
            self.added_to_layers = True
            return
        if not mouse_pressed and self.center != None:
            self.drawn = True
            return
        #getting the mouse position
        pos = pygame.mouse.get_pos()
        if self.center == None:
            #setting the mouse position as center if we have entered the function for the firss time for this instance
            self.center = pos
        
        #calculating the radius using the distance formula
        self.radius = math.sqrt((pos[0] - self.center[0])**2 + (pos[1] - self.center[1])**2)
        #drawing the circle on the screen not on its layaer yet to avoid creating too much layers
        pygame.draw.circle(self.screen, self.color, self.center, self.radius, self.draw_size)
       
        
    def draw_on_layer(self):
        #drawing the current circle on its layer and adding it to the Figure class's layers list
        pygame.draw.circle(self.layer, self.color, self.center, self.radius, self.draw_size)
        self.add_to_layers()


class Palette():
    '''
    Palette class. Used to activate color selection by blitting a spectrum image and returning a color tuple on mouse click
    '''
    enable = False
    def __init__(self, screen : pygame.surface.Surface):
        self.screen = screen
        self.spectrum = pygame.image.load("color_select.jpg")
        self.spectrum_rect = self.spectrum.get_rect(center = (180, 196))
    
    def draw_spectrum(self):
        #creating an interactive color selection button
        self.spectrum_button = self.screen.blit(self.spectrum, self.spectrum_rect)
    def select_color(self, pressed : Tuple[bool, bool, bool], mouse_pos : Tuple[int, int], current_color : Tuple[int,int,int]):
        #if LMB is pressed on the position of the spectrum button, we return a color value at this point
        #then we automatically swithc off the palette and color selection
        if pressed[0] and self.spectrum_button.collidepoint(mouse_pos):
            Palette.enable = False
            color = self.spectrum.get_at((mouse_pos[0], mouse_pos[1]-80))
            if color == None:
                return current_color
            else:
                return color
        else:
            return current_color




class NRect(Figure):
    '''
    The class NRect - child class of Figure. Used to draw simple rectangles.
    Named NRect to avoid confusion with pygame's Rect class
    Has class var enable that turns on/off the drawing rectangles mode
    Has adjustable thickness
    '''
    enable = False

    def __init__(self, color : Tuple[int, int, int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing as a child of Figure class 
        Setting the start_point to None as we did not put the first point of the rectangle
        '''
        super().__init__(color, screen, draw_size)
        self.start_point = None

    def change_size(self, direction : int):
        '''
        Changes the thickness of border lines(affect only the next rects). The min value is 5, the max value of thickness is the largest side of the rectangle
        '''
        if direction > 0 and self.start_point != None:
            self.draw_size = min(max(self.rect.width, self.rect.height), self.draw_size + 2)
        elif direction < 0 and self.start_point != None:
            self.draw_size = max(5, self.draw_size - 2)


    def draw(self, mouse_pressed : bool):
        '''
        Function that draws a rectangle based on the current mosue position
        If the rectangle is drawn and is not added to the layers list of the parent class, we draw it on the layer and quit the function
        If we have already set the rectangle's size and its position is not empty, we mark it as a drawn rectangle
        '''
        if self.drawn and not self.added_to_layers:
            self.draw_on_layer()
            self.added_to_layers = True
            return

        if not mouse_pressed and self.start_point != None:
            self.drawn = True
            return
        #get the mouse's position
        pos = pygame.mouse.get_pos()

        #if we are setting the size for the first time, the mouse's position as the start point
        if self.start_point == None:
            self.start_point = pos
        
        #get the difference between the starting position and the current mouse position
        x = min(self.start_point[0], pos[0])
        y = min(self.start_point[1], pos[1])
        
        #setting the width and the height of the rect
        width = max(pos[0], self.start_point[0]) - x
        height = max(pos[1], self.start_point[1]) - y

        self.rect = pygame.Rect(x, y, width, height)   #adjustable rect
        pygame.draw.rect(self.screen, self.color, self.rect, self.draw_size)    #when we are in the adjusting/drawing/setting size mode we draw the rect on the screen, and only when we finished doing so, we draw everything on the corresponding layer

    def draw_on_layer(self):
        #drawing the current instance on its corresponding layer, and then adding it to the parent class' layers list
        pygame.draw.rect(self.layer, self.color, self.rect, self.draw_size)
        self.add_to_layers()



class Eraser(Figure):
    '''
    Eraser class - child class of Figure.
    When enalbed, draws circles of background color to eraser the objects on the canvas (if the LMB is pressed).
    When the process of erasing is finished i.g. the LMB is not pressed anymore, the drawn circles are added to a new layer on the canvas. Thus, everything that is drawn next, will be displayed upon the erased layer.
    Has dynamic size.
    '''
    def __init__(self, bg_color : Tuple[int,int,int], screen : pygame.surface.Surface, draw_size : int):
        '''
        Initializing the eraser as a child of Figure class
        The draw_size is set as the radius of circles that are drawn to erase layers on canvas
        '''
        super().__init__(bg_color, screen, draw_size)
        self.enable = False
        self.radius = draw_size
        self.points = []

    def change_size(self, direction : int):
        '''
        Changing the size of the circles
        '''
        if direction > 0:
            self.radius = min(self.radius, self.draw_size + 2)
        elif direction < 0:
            self.radius = max(15, self.draw_size - 2)
 

    def erase(self, mouse_pos : Tuple[int,int]):
        '''
        Drawing the circles on the eraser's layer, not on the screen yet.
        mouse_pos parameter is required to place the circles on the mouse's current position
        '''
        pygame.draw.circle(self.layer, self.color, mouse_pos, self.radius)
        

    def draw_on_layer(self):
        '''
        Adding the current layer to the parent class' layers list
        '''
        self.add_to_layers()

    
def drawLine(screen, index, start, end, width, color_mode):
    #default drawing function

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):            
        progress = 1.0 * i /iterations
        aprogress = 1 - progress

        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color_mode, (x,y), width)


def change_size_all(draw_size : int, circle : Circle, nrect : NRect, eraser : Eraser, direction : int):
    #every figure's size is changed correspondingly with their own function (polymorphism, i guess)
    for el in (circle, nrect, eraser):
        el.change_size(direction)
    #changin the size of the default mode
    if direction == 1:
        draw_size = min(40, draw_size + 2)
    elif direction == -1:
        draw_size =  max(5, draw_size - 2)
    return draw_size


    
    
    
