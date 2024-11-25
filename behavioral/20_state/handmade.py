from enum import Enum, auto

# states that the phone can be in
class State(Enum):
    OFF_HOOK = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    ON_HOLD = auto()
    ON_HOOK = auto()


# triggers are the events that cause the state to transition
class Trigger(Enum):
    CALL_DIALED = auto()
    HUNG_UP = auto()
    CALL_CONNECTED = auto()
    PLACED_ON_HOLD = auto()
    TAKEN_OFF_HOLD = auto()
    LEFT_MESSAGE = auto()


if __name__ == '__main__':
    # rules for the state machine
    rules = {
        # from this state
        State.OFF_HOOK: [
            # if this trigger occurs, go to this state
            (Trigger.CALL_DIALED, State.CONNECTING)
        ],
        State.CONNECTING: [
            (Trigger.HUNG_UP, State.ON_HOOK),
            (Trigger.CALL_CONNECTED, State.CONNECTED)
        ],
        State.CONNECTED: [
            (Trigger.LEFT_MESSAGE, State.ON_HOOK),
            (Trigger.HUNG_UP, State.ON_HOOK),
            (Trigger.PLACED_ON_HOLD, State.ON_HOLD)
        ],
        State.ON_HOLD: [
            (Trigger.TAKEN_OFF_HOLD, State.CONNECTED),
            (Trigger.HUNG_UP, State.ON_HOOK)
        ]
    }

    # start and end states, for modeling a simple phone call
    state = State.OFF_HOOK
    exit_state = State.ON_HOOK  # might not be necessary, depending on use case

    while state != exit_state:
        print(f'The phone is currently {state}')

        # for each rule in the current state
        for i in range(len(rules[state])):
            trigger = rules[state][i][0]
            print(f'{i}: {trigger}')

        idx = int(input('Select a trigger:'))
        # state transition (state we are going to)
        s = rules[state][idx][1]
        state = s

    print('We are done using the phone.')