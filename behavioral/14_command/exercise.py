# Command Coding Exercise

# Implement the Account.process()  method to process different account commands.

# The rules are obvious:
# - success indicates whether the operation was successful
# - you can only withdraw money if you have enough in your account

import unittest
from enum import Enum


class Command:
    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(self, action, amount):
        self.action = action
        self.amount = amount
        self.success = False


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def process(self, command):
        command.success = True

        if command.action == Command.Action.DEPOSIT:
            self.balance += command.amount
            
        elif command.action == Command.Action.WITHDRAW:
            if self.balance >= command.amount:
                self.balance -= command.amount
            else:
                command.success = False


class TestSuite(unittest.TestCase):
    def test_exercise(self):
        acc = Account()

        cmd = Command(Command.Action.DEPOSIT, 100)
        acc.process(cmd)
        self.assertTrue(cmd.success)
        self.assertEqual(100, acc.balance)

        cmd = Command(Command.Action.WITHDRAW, 50)
        acc.process(cmd)
        self.assertTrue(cmd.success)
        self.assertEqual(50, acc.balance)

        cmd = Command(Command.Action.WITHDRAW, 150)
        acc.process(cmd)
        self.assertFalse(cmd.success)
        self.assertEqual(50, acc.balance)

        cmd = Command(Command.Action.DEPOSIT, 100)
        acc.process(cmd)
        self.assertTrue(cmd.success)
        self.assertEqual(150, acc.balance)


if __name__ == '__main__':
    unittest.main(exit=False)
