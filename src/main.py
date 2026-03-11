import pygame
import sys
import controller

def main():
	pygame.init()
	controller.runGame()
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
    main()