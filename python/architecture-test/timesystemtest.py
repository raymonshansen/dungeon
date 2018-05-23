"""Time system test"""

import pygame as pg


TURN_COST = 1000


class Hero():
    def __init__(self):
        self.speed = 100
        self.next_action = False
        self.energy = 0

    def do_action(self, action):
        # return self.next_action.get_cost()
        self.energy -= 1000
        self.next_action = False

    def set_action(self, action):
        self.next_action = action

    def can_take_turn(self):
        return self.energy >= TURN_COST


class Monster():
    def __init__(self):
        self.speed = 50
        self.next_action = False
        self.energy = 0

    def do_action(self, action):
        """Each action will be an instance of a class.
        This way they can be given to anyone for
        easy moding of behaviour.
        """
        # return self.next_action.get_cost()
        self.energy -= 1000
        # Monsters are always ready!
        self.next_action = True

    def set_action(self, action):
        self.next_action = action

    def can_take_turn(self):
        return self.energy >= TURN_COST

pg.init()
# Make some actors
hero = Hero()
rat = Monster()
actors = [hero, rat]
done = False


def check_input():
    print("check_input()")
    events = pg.event.get()
    for event in events:
        print("got events")
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            return True
        if event.type == pg.KEYDOWN and event.key == pg.K_A:
            hero.set_action(True)
        if event.type == pg.KEYDOWN:
            print(event.key)


def tick():
    print("tick()")
    # Wait for the player to do something
    if not actors[0].next_action:
        print("return")
        return
    # Everyone who can, gets to go!
    else:
        print("actions!")
        for actor in actors:
            # Give everyone some energy
            actor.energy += 20
            if actor.can_take_turn():
                actor.do_action()


while not done:
    done = check_input()
    tick()

pg.quit()
