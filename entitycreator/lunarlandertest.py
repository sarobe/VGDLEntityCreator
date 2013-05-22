import random
from vgdl.core import VGDLParser


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BASEDIRS = [UP, LEFT, DOWN, RIGHT]

gravity = 0.5

REPEATS = 1
ACTIONS = 5

ended = False
win = False


def runLunarLander():
    # import lunar lander
    from vgdl.examples.continuousphysics.lander import lander_game, lander_level

    # build the game
    g = VGDLParser().parseGame(lander_game)
    g.buildLevel(lander_level)

    # TODO: Determine how to not need to bring up the pygame display in order to run the game.
    g._initScreen([1, 1])

    ship = g.getAvatars()[0]

    # store initial ship state
    initState = [ship.rect.x, ship.rect.y, ship.speed, ship.orientation]

    print "starting position: " + str(ship)
    print "starting state: " + str(initState)
    # get random actions
    actions = generateInput(ACTIONS)

    states = [initState]
    # move ship based on random actions
    print actions
    for a in actions:
        for i in range(REPEATS):
            ship.action = a
            updateGame(g, a)
            if ended:
                print a, i
                break
        states.append(makeState(ship))

    endState = states[len(states)-1]

    # confirm final position
    print "first final position after actions: " + str(ship)
    print "final state: " + str(endState)

    # reroll ship back to initial state
    setState(ship, initState)

    # vary action sequence
    # first pick a point to vary
    random.seed(10466)
    varyIndex = random.randint(0, len(actions) - 1)

    # then change that action
    oldAction = actions[varyIndex]
    actions[varyIndex] = BASEDIRS[random.randint(0, len(BASEDIRS) - 1)]

    # print out the change and the full list of actions
    print "changed action " + str(varyIndex) + " to " + str(actions[varyIndex])
    print "new actions: " + str(actions)

    # predict through simple calculation how the final position should be
    predictState = predictOutcome(states, actions, oldAction, varyIndex)
    print "predicted state " + str(predictState)

    # find out where the actual final position is
    for a in actions:
        for i in range(REPEATS):
            updateGame(g, a)
            if ended:
                print a, i
                break

    endState = makeState(ship)
    print "actual ending position: " + str(ship)
    print "ending state: " + str(endState)

    # get error
    error = [endState[0] - predictState[0], endState[1] - predictState[1]]
    print "prediction error: " + str(error)


def predictOutcome(states, actions, oldAction, newActionIndex):
    # determine the effective change in action
    newAction = actions[newActionIndex]
    changedAction = [newAction[0] - oldAction[0], newAction[1] - oldAction[1]]

    # try one! adjust position only without compensating for velocity!
    # endState = states[len(states)-1]
    # finalX = endState[0] + (changedAction[0] * REPEATS)
    # finalY = endState[1] + (changedAction[1] * REPEATS)
    # didn't work, unsurprisingly

    # try two! compensate for velocity!
    endState = states[len(states)-1]

    stateOfChange = states[newActionIndex]
    velocityBeforeChange = [stateOfChange[2] * stateOfChange[3][0], stateOfChange[2] * stateOfChange[3][1]]
    velocityCausedByChange = [changedAction[0] * REPEATS, changedAction[1] * REPEATS]
    changedVelocity = [velocityBeforeChange[0] + velocityCausedByChange[0],
                       velocityBeforeChange[1] + velocityCausedByChange[1]]

    # compensate for gravity
    changedVelocity[1] += gravity * REPEATS

    # calculate the ending impact this has on the position after this action
    diffX = changedVelocity[0]
    diffY = changedVelocity[1]

    finalX = endState[0] + diffX
    finalY = endState[1] + diffY

    return [finalX, finalY]


def makeState(ship):
    return [ship.rect.x, ship.rect.y, ship.speed, ship.orientation]


def setState(ship, state):
    ship.rect.x = state[0]
    ship.rect.y = state[1]
    ship.speed = state[2]
    ship.orientation = state[3]


def generateInput(totalActions):
    random.seed(1234)
    actions = []
    for i in range(totalActions):
        actions.append(BASEDIRS[random.randint(0, len(BASEDIRS) - 1)])

    return actions


def setKeystate(game, action):
    from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

    # an incredible kludge that makes me somewhat ashamed
    keystate = [False] * 350

    if action == RIGHT:
        keystate[K_RIGHT] = True
    elif action == LEFT:
        keystate[K_LEFT] = True
    if action == UP:
        keystate[K_UP] = True
    elif action == DOWN:
        keystate[K_DOWN] = True

    return keystate

def updateGame(game, action):
    game.keystate = setKeystate(game, action)
    setKeystate(game, action)
    # termination criteria
    for t in game.terminations:
        ended, win = t.isDone(game)
        if ended:
            break
        # update sprites
    for s in game:
        s.update(game)
        # handle collision effects
    game._updateCollisionDict()
    game._eventHandling()


if __name__ == '__main__':
    runLunarLander()