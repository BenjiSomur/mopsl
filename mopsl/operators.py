import decoder as d
import random as rnd

rnd.seed()


def selection(_pop):
    _tot_fitness = 0
    _evs = []
    _parents = []
    for _indiv in _pop:
        _tot_fitness += _indiv[1]

    for _indiv in _pop:
        _evs.append(_indiv[1] / _tot_fitness)

    while len(_parents) < len(_pop):
        r = rnd.uniform(0, _tot_fitness)
        _sum = 0
        for _indx, _val in enumerate(_evs):
            _sum += _val
            if _sum >= r:
                _parents.append(_indx)
                break
    rnd.shuffle(_parents)
    return _parents


def get_last_pos(_indiv):
    for i, val in enumerate(_indiv):
        if val == 0:
            return i


def create_cp(_wps):
    _aux = [*range(len(_wps))]
    aux1, aux2 = rnd.sample(_aux, 2)
    if aux1 > aux2:
        return [aux2, aux1]
    else:
        return [aux1, aux2]


def first_group(j1, child, parent):
    for idx, tsk in enumerate(parent):
        if tsk[0] in j1:
            child[idx] = tsk.copy()


def second_group(j2, child, parent):
    for tsk in parent:
        if tsk[0] in j2:
            posaux = get_last_pos(child)
            child[posaux] = tsk.copy()


def crossover(parents, ref, cp):
    p1 = parents[0].copy()
    p2 = parents[1].copy()
    if rnd.uniform(0, 1) > cp:
        return [p1.copy(), p2.copy()]

    wps = [*range(1, ref['workpieces'] + 1)]
    rnd.shuffle(wps)
    cp1, cp2 = create_cp(wps)
    j1 = wps[:cp1]
    j2 = wps[cp1:]
    c1 = [0] * len(p1)
    c2 = [0] * len(p2)
    first_group(j1, c1, p1)
    first_group(j1, c2, p2)
    second_group(j2, c1, p2)
    second_group(j2, c2, p1)

    _offspring = [c1, c2]
    return _offspring


def get_min_mach(proc, sec, machs, ref):
    _min = 1000
    i_aux = 0
    for idx, _id in enumerate(machs):
        time = ref['process_time']['j{}'.format(proc)][sec][_id]
        if time < _min:
            i_aux = idx
            _min = time
    return i_aux + 1


def mutation(chrom, ref, mp):
    _aux = chrom.copy()
    if rnd.uniform(0, 1) < mp:
        idx1, idx2 = rnd.sample([*range(len(_aux)-1)], 2)
        sec1 = d.get_sec(_aux, idx1)
        sec2 = d.get_sec(_aux, idx2)
        machs1 = d.get_possible_machines(_aux[idx1][0], sec1, ref)
        machs2 = d.get_possible_machines(_aux[idx2][0], sec2, ref)
        _aux[idx1][1] = rnd.randint(1, len(machs1))
        #_aux[idx2][1] = rnd.randint(1, len(machs2))
        _min_mach = get_min_mach(_aux[idx2][0], sec2, machs2, ref)
        _aux[idx2][1] = _min_mach
    return _aux


if __name__ == '__main__':
    print('Operators module')
