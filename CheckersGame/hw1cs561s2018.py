import operator
import sys
import copy
import math
#input from the file

f=open('input1.txt','r')
array=[]
for line in f:
    array.append(line.rstrip('\n'))
my_player=array[0]
play_method=array[1]
max_depth=array[2]

table_state=[]
for i in range(3,11):
    list=array[i].split(',')
    table_state.append(list)

weight1=array[11].split(',')
weight2=copy.copy(weight1)
weight2.reverse()

row=['H','G','F','E','D','C','B','A']

#player and opponent
if my_player=='Star':
    opponent='Circle'
else:
    opponent='Star'

def copyboard(B):
    copy=[]
    for row in B:
        copy.append(row)
    return copy

n=8
#evaluate function
def evaluate(my_player, oppo_player, board):
    if my_player == 'Star':
        player='S'
        oppo='C'
        player_weight=weight2
        oppo_weight=weight1
    else:
        player='C'
        oppo='S'
        player_weight=weight1
        oppo_weight=weight2
    my_score,opponent_score=0,0
    for i in range(n):
        for j in range(n):
            if board[i][j]!='0':
				string=board[i][j]

				if string[0]==player:
					my_score+=(int)(string[1])*(int)(player_weight[i])
				elif string[0]==oppo:
					opponent_score+=(int)(string[1])*(int)(oppo_weight[i])
    total_score=my_score-opponent_score
    return total_score
#print evaluate(my_player,opponent,table_state)

#generate next possible move
def generate_moves(board,player):
    if player == 'Star':
        oppo='Circle'
    else:
        oppo='Star'
    moves=[]
    if player == 'Star':
        for i in range(1,n):
            for j in range(n):
                string=board[i][j]
                if(string[0]=='S'):
                    if j-1>=0:
                        temp=board[i-1][j-1]
                        if i-1==0:
                            if temp=='0' or temp[0]=='S':
                                moves.append([[i-1,j-1],[i,j]])
                        if i-1>0:
                            if temp=='0':
                                moves.append([[i-1,j-1],[i,j]])
                            if j-2>=0:
                                temp2=board[i-2][j-2]
                                if i-2==0 and temp[0]=='C' and (temp2=='0'or temp2[0]=='S'):
                                    moves.append([[i-2,j-2],[i,j]])
                                if i-2>0 and temp[0]=='C' and temp2=='0':
                                    moves.append([[i-2,j-2],[i,j]])
                    if j+1<n:
                        temp=board[i-1][j+1]
                        if i-1==0:
                            if temp=='0' or temp[0]=='S':
                                moves.append([[i-1,j+1],[i,j]])
                        if i-1>0:
                            if temp=='0':
                                moves.append([[i-1,j+1],[i,j]])
                            if j+2<n:#cuole
                                temp2=board[i-2][j+2]
                                if i-2==0 and temp[0]=='C' and (temp2=='0' or temp2[0]=='S'):
                                    moves.append([[i-2,j+2],[i,j]])
                                if i-2>0 and temp[0]=='C' and temp2=='0':
                                    moves.append([[i-2,j+2],[i,j]])
    else:
        for i in range(n-1):
            for j in range(n):
                string=board[i][j]
                if(string[0]=='C'):
                    if j-1>=0:
                        temp=board[i+1][j-1]
                        if i+1==n:
                            if temp=='0' or temp[0]=='C':
                                moves.append(([i+1,j-1],[i-1,j+1],[i,j]))
                        if i+1<n:
                            if temp=='0':
                                moves.append([[i+1,j-1],[i,j]])
                            if j-2>=0:
                                if i+2<n:

									temp2=board[i+2][j-2]
									if i+2==n-1 and temp[0]=='S' and (temp2=='0'or temp2[0]=='C'):
										moves.append([[i+2,j-2],[i,j]])
									if i+2<n-1 and temp[0]=='S' and temp2=='0':
										moves.append([[i+2,j-2],[i,j]])
                    if j+1<n:
                        temp=board[i+1][j+1]
                        if i+1==n:
                            if temp=='0' or temp[0]=='C':
                                moves.append([[i+1,j+1],[i,j]])
                        if i+1<n:
                            if temp=='0':
                                moves.append([[i+1,j+1],[i,j]])
                            if j+2<n:
                                if i+2<n:
                                    temp2=board[i+2][j+2]
                                    if i+2==n-1 and temp[0]=='S' and (temp2=='0' or temp2[0]=='C'):
                                        moves.append([[i+2,j+2],[i,j]])
                                    if i+2<n-1 and temp[0]=='S' and temp2=='0':
                                        moves.append([[i+2,j+2],[i,j]])
    return moves
#moves=generate_moves(table_state,my_player)[0]
#print generate_moves(table_state,my_player)
#moves=generate_moves(table_state,my_player)[0]


def make_move(board, move, player):
    #print board
	if move is None:
		return "NoValidMove" #do i need to put "pass" here?
	if player == 'Star':
		play='S'
		oppo='C'
	else:
		play='C'
		oppo='S'
	before=move[1]
	after=move[0]
	x1=before[0]
	y1=before[1]
	x2=after[0]
	y2=after[1]
	#print x1,y1,x2,y2
	#print 'y2',x2,y2
	middle_x=(x1+x2)/2
	middle_y=(y1+y2)/2
	if math.fabs(y2-y1)==1:
		temp=board[x2][y2]
		if len(temp)==2:
			letter=temp[0]
			number=int(temp[1])
			if letter==play:
				number+=1
				temp=letter+str(number)
				board[x2][y2]=temp
				board[x1][y1]='0'
		else:
			board[x2][y2]=board[x1][y1]
			board[x1][y1]='0'
	else: #check whethermath.fabs(y2-y1)==2
		temp=board[x2][y2]
		#print 'temp=',temp,board[x2][y2]
		if len(temp)==2:
			letter=temp[0]
			number=int(temp[1])
			if letter==play:
				number+=1
				temp=letter+str(number)
				board[middle_x][middle_y]='0'
				board[x2][y2]=temp
				board[x1][y1]='0'
		else:
			board[middle_x][middle_y]='0'
			board[x2][y2]=board[x1][y1]
			board[x1][y1]='0'
	return board
#print make_move(table_state,moves,my_player)

def game_over(board,player,oppo):
	if (len(generate_moves(board,player))==0 and len(generate_moves(board,oppo))==0):
		return True
	star_num=0
	circle_num=0
	for i in range(n):
		for j in range(n):
			if(board[i][j]!='0'):
				if(board[i][j][0]=='S'):
					star_num+=1
				else:
					circle_num+=1
				if(star_num>=1 and circle_num>=1):
					return False
	return star_num==0 or circle_num==0


def alphabeta_value(board,player,d):
	global state
	if player == 'Star':
		oppo='Circle'
	else:
		oppo='Star'

	if game_over(board,player,oppo):
		return [evaluate(player,oppo,board),evaluate(player,oppo,board),'pass',state+2]
	# Functions used by alphabeta
	def max_value(board, alpha, beta, depth,player,oppo):

		global state
		if game_over(board,player,oppo):
			#print evaluate(oppo,player,board)
			return evaluate(player,oppo,board)
		#print player
		# print depth
		if depth==int(max_depth):
			#print board
			return evaluate(player,oppo,board)
		v = -sys.maxsize-1
		moves=generate_moves(board,player)
		#print moves

		if(len(moves)==0):
			state+=1
			return min_value(board,best_score, beta,d+1,oppo,player)

		for a in moves:
			b=copy.deepcopy(board)
			mv=make_move(b,a,player)
			state+=1
			v = max(v, min_value(mv,
								 alpha, beta, depth + 1,oppo,player))
			if v >= beta:
				return v
			alpha = max(alpha, v)
		return v

	def min_value(board, alpha, beta, depth,player,oppo):
		global state
		if game_over(board,player,oppo):
			#print evaluate(oppo,player,board)
			return evaluate(oppo,player,board)
		#print player
		# print depth
		if depth==int(max_depth):
			#print board
			return evaluate(oppo,player,board)
		v = sys.maxsize
		moves=generate_moves(board,player)
		#print moves

		if(len(moves)==0):
			state+=1
			return max_value(board,alpha, beta, depth + 1,oppo,player)

		for a in moves:
			b=copy.deepcopy(board)
			mv=make_move(b,a,player)
			state+=1
			v = min(v, max_value(mv,
								 alpha, beta, depth + 1,oppo,player))
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state

	best_score =-sys.maxsize-1
	max_score=-sys.maxsize-1
	beta = sys.maxsize
	best_action = None


	moves=generate_moves(board,player)
	#print moves

	if(len(moves)==0):
		state+=1
		max_score=evaluate(player,oppo,board)
		best_score=min_value(board,best_score, beta,d+1,oppo,player)
		return [max_score,best_score,'pass',state]

	for a in moves:
		b=copy.deepcopy(board)
		mv=make_move(b,a,player)
		#print mv
		state+=1
		max_score=max(max_score,evaluate(player,oppo,mv))
		#print mv
		v = min_value(mv, best_score, beta, d+1,oppo,player)

		if v > best_score:
			best_score = v
			best_action = a
		#print best_score
	return [max_score,best_score,best_action,state]

#print alphabeta_value(table_state,'Star',7)


def minimax_value(board, player,d):
	global state
	#global max_score
	if player == 'Star':
		oppo='Circle'
	else:
		oppo='Star'

	if game_over(board,player,oppo):
			return [evaluate(player,oppo,board),evaluate(player,oppo,board),'pass',state+2]

	def max_value(board,depth,player,oppo):
		global state


		if game_over(board,player,oppo):
			#print evaluate(player,oppo,board)
			return evaluate(player,oppo,board)

		if depth==int(max_depth):
			#print evaluate(oppo,player,board)
			return evaluate(player,oppo,board)
		v = -sys.maxsize-1

		moves=generate_moves(board,player)
		#print moves

		if(len(moves)==0):
			state+=1
			return min_value(board,depth+1,oppo,player)

		for a in moves:
			b=copy.deepcopy(board)
			mv=make_move(b,a,player)
			state+=1
			v = max(v, min_value(mv,depth+1,oppo,player))
			#print v
		return v

	def min_value(board,depth,player,oppo):

		global state
		# print board
		if game_over(board,player,oppo):

			return evaluate(oppo,player,board)

		if depth==int(max_depth):
			#print evaluate(oppo,player,board)

			return evaluate(oppo,player,board)
		v = sys.maxsize

		moves=generate_moves(board,player)
		#print moves

		if(len(moves)==0):
			state+=1
			return min(v,max_value(board,depth+1,oppo,player))

		for a in moves:
			b=copy.deepcopy(board)
			mv=make_move(b,a,player)
			state+=1
			v = min(v, max_value(mv,depth+1,oppo,player))
			#print(v)
		return v

	best_score =-sys.maxsize-1
	max_score=-sys.maxsize-1
	best_action = None

	moves=generate_moves(board,player)
	#print moves
	if(len(moves)==0):
		if(len(generate_moves(board,oppo))==0):
			return 'pass'
		state+=1
		max_score=evaluate(player,oppo,board)
		best_score=min_value(board,d+1,oppo,player)
		return [max_score,best_score,'pass',state]

	for a in moves:
		b=copy.deepcopy(board)
		mv=make_move(b,a,player)
		max_score=max(max_score,evaluate(player,oppo,mv))
		state+=1

		v = min_value(mv,d+1,oppo,player)

		if v > best_score:
				best_score = v
				best_action = a

		#print best_score
	return [max_score,best_score,best_action,state]

def printstate(A):
	nextstep=[]
	before=A[1]

	after=A[0]
	B_letter=row[before[0]]
	B_number=before[1]+1
	A_letter=row[after[0]]
	A_number=after[1]+1
	return B_letter+str(B_number)+'-'+A_letter+str(A_number)

################minimax works###############
if play_method=='MINIMAX':
    #print my_player

	state=1
	minimax=minimax_value(table_state,my_player,0)
	if(minimax[2]!='pass'):
		next_move=printstate(minimax[2])
	else:
		next_move='pass'
	myopic=str(minimax[0])
	farsighted=str(minimax[1])
	final_state=str(minimax[3])
else:
	state=1
	minimax=alphabeta_value(table_state,my_player,0)
	if(minimax[2]!='pass'):
		next_move=printstate(minimax[2])
	else:
		next_move='pass'
	myopic=str(minimax[0])
	myopic=str(minimax[0])
	farsighted=str(minimax[1])
	final_state=str(minimax[3])
f1=open('output.txt',"w")
f1.write(next_move)
f1.write('\n')
f1.write(myopic)
f1.write('\n')
f1.write(farsighted)
f1.write('\n')
f1.write(final_state)
f1.close()



    # f1=open('output.txt',"w")
    # f1.write(next_state)
    # f1.close()
    # print next_state
