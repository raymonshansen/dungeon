"""Time management-system."""

class PriorityQueue():
    """A priority queue to handle all actors(Monster and Hero)."""

    def __init__(self):
        """Construct the queue as a list sorted on priority."""
        self.queue = list()
    
    def __len__(self):
        return len(self.queue)

    def enqueue(self, value, priority = 1.0):
        """Add an actor to the queue"""
        actor = [priority, value]

        # Insert the tuple in sorted position in the queue. If a
        # tuple with equal priority is encountered, the new tuple is
        # inserted after it.

        # Binary search for where to put... :)
        finalPos = 0
        high = len(self)
        while finalPos < high:
            middle = (finalPos + high) // 2
            if actor[0] < self.queue[middle][0]:
                high = middle
            else:
                finalPos = middle + 1

        self.queue.insert(finalPos, actor)
    

    def adjustPriorities(self, amount):
        """Increase all priorities with amount."""
        for actor in self.queue:
            actor[0] += amount
    
    def dequeue(self):
        """Pop the value with the lowest priority."""
        return self.queue.pop(0)[1]

    def dequeueWithKey(self):
        """Pop the (priority, value)-list with the lowest priority."""
        return self.queue.pop(0)

    def erase(self, value):
        """Removes an element from the queue by value."""
        self.__erase(value, lambda a, b: a == b)

    def erase_ref(self, value):
        """Removes an element from the queue by reference."""
        self.__erase(value, lambda a, b: a is b)

    def __erase(self, value, test):
        """All tupples t are removed from the queue
        if test(t[1], value) evaluates to True.
        """
        i = 0
        while i < len(self.queue):
            if test(self.queue[i][1], value):
                del self.queue[i]
            else:
                i += 1

class TimeSchedule(object):
    """Represents a series of events that occur over time."""

    def __init__(self):
        self.schedule = PriorityQueue()

    def scheduleEvent(self, event, delay = 0.0):
        """Schedules an event to occur after a certain delay."""
        if event:
            self.schedule.enqueue(event, delay)

    def nextEvent(self):
        """Dequeues and returns the next event to occur."""
        time, event = self.schedule.dequeueWithKey()
        self.schedule.adjustPriorities(-time)

        return event

    def cancelEvent(self, event):
        """Cancels a pending event."""
        self.schedule.erase_ref(event)

class Thing(object):
    """Just something to test. Assumes that the maximum speed
    of a thing is 10.
    """

    BASE_TIME = 10.0

    def __init__(self, id, speed):
        self.id = id
        self.speed = speed

    def __str__(self):
        return self.id

    def actionDelay(self):
        return Thing.BASE_TIME / self.speed

# TEST
TURN_ROUNDS = 10

if __name__ == '__main__':
    actors = [Thing('Hero', 1), Thing('Bat', 2), Thing('Cat', 1)]
    timequeue = TimeSchedule()

    turns = 0
    turnsTaken = {}

    # For each actor:
    for actor in actors:
        # Add the actor and its delay(small delay = faster actor)
        timequeue.scheduleEvent(actor, actor.actionDelay())
        # Sum up the total number of turns we're doing
        turns += actor.speed
        turnsTaken[actor] = 0

    turns *= TURN_ROUNDS

    while turns > 0:
        thing = timequeue.nextEvent()

        turnsTaken[thing] += 1
        print(thing)
        turns -= 1

        timequeue.scheduleEvent(thing, thing.actionDelay())

    for thing, numTurns in turnsTaken.items():
        assert numTurns == (thing.speed * TURN_ROUNDS)

    print("\nActions per actor in {} rounds:".format(TURN_ROUNDS))
    for id, numTurns in turnsTaken.items():
        print(id, numTurns)
