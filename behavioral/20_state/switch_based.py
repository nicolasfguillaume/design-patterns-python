# instead of using a set of rule in a dictionary to determine the state transition, 
# we can use a switch statement (if/then)
# we are not storing the transitions, only storing the state

from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()


if __name__ == '__main__':
    code = '1234'
    # starting state
    state = State.LOCKED
    # stores the current entry (single digit entered by the user)
    entry = ''

    while True:
        if state == State.LOCKED:
            # get user input
            entry += input(entry)

            if entry == code:
                state = State.UNLOCKED

            if not code.startswith(entry):
                # the code is wrong
                state = State.FAILED
        
        elif state == State.FAILED:
            print('\nFAILED')
            entry = ''
            state = State.LOCKED
        
        elif state == State.UNLOCKED:
            print('\nUNLOCKED')
            break
