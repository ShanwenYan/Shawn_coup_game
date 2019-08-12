#!/usr/bin/env python
# coding: utf-8

# # Building a simple Coup game
# 
# Coup is a popular board game which has a fast pace. The description of the game can be found at this website: https://boardgamegeek.com/boardgame/131357/coup. Basically there are five different cards and each turn a player can make a single decision. I divided the coding procedure into 7 parts:
# 
# 
# 1. Define player
# 2. Define actions
# 3. Simulate the game for human players
# 4. Develop AI
# 5. Come up with a strategy for AI
# 6. Upgrade to a multi-player set
# 7. Define a lying game
# 

# In[ ]:


# Import packages
import sys                        # for executing the program
from random import shuffle        # for deck shuffling


# # Part one: Define player
# 
# I first create a game with only three players. Player will be a class distinguished by their names which has instance coin (initially 2) and hands. Hands should be a dictionary with a maximum length two. If the player has no cards he will die.

# In[ ]:


class Player:

    
    # variable is assigned by given a player name, initialize 2 coins and an empty hand, player is also alive
    def __init__(self,name):
        self.name = name
        self.coins = 2
        self.hands = []
        self.status = True
        
    # function to show players their current card
    def show_hand(self):
        print('Your hands are:\n')
        for hand in self.hands:
            print(hand)
        print('\n')    
    


# # Part two: Define actions

# Before define the actual game actions, we need to define some basic actions firsts. 

# We first define a function to check whether the game stops, this function will be triggered everytime player show down their card.

# In[ ]:


def endgame_check():
    global players
    if sum([player.status for player in players.values()]) == 1:
        winner = [player.name for player in players.values() if player.status]
        print('The winner of the game is ' + winner[0] + '. Congratulations!\n')
        sys.exit()
    else: pass


# There should also be a function for a player choosing one card to loose(which also means you lose one life), after this action, we always check if the player is still alive and if the game ends.

# In[ ]:


def discard(victim):
    
    global players
    
    if len(victim.hands) == 1:
        card_discard = victim.hands[0]
        victim.hands.remove(card_discard)
        discarded_pool.append((victim.name,card_discard))
    else:
        card_discard = input('Player '+victim.name+', please select one card to show down: ')

        while not card_discard in victim.hands:
            card_discard = input('This is not the right place to lie, please re-enter: ')

        victim.hands.remove(card_discard)
        discarded_pool.append((victim.name,card_discard))
    
    if victim.hands == []:
        victim.status = False
        print('Player '+victim.name+' has been eliminated. Good luck next time!\n')
        del existing_players[victim.name]
        
    endgame_check()
            


# Define a function to exchange hand with pool, note that you might get back the same card. After this the player will check his hands.

# In[ ]:


def exchange(player,card):
    player.hands.remove(card)
    pool.append(card)
    shuffle(pool)
    new_card = pool.pop()
    player.hands.append(new_card)
    shuffle(pool)
    input(player.name+', Press any key to see your hand\n')
    player.show_hand()


# Since for all actions, other players will be asked whether to qustion or not. So we create question function which
# will only be called with action methods. Players will be asked in turn whether they want to question. If nobody questions the function does nothing. If somebody questions the funtion will judge whether this quesiton is successful or not. I call the input of this function 'actioner', while who question this 'questioner'.

# When questioning or blocking, we need an iterator which takes the seccond next player and loop till the player before him. So we create a function to generate the iterator.

# In[ ]:


def calling(actioner):
    global existing_players
    players_name = [name for name in existing_players.keys()]*2
    initial = players_name.index(actioner.name)+1
    iterator = []
    for i in range(initial,initial+len(existing_players)-1):
        iterator.append(existing_players[players_name[i]])
    return iterator


# In[ ]:


def question(actioner,card):
    iterator = calling(actioner)
    for questioner in iterator:
        respond = input('Player '+questioner.name+', do you what to question? [yes/no] ')
        print('\n')
        if respond == 'yes':
            if card in player.hands:
                print('Question failed!\n')
                discard(questioner)
                exchange(actioner,card)
                continue_action = True
                return continue_action
            else:
                print('Question success!\n')
                discard(actioner)
                continue_action = False
                return continue_action
    continue_action = True
    return continue_action


# We put all possible actions inside a function called action, the input will be the player and name of the action, then different effects will happen according to what the player inputs. To make things simple, we first create an action list for the future check.

# In[ ]:


action_list = ['income','foreign aid','coup','duke','assassin','duke','ambassador','captain']


# In[ ]:


def take_action(player,action):
    
    
    
    if action == 'income':
        player.coins += 1
    
    
    
    elif action == 'foreign aid':
        iterator = calling(player)
        for blocker in iterator:
            respond = input('Player '+blocker.name+', do you what to block? [yes/no] ')
            if respond == 'yes':
                continue_action = question(blocker,'duke')
                if continue_action:
                    return
                else: 
                    print('block failed!\n')
                    player.coins += 2
                    return
        player.coins += 2
        return
      
        
        
    elif action == 'coup':
        victim = input('please select a player to coup: ')        
        while not victim in existing_players:
            victim = input('Player doesn\'t exit or has been eliminated, please re-enter: ')
            if victim == 'player.name':
                victim = input('You can\'t kill yourself, please re-enter: ')
                while (not victim in existing_players) or  victim == 'player.name':
                    victim = input('Player doesn\'t exit, please re-enter: ')
        discard(players[victim])        
        player.coins -= 7
        
        
        
    elif action == 'duke':
        continue_action = question(player,'duke')
        if continue_action:
            player.coins += 3
        
        return
        
        
        
    elif action == 'assassin':
        player.coins -= 3
        victim = input('Who do you want to assassinate: ')
        while not victim in existing_players:
            victim = input('Player doesn\'t exit, please re-enter: ')
        if victim == 'player.name':
            victim = input('You can\'t kill yourself, please re-enter: ')
            while (not victim in existing_players) or  victim == 'player.name':
                victim = input('Player doesn\'t exit, please re-enter: ')
        continue_action = question(player,'assassin')
        if continue_action:
            try:
                victim_player = existing_players[victim] 
                defend = input('Player '+victim+', do you want to play contessa? [yes/no] ')
                print('\n')
                if defend == 'yes':
                    continue_action_2 = question(players[victim] ,'contessa')
                    if continue_action_2:
                        print('Successfully defended!\n')
                        return
                print('Attack succeed!\n')
                discard(players[victim])
                return
            except KeyError:
                print('Target already down.\n')
                return
        print('Attack failed!\n')
        return
    
    
    
    elif action == 'captain':
        target = input('Who do you want to steal: ')
        while not target in existing_players:
            target = input('Player doesn\'t exit, please re-enter: ')
        continue_action = question(player,'captain')
        if continue_action:
            defend = input('Player '+target.name+', do you want to block stealing? [yes/no] ')
            print('\n')
            if defend == 'yes':
                iterator = calling(target)
                for questioner in iterator:
                    respond = input('Player '+questioner.name+', do you what to question? [yes/no] ')
                    print('\n')
                    if respond == 'yes':
                        if 'captain' in player.hands:
                            print('Question failed!\n')
                            discard(questioner)
                            exchange(target,'captain')
                            print('block succeed!\n')
                            return
                        elif 'ambassador' in player.hands:
                            print('Question failed!\n')
                            discard(questioner)
                            exchange(target,'ambassador')
                            print('block succeed!\n')
                            return
                        else:
                            print('Question succeed, block failed!\n')
                            discard(target)
                            if target.coins < 2:
                                target.coins -= target.coins
                                player.coins += target.coins
                            else:
                                target.coins -= 2
                                player.coins += 2
                            return
                return    
            target.coins -= 2
            player.coins += 2
            return
        return
    
    
    
    
    else:
        continue_action = question(player,'ambassador')
        if continue_action:
            for _ in range(2):
                new_card = pool.pop()
                player.hands.append(new_card)        
            input(player.name+', Press any key to see your hand\n')
            player.show_hand()
            
            put_back = input('Please select the first card you want to put back: ')
            print('\n')
            while not put_back in player.hands:
                put_back = input('Please put back a card you own: ') 
                print('\n')
            player.hands.remove(put_back)
            pool.append(put_back)
            
            put_back = input('Please select the second card you want to put back: ')
            print('\n')
            while not put_back in player.hands:
                put_back = input('Please put back a card you own: ') 
                print('\n')
            player.hands.remove(put_back)
            pool.append(put_back)
            
            shuffle(pool)
            return
        return
                
            
            


# # Part three: create a game
# 
# We should have card pool since the player will exchange cards with the pool. 
# 
# We assume there are infinitely many coins in the bank.
# 
# We also need a termination of the game. The game has only one survivor so we will end this game if the number of players is one.

# # Configuration

# In[ ]:


# Players login
number_of_players = input('Please enter the number of total players: ')
number_of_players = int(number_of_players)

if number_of_players <= 2:
    print('At least three players required for this game\n')
    sys.exit()


players = {}

for i in range(number_of_players):
    name = input('Player {}, please enter your player name: '.format(i+1))
    players[name] = Player(name)

print('\n')


# Initialize reference dictionary existing_players

existing_players = players.copy()


# Create the card pool

pool = ['assassin','duke','contessa','ambassador','captain']*3

shuffle(pool)

# Card dealing

for player in players.values():
    for _ in range(2):
        new_card = pool.pop()
        player.hands.append(new_card)        
    
    input(player.name+', press any key to see your hand.\n')
    player.show_hand()

# Create discarded cards, this will be a list of (player name, card name) tupple

discarded_pool = []


# # Game phase
# 
# 1. check whether player is forced to coup (coins >= 10)
# 2. select an action
# 3. check whether game stops (len(players) == 1)

# In[ ]:


# Although the game will terminate itself, we need to add a loop to keep it working. For safety consideration we use the termination check.
# This really shouldn't happen
while not len(existing_players) == 1:
    for player in players.values():
        if not player.status:
            continue
        else:
            print('Player '+player.name+',it\'s your turn.\n')

            # show the discarded card pool for reference, this is probably the best time to show it.
            print('Open information now:\n')        
            print('Open cards: {}\n'.format(discarded_pool))
            print('Coins of each player:\n')
            for gamers in existing_players.values():
                print('Player {} has {} coins.\n'.format(gamers.name,gamers.coins))


            # force coup check
            if player.coins >= 10:
                victim = input('You are forced to coup, please select a player to coup: ')
                take_action(player,'coup')

            else: 
                action = input('Please select an action: ')
                print('\n')

                while not action in action_list:
                    action = input('Please re-enter a valid action: ')          
                # A player can only chooese assassin if he or she has 3+ coins
                if action == 'assassin' and player.coins < 3:
                    action = input('You don\'t have enough coins, please re-enter: ')
                    while (not action in action_list) or action == 'assassin':
                        action = input('Please re-enter a valid action: ')
                if action == 'coup' and player.coins < 7:
                    action = input('You don\'t have enough coins, please re-enter: ')
                    while (not action in action_list) or action == 'coup':
                        action = input('Please re-enter a valid action: ')
                take_action(player,action)
            
        print('-'*100)


# # Future improvements
# 
# 1. The iterator definitely needs a big fix, first it needs to be more consise. Also the iterator should start at the correct position for blocker and contessa 
# 2. Adding GUI (change input string to button for instance)
# 3. Use machine learning to improve AI performance
# 4. Break down the code to different files that only the main file will be executed
# 5. Change to a design which allows new action/card to be added in easily
# 6. I forgot dictionaries can't change size as a iterator, need another way to intepret the loop
# 7. Hide hands information after a player checks it.
