import random, sys, math, time
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
        self.total_infected = 0 
        self.total_dead = 0 
        self.current_infected = []
        self.newly_infected = []
        self.new_population = []

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

        self.new_population = self.population[:]
        return self.new_population

    def _simulation_should_continue(self):
        total_vaccinated = 0
        total_unvaccinated = 0
        for person in self.new_population:
            # print("vac people", person._id)
        # return
            if person.is_alive and person.is_vaccinated:
                total_vaccinated += 1
            else:
                total_unvaccinated += 1

        if (self.total_dead == len(self.population)) or (total_vaccinated == self.pop_size):
            return False
        return True

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        self.logger.log_interaction(person, random_person)

        can_be_infected = False

        if random_person.is_vaccinated:
            can_be_infected = False
        elif random_person.infection != None:
            can_be_infected = False
            if random_person.did_survive_infection() == False:
                self.total_dead += 1
                self.pop_size -= 1
                random_person.virus = None
                self.new_population.remove(random_person)
                self.current_infected.remove(random_person)
            self.logger.log_infection_survival(random_person)
        else:
            infected_chance = random.randint(0, 100) 
            if infected_chance <= self.virus.repro_rate * 100:
                random_person.infection = self.virus
            can_be_infected = True

        return can_be_infected

    # def _infect_newly_infected(self):
        # print(self.newly_infected)
        # for person in self.newly_infected:
        #     person.infection = self.virus
        # self.current_infected = self.newly_infected
        # self.newly_infected = []
        # print("infected_newly running")
        # print('newly infected function')

    def time_step(self):
        interactions = 0
        interactions_limit = 10

        while interactions < interactions_limit:
            # if len(self.current_infected) == 0:
            #     break

            # infected interacts with random person
            for infected_person in self.current_infected:
                repro_pop = 0
                # picks random person
                random_index = random.randint(0, len(self.new_population) - 1)
                random_person = self.new_population[random_index]
                while (random_person.is_alive == False):
                    random_person = self.new_population[random_index]

                # interaction occurs
                if self.interaction(infected_person, random_person):
                    random_person.infection = self.virus
                    repro_pop += 1
                    if random_person.did_survive_infection() == False:
                        self.total_dead += 1
                        self.pop_size -= 1
                        random_person.virus = None
                        
                        self.new_population.remove(random_person)
                    else:
                        self.current_infected.append(random_person)
                    self.logger.log_infection_survival(random_person)
                else:
                    random_person.is_vaccinated = True

                interactions += 1
                # if interactions == interactions_limit:
                #     break
                
    def run(self):
        self._create_population()
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate, self.initial_infected)
        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()
            if should_continue:
                self.logger.log_time_step(time_step_counter)

        print(f'The simulation has ended after {time_step_counter} turns.')

def main():
    random.seed(time.time())
    virus = Virus('Ebola', 0.25, 0.70)
    sim = Simulation(50, 0.50, virus, 5)
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
