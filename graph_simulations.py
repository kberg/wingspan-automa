from collections import Counter
from cycler import cycler
import matplotlib
import matplotlib.pyplot as plt
import statistics
import matplotlib.ticker as plticker
import simio

LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dotted']
NUM_STYLES = len(LINE_STYLES)

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
def p_params(v): return PlotLine(lambda x : x.parameters == v, v)

def axis(axis, plotline):
  plotline.axis = axis
  return plotline

def go():
  rows = simio.readPlays("scores.csv")
  print(f'read {len(rows)} rows')

  def graph(title, basename, *plots):
    print(f'Generating {title}')
    fig, ax = plt.subplots()
    ax.get_yaxis().set_ticklabels([]) # Hide y axis values
    ax.xaxis.set_minor_locator(plticker.MultipleLocator(base=2.0))
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    def addPlot(plotline, nth, result, mean, stdev):
      height = max(result.values())
      xs = sorted(result.keys())
      ys = [result[x] for x in xs]
  
      # Choose color here so the plot and error bars share it.
      color = next(ax._get_lines.prop_cycler)['color']

      ax.plot(
        xs,
        ys,
        color=color,
        label=plotline.label,
        linestyle=LINE_STYLES[int(nth / 6)])

      ax.errorbar(
        mean,
        (height / 2) - (nth * 1000),
        xerr=stdev,
        snap=True,
        color=color,
        linestyle=LINE_STYLES[int(nth / 6)],
        marker='^')

    statsTable=[]
    nth=0

    for plot in plots:
      print(f'Calculating {plot.label}')
      result = calculate(rows, plot.filter)
      mean = statistics.mean(result.elements())
      stdev = statistics.stdev(result.elements())
      addPlot(plot, nth, result, mean, stdev)
      nth = nth + 1
      statsTable.append([plot.label,mean,stdev])

    ax.set(xlabel='score', ylabel='count', title=title)

    ax.legend()
    ax.grid()

    fig.savefig(f'{basename}.png')
    simio.writeStats(f'{basename}.csv', statsTable)

    plt.show()

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
