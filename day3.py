"""
--- Day 3: Toboggan Trajectory ---

With the toboggan login problems resolved, you set off toward the airport.
While travel by toboggan might be easy, it's certainly not safe: there's very
minimal steering and the area is covered in trees. You'll need to see which
angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer
coordinates in a grid. You make a map (your puzzle input) of the open squares
(.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
These aren't the only trees, though; due to something you read about once
involving arboreal genetics and biome stability, the same pattern repeats to the
right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->

You start on the open square (.) in the top-left corner and need to reach the
bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper
model that prefers rational numbers); start by counting all the trees you would
encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3
and down 1. Then, check the position that is right 3 and down 1 from there, and
so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where
there was an open square and X where there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
In this example, traversing the map using this slope would cause you to
encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3
and down 1, how many trees would you encounter?


--- Part Two ---
Time to check the rest of the slopes - you need to minimize the probability of a
sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following
slopes, you start at the top-left corner and traverse the map all the way to the
bottom:

Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s)
respectively; multiplied together, these produce the answer 336.

What do you get if you multiply together the number of trees encountered on each
of the listed slopes?

###############################################################################
We can do this by working out which index of a 2D array we'll need
We also need to know how many copies to the right to "glue" on
"""
import numpy as np
import pandas as pd

def nearTrees(fn, right, down):
    # Open the file but just read the first line
    with open(fn) as f:
        firstLine = f.readline()

    # How many characters are in a line? Make sure to remove the '\n'
    lineLen = len(firstLine.split('\n')[0])

    # Read the data into a 2D array
    df = pd.read_fwf(fn, header=None, widths=[1]*lineLen).to_numpy(dtype='S1')

    # How many times are we going down per step / need to go down?
    numSteps = np.ceil(df.shape[0]/down)

    # How many moves right will we do in that time?
    rightMoves = numSteps*right

    # How many copies of the array do we need?
    copies = np.int(np.ceil(rightMoves/df.shape[1]))

    # Make the copies of the array
    df = np.tile(df, copies)

    # Set the initial index
    ind = np.array([[down,right]])

    # We just have to multiply the index by the number of steps we do, e.g.
    # 3,1 and 6,2 and 9,3 is just 3,1*1, *2 and *3.
    factors = np.repeat(np.array(np.arange(1,numSteps),ndmin=2),2,axis=0)
    idx = np.repeat(ind, numSteps-1, axis=0)*factors.T
    idx = np.array(idx, dtype=int)

    # Now just pull out of the grid those indices
    vals = df[idx[:,0], idx[:,1]]

    # Cound the trees ('#')
    return len(np.where(vals == b'#')[0])

if __name__ == "__main__":
    fn = 'day3.dat'

    print(nearTrees(fn, 3, 1))

    rights = [1,3,5,7,1]
    downs = [1,1,1,1,2]
    tries = len(downs)
    treeHits = np.zeros(tries)
    for i in np.arange(tries):
        treeHits[i] = nearTrees(fn, rights[i], downs[i])

    print(np.product(treeHits))
