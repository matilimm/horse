import pygambit as gbt
# define shot types
options  = [["p1 advantage", gbt.Rational(2,3), gbt.Rational(1,3)],
            ["medium", gbt.Rational(1,2), gbt.Rational(1,2)]]
names = [] # this an array of just the names for when a player choses a shot
for i in options: names.append(i[0])

# h is a full game of horse
h = gbt.Game.new_tree(players=["player1","player2"], title="full game of horse")
# set outcomes
pl_one_win = h.add_outcome([1,0], label = "player 1 wins")
pl_two_win = h.add_outcome([0,1], label = "player 2 wins")

rounds = 2

def populate(g, node, playerup, playerdown, letters_one, letters_two):
    print('loop '+str(letters_one,)+','+str(letters_two,)+' node: '+str(node))
    g.append_move(node, playerup, names) #playerup choses a shot
    if letters_one == rounds:
        g.set_outcome(node, pl_two_win)
    elif letters_two == rounds:
        g.set_outcome(node, pl_one_win)
    else:
        for i in range(len(options)): # i here represents the diffrent shot types
            g.append_move(node.children[i], g.players.chance, ["hit", "miss"])
            g.set_chance_probs(node.children[i].infoset, [options[i][1], (1 - options[i][1])]) #set the chance that playerup hits
            # if playerup hits:
            g.append_move(node.children[i].children[0], g.players.chance, ["hit", "miss"])
            g.set_chance_probs(node.children[i].children[0].infoset, [options[i][2], (1 - options[i][2])]) #chance that playerdown hits
            populate(g, node.children[i].children[0].children[1], playerdown, playerup, (letters_one + 1), letters_two)
            populate(g, node.children[i].children[0].children[0], playerup, playerdown, (letters_one), letters_two + 1)
            # if playerup misses:
            populate(g, node.children[i].children[1], playerup, playerdown, (letters_one + 1), letters_two)
populate(h, h.root, 'player1', 'player2', 0, 0)
print('done building game')

result = gbt.nash.lcp_solve(h, rational=False)
print(result)
