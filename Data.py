import pygame.image

fishing_rods = [pygame.transform.scale(pygame.image.load("Source/Fishing road 1.png"), (154, 99)),
                 pygame.transform.scale(pygame.image.load("Source/Fishing road 2.png"), (154, 99))]
hooks = [pygame.transform.scale(pygame.image.load("Source/Hook 1.png"), (154, 99)),
         pygame.transform.scale(pygame.image.load("Source/Hook 2.png"), (154, 99))]
fishes = ["Source/Fish 1.png",
          "Source/Fish 2.png",
          "Source/Fish 3.png"]
backgrounds = [pygame.transform.scale(pygame.image.load("Source/BG 1.jpg"), (496, 425)),
               pygame.transform.scale(pygame.image.load("Source/BG 2.jpg"), (496, 425))]

achivs = ["Поймай первую рыбу", "Набери 7 рыбы", "Улучши удочку", "Улучши крючок", "Поймай рыбу-камень",
          "Перестань ловить рыбу на крючке"]
