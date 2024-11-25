# Composite Command a.k.a. Macro
# also: Composite design pattern ;)

import unittest
from abc import ABC, abstractmethod
from enum import Enum


class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'Deposited {amount}, balance = {self.balance}')

    def withdraw(self, amount):
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f'Withdrew {amount}, balance = {self.balance}')
            return True
        return False

    def __str__(self):
        return f'Balance = {self.balance}'


class Command(ABC):
    def __init__(self):
        # the success flag is now in the Command base class
        self.success = False

    def invoke(self):
        pass

    def undo(self):
        pass


class BankAccountCommand(Command):
    def __init__(self, account, action, amount):
        super().__init__()  # initialize the success flag
        self.amount = amount
        self.action = action
        self.account = account

    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True
        elif self.action == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        if not self.success:
            return
        # strictly speaking this is not correct
        # (you don't undo a deposit by withdrawing)
        # but it works for this demo, so...
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)


# A composite command is a command but also a list of several commands (aka macro)
class CompositeBankAccountCommand(Command, list):
    def __init__(self, items=[]):
        # __init__ of class Command is called first (if it exists)
        super().__init__()
        # add all the commands to ourselves
        for i in items:
            self.append(i)

    def invoke(self):
        # invoke all the commands in order
        for x in self:
            x.invoke()

    def undo(self):
        # undo all the commands in reverse order
        for x in reversed(self):
            x.undo()


class MoneyTransferCommand(CompositeBankAccountCommand):
    def __init__(self, from_acct, to_acct, amount):
        super().__init__([
            BankAccountCommand(from_acct,
                               BankAccountCommand.Action.WITHDRAW,
                               amount),
            BankAccountCommand(to_acct,
                               BankAccountCommand.Action.DEPOSIT,
                               amount)])

    def invoke(self):
        ok = True  # flag to check if the previous operation was successful
        for cmd in self:
            if ok:
                cmd.invoke()
                ok = cmd.success
            else:
                # we don't invoke the command, because the previous one failed
                # we only mark the command as failed
                cmd.success = False
        # we need to save the status (success or failure) of the composite command
        self.success = ok


class TestSuite(unittest.TestCase):
    def test_composite_deposit(self):
        ba = BankAccount()
        deposit1 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 1000)
        deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 1000)
        composite = CompositeBankAccountCommand([deposit1, deposit2])
        composite.invoke()
        print(ba)
        composite.undo()
        print(ba)

    def test_transfer_fail(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()

        # composite isn't so good because of failure
        amount = 1000  # try 1000: no transactions should happen
        wc = BankAccountCommand(ba1, BankAccountCommand.Action.WITHDRAW, amount)
        dc = BankAccountCommand(ba2, BankAccountCommand.Action.DEPOSIT, amount)

        transfer = CompositeBankAccountCommand([wc, dc])

        transfer.invoke()
        print('ba1:', ba1, 'ba2:', ba2)  # end up in incorrect state
        transfer.undo()
        print('ba1:', ba1, 'ba2:', ba2)

    def test_better_tranfer(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()

        amount = 1000

        transfer = MoneyTransferCommand(ba1, ba2, amount)
        transfer.invoke()
        print('ba1:', ba1, 'ba2:', ba2)
        transfer.undo()
        print('ba1:', ba1, 'ba2:', ba2)
        print(transfer.success)


if __name__ == '__main__':
    unittest.main(exit=False)
