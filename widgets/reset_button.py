from pygame_widgets.button import Button

def resetButton(headSurface, game):
    return Button(
        headSurface,
        100,
        10,
        100,
        100,
        text='Reset',
        margin=20,
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),
        pressedColour=(0, 200, 20),
        onClick=lambda: game.generateBoard()
    )