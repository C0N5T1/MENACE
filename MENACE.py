import numpy as np
import random
import json

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
    
    def __init__(self):
        self.q_table = {}
        self.move_log = []
        
    def save_q_table(self, filename):
        data = self.q_table
        
        # Convert tuple keys to strings and numpy arrays to lists for JSON compatibility
        data_to_save = {str(k): v.tolist() for k, v in data.items()}

        # Save to JSON file
        with open(f'{filename}', 'w') as json_file:
            json.dump(data_to_save, json_file)
            
    def load_q_table(self, filename):
        with open(f'{filename}', 'r') as json_file:
            loaded_data = json.load(json_file)

        # Convert string keys back to tuples and lists to numpy arrays
        data_loaded = {tuple(map(int, k.strip('()').split(', '))): np.array(v) for k, v in loaded_data.items()}
        
        self.q_table = data_loaded
     
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

    # function that returns an action based on wieghts
    def get_weighted_action(self, state):
        
        valid_actions = self.get_valid_actions(state)
        
        if state not in self.q_table:
            self.q_table[state] = np.ones(9) * 10
            
        weights = np.array([self.q_table[state][i] for i in valid_actions]) 
        
        weights /= weights.sum()
        
        action = random.choices(valid_actions, weights=weights, k=1)[0]
        
        return action
        
    # function that takes a state, action and reward
    # and updates the q_table
    def update_q_table(self, state, action, reward):
        
        if state not in self.q_table:
            self.q_table[state] = np.ones(9) * 10
        
        # applying a minimum of 1 for any one action   
        if self.q_table[state][action] < 3 and reward == -2:
            pass
        
        else:
            self.q_table[state][action] += reward
        
    # function that appends a move to the move log
    def update_move_log(self, state, action):
        self.move_log.append((state, action))
        
    # function that trains the model for a number of epochs using the q_table
    def train(self, epochs):
        
        for _ in range(epochs):
            
            gamestate = Gamestate()
            
            done = False
            
            while not done:
                
                state = self.get_state(gamestate.board)
                
                # training with weighted actions
                action = self.get_weighted_action(state)
                square = str(action + 1)
                
                gamestate.make_move(square)
                
                self.update_move_log(state, action)
                
                if gamestate.check_win():
                    
                    winner = gamestate.move_log[-1][2]
                    
                    log_1 = self.move_log[::2]
                    log_2 = self.move_log[1::2]

                    
                    if winner == 1:
                        for state, action in log_1:
                            self.update_q_table(state, action, reward=3)
                            
                        for state, action in log_2:
                            self.update_q_table(state, action, reward=-1)
                    
                    else:
                        for state, action in log_1:
                            self.update_q_table(state, action, reward=-1)
                            
                        for state, action in log_2:
                            self.update_q_table(state, action, reward=3)
                      
                    done = True
                    
                elif gamestate.check_draw():                    
                    for state, action in self.move_log:
                        self.update_q_table(state, action, reward=1)
                        
                    done = True
                    
            self.move_log = []
                    
        print(self.q_table)
        
    # function that trains the agent on random actions
    # for an amount of epochs
    def train_random(self, epochs):
        
        for _ in range(epochs):
            
            gamestate = Gamestate()
            
            done = False
            
            while not done:
                
                state = self.get_state(gamestate.board)
                
                # training with weighted actions
                action = self.get_random_action(state)
                square = str(action + 1)
                
                gamestate.make_move(square)
                
                self.update_move_log(state, action)
                
                if gamestate.check_win():
                    
                    winner = gamestate.move_log[-1][2]
                    
                    log_1 = self.move_log[::2]
                    log_2 = self.move_log[1::2]

                    
                    if winner == 1:
                        for state, action in log_1:
                            self.update_q_table(state, action, reward=3)
                            
                        for state, action in log_2:
                            self.update_q_table(state, action, reward=-2)
                    
                    else:
                        for state, action in log_1:
                            self.update_q_table(state, action, reward=-2)
                            
                        for state, action in log_2:
                            self.update_q_table(state, action, reward=3)
                      
                    done = True
                    
                elif gamestate.check_draw():                    
                    for state, action in self.move_log:
                        self.update_q_table(state, action, reward=1)
                        
                    done = True
                    
            self.move_log = []
                    
        print(self.q_table)
                    
