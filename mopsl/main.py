import decoder as d
import operators as op
import json
import argparse
import random as rnd
from operator import itemgetter
import gc
import os
import sys

rnd.seed()

# This file has been modified to be used with
# IRACE for paramtere calibration


def get_init_sec(_indiv, _proc):
    sec = 0
    for tsk in _indiv:
        if tsk[0] == _proc:
            sec += 1
    return sec


def create_aux(ref):
    _aux = []
    for i in range(ref['workpieces']):
        for _ in range(ref['no_process']['j{}'.format(i+1)]):
            _aux.append(i+1)
    rnd.shuffle(_aux)
    return _aux


def create_indiv(_aux, ref):
    _indiv = []
    for proc in _aux:
        sec = get_init_sec(_indiv, proc)
        machs = d.get_possible_machines(proc, sec, ref)
        _indiv.append([proc, rnd.randint(1, len(machs))])
    return _indiv


def init_pop(pop_size, ref):
    _pop = []
    while len(_pop) < pop_size:
        aux = create_aux(ref)
        indiv = create_indiv(aux, ref)
        tasks = d.get_tasks(indiv, ref)
        schdl = d.create_schedule(tasks, ref)
        fitness = d.get_fitness(schdl)
        _pop.append([indiv, fitness])
    return _pop


def main(filename, pop_size, cp, mp, no_gen):
    with open('./Instances/{}.json'.format(filename), 'r') as f:
        _aux = json.load(f)
    ref = _aux['machine']
    _pop = init_pop(pop_size, ref)
    _pop.sort(key=itemgetter(1))
    best = _pop[-1][0]
    gen = 0

    while gen < no_gen:
        parents = op.selection(_pop)
        for i in range(0, len(parents), 2):
            p1 = _pop[parents[i]][0]
            p2 = _pop[parents[i+1]][0]
            offspring = op.crossover([p1, p2], ref, cp)
            _mut_offspring = []
            for _child in offspring:
                _mut_offspring.append(op.mutation(_child, ref, mp))
            for _indiv in _mut_offspring:
                _aux_indiv = _indiv.copy()
                _tasks = d.get_tasks(_aux_indiv, ref)
                _schdl = d.create_schedule(_tasks, ref)
                _fitness = d.get_fitness(_schdl)
                _pop.append([_aux_indiv, _fitness])
        _pop = sorted(_pop, key=itemgetter(1))
        gen += 1
        _best = _pop[-1][0]
        _best_fitness = _pop[-1][1]
        while len(_pop) > pop_size:
            del (_pop[0])
        gc.collect()

    _best = _pop[-1][0]
    _best_fitness = _pop[-1][1]
    return _best_fitness

# Useful function to print errors.


def target_runner_error(msg):
    now = datetime.datetime.now()
    print(str(now) + " error: " + msg)
    sys.exit(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='FJSP algorithm with paired list encoding')
    ap.add_argument("--pop_size", dest='pop_size',
                    type=int, help="Population size")
    ap.add_argument("--cp", dest='cp', type=float,
                    help="Crossover probability")
    ap.add_argument('--mp', dest='mp', type=float, help='Mutation probability')
    ap.add_argument('--no_gen', dest='no_gen', type=int,
                    help='Max no. of generations')
    ap.add_argument('--i', dest='filename', type=str,
                    help='Instance of benchmark to be evaluated')
    ap.add_argument('--s', dest='seed', type=float, help='Seed value')
    args = ap.parse_args()

    rnd.seed(args.seed)

    print(main(args.filename, args.pop_size, args.cp, args.mp, args.no_gen))
