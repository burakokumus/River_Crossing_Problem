'''
CS 461 - Artificial Intelligence - Fall 2020 - Homework 1
Professor: Varol Akman
Group Name: PROMINI
Group Members:
    -Hakkı Burak Okumuş
    -Göksu Ece Okur
    -Yüce Hasan Kılıç
'''

'''
READ BEFORE RUNNING:
    Toggle TRACE_MOD on line 35 if you want to observe intermediate steps
    Assign number of initial people on sides and the boat size starting from line 158 for different problems
'''

'''
Node class represents a single state in River Crossing Problem.
Program creates all valid children (next states) that are not visited yet from a given node
Uses Depth First Search (DFS) approach to solve the problem.
Tree data structure is used to represent paths and find a solution (not necessarily the optimal one).
Tries to reach to a leaf node following the same branch until it is exhausted. 

Constraints for creating next states
    1. Boat cannot carry more than its size
    2. Boat cannot move while it is empty
    3. Boat cannot pick up nonexisting people on the side that it is leaving
    4. There cannot be more Cannibals than Missionaries on board
    5. There cannot be more Cannibals than Missionaries when boat leaves
    6. Already visited states must not be regenerated
    7. There is no next state when everyone is on the right side.
'''

# Allows single stepping when True
TRACE_MOD = False

class Node:

    def __init__(self, left_missionary, right_missionary, left_cannibal, right_cannibal, boat_size, boat_location = 1, path = [], children = []):
        self.left_missionary = left_missionary
        self.right_missionary = right_missionary
        self.left_cannibal = left_cannibal
        self.right_cannibal = right_cannibal
        self.boat_size = boat_size
        self.boat_location = boat_location # 1 denotes left 0 denotes right.
        self.path = path
        self.children = children
    
    # Generates all valid children that do not violate constraints
    def generate_child(self):
        # first try to send a full boat, if that does not work, reduce passenger number by 1
        # because of the limits of these loops, boat size constraints cannot be violated
        for i in range(self.boat_size, 0, -1): 
            # first try to send i cannibals, if that does not work, reduce 1 cannibal and add 1 missionary
            for j in range(0, i + 1):
                # Boat cannot carry more C than M
                if j > 0 and i - j > j:
                    continue
                new_path = self.path[:]
                new_path.append(self)
                if self.boat_location == 1: # send boat to right
                    new_location = 0
                    new_node = Node(self.left_missionary - j, self.right_missionary + j, self.left_cannibal - i + j, self.right_cannibal + i - j, self.boat_size, new_location, new_path, [])
                
                else: # send boat to left
                    new_location = 1
                    new_node = Node(self.left_missionary + j, self.right_missionary - j, self.left_cannibal + i - j, self.right_cannibal - i + j, self.boat_size, new_location, new_path, [])

                # CONSTRAINT: Boat cannot carry nonexisting people on the side that it is leaving
                if new_node.left_cannibal < 0 or new_node.left_missionary < 0 or new_node.right_cannibal < 0 or new_node.right_missionary < 0:
                    continue

                # CONSTRAINT: Boat cannot leave more C than M

                if new_node.left_cannibal > new_node.left_missionary and new_node.left_missionary > 0:
                    continue

                # CONSTRAINT: There can not be more C than M at the destination
                if new_node.right_cannibal > new_node.right_missionary and new_node.right_missionary > 0:
                    continue
                
                # CONSTRAINT: Already visited states must not be regenerated
                if new_node in new_node.path:
                    continue
                    
                # If new node does not violate constraints, add it to node's children
                self.children.append(new_node)
    
    # Recursive function that solves River Crossing Problem
    # Depth is the current level of the node, root node is considered at level 1
    def solve(self, depth = 1):
        
        if TRACE_MOD and depth == 1:
            print("Initial state:")
            print(self)
            input("Press enter to proceed\n")
        
        # Boolean variable to stop the program if we reach a solution 
        solution_found = False

        # Base case
        if self.left_missionary == 0 and self.left_cannibal == 0: # All people are on the right side

            if TRACE_MOD:
                input("{}Solution found. Press enter to see the solution\n".format("  " * depth))

            print('Solution: ')
            for n in self.path:
                print(n)
            print(self)
            return True
        
        # Generate children nodes
        self.generate_child()

        if TRACE_MOD and len(self.children) == 0: # If there is no new child
            print("{}No new child available. Backtracing...\n".format("  " * depth))
            return False

        # Try to solve problem for each children
        for child in self.children:

            if TRACE_MOD:
                if self.boat_location == 0:
                    print("{}Carrying {} cannibals and {} missionaries to left".format("  " * depth, (self.right_cannibal - child.right_cannibal), (self.right_missionary - child.right_missionary)))
                if self.boat_location == 1:
                    print("{}Carrying {} cannibals and {} missionaries to right".format("  " * depth, (self.left_cannibal - child.left_cannibal), (self.left_missionary - child.left_missionary)))
                print("  " * depth + child.__repr__())
                input("{}Press enter to proceed\n".format("  " * depth))

            # Solve the child and increase the depth.  Do not try the next sibling until this branch is exhausted (DFS Algorithm)  
            solution_found = child.solve(depth + 1)

            # Return if we found a solution
            if solution_found:
                return True
        
        # If we trace back to the root node and there is no unvisited child
        if depth == 1:
            print("No solution found")
        return False
         
    def __repr__(self):
        return ('left: {}M {}C    right: {}M {}C    boat: {}'.format(self.left_missionary, self.left_cannibal, self.right_missionary, self.right_cannibal, self.boat_location))     

    def __eq__(self, other):
        if (
            self.left_missionary == other.left_missionary and 
            self.left_cannibal == other.left_cannibal and 
            self.right_missionary == other.right_missionary and
            self.right_cannibal == other.right_cannibal and
            self.boat_location == other.boat_location
           ):
            return True
        return False

if __name__ == "__main__":

    no_of_m_right = 0 # Number of missionaries on right, initially
    no_of_m_left  = 0 # Number of missionaries on left, initially
    no_of_c_right = 0 # Number of cannibals on right, initially
    no_of_c_left  = 0 # Number of cannibals on left, initially
    boat_size     = 0 # Boat size

    input("Press enter to solve Question 1\n")

    # QUESTION 1
    print("Solving Question 1\n")
    problem_one = [5, 0, 5, 0, 3]
    no_of_m_right, no_of_m_left, no_of_c_right, no_of_c_left, boat_size = problem_one
    # Create the initial state
    root_node = Node(no_of_m_right, no_of_m_left, no_of_c_right, no_of_c_left, boat_size, 1, [], [])
    # Solve
    root_node.solve()

    '''
    Solution for Q1

    left: 5M 5C    right: 0M 0C    boat: 1
    left: 5M 2C    right: 0M 3C    boat: 0
    left: 5M 4C    right: 0M 1C    boat: 1
    left: 5M 1C    right: 0M 4C    boat: 0
    left: 5M 3C    right: 0M 2C    boat: 1
    left: 5M 0C    right: 0M 5C    boat: 0
    left: 5M 2C    right: 0M 3C    boat: 1
    left: 2M 2C    right: 3M 3C    boat: 0
    left: 3M 3C    right: 2M 2C    boat: 1
    left: 0M 3C    right: 5M 2C    boat: 0
    left: 0M 5C    right: 5M 0C    boat: 1
    left: 0M 2C    right: 5M 3C    boat: 0
    left: 0M 4C    right: 5M 1C    boat: 1
    left: 0M 1C    right: 5M 4C    boat: 0
    left: 0M 3C    right: 5M 2C    boat: 1
    left: 0M 0C    right: 5M 5C    boat: 0
    '''

    input("\nPress enter to solve Question 2a\n")

    # QUESTION 2a)
    print("Solving Question 2a\n")
    problem_two_a = [6, 0, 6, 0, 4]
    no_of_m_right, no_of_m_left, no_of_c_right, no_of_c_left, boat_size = problem_two_a

    # Create the initial state
    root_node = Node(no_of_m_right, no_of_m_left, no_of_c_right, no_of_c_left, boat_size, 1, [], [])
    root_node.solve()

    '''
    Solution for Q2a

    left: 6M 6C    right: 0M 0C    boat: 1
    left: 6M 2C    right: 0M 4C    boat: 0
    left: 6M 5C    right: 0M 1C    boat: 1
    left: 6M 1C    right: 0M 5C    boat: 0
    left: 6M 4C    right: 0M 2C    boat: 1
    left: 6M 0C    right: 0M 6C    boat: 0
    left: 6M 3C    right: 0M 3C    boat: 1
    left: 3M 3C    right: 3M 3C    boat: 0
    left: 4M 4C    right: 2M 2C    boat: 1
    left: 2M 2C    right: 4M 4C    boat: 0
    left: 3M 3C    right: 3M 3C    boat: 1
    left: 1M 1C    right: 5M 5C    boat: 0
    left: 2M 2C    right: 4M 4C    boat: 1
    left: 0M 0C    right: 6M 6C    boat: 0
    '''
