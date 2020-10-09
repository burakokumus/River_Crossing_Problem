TRACE_MOD = False

class Node:
    def __init__(self, left_missionary, right_missionary, left_cannibal, right_cannibal, boat_size, boat_location = 1, path = []):
        self.left_missionary = left_missionary
        self.right_missionary = right_missionary
        self.left_cannibal = left_cannibal
        self.right_cannibal = right_cannibal
        self.boat_size = boat_size
        self.boat_location = boat_location
        self.path = path

    def generate_next(self):
        if TRACE_MOD:
            print(self)
        # base case
        if self.left_missionary == 0 and self.left_cannibal == 0:
            print('base case')
            for n in self.path:
                #print(n.left_missionary, n.left_cannibal, n.right_missionary, n.right_cannibal, n.boat_location)
                print(n)
            return True

        # CONSTRAINT: Boat cannot carry nonexisting people on the side that it is leaving
        if self.left_cannibal < 0 or self.left_missionary < 0 or self.right_cannibal < 0 or self.right_missionary < 0:
            return False

        # CONSTRAINT: Boat cannot leave more C than M
        if self.left_cannibal > self.left_missionary and self.left_missionary > 0:
            return False

        #CONSTRAINT: There can not be more C than M at the destination
        if self.right_cannibal > self.right_missionary and self.right_missionary > 0:
            return False
        
        #CONSTRAINT: Already visited states must not be regenerated
        if self in self.path:
            return False
            
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
                    new_node = Node(self.left_missionary - j, self.right_missionary + j, self.left_cannibal - i + j, self.right_cannibal + i - j, self.boat_size, new_location, new_path)
                    if TRACE_MOD:
                        print("Carrying {} cannibals and {} missionaries to right".format(i - j, j))
                        input("Press Enter to proceed")
                else: # send boat to left
                    new_location = 1
                    new_node = Node(self.left_missionary + j, self.right_missionary - j, self.left_cannibal + i - j, self.right_cannibal - i + j, self.boat_size, new_location, new_path)
                    if TRACE_MOD:
                        print("Carrying {} cannibals and {} missionaries to left".format(i - j, j))
                        input("Press Enter to proceed")

                if new_node.generate_next():
                    return True
                

    def __eq__(self, other): # Tested, works
        if (
            self.left_missionary == other.left_missionary and 
            self.left_cannibal == other.left_cannibal and 
            self.right_missionary == other.right_missionary and
            self.right_cannibal == other.right_cannibal and
            self.boat_location == other.boat_location
           ):
            return True
        return False

    def __repr__(self):
        return ('left: {}M {}C    right: {}M {}C    boat: {}'.format(self.left_missionary, self.left_cannibal, self.right_missionary, self.right_cannibal, self.boat_location))

if __name__ == "__main__":
    n1 = Node(5, 0, 5, 0, 3)
    n1.generate_next()
    pass
