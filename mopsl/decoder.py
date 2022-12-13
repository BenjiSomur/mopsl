def get_sec(chrom, idz):
    ref = chrom[idz][0]
    count = 0
    for i in range(0, idz, 1):
        if chrom[i][0] == ref:
            count += 1
    return count


def get_possible_machines(op, sec, ref):
    pom = []
    workpiece = get_workpiece([op], ref)
    for idy, m in enumerate(workpiece[sec]):
        if m > 0:
            pom.append(idy)
    return pom


def get_workpiece(tsk, ref):
    return ref['process_time']['j{}'.format(tsk[0])]


def get_tasks(chrom, ref, val=False):
    _aux = chrom.copy()
    tasks = list()
    for idx, tsk in enumerate(_aux):
        sec = get_sec(_aux, idx)
        machs = get_possible_machines(tsk[0], sec, ref)
        t = get_workpiece(tsk, ref)[sec][machs[tsk[1]-1]]
        task = [tsk[0], sec + 1, machs[tsk[1]-1]+1, t]
        tasks.append(task)
    return tasks


def search_prev_op(task, schdl):
    if task[1] == 1:
        return None
    for key in schdl.keys():
        if not schdl[key]:
            continue
        for tsk in schdl[key]:
            if tsk[1] == task[1] - 1 and tsk[0] == task[0]:
                return tsk
    return False


def get_start_time(tsk, schdl):
    prev_tsk = search_prev_op(tsk, schdl)
    lst_time = 0
    lst_t_time = 0
    if prev_tsk:
        lst_t_time = prev_tsk[-1][1]

    if schdl['m{}'.format(tsk[2])]:
        lst_time = schdl['m{}'.format(tsk[2])][-1][-1][1]

    if lst_time >= lst_t_time:
        return lst_time
    else:
        return lst_t_time


def create_schedule(tasks, ref):
    schdl = dict()
    for i in range(ref['no_machines']):
        schdl['m{}'.format(i+1)] = list()
    for tsk in tasks:
        mach = 'm{}'.format(tsk[2])
        start_time = get_start_time(tsk, schdl)
        schdl[mach].append([tsk[0], tsk[1], [start_time, start_time + tsk[3]]])
    return schdl


def get_fitness(schdl):
    _max = 0
    for key in schdl.keys():
        if not schdl[key]:
            continue
        if _max < schdl[key][-1][-1][1]:
            _max = schdl[key][-1][-1][1]
    if _max > 0:
        return round(1 / _max, 5)
    else:
        return round(1/10000000, 5)


if __name__ == '__main__':
    print('decoder module')
