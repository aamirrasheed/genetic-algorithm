import numpy as np

NUM_CHROMOSOMES = 500
NUM_GENES = 9
GENE_LENGTH = 4
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
SEARCH_RADIUS = 10000

TARGET = 42

def init_chromosome():
    chromosome = ""
    for i in range(NUM_GENES):
        gene = ""
        for j in range(GENE_LENGTH):
            if np.random.random() > 0.5:
                gene += "1"
            else:
                gene += "0"
        chromosome += gene
    return chromosome

# check correct length
x = init_chromosome()
assert(len(x) == NUM_GENES * GENE_LENGTH) 

# check that values are 0 or 1 only
y = [True if i == '0' or i == '1' else False for i in x]
assert(all(y))

def init_chromosomes():
    chromosomes = []
    for i in range(NUM_CHROMOSOMES):
        chromosome = init_chromosome()
        chromosomes.append(chromosome)

    return chromosomes

# check correct length
x = init_chromosomes()
assert(len(x) == NUM_CHROMOSOMES) 

def chromosome_to_genes(chromosome):
    return [chromosome[i:i+GENE_LENGTH] for i in range(0, len(chromosome), GENE_LENGTH)]

x = chromosome_to_genes('011010100101110001001101001010100001')
assert(len(x) == NUM_GENES)

translate = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': '+',
    '1011': '-',
    '1100': '*',
    '1101': '/',
    '1110': '',
    '1111': '',
}
def translation(chromosome):
    """
    Input: A 'chromosome' string of the format:
    'XXXX XXXX XXXX XXXX ... XXXX'

    Output: An expression representing which
    operators/digits each gene responds to in the format:
    '9 + 4 / - - 4 * 2 2'
    """
    genes = chromosome_to_genes(chromosome)
    arithmetic = ""
    for gene in genes:
        # print(gene)
        arithmetic += translate[gene]
    return arithmetic

chrome = '011010100101110001001101001010100001'
assert(translation(chrome) == '6+5*4/2+1')

chrome = '0010001010101110101101110010'
assert(translation(chrome) == '22+-72')

def fitness(chromosomes):
    """
    Calculates and returns fitness score for all chromosomes based on formula:

    1/abs(TARGET - arithmetic_value)

    If chromosome is invalid, the fitness score is 0.

    If target is found, it returns early.

    Not normalized so do that later if you want.
    """
    fitness_scores = []
    results = []
    for chromosome in chromosomes:
        # translate chromosome to arithmetic
        arithmetic = translation(chromosome)

        # get fitness scores
        result = 0
        fitness_score = 0
        try: # valid chromosome
            result = eval(arithmetic)
            if abs(result) > TARGET + SEARCH_RADIUS:
                result = None
        except: # invalid chromosome
            result = None
        finally: 
            if result == TARGET: # found it. Return early
                fitness_score = None
                fitness_scores.append(fitness_score)
                return fitness_scores, None
            elif result == None: # invalid chromosome
                fitness_score == 0
            else: # valid, but not target
                fitness_score = 1/abs(TARGET - result)
        results.append(result)
        fitness_scores.append(fitness_score)

    return fitness_scores, results

chrome = ['011010100101110001001101001010100001']
assert(fitness(chrome)[0] == [1/25])

def crossover(mate1, mate2):
    """
    Input: Two genes to potentially crossover
    Output: One gene if crossed over; two genes if not crossed over
    """
    if np.random.random() < CROSSOVER_RATE:
        crossover_index = GENE_LENGTH * int(NUM_GENES * np.random.random())
        return mate1[:crossover_index] + mate2[crossover_index:]
    else:
        return [mate1, mate2]
    pass

x = '011010100101110001001101001010100001'
y = crossover(x, x)
assert(len(y) == NUM_GENES * GENE_LENGTH or len(y) == 2)

def mutate(chromosome):
    """
    Flips bit of chromosome according to mutation rate
    """
    new_chromosome = ''
    for bit in chromosome:
        if np.random.random() < MUTATION_RATE:
            if bit == '1':
                new_chromosome += '0'
            elif bit == '0':
                new_chromosome += '1'
            else:
                raise Exception("Bit encountered in chromosome {} that is neither 0 nor 1".format(chromosome))
        else:
            new_chromosome += bit
    return new_chromosome

def main():
    # init N random chromosomes, set as current
    chromosomes = init_chromosomes()
    iteration = 0
    # Loop until solution is found
    while(True):
        
        # assign fitness score to each chromosome
        fitness_scores, results = fitness(chromosomes)

        # if any satisfy the problem, break and return
        if any([True if x is None else False for x in fitness_scores]):
            print()
            print("Done! Iteration:", iteration)
            index = fitness_scores.index(None)
            winner = chromosomes[index]
            print("Winner")
            print(winner)
            solution = translation(winner)
            print("Solution is:", solution)
            return

        # log current progress
        # average score
        avg = 0
        num_valid = 0
        for result in results:
            if result is not None:
                avg += result
                num_valid += 1 
        avg /= num_valid

        # Current leader
        leader = results[np.argmin([np.inf if x is None else abs(x - TARGET) for x in results])]
        iteration += 1
        print("Generation:", iteration, "Avg:", avg, "Leader:", leader)

        # create new generation 
        new_chromosomes = []
        while len(new_chromosomes) < NUM_CHROMOSOMES:

            normalized_fitnesses = [x/sum(fitness_scores) for x in fitness_scores]

            # sample two chromosomes with probability proportional to fitness
            mates = np.random.choice(chromosomes, 2, fitness_scores)

            # crossover bits to create new chromosome
            new_chromosome = crossover(mates[0], mates[1])

            # mutate chromosome - get a new chromosomes or 
            # get back two old chromosomes
            if len(new_chromosome) == 2:
                new_chromosomes += new_chromosome
            else:
                new_chromosome = mutate(new_chromosome)
                new_chromosomes.append(new_chromosome)

        chromosomes = new_chromosomes

if __name__ == '__main__':
    main()
