import MENACE

def main():
    
    gamestate = MENACE.Gamestate()
    
    agent = MENACE.Q_Learning()
    
    agent.train(1000)
    
    agent.save_q_table('my_first_AI.json')
    

if __name__ == '__main__':
    main()