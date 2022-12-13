from matplotlib import pyplot as plt
from matplotlib import colors
import decoder as d
import random as rnd

rnd.seed()


def generate_colours(ref):
    colours = []
    for _ in range(ref['workpieces']):
        r = rnd.uniform(0, 1)
        g = rnd.uniform(0, 1)
        b = rnd.uniform(0, 1)
        colours.append((r, g, b))
    for colour in colours:
        yield colors.to_hex(colour)


def add_bar(gnt, task, size, yref, colours):
    start_time = task[-1][0]
    duration = task[-1][1] - start_time
    lower_yaxis = yref - int((size/2))
    windx = task[0] - 1
    label = '{}/{}'.format(task[0], task[1])
    gnt.broken_barh([(start_time, duration)],
                    (lower_yaxis, size),
                    facecolors=(colours[windx]),
                    edgecolor='black')
    gnt.text(start_time + 0.3, yref, label, c='black')


def create_graph(indiv, ref):
    colours = [x for x in generate_colours(ref)]
    chrom = indiv[0]
    fitness = indiv[1]
    tasks = d.get_tasks(chrom, ref)
    schdl = d.create_schedule(tasks, ref)
    fig, gnt = plt.subplots()
    ylim = 2*ref['no_machines']*10
    yref = int(ylim-(ylim/5))
    gnt.set_xlim(0, (1/fitness) + 1)
    gnt.set_ylim(ylim)
    gnt.set_xlabel('Time per operation')
    gnt.set_ylabel('Machine')
    size = int(yref / ref['no_machines'])
    ticks = [size + x for x in range(0, yref, size)]
    gnt.set_yticks(ticks)
    gnt.set_yticklabels(list(schdl.keys()))
    gnt.grid(False)

    for idx, key in enumerate(schdl.keys()):
        for task in schdl[key]:
            add_bar(gnt, task, size, ticks[idx], colours)
    return gnt


if __name__ == '__main__':
    print('Chart module')
