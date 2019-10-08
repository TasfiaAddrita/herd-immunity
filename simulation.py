import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        self.population = [] 
        self.pop_size = pop_size 
        self.vacc_percentage = vacc_percentage 
        self.virus = virus 
        self.initial_infected = initial_infected 

        self.next_person_id = 0 
        self.current_infected = self.initial_infected
        self.total_infected = 0 
        self.total_dead = 0 
        self.newly_infected = []

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(self.virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)

    def _create_population(self):
        _id = 1
        for _ in range(self.pop_size):
            if _id <= self.initial_infected:
                self.population.append(Person(_id, False, self.virus))
            else:
                self.population.append(Person(_id, True))
            _id += 1

        return self.population

    def _simulation_should_continue(self):
        total_vaccinated = 0
        for person in self.population:
            if person.is_alive:
                total_vaccinated += 1

        if (self.total_dead == self.pop_size) or (total_vaccinated == self.pop_size):
            return False
        return True

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated: 
            return False # replace with logger method
        elif random_person.infection != None:
            return False
        else:
            print("Something happens")
            infected_chance = random.randint(0, 100) 
            if infected_chance <= self.virus.repro_rate * 100:
                random_person.infection = self.virus
            return True

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infected = self.virus
        self.newly_infected = []

    def time_step(self):
        interactions = 0

        random_person = self.population[random.randint(0, len(self.population) - 1)]
        while (random_person.is_alive == False):
            random_person = self.population[random.randint(0, len(self.population) - 1)]

        while interactions < 100:
            for infected_person in self.newly_infected:
                if self.interaction(infected_person, random_person):
                    self.newly_infected.append(infected_person._id)
                    self._infect_newly_infected()
            interactions += 1

    def run(self):
        time_step_counter = 0
        should_continue = None

        while should_continue:
            pass

        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))
        pass

if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])

    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])

    # if len(params) == 6:
    #     initial_infected = int(params[5])
    # else:
    #     initial_infected = 1

    # virus = Virus(virus_name, repro_num, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    virus = Virus('Ebola', 0.25, 0.70)
    sim = Simulation(20, 0.90, virus, 10)
    sim._create_population()
    # sim.run()
