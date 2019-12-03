# The Genetic Algorithm

## So what exactly does this do?

This my attempt to learn and implement a genetic algorithm. [I succeeded! Here's a video of it running](https://youtu.be/JW3IRKXpUCs)

Specifically, this is a Python implementation of the genetic algorithm to find an arithmetic expression consisting of 9 or less operators (can be modified by changing `NUM_GENES` on line 4) that evaluates to a particular number. I've set it to 42, though that can be changed by changing the `TARGET` variable on line 10.

As the program runs, you'll see what generation the program is currently on, the average arithmetic result in the population (a measure of the overall fitness of the population), and the best current result (which tells you how close your program may be to converging, since you only need one solution).

## Inspiration
I was inspired to learn about genetic algorithms by this [YouTube video](https://www.youtube.com/watch?v=qv6UVOQ0F44) that shows a program learning to play a Mario level using the genetic algorithm. So freakin' cool!

I used [this website](http://www.ai-junkie.com/ga/intro/gat1.html) to learn how the genetic algorithm works. This repo is an implementation of the exercise suggested by that tutorial.

## Requirements

- Python
- The `numpy` package

## How to run it

1. Make sure the `numpy` package is installed in your python's environment.
2. Adjust `TARGET` on line 10 as desired.
3. Run `python genetic.py`

## Thoughts
Sometimes the expressions come out wonky. For example, I just ran it and got '6+++36' which doesn't look readable to humans, but because the algorithm judges a valid gene based on Python's inbuild `eval()` function, it does make sense. The first `+` is an addition, and the next two are indicating that 36 is a positive number.

I've only tested this with the number 42. Setting `TARGET` to a decimal number or a prime number will make it harder for the genetic algorithm to converge since only integers are being used.

It's pretty cool seeing the algorithm converge on an expression that works, even though this application in particular isn't that exciting. Now that I understand genetic algorithms better, I hope to apply it to other areas, such as my robotics research. Feel free to play with the parameters defined at the top of the file to see if you can get it to converge faster. 

It's such a cool idea, though. I've read that simulated annealing is a more effective algorithm for these kind of search problems. Guess I will try to learn that next!
