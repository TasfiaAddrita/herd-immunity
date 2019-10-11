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

        self.total_infected = 0 
        self.total_dead = 0 
        self.current_infected = []
        self.newly_infected = []
        self.new_population = []
        self.total_vaccinated = 0

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(self.virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)

    def _create_population(self):
        _id = 1
        total_vaccinated_population = math.ceil(self.vacc_percentage * self.pop_size)

        for _ in range(self.pop_size):
            # person is infected
            if _id <= self.initial_infected:
                # infect person
                infected = Person(_id, False, self.virus)
                # add infected person to population
                self.population.append(infected)
                # add infected person to list of infected people
                self.current_infected.append(infected)
                self.total_infected += 1
                assert infected.is_alive == True
                assert infected.infection == self.virus
            # person not infected
            else:
                # person vaccinated
                if self.total_vaccinated <= total_vaccinated_population:
                    vaccinated = Person(_id, True)
                    self.population.append(vaccinated)
                    self.total_vaccinated += 1
                    assert vaccinated.is_vaccinated == True
                    assert vaccinated.infection == None
                # person unvaccinated
                else:
                    unvaccinated = Person(_id, False)
                    self.population.append(unvaccinated)
                    assert unvaccinated.is_vaccinated == False
                    assert unvaccinated.infection == None
            _id += 1

        # for person in self.population:
        #     print(person._id, person.is_vaccinated, person.infection)
        # print(self.total_vaccinated)
        # print(self.total_infected)

        # population contains vaccinated, unvaccinated, alive, dead, virus, and virus-free persons
        # new_population will be modified to remove dead persons
        self.new_population = self.population[:]
        return self.new_population

    def remove_dead_from_new_pop(self):
        for person in self.new_population:
            if person.is_alive == False:
                self.new_population.remove(person)

    def _simulation_should_continue(self):
        # total_vaccinated = 0
        # total_unvaccinated = 0
        # for person in self.new_population:
        #     if person.is_alive and person.is_vaccinated:
        #         total_vaccinated += 1
        #     else:
        #         total_unvaccinated += 1

        if (self.total_dead == len(self.new_population)) or (self.total_vaccinated == self.pop_size):
            return False
        return True

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        infected = False

        # check un-vaccinated AND virus-free person
        if random_person.is_vaccinated == False and random_person.infection == None:
            infected_chance = random.randint(0, 100) 
            # infected_chance = random.random()
            # person is infected if result less than virus's repro rate 
            if infected_chance <= self.virus.repro_rate * 100:
                infected = True
            # person is vaccinated if result more than virus's repro rate, 
            else:
                print("person is not infected")
        # check alive person with virus (automatically unvaccinated), infected is True
        elif random_person.infection != None and random_person.is_alive == True:
            print("alive person with virus")
            infected = True
            assert random_person.is_alive == True
            assert random_person.infection == self.virus
        # check if person is vaccinated, infected will remain False
        elif random_person.is_vaccinated == True:
            print("vaccinated person")
            assert random_person.is_alive == True
            assert random_person.is_vaccinated == True
            assert random_person.infection == None
        else:
            print("Error")
        
        self.logger.log_interaction(person, random_person)
        return infected
            

    def _infect_newly_infected(self):
        for infected_person in self.newly_infected:
            print(infected_person._id, infected_person.infection, infected_person.is_vaccinated)
            infected_person.infection = self.virus

            # self.current_infected.append(infected_person)
        # self.current_infected.pop(len(self.current_infected) - 1)
        self.newly_infected = []

    def time_step(self):
        interactions = 0
        time_step_infected = 0
        time_step_dead = 0

        # choose 100 random persons and interact with them
        while interactions < 100:
            for infected_person in self.current_infected: # line 36 for append
                # generate random alive person from new population
                random_index = random.randint(0, len(self.new_population) - 1) # randint is inclusive
                random_person = self.new_population[random_index]
                while (random_person.is_alive != True):
                    random_person = self.new_population[random_index]
                infected = self.interaction(infected_person, random_person)
                if infected == True:
                    self.newly_infected.append(random_person)
                    self.total_infected += 1
                    time_step_infected += 1
                else:
                    random_person.is_vaccinated = True
                    random_person.infection = None
                interactions += 1
            if interactions == 100:
                break
        
        self._infect_newly_infected()

        # infected person will either survive + vaccinate or die, both cases virus is removed
        for infected_person in self.current_infected:
            # print(infected_person._id, infected_person.infection, infected_person.is_vaccinated)
            survive = infected_person.did_survive_infection()
            if survive:
                self.total_vaccinated += 1
                assert infected_person.is_vaccinated == True
            else:
                self.total_dead += 1
                time_step_dead += 1
                self.pop_size -= 1
                # self.current_infected.remove(infected_person)
                assert infected_person.is_alive == False
            # print(infected_person.infection)
            assert infected_person.infection == None
            self.current_infected.remove(infected_person)
            self.logger.log_infection_survival(infected_person)
        
        return [time_step_infected, self.total_infected, time_step_dead, self.total_dead]
                
    def run(self):
        self._create_population()
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate, self.initial_infected)
        time_step_counter = 1
        should_continue = True
        while should_continue:
            self.logger.log_time_step_start(time_step_counter)
            stats = self.time_step()
            self.logger.log_time_step_stats(stats)
            time_step_counter += 1
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')
        # print('run function')

def main():
    random.seed(time.time())
    virus = Virus('Ebola', 0.25, 0.70)
    sim = Simulation(100, 0.50, virus, 10)
    # sim._create_population()
    sim.run()

if __name__ == "__main__":
    main()

    # params = sys.argv[1:]
    # virus_name = str(params[2])
    # repro_num = float(params[4])
    # mortality_rate = float(params[3])

    # pop_size = int(params[0])
    # vacc_percentage = float(params[1])

    # if len(params) == 6:
    #     initial_infected = int(params[5])
    # else:
    #     initial_infected = 1
    
    # virus = Virus(virus_name, repro_num, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)
    # sim.run()