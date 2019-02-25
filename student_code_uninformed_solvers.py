from solver import *
from queue import *
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
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        canMove = self.gm.getMovables()
        curr = self.currentState
        if canMove:
            for i in canMove:
                self.gm.makeMove(i)                                                 
                child_state = GameState(self.gm.getGameState(), 1 + curr.depth, i)              
                curr.children.append(child_state)       
                child_state.parent = curr  
                self.gm.reverseMove(i)   
            for c in curr.children:   
                if c not in self.visited:            
                    self.visited[c] = True       
                    self.gm.makeMove(c.requiredMovable)               
                    self.currentState = c 
                    break 
        else: 
            self.gm.reverseMove(self.currentState.requiredMovable)       

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    
    path = Queue()
    spot = 0

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
            while not self.path.empty():
                self.path.get()
            return True

        if self.gm.getMovables():
            for i in self.gm.getMovables():
                self.gm.makeMove(i)         
                child = GameState(self.gm.getGameState(), 0, i)     
                self.currentState.children.append(child)                
                child.parent = self.currentState
                self.gm.reverseMove(i)              
        for i in self.currentState.children:        
            if i not in self.visited:       
                self.path.put(i)        
        while not self.path.empty():        
            kid = self.path.get()       
            if kid not in self.visited: 
                curr = self.currentState    
                visits = []                
                while curr.requiredMovable:             
                    visits.append(curr.requiredMovable)           
                    curr = curr.parent 
                curr = kid      
                child_visits = [] 
                while curr.requiredMovable:  
                    child_visits.append(curr.requiredMovable)  
                    curr = curr.parent    
                child_visits = reversed(child_visits)  
                for i in visits:     
                    self.gm.reverseMove(i)
                for i in child_visits:
                    self.gm.makeMove(i) 
                self.currentState = kid     
                self.visited[kid] = True   
                self.spot = self.spot + 1      
                self.currentState.depth = self.spot          
                break
        return False