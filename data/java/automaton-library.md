type: article
title: Automaton Java Library
last-updated: 2017-07-12
meta-keywords: Automaton, Java, GitHub, Fork

The Automaton Java Library is a full-featured, high-performance regular expression matching library written in Java. It supports both deterministic finite automata (DFAs) and Non-deterministic Finite Automata (NFAs). The library is designed to be efficient, scalable, and easy to use.

One of the key features of the Automaton Java Library is its support for high-volume multi-threaded applications. The library is able to efficiently match regular expressions against large amounts of data, even in multi-threaded environments. This is due to the library's use of a number of optimization techniques, such as lazy evaluation and memoization.

I forked the library to add performance optimizations for high-volume multi-threaded applications, in particular with certain regular expressions what would enter into a dead-loop cycle.

My fork of `automaton` Java Library is at [github.com/davipt/automaton](https://github.com/davipt/automaton/tree/davipt).
