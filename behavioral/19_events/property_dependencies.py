class Event(list):
  def __call__(self, *args, **kwargs):
    for item in self:
      item(*args, **kwargs)


class PropertyObservable:
  def __init__(self):
    # event for when a property changes
    self.property_changed = Event()


class Person(PropertyObservable):
  def __init__(self, age=0):
    super().__init__()
    self._age = age

  # this property is dependent on the age property
  @property
  def can_vote(self):
    return self._age >= 18

  @property
  def age(self):
    return self._age

  @age.setter
  def age(self, value):
    if self._age == value:
      return

    # we need to cache the can_vote property
    old_can_vote = self.can_vote

    self._age = value
    # this fires the property_changed event
    self.property_changed('age', value)

    # if the can_vote property has changed, we fire the property_changed event
    if old_can_vote != self.can_vote:
      self.property_changed('can_vote', self.can_vote)


if __name__ == '__main__':
  # define a subscriber
  def person_changed(name, value):
    if name == 'can_vote':
      print(f'Voting status changed to {value}')

  p = Person()
  # add the subscriber to the property_changed event
  p.property_changed.append(
    person_changed
  )

  for age in range(16, 21):
    print(f'Changing age to {age}')
    p.age = age