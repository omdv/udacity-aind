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


## Week 3 - Lesson 11 (Search)
* Definition of a problem (states, actions, goals, costs, etc)
* Frontier, explored region and unexplored region
* Tree search methods are similar, the difference is in how you choose the action
* Breadth-first search - shortest path always, first found may suffice and be a solution (one of)
* Uniform cost (or cheapest first) search - continues to search until the path is removed from frontier, guaranteed
* Depth-first search - expand the longest path first, not guaranteed to find the optimal path
* All the above algos are non-efficient time-wise as they explore in all directions, need additional knowledge
* The best knowledge for search is distance to the goal
* Greedy best-first search uses the distance, effective but cannot handle barriers
* A* - minimum of g+h (path cost + distance of the final state of the path to the distance to the goal), could also be called
best estimated total path cost first
* For Search to work domain should have some characteristics: fully observable, known (know available actions), discrete (a limited set of actions to choose from), deterministic (know the result of taking an action), static (only our actions change the world)
* To implement we define node with state, action, cost and parent, frontier is defined as set, should be able to remove members, add new and do a membership test, priority queue.

## Week 4 - Lesson 12 (Simulated Annealing)
* Techniques to solve very complex problems by trying simple heuristics first
* Example of travelling salesman of n-queens problems - initiate randomly, move pieces with largest number of conflicts and iterate
* The issue is the local maxima/minima, solution is to do a random restart
* Random restart with many attempts. Use Taboo search to avoid areas which were explored
* Step-size selection - typical for optimization problems
* Simulated annealing - "heating" and "cooling" the system to achieve the "minimum energy level" or global minima/maxima. Heating in this context means increasing randomness and cooling vice versa.
* Local beam search - variation of random restart but with N particles, which further exchange information between them by being compared. We choose only the best.
* Generic algorithms - crossovers, mutation, etc

## Week 5 - Lesson 13 (Constraint Satisfaction)
* Constraint optimization techniques - backtracking optimization and forward checking.
* Some heuristics may be applied to backtracking, such as least constraining value, minimum remaining values
* Structured CSPs - tricks to divide problem into smaller pieces or acyclic graphs to reduce complexity

## Week 6 - Lesson 14 (Login and Reasoning)
* Peter Norvig's vision of future directions for planning algorithms: learning from examples, transfer learning, interactive planning (human + machine), explaining things in terms human can understand
* Propositional logic to define models between events/variables. Truth tables.
* Limitations of P.L. - can handle only binary values, can't handle uncertainty, can't cover physical world objects, no shortcuts to cover many things happening at the same time
* First order logic extent P.L. as it introduces relations, objects and functions which can describe the world, while P.L. had only facts
* FOL models contain constants, where multiple constants can refer to the same object and functions, which map objects to objects

## Week 7 - Lesson 15 (Planning)
* Planning requires some interaction with the environment during execution phase
* In stochastic worlds it is helpful to operate in the space of belief states
* Conformant plans require no information about the world
* Partially observable world
* In stochastic environments actions tend to increase the uncertainty, while observations tend to bring it back down
* Classical planning representation: state space, world state, belief state, action schema (part 12)
* Progression state search
* Our classical planning representation allows us to use regression search
* Regression vs progression - depends on the goal
* Plan space search - used to be popular in 1990s.
* Forward search is more popular now, because it allows to come up with better heuristics
* The classical planning representation allows to do automatic heuristics search by relaxing some of conditions automatically and search through it
* Situation Calculus - can't apply Classical Planning to all cargo. S.C. allows it with First Order Logic

## Week 8 - Lesson 16 (Probabilities & Bayes Networks)
* Bayes networks are the building blocks of more advanced AI techniques, like particle filters, Kalman, etc
* Conditional probabilities refresher

## Week 9 - Lesson 17 Bayes Nets
* Bayes nets statement:
 * We know the prior about A - P(A), but A is not observable
 * B is observable and we know P(B|A) and P(B| notA)
 * We need to do the diagnostic reasoning, i.e. P(A|B) and P(A| notB)
* Two test cancer quiz:
 * P(C)=0.01, P(+|C)=0.9, P(+,!C)=0.8, P(C|++)?
 * Using [tabular approach](http://www.greenteapress.com/thinkbayes/thinkbayes.pdf) is the easiest
 * P(++|C) = P(+|C) * P(+|C) assuming conditional independence
* Other techniques - conditional independence, total probability conditioned on 1
* Explaining away - if there is an effect explained by multiple causes and one cause is already observed then it is less likely that other causes had an effect
* Complex conditional probabilities like P (A | B,C) can be expanded using simple Bayes rule, i.e. P(A|B) = P(B|A)P(A)/P(B) where all variables are given C, i.e. p(A|B,C) = p(B|A,C)p(A|C)/p(B|C)
* Bayes nets use the graph representation which allows to represent complex networks with small number of joint probability distributions
* D-separation for independence, explain away may bring dependence into a pair of previously independent variables

## Week 10 - Lesson 18 Inference in Bayes Nets (Exact inference)
* Evidence, query and hidden variables
* We are looking for probability of one or more query variables given some values for one or more evidence variables - P(Q1, Q2 | E1=e1, E2=e2)
* Enumeration technique, but can be slow for large bayes nets
* Speeding up techniques: Pulling out, maximizing independence
* Bayes nets are the most compact and easiest to work if they are written in causal direction
* Variable elimination technique - step by step factor multiplication

## Week 11 - Approximate Inference
* Use sampling to get joint probability distributions. This also let us build the conditional probability tables
* Gibbs sampling using MCMC

## Week 11 - Lesson 19 Hidden Markov Models
* Time series pattern recognition
* A lot of human activities fall in domain of pattern recognition through time series
* How to match two signals - use delta frequency for freq matching and dynamic time warping for matching across time
* [Dynamic time warping myths](http://wearables.cc.gatech.edu/paper_of_week/DTW_myths.pdf)
* HMM training - break your sequence into a number of states, calculate prob distribution, calculate transition probabilities, update boundaries and so forth until convergence
* Baum Welch - variation of the expectation maximization process
* Any distribution may be represented by a mixture og Gaussians
* Choosing HMM topology
* Different specific tricks: Context grammar and statistical grammar combined reduce the error rate by 8
* HMMs are generally bad for generating data, while good at classifying it - the problem is that the output has no continuity.

# Term 2 - Deep Learning

## Week 1 - Deep NN
* Usual NN explanations - AND, OR, NAND, XOR, etc
* Using graphical representation to explain the separation of classes
* Moving line towards misclassified points with learning rate
* Error functions, gradient descent, error function needs to be continuous for GD
* Sigmoid is needed vs step function to give a continuous change, good explanation of activation functions overall
* Softmax for multiclass problems - normalized exponents of linear outputs
* One-hot encoding
* Maximum likelihood (log-likelihood is required to get rid of products of probabilities)
* Cross-entropy is the negative sum of log of probabilities. Good model - low cross-entropy. Misclassified points have higher negative log of probability, because log of probability of 1 is zero. Cross-entropy is the sum of all outcome probabilities times the outcome for all samples. Essentially we are adding probabilities only of the events that have occured by multiplying log of probability by the label for the event.
* Logistic regression - explanation is based on error function described earlier, which is a mean of log of probabilities times label
* Gradient descent calculations - analytical derivations. For logistic regression the gradient turns out to be just the scalar times coordinates of the point, where scalar is just the difference between the label and the prediction. Updating weights and bias becomes as simple as just multiplying learning rate (normalized by number of points) by coordinates. GD algo is similar to previously discussed Perceptron algo.
* Perceptron just draws a line or hyperplane given weights for each input and bias and determines if given point is positive or negative (activation function -> sigmoid vs step function)
* Neural networks (or MLP) - combining first level models to get more complex models, using weights for previous models to achieve the right combination, applying activation functions (sigmoid) to get continuous probability and also cut-off probability at one.
* NN architecture - nodes equal to problem dimension, output equal to a number of classes needed to be classified.
* Feedforward - forward calculation to get the error function for the whole network
* Backprop - feedforward with gradient descent. Calculating derivatives at each layer, use chain rule for derivatives.
* Bias vs variance - it is better to stay on overcomplicated side and implement some techniques to prevent overfittting
* Early stopping - stop when test error starts to increase
* Regularization - we don't want too certain models, because their activation function has too steep curve in the vicinity of zero and as such are difficult to be handled by gradient descent. Large coefficients cause the overfitting. Regularization punishes big coefficients. L1 or L2 regularization. L1 regularization is better for feature selection, L2 is better for training models.
* Dropout - randomly turning off some nodes during the training to let other nodes train and train the whole network more uniformly.
* Vanishing gradient with sigmoid function - either tanh or relu.
* Random restarts to solve the local minimum problem.
* Momentum to skip small humps to not get stuck in local minima - work really well in practice.