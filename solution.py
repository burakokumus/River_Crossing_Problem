# Allows single stepping when True
TRACE_MOD = False

'''
Node class represents a single state in River Crossing Problem.
'''
class Node:
    def __init__(self, left_missionary, right_missionary, left_cannibal, right_cannibal, boat_size, boat_location = 1, path = [], children = []):
        self.left_missionary = left_missionary
        self.right_missionary = right_missionary
        self.left_cannibal = left_cannibal
        self.right_cannibal = right_cannibal
        self.boat_size = boat_size
        self.boat_location = boat_location
        self.path = path
        self.children = children
    

    def generate_child(self, depth):
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
    
    def solve(self, depth = 1):
        
        if TRACE_MOD and depth == 1:
            print("Initial state:")
            print(self)
            input("Press Enter to proceed")
        
        # Boolean variable to stop the program if we reach a solution 
        solution_found = False

        # Base case
        if self.left_missionary == 0 and self.left_cannibal == 0: # All people are on the right side

            if TRACE_MOD:
                input("{}Solution found. Press Enter to see the solution".format("  " * depth))

            print('Solution: ')
            for n in self.path:
                print(n)
            print(self)
            return True
        
        # Generate children nodes
        self.generate_child(depth)

        if TRACE_MOD and len(self.children) == 0: # If there is no new child
            print("{}No new child available. Backtracing...".format("  " * depth))
        
        # Try to solve problem for each children
        for child in self.children:

            if TRACE_MOD:
                if self.boat_location == 0:
                    print("{}Carrying {} cannibals and {} missionaries to left".format("  " * depth, (self.right_cannibal - child.right_cannibal), (self.right_missionary - child.right_missionary)))
                if self.boat_location == 1:
                    print("{}Carrying {} cannibals and {} missionaries to right".format("  " * depth, (self.left_cannibal - child.left_cannibal), (self.left_missionary - child.left_missionary)))
                print("  " * depth + child.__repr__())
                input("{}Press Enter to proceed".format("  " * depth))

            # Solve the child and increase the depth    
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
    no_of_m_right = 6
    no_of_m_left = 0
    no_of_c_right = 6
    no_of_c_left = 0
    boat_size = 5

    n1 = Node(no_of_m_right, no_of_m_left, no_of_c_right, no_of_c_left, boat_size)
    n1.solve()

    pass