from deap import base, creator, tools, algorithms
from deap.tools import Logbook

from UserPreferencePredictor.Model import PredictModel

import random
from statistics import mean, stdev
from .image_generator import ImageGenerator
from .bit_decorder import BitDecoder


class Optimizer:
    def __init__(self, model: PredictModel,
                 image_generator: ImageGenerator,
                 bit_decoder: BitDecoder):
        self.image_generator = image_generator
        self.bit_decoder = bit_decoder
        self.model = model
        self.toolbox = self._init_deap()

    def _evaluate(self, individual):
        param = self.bit_decoder.decode(individual)
        image = self.image_generator.generate(param)

        predict_evaluate = self.model.predict([image]).tolist()[0][0]

        mu = 1
        variation_width = 0.5
        sigma = variation_width/3
        return predict_evaluate*random.gauss(mu, sigma),

    def _init_deap(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat,
                         creator.Individual, toolbox.attr_bool, 100)
        toolbox.register("population", tools.initRepeat,
                         list, toolbox.individual)

        toolbox.register("evaluate", self._evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        return toolbox

    def _individual_to_list(self, individual_tuple):
        individual_list = [ind[0] for ind in individual_tuple]
        return individual_list

    def optimize(self, ngen: int, *,
                 population_num: int = 30,
                 param_list_num: int = 4) -> (list, Logbook):
        pop = self.toolbox.population(n=population_num)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", lambda ind: mean(self._individual_to_list(ind)))
        stats.register("std", lambda ind: stdev(self._individual_to_list(ind)))
        stats.register("min", lambda ind: min(self._individual_to_list(ind)))
        stats.register("max", lambda ind: max(self._individual_to_list(ind)))

        pop, logbook = algorithms.eaSimple(
            pop, self.toolbox, cxpb=0.5, mutpb=0.2,
            ngen=ngen, stats=stats, halloffame=hof)

        param_list = [self.bit_decoder.decode(ind)
                      for ind in tools.selBest(pop, param_list_num)]
        return param_list, logbook
