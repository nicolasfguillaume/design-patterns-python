class Event(list):
  def __call__(self, *args, **kwargs):
    for item in self:
      item(*args, **kwargs)


# a class can inherit from this class and thereby get a property changed event
class PropertyObservable:
  def __init__(self):
    # event for when a property changes
    self.property_changed = Event()


class Person(PropertyObservable):
  def __init__(self, age=0):
    super().__init__()
    # setting the inner age
    self._age = age

  @property
  def age(self):
    return self._age

  @age.setter
  def age(self, value):
    if self._age == value:
      return
    self._age = value
    # this fires the event
    self.property_changed('age', value)


class TrafficAuthority:
  def __init__(self, person):
    self.person = person
    # add a new subscriber (self.person_changed) to the person.property_changed event
    person.property_changed.append(self.person_changed)

  def person_changed(self, name, value):
    # if the name of the property that was changed is age
    if name == 'age':
      if value < 16:
        print('Sorry, you still cannot drive')
      else:
        print('Okay, you can drive now')
        # unsubscribe from the person.property_changed event
        self.person.property_changed.remove(
          self.person_changed
        )


if __name__ == '__main__':
  p = Person()
  ta = TrafficAuthority(p)
  for age in range(14, 20):
    print(f'Setting age to {age}')
    p.age = age