# Proxy Coding Exercise

# You are given the Person  class and asked to write a ResponsiblePerson  proxy that does the following:

# Allows person to drink unless they are younger than 18 (in that case, return "too young")

# Allows person to drive unless they are younger than 16 (otherwise, "too young")

# In case of driving while drink, returns "dead", regardless of age

class Person:
  def __init__(self, age):
    self.age = age

  def drink(self):
    return 'drinking'

  def drive(self):
    return 'driving'

  def drink_and_drive(self):
    return 'driving while drunk'

class ResponsiblePerson:
  def __init__(self, person: Person):
    # internal attribute that should not be accessed directly
    self._person = person

  @property
  def age(self):
    return self._person.age

  @age.setter
  def age(self, value):
    self._person.age = value

  def drink(self):
    if self.age >= 18:
      return self._person.drink()
    else:
      return 'too young'

  def drive(self):
    if self.age >= 16:
      return self._person.drive()
    else:
      return 'too young'

  def drink_and_drive(self):
      return 'dead'

if __name__ == '__main__':
  p = Person(10)
  rp = ResponsiblePerson(p)

  print(rp.drive())
  print(rp.drink())
  print(rp.drink_and_drive())

  # internal attribute should not be accessed directly
  # rp._person.age = 20
  rp.age = 20

  print(rp.drive())
  print(rp.drink())
  print(rp.drink_and_drive())
