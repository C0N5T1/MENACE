import MENACE
import numpy as np

filename = 'enforced_AI.json'

reward_win = 3
reward_draw = 2
reward_loss = -2

def main():
    
    game_state = MENACE.Gamestate()
    
    agent=MENACE.Q_Learning()
    
    agent.load_q_table(filename)
    
    while True:
        print('Do you want to play multi-player (1) or against MENACE (2)?')
        mode = int(input())
        
        if mode in [1, 2]:
            break
        
        else:
            print('Sorry please enter a valid number!')
    
    # multiplayer
    if mode == 1:
        running = True
        while running:
            
            print(game_state.board)
            print('Please input the square you want to place your piece on')
            square = input()
            game_state.make_move(square)
            
            if game_state.check_win():
                print(f'Congratulations! Player {game_state.move_log[-1][2]} won the game!')
                print(game_state.board)
                running = False
            
            elif game_state.check_draw():
                print(f'This game ends in a draw!')
                print(game_state.board)
                running = False
    
    # singleplayer           
    elif mode == 2:
        
        while True:
            
            print('Do you want to go first (1), or should MENACE go first (2)?')
            player = int(input())
            
            if player in [1, 2]:
                break
            else:
                print('Sorry please enter a valid number!')
        
        # human goes first
        if player == 1:
            
            running = True
            print('you chose to be player 1')
            
            while running:
                
                print(game_state.board)
                print('Please input the square you want to place your piece on')
                square = input()
                game_state.make_move(square)
                
                print(game_state.board)
                
                if game_state.check_win():
                    print(f'Congratulations! You won!')
                    print(game_state.board)
                    
                    #setting the reward
                    reward = reward_loss
                    
                    running = False
                
                elif game_state.check_draw():
                    print(f'This game ends in a draw!')
                    print(game_state.board)
                    
                    #setting the reward
                    reward = reward_draw
                    
                    running = False
                
                else:
                    state = agent.get_state(game_state.board)
                    
                    # here the agent decides what to do                    
                    action = agent.get_weighted_action(state)
                    
                    print(agent.q_table[state])
                    
                    # the input in the make_move function is a string
                    square = str(action + 1)
                    game_state.make_move(square)
                    
                    agent.update_move_log(state, action)
                    
                    print(f'MENACE chose the square {square}')
                    
                    if game_state.check_win():
                        print(f'Well, MENACE beat ya!')
                        print(game_state.board)
                        
                        # setting the reward
                        reward = reward_win
                                                
                        running = False
                    
                    elif game_state.check_draw():
                        print(f'This game ends in a draw!')
                        print(game_state.board)
                        
                        # setting the reward
                        reward = reward_draw
                        
                        running = False
                        
            # iterating through the move log         
            for state, action in agent.move_log:
                board = np.array(state).reshape((3, 3))
                equal_states, equal_actions = game_state.get_equal_states(board, action)
                
                # iterating through the equivalent states/actions
                for i in range(len(equal_states)):
                    agent.update_q_table(equal_states[i], equal_actions[i], reward)
                
            agent.save_q_table(filename)
            
        # machine goes first
        elif player == 2:
            print('you chose to be player 2')
            running = True
            
            while running:
                
                
                
                state = agent.get_state(game_state.board)
                    
                # here the agent decides what to do                    
                action = agent.get_weighted_action(state)
                
                print(agent.q_table[state])
                
                # the input in the make_move function is a string
                square = str(action + 1)
                game_state.make_move(square)
                
                agent.update_move_log(state, action)
                
                print(f'MENACE chose the square {square}')
                print(game_state.board)
                
                if game_state.check_win():
                    print(f'Well, MENACE beat ya!')
                    print(game_state.board)
                    
                    # setting the reward
                    reward = reward_win
                                            
                    running = False
                
                elif game_state.check_draw():
                    print(f'This game ends in a draw!')
                    print(game_state.board)
                    
                    # setting the reward
                    reward = reward_draw
                    
                    running = False
            
                else:
                    print('Please input the square you want to place your piece on')
                    square = input()
                    game_state.make_move(square)
                    
                    print(game_state.board)
                    
                    if game_state.check_win():
                        print(f'Congratulations! You won!')
                        print(game_state.board)
                        
                        #setting the reward
                        reward = reward_loss
                        
                        running = False
                    
                    elif game_state.check_draw():
                        print(f'This game ends in a draw!')
                        print(game_state.board)
                        
                        #setting the reward
                        reward = reward_draw
                        
                        running = False
                    
                        
            for state, action in agent.move_log:
                board = np.array(state).reshape((3, 3))
                equal_states, equal_actions = game_state.get_equal_states(board, action)
                
                # iterating through the equivalent states/actions
                for i in range(len(equal_states)):
                    agent.update_q_table(equal_states[i], equal_actions[i], reward)
                
            agent.save_q_table(filename)
            
        

if __name__ == '__main__':
    main()