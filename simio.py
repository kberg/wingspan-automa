from collections import namedtuple
import csv

COLUMNS = [
    'parameters',
    'p_level',
    'p_autombon',
    'p_deck',
    'p_goal',
    'eggs',
    'birds',
    'game_end_bonus',
    'round_end_bonus',
    'total']

Play = namedtuple('Play', COLUMNS)

def readPlays(filename):
  print(f'Reading {filename}')
  rows = []
  with open(filename, newline='') as csvfile:
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

def writePlays(filename, plays):
  try:
    with open(filename, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
      writer.writeheader()
      for play in plays:
        writer.writerow(play._asdict())

  except IOError:
    print(f'Error! {e}')

def writeStats(filename, statsTable):
  try:
    with open(filename, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=['plot', 'mean', 'stdev'])
      writer.writeheader()
      for row in statsTable:
        writer.writerow({'plot': row[0], 'mean': row[1], 'stdev': row[2]})

  except IOError:
    print(f'Error! {e}')
