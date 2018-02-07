\title{Research Review}
\author{Oleg Medvedev}
\date{February, 2018}
\maketitle

## Introduction
The purpose of this report is to provide a brief overview of few major historical developments in the area of AI planning. This report is based on several references, including \cite{AIMA}, \cite{overview1} and \cite{overview2}.

It is impossible to not start any overview of AI planning field without mentioning the STRIPS (Stanford Research Institute Problem Solver) planning system, developed in 1971 by Fikes and Nilsson, so this will be the first development described in this report. The influence of STRIPS was significant due to its representation, rather than the algorithm itself. It defined the "classical" representation of the AI planning problems and kicked off the development of several languages, which culminated in the development of PDDL (Problem Domain Description Language) in 1998 which became a standard approach for representing planning problems, so it will be the second development described here. Finally we'll review the GRAPHPLAN system, developed by Blum and Furst in 1995 and 1997 which tries to solve the problem by backward chaining starting from the description of the goal.

## STRIPS
STRIPS was the algorithm developed in 1971 in Stanford Research Institute. As was mentioned earlier the language proposed by authors to describe the planning problem had by far larger influence on the AI planning field than the algorithm itself. STRIPS defines state variables, as the one having either TRUE or FALSE values. The action is defined as an operator, consisting of three sets of state variables - PRECONDITION, ADD and DELETE. GOAL is also expressed as the set of state variables. Any STRIPS instance is a combination of propositional variables or conditions, set of operators (each consisting of three sets, as described above), initial state and goal state. It is assumed that there exists a sequence of operators, which can transform the problem world into the goal state, so the goal is to find this sequence of operators, or a plan. Such definition allows to use various searching algorithms to find the right sequence of actions. For a while the combination of STRIPS representation with various search techniques and different heuristics was the only available approach to solve planning problems.

## PDDL
PDDL initiative was focused on providing a universal and consistent way to describe planning problems. While it did not provide any new algorithms by itself it enabled a much faster progress in the field by providing a standard framework to compare various models. In fact one of the reasons for its innception in 1998 was to enable the International Planning Competition, which has been hosted every year since 1998. 

PDDL was heavily inspired by STRIPS and went through several iterations (current version is 3.1) and inspired several followers. The main contribution of PDDL was the separation of domain description from the problem description, which essentially allows multiple problem definitions for the same domain. It also introduced PRECONDITIONS which may be any Boolean combination of simple atomic facts. The action EFFECTS can also be conditional. As a result the PDDL description is much more compact and informative compared to STRIPS.

It is worth noting again, however, that PDDL itself have not provided any improvements in the search algorithms, it just enabled the easier comparison of different techniques and methods.

## GRAPHPLAN
GRAPHPLAN invented in 1995 by Blum and Furst approached the problem by traversing the search tree backwards, starting from the goal state. GRAPHPLAN uses the different representation of the planning problem. Instead of placing states in nodes and connecting them with possible actions as edges GRAPHPLAN puts actions and atomic facts in alternate levels (action levels and state levels). The edges or connections between levels are of different kind, depending which levels are being connected. It can either connect atomic facts to actions, for which the facts are a precondition. Or it can connect actions to atomic facts, which are made either true or false as a result of this action. The graph is then constructed iteratively, while ensuring that there is no goal state at each of the state levels. So essentially GRAPHPLAN considers all plans of length 0, 1, 2 and so on.

It is worth noting that GRAPHPLAN is quite similar to SATPLAN (Planning as Satisfiability) method, proposed in 1996 by Kautz and Selman, which constructs a Boolean satisfiability problem from a given STRIPS or PDDL definition and iteratively considers plans of increasing lengths for satisfiability. GRAPHPLAN, SATPLAN and few others are considered a new family of so-called constraint-based algorithms compared to traditional search-based techniques.

## Summary
AI planning is a continuously evolving field. STRIPS and PDDL representation languages facilitated the development of various methods in this area. In the early days majority of the methods were involving the search-based algorithms. In late 1990s several new methods were proposed, approaching the problem differently and trying to find the solution by considering various constraints and changing the representation of the problem space. Some of the latest studies, discussed in \cite{AIMA} indicate that both search-based and constraint-based methods may be viable, depending on the domain and there is no one-size-fits-all solution.


\begin{thebibliography}{999}

\bibitem{AIMA}
  Stuart Russell, Peter Norvig,
  \emph{Artificial Intelligence: A Modern Approach}.
  3rd Edition,

\bibitem{overview1}
  Jussi Rintanen, Jorg Hoffmann,
  \emph{An overview of recent algorithms for AI planning}

\bibitem{overview2}
  Jussi Rintanen
  \emph{A brief overview of AI planning}
  https://users.aalto.fi/~rintanj1/planning.html

\end{thebibliography}
