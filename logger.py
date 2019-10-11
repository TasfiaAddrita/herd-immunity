class Logger(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected):
        f = open(self.file_name, 'w+')
        f.write(f'------------------------ META DATA ------------------------\nVirus\n\tName - {virus_name} \n\tMortality - {mortality_rate * 100}%\n\tReproduction - {basic_repro_num * 100}%\n\nPopulation\n\tSize - {pop_size}\n\tVaccinated - {vacc_percentage * 100}%\n\tInitial infected - {initial_infected}\n--------------------------------------------------------------\n\n')

        f.close()

    def log_interaction(self, person, random_person):
        f = open(self.file_name, 'a')
        if random_person.is_vaccinated:
            # print(f'{person._id} did not infect {random_person._id} because they are vaccinated.')
            f.write(f'{person._id} did not infect {random_person._id} because they are vaccinated.\n')
        elif random_person.infection != None:
            # print(f'{person._id} did not infect {random_person._id} because they are already infected.')
            f.write(f'{person._id} did not infect {random_person._id} because they are already infected.\n')
        else:
            # print(f'{person._id} infected {random_person._id}.')
            f.write(f'{person._id} infected {random_person._id}.\n')

        f.close()

    def log_infection_survival(self, person):
        f = open(self.file_name, 'a')
        if person.is_alive:
            # print(f'{person._id} survived the infection and is now vaccinated.')
            f.write(f'{person._id} survived the infection and is now vaccinated.\n')
        else:
            # print(f'{person._id} died from the infection.')
            f.write(f'{person._id} died from the infection.\n')
        f.close()

    def log_time_step_start(self, time_step_number):
        f = open(self.file_name, 'a')
        f.write(f'\n------------------------ TIME STEP {time_step_number} -------------------------\n')
        f.close()

    def log_time_step_stats(self, stats):
        f = open(self.file_name, 'a')
        # print(f'Time step {time_step_number} ended, beginning {time_step_number + 1}\n')
        # f.write(f'Time step {time_step_number} ended, beginning {time_step_number + 1}\n')
        f.write('STATS -----------------\n')
        f.write(f'# of people infected during this time step: {stats[0]}\n')
        f.write(f'total # of people infected at the end of this time step: {stats[1]}\n')
        f.write(f'# of people who died during this time step: {stats[2]}\n')
        f.write(f'total # of people who died at the end of this time step: {stats[3]}\n--------------------------------------------------------------\n\n\n')

        f.close()

    # def log_time_step_stats(self, stats):
    #     f = open(self.file_name, 'a')
    #     f.write(f'# of people infected during this time step: {stats}\n')
    #     f.close()

    # def log_time_step(self, time_step_number):
    #     f = open(self.file_name, 'a')
    #     f.write(f'time_step')
    #     f.close()