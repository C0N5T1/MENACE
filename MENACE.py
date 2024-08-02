import numpy as np
import random


class Gamestate():
    
    def __init__(self):
        
        self.board = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]])
        
        self.x_to_move = True
        self.move_log = []
    
    # makes a move on the board 
    # 1 if it is x's turn -1 if it is o's turn
    def make_move(self, square):
        
        dict = {
            '1' : (0, 0), '2' : (0, 1), '3' : (0, 2),
            '4' : (1, 0), '5' : (1, 1), '6' : (1, 2),
            '7' : (2, 0), '8' : (2, 1), '9' : (2, 2)
        }
        
        
        if square in dict:
            row, col = dict[square]
            
        else:
            print('Invalid Input, please enter a number from (1-9)')
        
        if self.board[row][col] != 0:
            print('Sorry this square is already occupied, pleas select a different square')
        
        else:
            if self.x_to_move:
                self.board[row][col] = 1
            else:
                self.board[row][col] = -1
            
            self.x_to_move = not self.x_to_move
            
            self.move_log.append((row, col, self.board[row][col]))
            
    # function that checks if a win has occured on the board
    def check_win(self):
        
        row = self.move_log[-1][0]
        col = self.move_log[-1][1]
        
        player = self.board[row][col]
        
        if np.all(self.board[row, :] == player):
            return True
        
        if np.all(self.board[:, col] == player):
            return True
        
        if row == col and np.all(np.diag(self.board) == player):
            return True
        
        if row + col == 2 and np.all(np.diag(np.fliplr(self.board)) == player):
            return True
    
    # function that checks if a draw occured  
    def check_draw(self):
        if not np.any(self.board == 0):
            return True
        else:
            return False
        
        
        
class Q_Learning():
    
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.move_log = []
     
    # turns a np.array into a tuple of length 9   
    def get_state(self, board):
        return tuple(board.flatten())
    
    # returns the all squares that are empty
    def get_valid_actions(self, state):
        valid_actions = [i for i in range(9) if state[i] == 0]
        return valid_actions
    
    # function that randomly chooses a move from the valid moves
    def get_random_action(self, state):
        
        valid_actions = self.get_valid_actions(state)
        
        action = random.choice(valid_actions)
        
        return action
    
####################################################################################
################################ Work in Progress ##################################
####################################################################################

    # function that takes a state, action and reward
    # and updates the q_table
    def update_q_table(self, state, action, reward):
        
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)
            
        self.qtable[state][action] = reward
        
    # function that appends a move to th move log
    def update_move_log(self, state, action):
        self.move_log.append((state, action))
        
    # function that trains the model for a number of epochs using random moves
    def train(self, epochs):
        
        for _ in range(epochs):
            
            Game = Gamestate()
            state = self.get_state(Game.board)
            done = False
            
            while not done:
                
                action = self.get_random_action(state)
                square = str(action + 1)
                
                Game.make_move(square)
                
                if Game.check_win():
                    reward = 1
                    
                    for state, action in self.move_log:
                        self.update_q_table(state, action, reward)
                        
                    done = True
                    
                elif Game.check_draw():
                    reward = 0.5
                    
                    for state, action in self.move_log:
                        self.update_q_table(state, action, reward)
                    done = True
                
                # if there was no draw but there are no more valid moves it means you lost    
                elif self.get_valid_actions == []:
                    reward = -1
                    done = True
                    

    
        
    