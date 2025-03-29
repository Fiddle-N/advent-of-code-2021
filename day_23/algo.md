# Amphipod algorithm


## Important things to remember
* 8 amphs - 16 moves max
  * Sometimes less if
    * The amph is already in its correct place
    * The amph can move directly from its original place to its correct place

## Amphipod state
* 3 states
  * Original
  * Hallway
  * Settled
* Amphipod can already be settled
* If not already settled then original
* Amphipod can move from og -> settled or og -> hallway -> settled
  * Cannot move backwards

## Game state
* 3 states
  * Unsettled
  * Stuck - unsettled but no more moves
  * Settled
* Location of all amphs
* Energy expended

## Pre-work

### Initial amph state
* Work out the state of the amphs to begin with
  * Some amphs may already be in a settled state
  * key because you can't tell if an amphipod in row 0 is settled without looking at the amphipod in row 1
* Check row 1 - if any amphipods are in their place, they are settled
* Check row 0 *for the settled amphipods in row 1* - if they are in their place, they are settled.

### Path from a to b
* Do a BFS from a to b
* Return all the nodes inbetween a and b, not including a and b
  * We are assuming a is filled by the amphipod
  * We are assuming the work to check that b is empty has already been done
  * So all we need to return is the nodes inbetween
* To prevent repeat returns, cache this function
  * Argument should be a frozenset of a and b, because the nodes from a to b are the same as the nodes from b to a

## Algorithm
* Keep a count of the energy needed
* Take the next state
  * Start with first game state - all amphs where they currently located, and energy = 0
  * Otherwise, take a game state (optimisations to be discussed later)
* Check for win condition
  * all amphs are in their correct places
  * If energy is lower than the current count, update
* Iterate over each amph
  * Is the amph state = settled? Do nothing
  * Is the amph in a hallway state?
    * Can the amph move into a settled state?
      * Either both 0 and 1 space are empty
      * Or, 0 is empty and 1 is filled with the correct amphipod.
      * Also, the path from amph to settled state must be free - use path logic
      * If so, move into settled state
        * Create new game state from this - update locations and energy
        * When creating new game state, save state and ask - have we seen this state before? 
          * Use a cache of states to work this out.
          * If we haven't seen this before, the next state is valid to be checked
          * if we have, we can discard this state because it has effectively already been processed
      * If no, continue
  * Is the amph in an og state?
    * Can the amph move into a settled state?
      * See code above (extracted into a function)
    * Can the amph move into a hallway state?
      * Calculate all the hallway states
      * For the ones the amph can move into (nothing blocking), create a new game state from this
      * If not, then...
  * The amph is temporarily stuck - do nothing
* If all the amphs are stuck then the game state is stuck - get rid of the game state


## Optimisations
* Use a DFS
  * DFS vs BFS - why use a DFS?
  * BFS seems like it would make the most sense - after all, aren't we looking for the lowest energy?
  * However, consider that if all amphipods are in non-settled positions to start, it's going to take 16 (or close to 16) moves to move the amphipods whatever happens
  * If your BFS is based on move-number as the "breadth" than you're going to basically have to go through the entire search space to find the lowest energy
  * and a BFS won't allow you to take care of a key optimisation that a DFS will
    * A DFS will let you record an overall energy state right away. You can use this to discard energy states that go over this value immediately.
* Use a priority queue of number of amphipods settled, and then type of amphipod settled (assign weight)
* If the energy has already gone over the count, scratch that game state entirely and move on
* Implement a state cache
  * Consider that A moving to hallway space 1 and then B moving to hallway space 2 is the same as B moving to hallway space 2 and then B moving to 1
  * Is A1 moving to hallway space 1 and A2 moving to hallway space 2 is the same as A1 moving to hallway space 2 and A2 moving to hallway space 1?
    * No because they start at very different places. The exact amphipod is key
* Enums are very slow