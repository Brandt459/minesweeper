import pygame
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button

class DropdownClass:
    def __init__(self, headSurface, screen, game):
        self.dropdownObject = Dropdown(
            headSurface, 
            5, 
            5, 
            100, 
            20, 
            name='Select Mode',
            choices=[
                'Easy',
                'Medium',
                'Hard'
            ],
            values=[
                0,
                1,
                2
            ],
            onClick=lambda: self.switchGamemode()
        )
        self.headSurface = headSurface
        self.screen = screen
        self.game = game
        self.gamemode = game.gamemode

    def switchGamemode(self):
        # fix needing to click dropdown button to get correct value from getSelected()
        if self.dropdownObject.getSelected() != self.gamemode:
            self.game.generateBoard(self.dropdownObject.getSelected(), self.screen)

