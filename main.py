import MENACE

def main():
    
    game_state = MENACE.Gamestate()
    
    while True:
        print('Do you want to play multi-player (1) or against MENACE (2)?')
        mode = int(input())
        
        if mode in [1, 2]:
            break
        
        else:
            print('Sorry please enter a valid number!')
    
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
                
    elif mode == 2:
        
        while True:
            
            print('Do you want to go first (1), or should MENACE go first (2)?')
            player = int(input())
            
            if player in [1, 2]:
                break
            else:
                print('Sorry please enter a valid number!')
        
        if player == 1:
            
            running = True
            while running:
                
                print('you chose to be player 1')
                
                print(game_state.board)
                print('Please input the square you want to place your piece on')
                square = input()
                game_state.make_move(square)
                
                print(game_state.board)
                
                if game_state.check_win():
                    print(f'Congratulations! You won!')
                    print(game_state.board)
                    running = False
                
                elif game_state.check_draw():
                    print(f'This game ends in a draw!')
                    print(game_state.board)
                    running = False
                
                else:
                    agent = MENACE.Q_Learning()
                    state = agent.get_state(game_state.board)
                    
                    # here the agent decides what to do
                    # right now the decision is random based on the available squares
                    action = agent.get_random_action(state)
                    
                    # the input in the make_move function is a string
                    square = str(action + 1)
                    game_state.make_move(square)
                    
                    print(f'MENACE chose the square {square}')
                    
                    if game_state.check_win():
                        print(f'Well, MENACE beat ya!')
                        print(game_state.board)
                        running = False
                    
                    elif game_state.check_draw():
                        print(f'This game ends in a draw!')
                        print(game_state.board)
                        running = False
            
        
        elif player == 2:
            print('you chose to be player 2')
            running = False

if __name__ == '__main__':
    main()