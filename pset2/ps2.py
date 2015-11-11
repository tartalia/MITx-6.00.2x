# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if width <= 0 or height <= 0:
            raise ValueError("Invalid widht or height")
        self.width = width
        self.height = height
        self.tiles = []
        for i in range(width):
            lines = [0 for j in range(height)]
            self.tiles.append(lines)

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[int(pos.getX())][int(pos.getY())] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[m][n] == 1

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        cleanedTiles = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] == 1:
                    cleanedTiles += 1
        return cleanedTiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        w = [x for x in range(self.width)]
        h = [y for y in range(self.height)]
        return Position(random.choice(w), random.choice(h))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.getX() >= 0 and pos.getX() < self.width \
            and pos.getY() >= 0 and pos.getY() < self.height:
            return True
        return False

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.angles = range(360)
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.choice(self.angles)
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        direction = self.direction
        while True:
            position = self.position.getNewPosition(direction, self.speed)
            if self.room.isPositionInRoom(position):
                self.position = position
                self.direction = direction
                break
            else:
                direction = random.choice(self.angles)
        self.room.cleanTileAtPosition(self.position)

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)

# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    trialSteps = []
    for i in range(num_trials):
        #trial initialization
        room = RectangularRoom(width, height)
        robots = []
        for j in range(num_robots):
            robots.append(robot_type(room, speed))

        # cleanup initialization
        steps, roomCleaned = 0, False
        while not roomCleaned:
            steps += 1
            for robot in robots:
                robot.updatePositionAndClean()
                coverage = ((room.getNumCleanedTiles() * 100) / room.getNumTiles()) * .01
                if coverage >= min_coverage:
                    trialSteps.append(steps)
                    roomCleaned = True
                    break
    return round(sum(trialSteps) / float(len(trialSteps)), 2)

# Uncomment this line to see how much your simulation takes on average
# print 'StandardRobot simulation'
# print  runSimulation(1, 1.0, 5, 5, 1.0, 30, StandardRobot)
# print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)
# print  runSimulation(1, 1.0, 10, 10, 0.9, 30, StandardRobot)
# print  runSimulation(1, 1.0, 20, 20, 1.0, 30, StandardRobot)
# print  runSimulation(3, 1.0, 20, 20, 1.0, 30, StandardRobot)

# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        while True:
            direction = random.choice(self.angles)
            position = self.position.getNewPosition(direction, self.speed)
            if self.room.isPositionInRoom(position):
                self.position = position
                self.direction = direction
                break
        self.room.cleanTileAtPosition(self.position)

# Uncomment this line to see how much your simulation takes on average
# print 'RandomWalkRobot simulation'
# print  runSimulation(1, 1.0, 5, 5, 1.0, 30, RandomWalkRobot)
# print  runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot)
# print  runSimulation(1, 1.0, 10, 10, 0.9, 30, RandomWalkRobot)
# print  runSimulation(1, 1.0, 20, 20, 1.0, 30, RandomWalkRobot)
# print  runSimulation(3, 1.0, 20, 20, 1.0, 30, RandomWalkRobot)
# testRobotMovement(RandomWalkRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room', \
#            "Number of Robots", "Time-steps")

# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
showPlot2('Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms', \
            'Aspect Ratio', ' Time-steps')

# ==== Tests
import unittest

class PS2TestCase(unittest.TestCase):

    def testNewObjectIsCreatedCorrectly(self):
        room = RectangularRoom(5, 5)
        self.assertEqual(room.width, 5)
        self.assertEqual(room.height, 5)
        self.assertEqual(len(room.tiles), 5)
        for i in range(len(room.tiles)):
            self.assertEqual(len(room.tiles[i]), 5)
        for i in range(room.height):
            for j in range(room.width):
                self.assertEqual(room.tiles[i][j], 0)

    def testTileMutation(self):
        room = RectangularRoom(5, 10)
        self.assertEqual(room.getNumTiles(), 50)
        #clean 2, 2
        pos = Position(2, 2)
        room.cleanTileAtPosition(pos)
        self.assertEqual(room.getNumCleanedTiles(), 1)
        self.assertEqual(room.isTileCleaned(2, 2), True)
        #clean 3, 4
        pos = Position(3, 4)
        room.cleanTileAtPosition(pos)
        self.assertEqual(room.getNumCleanedTiles(), 2)
        self.assertEqual(room.isTileCleaned(3, 4), True)
        #clean 1, 4
        pos = Position(1, 4)
        room.cleanTileAtPosition(pos)
        self.assertEqual(room.getNumCleanedTiles(), 3)
        self.assertEqual(room.isTileCleaned(1, 4), True)
        #clean 4, 10
        pos = Position(4, 9)
        room.cleanTileAtPosition(pos)
        self.assertEqual(room.getNumCleanedTiles(), 4)
        self.assertEqual(room.isTileCleaned(4, 9), True)

    def testPositionsInRoom(self):
        room = RectangularRoom(3, 6)
        for i in range(3):
            for j in range(6):
                pos = Position(i, j)
                self.assertEqual(room.isPositionInRoom(pos), True)

        #boundaries
        pos = Position(-1, 0)
        self.assertEqual(room.isPositionInRoom(pos), False)
        pos = Position(0, -1)
        self.assertEqual(room.isPositionInRoom(pos), False)
        pos = Position(-1, -1)
        self.assertEqual(room.isPositionInRoom(pos), False)
        pos = Position(3, 6)
        self.assertEqual(room.isPositionInRoom(pos), False)

    def testPositionsInRoom(self):
        random.seed(1)
        room = RectangularRoom(3, 6)
        pos = room.getRandomPosition()
        self.assertEqual(pos.getX(), .0)
        self.assertEqual(pos.getY(), 5)

    def testRobotCreation(self):
        room = RectangularRoom(3, 6)
        robot = Robot(room, 1)
        self.assertNotEqual(robot.getRobotPosition(), None)
        self.assertNotEqual(robot.getRobotDirection(), None)
        self.assertEqual(robot.room, room)
        self.assertEqual(robot.speed, 1)

# if __name__ == '__main__':
#     unittest.main()
