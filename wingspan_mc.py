import random
import sys
import csv

def log(text):
  if (False):
    print(text)

class Automa:
  # Each card has three characters. The first is a digit used for eggs, to indicate
  # how many eggs to include. 
  # d = die from the birdfeeder
  # e = take eggs
  # c = get card
  # g = get goal card
  # p = activate pink powers
  # + / -, change end of round goals tokens.
  automa_decks = [
    [" d+", "1e-", " c+", " g ", " g ", "1e ", "1e+", " dp", " dp", " c-", " g+"],
           [" c+", "2e-", "2e-", " c ", " g+", " dp", " g ", "2e+", " dp", " g+"],
                  [" g+", " c-", " dp", " g+", "3e-", "2e+", " c ", " dp", " g+"],
                         [" dp", "3e+", "3e+", " c-", " c+", "3e-", " g ", " g+"],

  ]

  def RaspbLifeFellow(self, display):
    opts = list(filter(lambda x: x in [5,6,7], display))
    if opts:
      c = max(opts)
      return [c]
    return None

  def Autwitcher(self, display):
    cs = list(filter(lambda x: x in [3,4], display)) # list().sort()
    if cs:
      cs.sort()
      result = cs[-2:]
      return result
    return None

  def __init__(self):
    self.eggs = 0
    self.birds = 0
    self.bonus_birds = []
    self.round_bonuses = []
    self.cubes = 0
    self.deck = []

  def initRound(self, round, use_autombon):
    if use_autombon:
      self.automa_deck = self.automa_decks[round][:] # [:] makes a copy
    else:
      self.automa_deck = self.automa_decks[round][:-1] # [:] makes a copy
    log(f'hey{self.automa_deck}')
    random.shuffle(self.automa_deck)
    self.cubes = 0

  def playCard(self, game, goal):
    card = self.automa_deck.pop()
    items = list(card)
    eggmod = items[0]
    action = items[1]
    rhs = items[2]
    log(f'Drew {card}')
    if action == 'e':   
      self.eggs += int(eggmod)

    if action == 'c':
      self.birds += 1
      game.resetDisplay()

    if action == 'g':
      if goal == 'RaspbLifeFellow':
        result = self.RaspbLifeFellow(game.display)
      elif goal == 'Autwitcher':
        result = self.Autwitcher(game.display)
      else:
        raise "Yo"
      if result and len(result) > 0:
        for x in result:
          self.bonus_birds.append(x)
          game.display.remove(x) 
        game.fillDisplay()
      else:
        self.birds += 1
  
    if rhs == '+':
      self.cubes += 1
    if rhs == '-':
      self.cubes = max(0, self.cubes - 1)

  def scoreRound(self, round):
    higher = [4, 5, 6, 7]
    lower = [1, 2, 3, 4]
    # +/-: goals, well, they're funny. Making an estimate, if the result is +2 or more, Automa wins.
    # +1, tie, 0, human wins.
    if self.cubes >= 2:
      round_bonus = higher[round]
    if self.cubes == 1:
      round_bonus = int((higher[round] + lower[round]) / 2)
    if self.cubes == 0:
      round_bonus = lower[round]

    self.round_bonuses.append(round_bonus)

  def score(self, parameters):
    log("\n\nscore")
    scores = {
        'eggs': self.eggs,
        'birds': self.birds * parameters['level'],
        'game-end-bonus': sum(self.bonus_birds),
        'round-end-bonus': sum(self.round_bonuses)
    }

    scores['total'] = sum(scores.values())
    for i in scores:
      log (f'{i}: {scores[i]}')
    return scores

class Game:
  bird_cards = [
    { 0:6, 1:12, 2:20, 3:33, 4:33, 5:34, 6:12, 7:8, 8:8, 9:5 }, # base OFF BY ONE
    { 0:3, 1:7,  2:8,  3:18, 4:24, 5:8,  6:6,  7:4, 8:2, 9:0 }  # ee
  ]

  def __init__(self, parameters):
    self.parameters = parameters
    self.makeDeck()
    self.display = []
    self.automa = Automa()
    self.round = -1
    self.prepareRound()
    self.human_draw = 0

  def prepareRound(self):
    self.round = self.round + 1
    log(f'\nRound {self.round}\n')
    self.automa.initRound(self.round, self.parameters['autombon'])
    self.resetDisplay()

  def resetDisplay(self):
    self.display = []
    self.fillDisplay()

  def fillDisplay(self):
    while len(self.display) < 3:
      self.display.append(self.deck.pop())

  def makeDeck(self):
    self.deck = []
    def add_all(cards):
      for points in cards:
        self.deck = self.deck + ([points] * cards[points])

    log(self.parameters)
    if (self.parameters['deck']) in ('base', 'both'):
      add_all(self.bird_cards[0])
    if (self.parameters['deck']) in ('ee', 'both'):
      add_all(self.bird_cards[1])
    random.shuffle(self.deck)

  def playTurn(self):
    # human removes 0, 1 or 2 cards.
    x = random.random()
    if (x < .15):
      self.deck.remove(random.choice(self.deck))
      self.human_draw = self.human_draw + 1
    if (x < .3):
      self.deck.remove(random.choice(self.deck))
      self.human_draw = self.human_draw + 1
    self.fillDisplay()

    self.automa.playCard(self, self.parameters['goal'])

  def completeRound(self):
    self.automa.scoreRound(self.round)

# How to score:
#
# d: taking a die from the birdfeeder does not impact the Automa's score
# e: add the number of eggs to the end score. +1 per egg.
# c: add to the number of birds scored, which will be multipled by its
#    multiplier (3, 4, 5). Replace the birds
# g: evaluate bonus condition and take cards. Keep a tally of points.
# p: pink powers don't really touch the player.
# +/-: goals, well, they're funny. Making an estimate, if the result is +2 or more, Automa wins.
# +1, tie, 0, human wins.
#
# Every other turn, replace 1 or 2 birds simulating player taking birds. (20% 20%)
# At the start of a round, replace the birds.
#

def run_simulation(params, writer):
  print(params)

  fmtdparams = '{c[level]}-{c[autombon]}-{c[deck]}-{c[goal]}'.format(c = params)

  pp_params = dict((f'p_{name}', val) for name, val in params.items())

  for x in range(0, 50000):
    if x % 5000 == 0:
      print(f' #{x}')
    g = Game(params)
    log(g.automa.automa_decks)
    for i in range(0, 8):
      g.playTurn()
    g.completeRound()
    g.prepareRound()
    for i in range(0, 7):
      g.playTurn()
    g.completeRound()
    g.prepareRound()
    for i in range(0, 6):
      g.playTurn()
    g.completeRound()
    g.prepareRound()
    for i in range(0, 5):
      g.playTurn()
    g.completeRound()
    data = g.automa.score(params)
    data["human-draw"] = g.human_draw
    writer.writerow({**data, **{'parameters': fmtdparams}, **pp_params})

def run_all():
  levels = [3,4,5]
  autombons = [True, False]
  decks = ['base', 'ee', 'both']
  goals = ['Autwitcher', 'RaspbLifeFellow']

  csv_columns = ['parameters', 'p_level', 'p_autombon', 'p_deck', 'p_goal', 'eggs', 'birds', 'game-end-bonus', 'round-end-bonus', 'total', 'human-draw']
  try:
    with open('scores.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for level in levels:
        for autombon in autombons:
          for deck in decks:
            for goal in goals:
              params = { 'level': level, 'autombon': autombon, 'deck': deck, 'goal': goal}
              run_simulation(params, writer)
  except IOError:
    print(f'Error! {e}')

def main():
  run_all()

if __name__ == "__main__":
  main()