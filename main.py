#! usr/bin/env python2

"""
A simple game where the user tries to collide with each blob.

"""
import pygame
import sys
import os
import math
import random
import traceback
import entities
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 900
FRAME_RATE_LIMIT = 20
SKY_COLOR = (30, 30, 100)
TWO_PI = math.pi * 2






def mainloop():
  """
  Main game loop.
  """
  
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill(SKY_COLOR)
  screen.blit(background, (0, 0))
  counter = 0
  rungame = True
  deltaTime = clock.tick(FRAME_RATE_LIMIT) / 1000.
  fps_font = pygame.font.Font(None, 18)
  #blob_text_font = pygame.font.Font(None, 12)

  gameBoundary = pygame.Rect(0, 0,
                             SCREEN_WIDTH,
                             SCREEN_HEIGHT)
  blobs = entities.Blobs(gameBoundary)
  
  player = entities.Player(gameBoundary, gameBoundary.center)
  movableActors = entities.MovableActors()
  movableActors.add(blobs)
  movableActors.add(player)
  
  while rungame:

    #Event Handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        rungame = False
      elif event.type == pygame.KEYDOWN:
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
          rungame = False
          break

    # Update display
    movableActors.clear(screen, background)
    blobs.update(deltaTime)
    #blobs.draw(screen)
    player.update(deltaTime)
    #screen.blit(player.image, player.rect)
    movableActors.draw(screen)

      
    if counter %300:
      fps_text = fps_font.render('FPS: %0.2f (%f)' % (clock.get_fps(), deltaTime*3), True, (255,255,255))
      fps_rect = fps_text.get_rect()
      fps_rect.top = 0
      fps_rect.left = 0
      screen.blit(background, fps_rect, fps_rect)
      screen.blit(fps_text, fps_rect)
      counter = 0

    pygame.display.flip()
      
    deltaTime = clock.tick(FRAME_RATE_LIMIT) / 1000.

    counter += 1
    
    
try:
  mainloop()
except Exception, e:
  tb = sys.exc_info()[2]
  traceback.print_exception(e.__class__, e, tb)
finally:
  # Call pygame.quit() even if there are errors
  # so that the game screen is closed.
  pygame.quit()
