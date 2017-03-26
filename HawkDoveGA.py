from random import randint, choice, random
import csv

MUTATION_PROB = 99.9
CROSSOVER_PROB = 75
GENERATIONS = 1000
V = 10
C = 100


def initialise_population():
    """Returns a list of 100 lists each of which containing 100 elements which are either 1's or 0's."""
    return [[randint(0, 2) for i in range(100)] for x in range(100)]


def fitness(chromosome, population):
    """Calculates the payoff from a population."""
    payoff = 0
    for player_choice in chromosome:
        # Each choice plays 5 times against a randomly chosen choice from the rest of the population
        total_payoff = 0
        for x in range(5):
            other_player = choice(choice(population))

            if player_choice == 1 and other_player == 1:
                # Hawk Hawk
                # 50/50 chance of winning the fight, otherwise you lose and a penalty C is applied to the payoff
                chance = random()
                if chance <= 0.5:
                    total_payoff += V
                else:
                    total_payoff -= C

            elif player_choice == 1 and other_player == 0:
                # Hawk Dove
                total_payoff += V

            elif player_choice == 1 and other_player == 2:
                # Hawk Big Dove
                total_payoff += V-10

            # Dove Hawk you get 0 payoff so do nothing
            # Dove Big Dove you get 0 payoff so do nothing

            # Dawkins' Hawk Dove
            elif player_choice == 0 and other_player == 0:
                # Dove Dove
                chance = random()
                if chance <= 0.5:
                    total_payoff += (V-10)
                else:
                    total_payoff -= 10

            # Regular Hawk Dove
            # elif player_choice == 0 and other_player == 0:
            #     # Dove Dove
            #     total_payoff += V/2

            elif player_choice == 2 and other_player == 2:
                chance = random()
                if chance <= 0.5:
                    total_payoff += (V-20)
                else:
                    total_payoff -= 20

            elif player_choice == 2 and other_player == 0:
                # Big Dove Small Dove
                total_payoff += V

            elif player_choice == 2 and other_player == 1:
                # Big Dove Hawk
                total_payoff -= 10

        payoff += total_payoff/5

    if payoff != 0:
        payoff /= len(chromosome)

    return payoff


def random_split_crossover(chromo1, chromo2):
    """Splits 2 lists at a random point and combines them from this split."""

    # Splits at a random point from 0-100
    split_point = randint(0, 100)
    # First list gets split
    chromo1_cross1 = chromo1[:split_point]
    chromo1_cross2 = chromo1[split_point:]
    # Second list gets split
    chromo2_cross1 = chromo2[:split_point]
    chromo2_cross2 = chromo2[split_point:]

    # Merge both lists into 2 new combined lists
    child1 = chromo1_cross1 + chromo2_cross2
    child2 = chromo2_cross1 + chromo1_cross2

    return child1, child2


def mutate(chromosome):
    """Randomly mutates ."""

    mutated_chromo = list()
    for x in chromosome:
        # Mutates depending on how big the mutation probability is
        if (random()*100) > MUTATION_PROB:
            # Switches a 1 to a 0 or vice versa
            x = (x + (randint(1, 2))) % 3
        mutated_chromo.append(x)
    return mutated_chromo


def tournament_select(chromosomes, population):
    """Returns the fittest gene from any genes passed in."""
    a = list()
    # Create new list with the fitness of each element instead of the actual list
    for chromo in chromosomes:
        a.append(fitness(chromo, population))
        # a.append(fitness_vs_mouse(chromo))
    # Use the index of the fitness list to return the fittest gene
    return chromosomes[a.index(max(a))]


def evolve(population):
    """Runs the genetic algorithm.
       Doing Selection, Crossover and Mutation."""
    int_population = list()
    # Create new list from tournament selected genes
    while len(int_population) < 100:
        # Chooses the fittest chromosome from 4 randomly chosen chromosomes from the population
        int_population.append(tournament_select([choice(population),
                                                 choice(population),
                                                 choice(population),
                                                 choice(population)],
                                                population))

    # Possibly crossover 2 genes
    for i in range(0, len(int_population)-1, 2):
        if randint(0, 100) > CROSSOVER_PROB:
            int_population[i], int_population[i+1] = random_split_crossover(int_population[i], int_population[i+1])

    mutated_pop = list()
    # Possibly mutate elements from each gene
    for gene in int_population:
        mutated_pop.append(mutate(gene))
    # Return the crossed-over and mutated population
    return mutated_pop

# Initialise a random population
pop = initialise_population()

# Run the algorithm
i = 0
amount_of_hawks_per_generation = list()
amount_of_small_doves_per_generation = list()
amount_of_big_doves_per_generation = list()
for i in range(GENERATIONS):
    pop = evolve(pop)
    total_hawk = 0
    total_small_dove = 0
    total_big_dove = 0
    for x in pop:
        total_hawk += x.count(1)
        total_small_dove += x.count(0)
        total_big_dove += x.count(2)
    # Prints the fitness of the first chromosome, just to have an idea of how the algorithm is working
    print("-----------------------------------------------")
    print(pop[0])
    print("Generation: {}".format((i+1)))

    print("Hawks: {}".format(total_hawk/100))
    print("Small Doves: {}".format(total_small_dove/100))
    print("Big Doves: {}".format(total_big_dove/100))
    print("-----------------------------------------------")

    amount_of_hawks_per_generation.append(total_hawk/100)
    amount_of_small_doves_per_generation.append(total_small_dove/100)
    amount_of_big_doves_per_generation.append(total_big_dove / 100)

with open('hawks_and_doves(BigSmall)_' + str(C) + '_' + str(V) + '.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(amount_of_hawks_per_generation)
    wr.writerow(amount_of_small_doves_per_generation)
    wr.writerow(amount_of_big_doves_per_generation)
