import random, sys, math
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
        self.current_infected = []
        self.total_infected = 0 
        self.total_dead = 0 
        self.newly_infected = []

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(self.virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)

    def _create_population(self):
        _id = 1
        total_vaccinated_population = math.ceil(self.vacc_percentage * self.pop_size)
        vaccinated_pop = 0

        for _ in range(self.pop_size):
            if _id <= self.initial_infected:
                infected = Person(_id, False, self.virus)
                self.population.append(infected)
                self.current_infected.append(infected)
            else:
                if vaccinated_pop <= total_vaccinated_population:
                    self.population.append(Person(_id, True))
                    vaccinated_pop += 1
                else:
                    self.population.append(Person(_id, False))
            _id += 1

        # print('create population ran')
        return self.population

    def _simulation_should_continue(self):
        total_vaccinated = 0
        for person in self.population:
            if person.is_alive:
                total_vaccinated += 1

        # print('simulation should continue ran')

        if (self.total_dead == self.pop_size) or (total_vaccinated == self.pop_size):
            return False
        return True

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        # is_infected = False

        if random_person.is_vaccinated:
            return False # replace with logger method
            # pass
        elif random_person.infection != None:
            return False
            # pass
        else:
            infected_chance = random.randint(0, 100) 
            if infected_chance <= self.virus.repro_rate * 100:
                random_person.infection = self.virus
            # is_infected = True
            return True

        # print('interaction ran')
        self.logger.log_interaction(person, random_person)
        # return is_infected

    def _infect_newly_infected(self):
        # print(self.newly_infected)
        for person in self.newly_infected:
            person.infection = self.virus
            if person.did_survive_infection() == False:
                self.total_dead += 1
            self.logger.log_infection_survival(person)
        self.current_infected = self.newly_infected
        self.newly_infected = []
        # print('newly infected function')

    def time_step(self):
        interactions = 0
        interactions_limit = 10
        while interactions < interactions_limit:

            # # picks random person
            # random_person = self.population[random.randint(0, len(self.population) - 1)]
            # while (random_person.is_alive == False):
            #     random_person = self.population[random.randint(0, len(self.population) - 1)]

            # infected interacts with random person
            for infected_person in self.current_infected:

                # picks random person
                random_person = self.population[random.randint(0, len(self.population) - 1)]
                while (random_person.is_alive == False):
                    random_person = self.population[random.randint(0, len(self.population) - 1)]

                # print(self.interaction(infected_person, random_person))
                if self.interaction(infected_person, random_person):
                    self.newly_infected.append(infected_person)
                    # self._infect_newly_infected()

                    # if random_person.did_survive_infection() == False:
                    #     self.total_dead += 1
                
                    # self.logger.log_infection_survival(random_person)

                # print('time step function')

                interactions += 1
                # print(interactions)
                if interactions == interactions_limit:
                    break
        self._infect_newly_infected()
                
    def run(self):
        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()

        # print(f'The simulation has ended after {time_step_counter} turns.')
        # print('run function')

def main():
    virus = Virus('Ebola', 0.25, 0.70)
    sim = Simulation(100, 0.50, virus, 10)
    sim._create_population()

    # for person in sim.population:
        # print(person._id, "vaccinated:", person.is_vaccinated, ',', "infected:", person.infection)
    
    # for infected in sim.newly_infected:
    #     print(infected._id)
    sim.run()

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

    main()
