import MENACE

def main():
    
    gamestate = MENACE.Gamestate()
    
    agent = MENACE.Q_Learning()
    
    agent.load_q_table('my_first_AI.json')
    
    epochs = 1000
    agent.train(epochs)
    
    agent.save_q_table('my_first_AI.json')
    

if __name__ == '__main__':
    main()