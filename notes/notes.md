# Term 1
## Week 1 - Lesson 1 (Intro and logistics)
- [x] Slack channel
- [x] Forum

* Waffle.io for project management/bug tracking
* gh-pages branch for sharing on github-pages
* linking code rather than pasting

## Week 1 - Lesson 2 (Setting up environment)
* Math refresher (optional)
  * [Udacity linear algebra refresher](https://classroom.udacity.com/courses/ud953)
  * Lessons 1, 3 and 6 of [Udacity Intro to Algos](https://www.udacity.com/course/intro-to-algorithms--cs215)

- [x] Udacity project assistant?

## Week 1 - CS215 (Intro to Algos deviation)

### Lesson 1 - Intro
* nodes and edges
* Eulerian path - moving along all edges once
* Starting and ending nodes with odd degrees
* Eulerian path always exists for graphs with all nodes with odd degrees (Eulerian tour)

### Lesson 3 - Simple Graph Theory
* Euler formula (nodes+regions-segments = 2)
* Different types of graphs (cliques, trees, hypercubes, etc)
* Clustering coefficient - degree between star (=0) and clique (=1), roughly a ratio of connections between neighbors of v and degree of v squared.
.... Continue


## Week 1 - Lesson 3 (Career Profile)
- [ ] Update udacity Career Profile
- [ ] Visit Extracurricular section and take two courses

## Week 1 - Lesson 4 (Intro to AI)
* Heuristic - additional logic, constraint which prompts brute-force to act more effficiently
* A* search algorithm for pathfinding. Improvement over Dijkstra due to heuristic.
* When choosing the best representation for the game model choose the one moving the problem to action-solution space in a way. E.g. for tic-tac-toe use every position as a node and edges between them if there is a legal move.
* Pruning the search tree with the help of heuristics
* Mini-max search and adversarial search - maximizing your chances during your turn and opponent minimizing chances during their turn.
* Definition of agent, environment, states and goal state
* Agent has perception to interact with environment, use cognition to take action to change environment
* Intelligent agent is the one that takes actions to maximize it's utility given a desired goal, i.e. rational behavior, however agent cannot behave optimally always, so we define "bounded optimality" to quantify the intelligence
- [ ] Get [AIMA book](https://www.amazon.com/Artificial-Intelligence-Modern-Approach-3rd/dp/0136042597)

## Week 1 - Lesson 5 (Applying AI to Sudoku)
* [Blog post by Peter Norvig](http://norvig.com/sudoku.html)
* Encoding the problem, coordinates, peers based on the rules we want to implement later
* Techniques:
  * Elimination
  * Only choice (i.e. in 3x3 square)

## Week 1 - Lesson 6 (Environment setup)
* Ended up installing pyenv to manage python installations
* pyenv virtualenv wrapper allows to activate conda environments

## Sudoku Project Summary
* Constraint propagation for heuristics
* Search for complex cases (depth first search)

## Week 2 - Lesson 8 (Playing Isolation game)
* Book of opening moves. How to choose best opening automatically - minmax algorithm.
* Min and max levels - our bot is trying to maximize his chances and opponent always plays perfectly to minimize it.
* Branching factor and depth of the search tree to estimate the time required to solve the game
* Typically b^d is too large to completely explore the whole tree
* Depth-limited search to estimate the max-depth for a given average branching factor to have acceptable "wait time"
* Start from the bottom of the tree. For each max node pick the maximum value along the child nodes, and vice-versa.
* Quiescent search - sensitivity analysis as to how results change based on how many level limitations we have. Choose the one after which results are stable.

## Week 2 - Lesson 9 (Advanced Game Playing)
* Iterative deepening - include next level consideration only if time allows
* Depth of possible search with ID may vary with branching factors and be different in different phases of the game
* Horizon effect
* Explore other evaluation functions and choose best for the game
* Alpha-Beta pruning - ignore subtrees which do not change results at higher tree level.
* Tips for 5x5 Isolation agent - symmetry, book of opening moves, reflection, separation, order nodes correspondingly to optimize pruning
* Multi-player isolation - no minimax, propagate values based on each players selection at every level
* For probabilistic games just add a probability for each branch and do minimax with probability accounted for

