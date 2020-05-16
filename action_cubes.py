from __future__ import division
from collections import Counter
from functools import reduce
from itertools import permutations 
from statistics import mean, stdev

decks = [
  [+1, +1, +1, 0, 0, 0, 0, 0, -1, -1],
  [+1, +1, +1, 0, 0, 0, 0, -1, -1],
  [+1, +1, +1, 0, 0, 0, -1, -1],
  [+1, +1, +1, 0, 0, -1, -1],
]

def calculate(cards):
  # This calculates a running sum of the cards. a+b adds a value
  # to the running total. The max(0, ...) is the guard that
  # prevents subtracting 1 from 0.
  # The 0 at the end is an initial value. This prevents
  # a case where the first two values are -1, 1, and are
  # happily added together. So instead, the first two
  # values are 0, -1, and the -1 will be rendered useless.
  return reduce(lambda a,b : max(0, a+b), cards, 0)

def process_deck(deck, use_autombon_society_card):
  if (use_autombon_society_card):
    deck = deck + [+1]

  c = Counter()
  for e in permutations(deck):
    # e[:-1] omits the last card, which won't be drawn.
    # or in the case of the Autombon Society card, 
    # omit the last two cards.
    drawn_cards = e[:-1] if not use_autombon_society_card else e[:-2]
    outcome = calculate(drawn_cards)
    c[outcome] = c[outcome] + 1
  print("For %s, %d permutations" % (len(deck), sum(c.values())))
  print(" units:   %s" % dict(c))
  print(" percent: %s" % dict((k, "%.3f%%" % (100 * c[k] / sum(c.values()))) for k in c))
  print(" stdev: %s" % stdev(c.elements()))
  print(" mean: %s" % mean(c.elements()))
  print

for deck in decks:
  process_deck(deck, False)
for deck in decks:
  process_deck(deck, True)
