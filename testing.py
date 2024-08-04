import MENACE

def main():
    
    gamestate = MENACE.Gamestate()
    
    agent = MENACE.Q_Learning()
    
    agent.train(100)
    

if __name__ == '__main__':
    main()