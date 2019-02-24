from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk onTop on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        answer = []
        for i in range(0, 3):
            p = []
            bindings = self.kb.kb_ask(parse_input("fact: (on ?x peg" + str(i+1) + ")"))
            if bindings:
                for j in bindings:
                    p.append(int(j['?x'][-1]))
            p.sort()
            answer.append(tuple(p))
        return tuple(answer)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        disk = str(movable_statement.terms[0])
        peg_source = str(movable_statement.terms[1])
        peg_dest = str(movable_statement.terms[2])

        if self.kb.kb_ask(parse_input("fact: (onTop " + disk + " ?y)")):
            new_top = self.kb.kb_ask(parse_input("fact: (onTop " + disk + " ?y)"))[0]
            self.kb.kb_retract(parse_input("fact: (onTop " + disk + " " + new_top['?y'] + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + new_top['?y'] + " " + peg_source + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + peg_source + ")"))
        top_bindings = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + peg_dest + ")"))
        if top_bindings:
            old_top = top_bindings[0]
            self.kb.kb_retract(parse_input("fact: (top " + old_top['?x'] + " " + peg_dest + ")"))
            self.kb.kb_assert(parse_input("fact: (onTop " + disk + " " + old_top['?x'] + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + peg_dest + ")"))
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + peg_source + ")"))
        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + peg_dest + ")"))
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + peg_source + ")"))
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + peg_dest + ")"))
 
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here
        answer = []
        p1 = []
        p2 = []
        p3 = []
        for i in range(1,4):
            bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos1)"))
            if bindings:
                tile_bind = bindings[0]
                tile_str = tile_bind['?tile']
                if tile_str == "empty":
                    tile_int = -1
                else:
                    tile_int = int(tile_str[-1])
                p1.append(tile_int)

        for i in range(1,4):    
            bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos2)"))
            if bindings:
                tile_bind = bindings[0]
                tile_str = tile_bind['?tile']
                if tile_str == "empty":
                    tile_int = -1
                else:
                    tile_int = int(tile_str[-1])
                p2.append(tile_int)

        for i in range(1,4):    
            bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos3)"))
            if bindings:
                tile_bind = bindings[0]
                tile_str = tile_bind['?tile']
                if tile_str == "empty":
                    tile_int = -1
                else:
                    tile_int = int(tile_str[-1])
                p3.append(tile_int)

        answer.append(tuple(p1))
        answer.append(tuple(p2))
        answer.append(tuple(p3))
        return tuple(answer)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = str(movable_statement.terms[0])
        x_start = str(movable_statement.terms[1])
        y_start = str(movable_statement.terms[2])
        x_finish = str(movable_statement.terms[3])
        y_finish = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (loc " + tile + " " + x_start + " " + y_start + ")"))
        self.kb.kb_retract(parse_input("fact: (loc  empty " + x_finish + " " + y_finish + ")"))
        self.kb.kb_assert(parse_input("fact: (loc " + tile + " " + x_finish + " " + y_finish + ")"))
        self.kb.kb_assert(parse_input("fact: (loc  empty " + x_start + " " + y_start + ")"))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))