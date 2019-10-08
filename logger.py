class Logger(object):

    def __init__(self, file_name):
        self.file_name = None

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected):
        f = open(self.file_name, 'w+')
        f.write(
        f'''
        ----------------- META DATA -----------------
        Virus
            Name - {virus_name}
            Mortality - {mortality_rate * 100}%
            Reproduction - {basic_repro_num * 100}%
        
        Population
            Size - {pop_size}
            Vaccinated - {vacc_percentage * 100}%
            Initial infected - {initial_infected}

        '''    
        )
        f.close()

    def log_interaction(self, person, random_person):
        if random_person.is_vaccinated:
            print(f'{person._id did} not infect {random._id} because they are vaccinated.')
        elif random_person.infection != None:
            print(f'{person._id did} not infect {random._id} because they are already infected.')
        else:
            print(f'{person._id did} infected {random._id}.')

    def log_infection_survival(self, person):
        if person.is_alive:
            print(f'{person._id} survived the infection.')
        else:
            print(f'{person._id} died from the infection.')

    def log_time_step(self, time_step_number):
        pass
