---
title: "Project: A Small Bank"
slug: project
summary: Use classes, inheritance, encapsulation, polymorphism and special methods to build a bank.
minutes: 14
---
## The plan

We will build a bank with two kinds of accounts:

- **Account** - deposit, withdraw (never below zero), and a history of transactions.
- **SavingsAccount** - an account that also earns interest and allows only 3 withdrawals.
- **Bank** - holds the accounts, finds them by number and reports the total.

## Step 1: the Account class

```python tryit
class Account:
    def __init__(self, number, owner):
        self.number = number
        self.owner = owner
        self._balance = 0
        self.history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Not enough money")
        self._balance -= amount
        self.history.append(("withdraw", amount))

    def __str__(self):
        return f"#{self.number} {self.owner}: {self._balance:.2f}"

acc = Account(1, "Ana")
acc.deposit(200)
acc.withdraw(50)
print(acc)
print(acc.history)
```

`balance` is a read-only property: the only way to change it is through `deposit` and `withdraw`. That is encapsulation.

## Step 2: a savings account

```python tryit
class Account:
    def __init__(self, number, owner):
        self.number, self.owner = number, owner
        self._balance = 0
        self.history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Not enough money")
        self._balance -= amount
        self.history.append(("withdraw", amount))

    def month_end(self):
        pass                     # normal accounts do nothing

    def __str__(self):
        return f"#{self.number} {self.owner}: {self._balance:.2f}"

class SavingsAccount(Account):
    def __init__(self, number, owner, rate):
        super().__init__(number, owner)
        self.rate = rate

    def withdraw(self, amount):
        taken = sum(1 for kind, _ in self.history if kind == "withdraw")
        if taken >= 3:
            raise ValueError("Only 3 withdrawals allowed")
        super().withdraw(amount)

    def month_end(self):         # polymorphism: same name, different job
        interest = round(self._balance * self.rate, 2)
        self.deposit(interest)

s = SavingsAccount(2, "Ben", 0.01)
s.deposit(1000)
s.month_end()
print(s)
for _ in range(4):
    try:
        s.withdraw(10)
    except ValueError as error:
        print(error)
```

## Step 3: the bank

The bank does not care which kind of account it holds: it calls `month_end()` on all of them.

```python tryit
class Account:
    def __init__(self, number, owner):
        self.number, self.owner = number, owner
        self._balance = 0

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount

    def month_end(self):
        pass

class SavingsAccount(Account):
    def __init__(self, number, owner, rate):
        super().__init__(number, owner)
        self.rate = rate

    def month_end(self):
        self.deposit(round(self._balance * self.rate, 2))

class Bank:
    def __init__(self, name):
        self.name = name
        self._accounts = {}

    def open(self, account):
        self._accounts[account.number] = account

    def find(self, number):
        return self._accounts[number]

    def month_end(self):
        for account in self._accounts.values():
            account.month_end()

    def __len__(self):
        return len(self._accounts)

    def total(self):
        return sum(a.balance for a in self._accounts.values())

bank = Bank("Ainolez Bank")
bank.open(Account(1, "Ana"))
bank.open(SavingsAccount(2, "Ben", 0.02))
bank.find(1).deposit(300)
bank.find(2).deposit(500)
bank.month_end()
print(len(bank), "accounts, total", bank.total())
```

## Ideas to try

- Add a `transfer(from_number, to_number, amount)` method to `Bank`.
- Add `__lt__` to `Account` so `sorted()` orders accounts by balance.
- Add a `CheckingAccount` that allows an overdraft down to -100.

```exercise
{
  "title": "Transfer money",
  "prompt_md": "Add a `transfer(source, target, amount)` method to `Bank` that withdraws from one account and deposits into the other. The code must print `70 130`.",
  "starter_code": "class Account:\n    def __init__(self, balance):\n        self.balance = balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise ValueError(\"Not enough money\")\n        self.balance -= amount\n\n    def deposit(self, amount):\n        self.balance += amount\n\nclass Bank:\n    pass  # write transfer here\n\na, b = Account(100), Account(100)\nBank().transfer(a, b, 30)\nprint(a.balance, b.balance)\n",
  "solution_code": "class Account:\n    def __init__(self, balance):\n        self.balance = balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise ValueError(\"Not enough money\")\n        self.balance -= amount\n\n    def deposit(self, amount):\n        self.balance += amount\n\nclass Bank:\n    def transfer(self, source, target, amount):\n        source.withdraw(amount)\n        target.deposit(amount)\n\na, b = Account(100), Account(100)\nBank().transfer(a, b, 30)\nprint(a.balance, b.balance)\n",
  "check_type": "output",
  "expected_value": "70 130",
  "hint": "def transfer(self, source, target, amount): withdraw first (it may refuse), then deposit."
}
```

```quiz
{
  "title": "Final quiz: Object-Oriented Python",
  "final": true,
  "questions": [
    {"question": "What is an object?", "options": ["A blueprint", "One instance made from a class", "A function"], "answer": 1, "explanation": "A class is the blueprint; an object is one thing made from it."},
    {"question": "What does __init__ do?", "options": ["Deletes an object", "Sets up a new object", "Prints an object"], "answer": 1, "explanation": "It runs when an object is created."},
    {"question": "What is self?", "options": ["The current object", "The parent class", "A global variable"], "answer": 0, "explanation": "self refers to the instance a method is working on."},
    {"question": "How do you call the parent's __init__?", "options": ["parent.__init__()", "super().__init__(...)", "self.__init__()"], "answer": 1, "explanation": "super() gives you the parent class."},
    {"question": "Several classes all have a draw() method and one loop calls draw() on each. This is...", "options": ["encapsulation", "polymorphism", "composition"], "answer": 1, "explanation": "The same call works for different types."},
    {"question": "What does @property let you do?", "options": ["Run a method when an attribute is read", "Make a class attribute", "Inherit from two classes"], "answer": 0, "explanation": "A property looks like an attribute but runs code."},
    {"question": "Which method makes obj1 + obj2 work?", "options": ["__plus__", "__add__", "__sum__"], "answer": 1, "explanation": "+ calls __add__."},
    {"question": "\"A car has an engine\" is an example of...", "options": ["inheritance", "composition", "polymorphism"], "answer": 1, "explanation": "Has-a relationships are composition."}
  ]
}
```
