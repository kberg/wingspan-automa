from collections import namedtuple, Counter
import csv
from cycler import cycler
import matplotlib
import matplotlib.pyplot as plt
import statistics
import matplotlib.ticker as plticker

Play = namedtuple(
  'Play',
  ['parameters', 'p_level', 'p_autombon', 'p_deck', 'p_goal',
   'eggs', 'birds', 'game_end_bonus', 'round_end_bonus', 'total'])

def read():
  print("Reading")
  rows = []
  with open('scores.csv', newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader) # skip header, todo compare header with namedtuple to verify
                   # fields are mapped.
      for row in reader:
        play = Play(
          parameters = row[0],
          p_level = int(row[1]),
          p_autombon = row[2] == 'True',
          p_deck = row[3],
          p_goal = row[4],
          eggs = int(row[5]),
          birds = int(row[6]),
          game_end_bonus = int(row[7]),
          round_end_bonus = int(row[8]),
          total = int(row[9]))
        rows.append(play)
  return rows

class PlotLine:
  def __init__(self, filter, label, axis=0):
    self.filter = filter
    self.label = label
    self.axis = axis

def calculate(rows, filter, field='total'):
  c = Counter()
  for row in rows:
    key = row.total # row[field] getattr(row,field) ?
    if filter(row) == True:
      c[key] = c[key] + 1
  return c

difficulties = { 3: 'Eaglet', 4: 'Eagle', 5: 'Eagle-eyed Eagle'}

def p_all(): return PlotLine(lambda _ : True, 'all')
def p_deck(v): return PlotLine(lambda x : x.p_deck == v, f'deck[{v}]')
def p_level(v): return PlotLine(lambda x : x.p_level == v, f'difficulty[{difficulties[v]}]')
def p_autombon(v): return PlotLine(lambda x : x.p_autombon == v, f'autumbon[{v}]')
def p_goal(v): return PlotLine(lambda x : x.p_goal == v, f'goal[{v}]')
def axis(axis, plotline):
  plotline.axis = axis
  return plotline

def go():
  rows = read()

  def graph(title, basename, *plots):
    fig, ax = plt.subplots()
    ax.get_yaxis().set_ticklabels([]) # Hide y axis values
    ax.xaxis.set_minor_locator(plticker.MultipleLocator(base=2.0))

    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    def addPlot(plotline, nth):
      print("Plot")
      result = calculate(rows, plotline.filter)
      mean = statistics.mean(result.elements())
      stdev = statistics.stdev(result.elements())
      height = max(result.values())
      xs = sorted(result.keys())
      ys = [result[x] for x in xs]
  
      # Choose color here so the plot and error bars share it.
      color = next(ax._get_lines.prop_cycler)['color']
      ax.plot(
        xs,
        ys,
        color=color,
        label=plotline.label)

      ax.errorbar(
        mean,
        (height / 2) - (nth * 1000),
        xerr=stdev,
        snap=True,
        color=color,
        marker='^')

    nth = 0
    for plot in plots:
      addPlot(plot, nth)
      nth = nth + 1

    ax.set(xlabel='score', ylabel='count', title=title)

    ax.legend()
    ax.grid()

    fig.savefig(f'{basename}.png')
    # plt.show()

  graph('By level', 'bylevel', p_level(3,), p_level(4), p_level(5))
  graph('By deck', 'bydeck', p_deck('base'), p_deck('ee'), p_deck('both'))
  graph('With Autumbon Society', 'byautumbon', p_autombon(False), p_autombon(True))
  graph('By goal', 'bygoal', p_goal('RaspbLifeFellow'), p_goal('Autwitcher'))
  graph('all', 'all',
     p_all(),
     axis(1, p_level(3)), axis(1, p_level(4)), axis(1, p_level(5)),
     axis(2, p_deck('base')), axis(2, p_deck('ee')), axis(2, p_deck('both')),
     axis(3, p_autombon(False)), axis(3, p_autombon(True)),
     axis(4, p_goal('RaspbLifeFellow')), axis(4, p_goal('Autwitcher')))

go()