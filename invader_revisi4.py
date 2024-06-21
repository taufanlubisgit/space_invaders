from ursina import *

app = Ursina()

class Tank(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.blue,
            scale=(0.5, 0.1, 0.5),  #Ubah ukuran tank
            position=(0, -3.5)
        )
        self.speed = 5

    def update(self):
        if held_keys['d'] and self.x < 3.5:
            self.x += self.speed * time.dt
        if held_keys['a'] and self.x > -3.5:
            self.x -= self.speed * time.dt

class Rudal(Entity):
    def __init__(self, position):
        super().__init__(
            model='quad',
            color=color.yellow,
            scale=(0.1, 0.5),
            position=position
        )
        self.speed = 4

    def update(self):
        self.y += self.speed * time.dt
        if self.y > 5:  # Adjust top screen boundary for missile
            destroy(self)
            if self in rudals:
                rudals.remove(self)

class Enemy(Entity):
    def __init__(self, position):
        super().__init__(
            model='circle',
            color=color.red,
            scale=(0.4, 0.4),
            position=position
        )

tank = Tank()

enemies = [Enemy((i, j)) for i in range(-3, 4) for j in range(4)]
rudals = []

# Variable to track if the game is over
game_over = False

def update():
    global enemies, rudals, game_over

    if game_over:
        return  # Stop updating if the game is over

    enemies_to_remove = []
    rudals_to_remove = []

    #------------------------------------------------------------------
    for enemy in enemies:
        if distance(enemy, tank) < 1:
            quit()

        for rudal in rudals:
            if distance(rudal, enemy) < 0.4:  
                rudals_to_remove.append(rudal)
                enemies_to_remove.append(enemy)
                break
    #------------------------------------------------------------------

    # Destroy and remove rudals after iterating through them
    for rudal in rudals_to_remove:
        if rudal in rudals:  # Check if rudal is still in the list
            destroy(rudal)
            rudals.remove(rudal)

    # Destroy and remove enemies after iterating through them
    for enemy in enemies_to_remove:
        if enemy in enemies:  # Check if enemy is still in the list
            destroy(enemy)
            enemies.remove(enemy)

    if len(enemies) == 0:
        game_over = True
        show_game_over()  # Call the function to display "Game Over"

def input(key):
    if key == 'space' and not game_over:  # Allow shooting only if the game is not over
        rudal = Rudal((tank.x, tank.y + 0.5))
        rudals.append(rudal)

def show_game_over():
    game_over_text = Text(
        text='Game Over',
        origin=(0, 0),
        scale=3,
        background=True
    )
    game_over_text.position = (0, 0)  # Center the text

app.run()
