import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i,j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        self.mines = set(dict.fromkeys(list(self.mines)))
        for sentence in self.knowledge:
            sentence.mark_mine(cell)


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        self.safes = set(dict.fromkeys(list(self.safes)))
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """       
        #1
        self.moves_made.add(cell)                                    
        
        #2
        if cell not in self.safes:                                   
            self.mark_safe(cell)

        #3
        neighbours = [
         (cell[0], cell[1]-1),      #Up
         (cell[0], cell[1]+1),      #Down
         (cell[0]-1, cell[1]),      #Left
         (cell[0]+1, cell[1]),      #Right
         (cell[0]-1, cell[1]-1),    #Up Left
         (cell[0]+1, cell[1]-1),    #Up Right
         (cell[0]-1, cell[1]+1),    #Down Left
         (cell[0]+1, cell[1]+1)     #Down Right
        ]
        
        for neighbour in neighbours.copy():
            if neighbour[0] == -1 or neighbour[1] == -1 or neighbour[0] == self.width or neighbour[1] == self.height:
                neighbours.remove(neighbour)

        neighbours = Sentence(set(neighbours).difference(self.moves_made), count)
        for cell in neighbours.cells:
            if cell in self.mines:
                self.mark_mine(cell)
            if neighbours.count == 0:
                self.mark_safe(cell)
        self.knowledge.append(neighbours)
        
        #4
        for sentence in self.knowledge:
            for cell in sentence.known_safes().copy():
                self.mark_safe(cell)
            for cell in sentence.known_mines().copy():
                self.mark_mine(cell)

        for cell in self.safes:
            self.mark_safe(cell)
        for cell in self.mines:
            self.mark_mine(cell)
        
        
        #5
        for sen1, sen2 in itertools.combinations(self.knowledge, 2):
            if sen1.cells.issubset(sen2.cells):
                diff_cells = sen2.cells - sen1.cells
                diff_count = sen2.count - sen1.count
                new_sentence = Sentence(diff_cells, diff_count)
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)
                
                if diff_count == 0:
                    for cell in diff_cells:
                        self.mark_safe(cell)
                elif diff_count == len(diff_cells) and diff_count != 0:
                    for cell in diff_cells:
                        self.mark_mine(cell)

        #filter through knowledge base to remove unnecessary knowledge
        trash = []
        for sen1 in self.knowledge:
            for sen2 in self.knowledge:
                if(
                    len(sen1.cells) == 0 or
                    sen1.cells == sen2.cells and
                    sen1.count == sen2.count and
                    self.knowledge.index(sen1) != self.knowledge.index(sen2)
                ):
                    trash.append(sen1)
        
        new_knowledge = []
        for sentence in self.knowledge:
            if sentence not in trash:
                new_knowledge.append(sentence)
        self.knowledge = new_knowledge
                
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        choices = self.safes.difference(self.moves_made)
        if len(choices) != 0:
            return choices.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        rand_moves = set()
        for i in range(self.width):
            for j in range(self.height):
                rand_moves.add((i,j))
        rand_moves = rand_moves.difference(self.mines).difference(self.moves_made)
        
        if len(rand_moves) == 0:
            return None
        else:
            return random.choice(list(rand_moves))
