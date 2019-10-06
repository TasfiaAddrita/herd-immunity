import random
random.seed(42)
from virus import Virus


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        self._id = None  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = None  # boolean
        self.infection = None  # Virus object or None

    def did_survive_infection(self):
        pass

''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None

def test_not_vacc_person_instantiation():
    person = Person(2, False)
    pass

def test_sick_person_instantiation():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(3, False, virus)
    pass

def test_did_survive_infection():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(4, False, virus)

    survived = person.did_survive_infection()
    if survived:
        assert person.is_alive is True
        pass
    else:
        assert person.is_alive is False
        pass
