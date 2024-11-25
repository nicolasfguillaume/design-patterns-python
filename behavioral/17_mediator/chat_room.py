class Person:
    def __init__(self, name):
        self.name = name
        self.chat_log = []
        self.room = None

    # person receives a message
    def receive(self, sender, message):
        s = f'{sender}: {message}'
        print(f'[{self.name}\'s chat session] {s}')
        self.chat_log.append(s)

    # person sends a message to the room
    def say(self, message):
        self.room.broadcast(self.name, message)

    # person sends a private message to another person in the room
    def private_message(self, who, message):
        self.room.message(self.name, who, message)


# central mediator, to connect several people together, and let them send messages to each other
class ChatRoom:
    def __init__(self):
        self.people = []

    # broadcast a message to everyone in the room, except to the source
    def broadcast(self, source, message):
        for p in self.people:
            if p.name != source:
                p.receive(source, message)

    # join a person to the room
    def join(self, person):
        join_msg = f'{person.name} joins the chat'
        self.broadcast('room', join_msg)
        person.room = self
        self.people.append(person)

    # send a message to a specific person in the room
    def message(self, source, destination, message):
        for p in self.people:
            if p.name == destination:
                p.receive(source, message)


if __name__ == '__main__':
    room = ChatRoom()

    john = Person('John')
    jane = Person('Jane')

    room.join(john)
    room.join(jane)

    john.say('hi room')
    jane.say('oh, hey john')

    simon = Person('Simon')
    room.join(simon)
    simon.say('hi everyone!')

    jane.private_message('Simon', 'glad you could join us!')