import pygame
import sys
import os
import math
import random
import traceback
from pygame.locals import *

TWO_PI = math.pi * 2
#random.seed(1234)

class MovableActors(pygame.sprite.Group):
  pass
  
  
class StaticActors(pygame.sprite.Group):
  pass

  
  
class Player(pygame.sprite.Sprite):
  """
  Player object.
  """
  
  def __init__(self, boundaryRect, startLocation):
    """
    Initializer for player object.
    Args:
      boundaryRect: Rect object to limit the player to.
      startLocation: coordinates to spawn the center of the object.
    """
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)
    self.boundaryRect = boundaryRect

    #Load image
    #self.image = pygame.image.load('images/0144.png').convert_alpha()
    self.image = pygame.Surface((100,100)).convert_alpha()
    self.image.fill((0,0,0,0))
    pygame.draw.circle(self.image, (255,0,0), (50,50), 50)
    self.rect = self.image.get_rect()
    self.rect.center = startLocation
    self.active_joysticks = []
    self.initJoyStick()

  def initJoyStick(self):
    joystick_count = pygame.joystick.get_count()
    for js in xrange(joystick_count):
      joystick = pygame.joystick.Joystick(js)
      joystick.init()
      self.active_joysticks.append(joystick)
      
        
  def update(self, deltaTime):
    self.move(deltaTime)

  def move(self, deltaTime):
    dx = 0
    dy = 0
    for js in self.active_joysticks:
      for axis in xrange(js.get_numaxes()):
        if axis in (0,4):
          dx += round(js.get_axis(axis) * 200 * deltaTime)
        elif axis in (1,3):
          dy += round(js.get_axis(axis) * 200 * deltaTime)
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] or key[pygame.K_LEFT]:
      dx -= 100 * (1 + key[pygame.KMOD_SHIFT]) * deltaTime
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
      dx += 100 * (1 + key[pygame.KMOD_SHIFT]) * deltaTime
    if key[pygame.K_w] or key[pygame.K_UP]:
      dy -= 100 * (1 + key[pygame.KMOD_SHIFT]) * deltaTime
    if key[pygame.K_s] or key[pygame.K_DOWN]:
      dy += 100 * (1 + key[pygame.KMOD_SHIFT]) * deltaTime
    
    self.rect.move_ip(dx, dy)

    if self.rect.top < self.boundaryRect.top:
      self.rect.top = self.boundaryRect.top
    if self.rect.left < self.boundaryRect.left:
      self.rect.left = self.boundaryRect.left
    if self.rect.bottom > self.boundaryRect.bottom:
      self.rect.bottom = self.boundaryRect.bottom
    if self.rect.right > self.boundaryRect.right:
      self.rect.right = self.boundaryRect.right

      


class Blobs(pygame.sprite.Group):
  """
  Sprite group of blob objects.
  """
  
  number_of_blobs = 100
  number_of_blob_sizes = 5
  
  def __init__(self, boundaryRect):
    """
    Load and scale images and initialize blobs.
    Args:
      boundaryRect: Rect object to bound the blobs.
    """
    pygame.sprite.Group.__init__(self)
    self.boundaryRect = boundaryRect
    self.loadImages()
    self.scaleImages(self.number_of_blob_sizes)
    self.createBlobs(self.number_of_blobs)
  
  
  def createBlobs(self, blob_count = None):
    """
    Creates blobs in group.
    Args:
      blob_count: integer number of blobs to create
    """
    if blob_count == None:
      blob_count = self.number_of_blobs
	
    for i in xrange(blob_count):
      blob = Blob( group = self,
                   scaled_images = self.scaled_images,
                   boundaryRect = self.boundaryRect,
	                 x = random.randint(self.boundaryRect.left,
	                                    self.boundaryRect.right),
                   y =  random.randint(self.boundaryRect.top,
				                               self.boundaryRect.bottom),
                   starting_scale = random.randint(1,
                     self.number_of_blob_sizes))
      			
  def loadImages(self):
    """
    Loads blob animation images into self.raw_images list
    """
    images=[]
    for i in range(144,155):
      images.append(pygame.image.load('images/0%s.png' % i).convert_alpha())
    # Load a copy of the images in reverse order to complete animation
    self.raw_images = images + images[::-1]
    self.images = self.raw_images
    self.image_count = len(self.images)


  def scaleImages(self, num_scales):
    """
    Creates a list of scaled image lists.
    Generates self.scaled_images list of each image set scaled
    down as the index increases.
    Args:
      num_scales: The number of different scales to create.    
    """
    
    image_rect = self.raw_images[0].get_rect()
    self.scaled_images = {num_scales : self.raw_images}
    # add zero key so we can at least get an image if the scale is unknown.
    #self.scaled_images[0] = self.raw_images
    new_height = image_rect.height
    new_width = image_rect.width
    for scale in xrange(num_scales-1, 0, -1):
      new_height -= int(new_height * 0.238)
      new_width -= int(new_width * 0.238)
      scaled_images = []
      for image in self.raw_images:
        scaled_images.append(pygame.transform.scale(
          image,(new_width, new_height)))
      self.scaled_images[scale] = scaled_images


class Blob(pygame.sprite.Sprite):
  """
  Blob object that moves semi-randomly.
  """
  
  def __init__(self, group, scaled_images, boundaryRect, x, y, starting_scale):
    """
    Initializer for blob object.
    Args:
	  images: list of image surfaces.
      x, y: coordinates to spawn the center of the object.
	  starting_scale: Scale index to start with.
    """
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self, group)

    self.scaled_images = scaled_images
    self.boundaryRect = boundaryRect
    self.images = self.scaled_images[1]
    self.rect = self.images[0].get_rect()
    self.rect.center = x, y
    
    self.setScale(starting_scale)

    # Randomize the starting image.
    self.image_number = random.randint(0, len(self.images))
    
    self.direction = random.random() * TWO_PI
    self.alive = True
    


      
  def setScale(self, scale):
    """
    Sets the active image set to a different scale.
    Args:
      scale: index of the self.scaled_images set.
    """
    
    self.scale = scale
    old_center = self.rect.center
    self.images = self.scaled_images[scale]
    self.rect = self.images[0].get_rect()
    self.rect.center = old_center
    self.speed_scale = (len(self.scaled_images) - scale + 1)/2.
    
  def nextImage(self):
    """
    Sets the next image for animation.
    """
    self.image_number += 1
    if self.image_number >= len(self.images):
      self.image_number = 0
    self.image = self.images[self.image_number]
    

  def changeDirection(self, timedelta):
    """
    Changes the direction of the object by a random amount.
    """
    direction_delta = random.uniform(-1.5708, 1.5708) * timedelta
    #direction_delta = random.uniform(-TWO_PI, TWO_PI) #* timedelta
    self.direction = (self.direction + direction_delta) % TWO_PI
    
  def combineWithOther(self, other_blob):
    """
    Merges blob with other blob.
    """
    pass

  

  def turnAround(self):
    """
    React to hitting wall.
    """
    direction_delta = random.choice((-1.5708, 3.1415, 1.5708))
    self.direction = (self.direction + direction_delta) % TWO_PI

    
  def move(self, timedelta):
    """
    Moves the object.
    """
    
    #if random.randint(0,10)>9:
    self.changeDirection(timedelta)
    distance = random.uniform(5., 50.) * timedelta * self.speed_scale
    
    self.dx = round(distance * math.cos(self.direction))
    # pygame has Y-axis top to bottom
    self.dy = -round(distance * math.sin(self.direction))
    self.rect.move_ip(self.dx, self.dy)
    
    if self.rect.top < self.boundaryRect.top:
      self.rect.top = self.boundaryRect.top
      self.turnAround()
    if self.rect.left < self.boundaryRect.left:
      self.rect.left = self.boundaryRect.left
      self.turnAround()
    if self.rect.bottom > self.boundaryRect.bottom:
      self.rect.bottom = self.boundaryRect.bottom
      self.turnAround()
    if self.rect.right > self.boundaryRect.right:
      self.rect.right = self.boundaryRect.right
      self.turnAround()

  def update(self, timedelta = 1):
    """
    Updates the object
    """
    self.move(timedelta)
    self.nextImage()
    