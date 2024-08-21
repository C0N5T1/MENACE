import MENACE

def main():
    
    gamestate = MENACE.Gamestate()
    
    agent = MENACE.Q_Learning()
    
    agent.load_q_table('enforced_AI.json')
    
    epochs = 5000
    agent.train(epochs)
    
    agent.save_q_table('enforced_AI.json')
    
    
def main_random():
    
    gamestate = MENACE.Gamestate()
    
    agent = MENACE.Q_Learning()
    
    agent.load_q_table('random_AI.json')
    
    epochs = 5000
    agent.train_random(epochs)
    
    agent.save_q_table('random_AI.json')
    
    

if __name__ == '__main__':
    main()
    main_random()