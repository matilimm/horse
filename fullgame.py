import pygambit as gbt
# define shot types
options  = [["easy", gbt.Rational(2,3), gbt.Rational(2,3)],
            ["hard", gbt.Rational(1,3), gbt.Rational(1,3)]]
names = [] # this an array of just the names for when a player choses a shot
for i in options: names.append(i[0])

# h is a full game of horse
h = gbt.Game.new_tree(players=["player1","player2"], title="full game of horse")
# set outcomes
pl_one_win = h.add_outcome([1,0], label = "player 1 wins")
pl_two_win = h.add_outcome([0,1], label = "player 2 wins")

def add_round(g, node, playerup, playerdown, letters_one, letters_two):
    print('loop '+str(letters_one,)+' '+str(letters_two,)+' node: '+str(node))
    g.append_move(node, playerup, names) #p1 choses a shot
    if letters_one == 2:
        g.set_outcome(node, pl_two_win)
    elif letters_two == 2:
        g.set_outcome(node, pl_one_win)
    else:
        for i in range(len(options)):
            g.append_move(node.children[i], g.players.chance, ["hit", "miss"])
            g.set_chance_probs(node.children[i].infoset, [options[i][1], (1 - options[i][1])]) #set the chance that p1 hits
            # if p1 hits:
            g.append_move(node.children[i].children[0], g.players.chance, ["hit", "miss"])
            g.set_chance_probs(node.children[i].children[0].infoset, [options[i][2], (1 - options[i][2])])
            add_round(g, node.children[i].children[0].children[1], playerdown, playerup, (letters_one+1), letters_two)
            add_round(g, node.children[i].children[0].children[0], playerup, playerdown, (letters_one), letters_two+1)
            # if p1 misses:
            add_round(g, node.children[i].children[1], playerup, playerdown, (letters_one+1), letters_two)
add_round(h, h.root, 'player1', 'player2', 0, 0)
print('done building game')

result = gbt.nash.lcp_solve(h)
print(result)
