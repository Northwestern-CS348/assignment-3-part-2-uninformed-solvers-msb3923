from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # If we are already at the victory state just return true

        #print(self.gm.getGameState())

        if self.currentState.state == self.victoryCondition:
            return True

        # Add all possible moves that can be taken from the given state to the states list of children
        # Iterate through all moves
        canMove = self.gm.getMovables()
        curr = self.currentState
        if canMove:
            for i in canMove:
                self.gm.makeMove(i)
                child_state = GameState(self.gm.getGameState(), curr.depth + 1, i)
                curr.children.append(child_state)
                child_state.parent = curr
                self.gm.reverseMove(i)
            for child in curr.children:
                if child not in self.visited:
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    break
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        curr_depth = self.currentState.depth
        foundCurr = False
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            index = self.currentState.nextChildToVisit
            if len(self.currentState.children) > index:
                foundCurr = True
                break
        if not foundCurr:
            for visited_state in self.visited.keys():
                visited_state.nextChildToVisit = 0
            curr_depth = curr_depth + 1
            if len(self.visited) == 1:
                for i in self.gm.getMovables():
                    self.gm.makeMove(i)
                    new_state = GameState(self.gm.getGameState(), curr_depth, i)
                    new_state.parent = self.currentState
                    self.visited[new_state] = False
                    self.currentState.children.append(new_state)
                    self.gm.reverseMove(i)
        while curr_depth != self.currentState.depth:
            index = self.currentState.nextChildToVisit  
            self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
            if len(self.currentState.children) > index:
                self.currentState = self.currentState.children[index]  
                trying_move = self.currentState.requiredMovable  
                self.gm.makeMove(trying_move) 
            else:   
                foundNew = False 
                while self.currentState.parent: 
                    self.gm.reverseMove(self.currentState.requiredMovable)  
                    self.currentState = self.currentState.parent                  
                    if len(self.currentState.children) > self.currentState.nextChildToVisit:    
                        foundNew = True   
                        break    
                if not foundNew:  
                    return False  
        if self.currentState.state == self.victoryCondition:  
            return True 
        else:
            self.visited[self.currentState] = True  
            child_depth = curr_depth + 1   
            for move in self.gm.getMovables(): 
                self.gm.makeMove(move)    
                new_state = GameState(self.gm.getGameState(), child_depth, move)          
                if new_state not in self.visited:                                       
                    self.visited[new_state] = False 
                    new_state.parent = self.currentState 
                    self.currentState.children.append(new_state)                                                               
                self.gm.reverseMove(move)
            return False