# wingspan-automa
Code for playing with the Wingspan Automa

To use this code, install Python 3 and matplotlib.

After running the monte carlo simulation, you can scan the results
to see the distribution of how many cards the human player
took with this command:

```
cat scores.csv | rev | cut -d',' -f 1 | rev | sort -n | uniq
```
