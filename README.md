Bridge one colour game
==============================

In this project we calculate the probability of taking all tricks by one pair in bridge game.
We calculate the probabilities for all possible moves by assuming that:
- all players play optimally,
- all players know all cards,
- each opponent have a given number of unknown cards (e.g. all cards might be unknown)

We allow user to iteratively choose the card of each player.

To test it on predefined example write:
```bash
   make demo
   ```

In the new version (2023) we weakened the assumptions of full knowledge of all players: 
- we assume only that our opponents have full knowledge,
- we have only a partial knowledge and we gain a full knowledge after the first trick.
To test it on predefined example write:
```bash
   make demo_wo_full_visibility
   ```