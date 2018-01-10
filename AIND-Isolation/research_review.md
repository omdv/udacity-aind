---
title: "Review of AlphaGo Research Papers"
author: "Oleg Medvedev"
date: "December, 2017"
header-includes:
   - \usepackage[margin=1in]{geometry}
output:
    pdf_document
---
\begin{abstract}
Review of two research papers [1] and [2] authored by Google DeepMind, describing the evolution of their AlphaGo engine.
\end{abstract}


## Problem Statement
Until recently the game of Go remained as one of the only major classical games where expert human players remained undefeated against AI. Similar to chess the exhaustive search of actions space in Go is not feasible due to both the large breadth and depth of the game. Furthermore while the chess was principally "solved" by DeepBlue in 1996 Go due to it's larger action space (both due to larger depth and breadth) was believed to be at least a decade away.

Prior to DeepMind's work the two primary techniques used were the position evaluation to reduce breadth and Monte Carlo tree search (MCTS) for optimum policy to reduce depth. Both were sufficient to create Go agents able to play adequately at strong human amateur level and easily defeated by professional Go players.

## Novel Techniques
In it's first paper [1] authors utilized deep convolutional neural networks to create three networks for position evaluation and for prediction of the probability of the next move and one shallow network for fast policy rollout calculations. Please see the descriptions below.

#### Supervised Learning (SL) policy network
It is a 13-layer neural network trained on 30 million of positions from KGS Go Server. The goal is to be able to predict the human expert move in the given position. After training this model managed to achieve the 57% accuracy using all input features (total of 48, shown below) or 55.7% using only raw board position, which is a dramatic improvement over 44.4% of prior existing models.

![Network features](/Users/om/Documents/Udacity/AIND/AIND-Isolation/images/network_features.png)

#### Rollout policy
It is a shallow version of SL policy network, consisting of only linear softmax layer. It achieved a much lower accuracy of 24.2%, however was three orders faster than SL policy network (2$\mu$s vs 3ms). It used more features than SL policy network, see below.

![Rollout policy](/Users/om/Documents/Udacity/AIND/AIND-Isolation/images/rollout.png)

#### Reinforcement Learning (RL) policy network
This network was used in the 2nd stage of training pipeline. Its structure is identical to SL network. It was trained by playing games between randomly chosen different iterations of itself to further improve the SL network. The games were played to the terminal state and then result was back propagated to modify weight correspondingly. After training the RL policy network achieved 80% win rate against SL network and 85% win-rate against some of the available open-source Go programs.

#### Value network
Value network was used to perform a position evaluation, i.e. provide a +1 or -1 value for the current state. Once again it used the similar structure as policy networks. In order to train it without the overfitting (as it appeared to memorize all KGS games) authors generated a new self-play data set of 30 million positions. The MSE was around 0.22-0.23 for both training and test datasets. This model allows evaluating position with accuracy similar to Monte Carlo rollouts, but with 15,000 times less computation.


#### Combining everything
AlphaGo uses four described networks in standard MCTS algorithm (see image below). During the _selection_ phase the we select the edge of tree with the highest action value based on policy network. Once we reach the leaf node it may be expanded and is evaluated in two ways - by running the rollout to the end with the fast rollout policy and by using the value network. Both estimates are then mixed with some weight. The obtained result is then back propagated to all edges on the path. It is interesting that at least in the first games of AlphaGo with human experts the weaker SL policy was used instead of stronger one RL, as RL network was more focused on providing a single move, instead of giving a variety of promising moves and thus limiting exploration during MCTS.

![Monte Carlo tree search](/Users/om/Documents/Udacity/AIND/AIND-Isolation/images/alphago_mcts.png)

## Results
Single-machine AlphaGo has 99.8% success rate against available Go programs, and is at least few dans stronger. At the time of the publication the described model managed to win a 5 game match (5:0) with 2 professional dan (2p) player on a full board without handicap, which was never achieved before. It is known that shortly after the similar model with minor modifications managed to win 4 games and the overall match against one of the strongest 9p human player.

Overall, it may be concluded that authors combined several previously known techniques (CNN, RL, MCTS) into an effective framework, which managed to provide a step change in performance.

## AlphaGo Zero
In October, 2017 authors released a new paper [2], describing the continuation of their work. They developed a new agent, which they called AlphaGo Zero, which not only defeated the previous version described earlier, but did so without any prior human knowledge, i.e. _tabula rasa_. Let's review the main differences vs the paper described above.

The first difference is that authors combined the SL-policy and value network into one (in fact they already had similar architecture), which predicts both the probability of the next move and the current state of the board from 19x19 board and 17 features for a given board grid. These features are essentially just tracking whether there is a stone (and its color) in the given grid and the history for the given grid for the past 7 moves, which is important to treat the [Ko rule](https://senseis.xmp.net/?Ko) properly.

The second and much more important difference is the reinforcement learning part. Authors still use MCTS to output probabilities $\pi$ for each move at given state. They note that these probabilities are much stronger than probabilities predicted by policy network $p$, so MCTS may be considered as a powerful RL tool by itself. Thus they use MCTS as a self-play algorithm which predicts the best move $\pi$ based on neural network parameters and given state (the move is selected based the exponentiated visit count for each move). Neural network is initialized to random parameters and then a self-game is played at every iteration. During a self-game MCTS uses the neural network weights from previous iteration to predict the best moves $\pi$. Once the final result of the game is reaches, whether it's actual win or loss, or surpassing a length threshold or resignation threshold the neural network weights are updated to minimize the error between the prediction of the value network and actual game result and also to minimize the deviation between MCTS predicted moves $\pi$ and policy network predictions $p$.

![AlphaGo zero reinforcement learning algorithm](/Users/om/Documents/Udacity/AIND/AIND-Isolation/images/alphazero_mcts.png)

The results are shown on the image below extracted from author's paper. One may see that approximately only after 3 days of training AlphaGo Zero surpasses the AlphaGo Lee version which defeated one of the strongest human players Lee Sedol. Note that that version was trained on 30 million of positions and AlphaGo Zero started from zero prior knowledge. And after about 30 days of training it defeated AlphaGo Master which was still based on some prior knowledge and defeated a number of best human players while playing online. Truly remarkable result.

![AlphaGo Zero results](/Users/om/Documents/Udacity/AIND/AIND-Isolation/images/alphazero_results.png)

As a conclusion let me copy the last sentence from author's paper: _Humankind has accumulated Go knowledge from millions of games played over thousands of years, collectively distilled into patterns, prov-erbs and books. In the space of a few days, starting tabula rasa, AlphaGo Zero was able to rediscover much of this Go knowledge, as well as novel strategies that provide new insights into the oldest of games._

## References
[1] "Mastering the game of Go with deep neural networks and tree search", doi:10.1038/nature16961

[2] "Mastering the game of Go without human knowledge", doi:10.1038/nature24270
