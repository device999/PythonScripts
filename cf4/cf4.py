from	Tkinter	import	*
import	numpy	as	np
import	random
import	math
LINE=6
COLUMN	=	7
POSITION	=	np.zeros((6,2))
#By	this	function	we	define	who's	turn	it	is
def	turn(x):
	if	x%2==0:
		return	0
	else	:
		return	1
#this functions checks whether there are 3 neighbors of our point and return the 1 in case player 1 won
# 2 case player 2 won and 0 in all other cases
#return	1	and	2	is	the	player's	number
def	gameOver(number,player):
	if	number>=3	and	player==1:
		return	1
	elif	number>=3	and	player==2:
		return	2
	else:
		return	0
#this	procedure	checks	the	content	of	upper	and	down	elements
#grid	is	the	board
#player	is	the	current	player
#line and column are initial points
def	checkUpandDown(grid,line,column,player):
	check	=	0
	xup	=	line
	xdown	=	line
	while	True:
		if	xdown>0	and grid[xdown-1][column]==player:
			check	=	check+1
			xdown	=	xdown	-	1
		elif	xup<LINE-1	and	grid[xup+1][column]==player:
			check	=	check	+	1
			xup	=	xup	+	1
		else:
			break
	return	gameOver(check,player)
#this	procedure	checks	the	content	of	right	and	left	elements
#grid	is	the	board
#player	is	the	current	player
#line and column are initial points
def	checkRightandLeft(grid,lin,column,player):
	check	=	0
	columnr	=	column
	columnl	=	column
	while	True:
		if	columnl>0	and	grid[lin][columnl-1]==player:
			check	=	check+1
			columnl	=	columnl	-	1
		elif	columnr<COLUMN-1	and	grid[lin][columnr+1]==player:
			check	=	check	+	1
			columnr	=	columnr	+	1
		else:
			break
	return	gameOver(check,player)
#this	procedure	checks	the	content	of	upper left	and	down right elements
#grid	is	the	board
#player	is	the	current	player
#line and column are initial points
def checkDiagonalLeftUpRightDown(grid,line,column,player):
	check=	0
	x1	=	line
	x2	=	line
	y1	=	column
	y2	=	column
	done	=	0
	while	True:
		if	y1<COLUMN-1	and	x1<LINE-1	and	grid[x1+1][y1+1]==player:
			check	=	check+1
			y1	=	y1+1
			x1	=	x1+1
		elif	y2>0	and	x2>0	and	grid[x2-1][y2-1]==player:
			check	=	check	+	1
			x2	=	x2	-	1
			y2	=	y2	-	1
		else:
			break
	return	gameOver(check,player)
#this	procedure	checks	the	content	of	upper right	and	down left	elements
#grid	is	the	board
#player	is	the	current	player
#line and column are initial points
def	checkDiagonalRightUpLeftDown(grid,line,column,player):
	check	=	0
	x1	=	line
	x2	=	line
	y1	=	column
	y2	=	column
	done	=	0
	while	True:
		if	y1<COLUMN-1	and	x1>0	and	grid[x1-1][y1+1]==player:
			check	=	check+1
			x1	=	x1-1
			y1	=	y1+1
		elif	y2>0	and	x2<LINE-1	and	grid[x2+1][y2-1]==player:
			check	=	check	+	1
			x2	=	x2	+	1
			y2	=	y2	-	1
		else:
			break
	return	gameOver(check,player)
	
#we	are	checking	the	fullness	of	the	array
#in other words we are defining whether the board is full or not
def	checkFullness(array):
	layers	=	42
	z=0
	for	row	in	array:
		for	elem	in	row:
			if	elem!=0:
				layers	=	layers-1
				z	=	z+1
			else:
				z	=	z+1
	if	layers==0:
		return	1
	else	:
		return	2
#This function is child of nextMove function
#some times while checking the diagonal elements or horizontal ones
#we can deal with the situation that some layer has 3 element in neighbor horizontally
#but this layer's down line is empty,therefore it is not considered as a dangerous one untill that line will be filled
def	checkdownNeighbor(grid,liniya,column,player):
	if	liniya<LINE-1:
		if	grid[liniya+1][column]!=0:
			return	1
		else:
			return	0
	elif liniya==LINE-1:
		if grid[liniya][column]==0:
			return	1
		else:
			return	0
	else	:
		return	0
#if number which is the number of neighbors is more than 3,game ends with
#assigning the player's victory
def	gameOver(number,player):
	if	number>=3	and	player==1:
		return	1
	elif	number>=3	and	player==2:
		return	2
	else:
		return	0
# in this function we are using brute force approach to find 3 neighbors out of 4
# and help the user not to lose and not to win  another user respectively.
def	nextMove(a,player):
	line_in	=	0
	column_in	=	0
	empty	=	0
	while	line_in<6:
		if	a[line_in][column_in]==0:
			if	checkUpandDown(a,line_in,column_in,player)==player:
				return	column_in
				break
			elif	checkRightandLeft(a,line_in,column_in,player)==player:
				empty = checkdownNeighbor(a,line_in,column_in,player)
				if empty==1:
					return	column_in
					break
				else:
					column_in	=	column_in+1
					if	column_in==	7:
						column_in	=	0
						line_in	=	line_in	+	1
			elif	checkDiagonalLeftUpRightDown(a,line_in,column_in,player):
				empty = checkdownNeighbor(a,line_in,column_in,player)
				if empty==1:
					return	column_in
					break
				else:
					column_in	=	column_in+1
					if	column_in==	7:
						column_in	=	0
						line_in	=	line_in	+	1
			elif	checkDiagonalRightUpLeftDown(a,line_in,column_in,player)==player:
				empty	=	checkdownNeighbor(a,line_in,column_in,player)
				if	empty==1:
					return	column_in
					break
				else:
					column_in	=	column_in+1
					if	column_in==	7:
						column_in	=	0
						line_in	=	line_in	+	1
			else:
				column_in=column_in+1
				if	column_in==	7:
					column_in	=	0
					line_in= line_in+1
		else:
			column_in=column_in+1
			if	column_in==	7:
				column_in	=	0
				line_in= line_in+1
	if	(line_in==6):
		return	-1
#my graphical interface
def	Start(a):
	root	=	Tk()
	column_coord	=	np.array([77,104,131,158,185,212])
	line_coord	=	np.array([102,129,156,183,210])
	text_coord	=	np.array([67,90,121,145,170,197,227])
	canvas	=	Canvas(root,	width=300,	height=300)
	canvas.pack(fill=BOTH)
	z=0
	for el in text_coord:
		canvas.create_text(text_coord[z],65,text=str(z))
		z=z+1
	canvas.create_rectangle(50,75,240,235,	outline="black")
	i=0
	for	element	in	column_coord:
		canvas.create_line(column_coord[i],75,column_coord[i],235,fill="black")
		i	=	i	+1
	j=0
	for	elem	in	line_coord:
		canvas.create_line(50,line_coord[j],240,line_coord[j],fill="black")
		j	=	j+1
	line_in	=	0
	column_in	=	0
	x_in	=	50
	y_in	=	75
	while	line_in<6:
		if	a[line_in][column_in]==1:
			canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="red")
		elif	a[line_in][column_in]==2:
			canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="blue")																								
		column_in	=	column_in+1
		if	column_in==	7:
			column_in	=	0
			line_in	=	line_in	+	1
	root.mainloop()
if	__name__=="__main__":
	a	=	np.zeros((LINE,COLUMN))
	print "   0   1   2   3   4   5   6"
	print	a
	line	=	0
	column	=	0
	step	=	0
	winner	=	0
	enemy	=	0
	attacker = -1
	defender = -1
	while	checkFullness(a)!=1	and	winner==0:
		if	turn(step)==0:
			player=1
			enemy=2
			print	"Player 1 plays"
		else:
			player=2
			enemy	=	1
			print	"Player 2 plays"
		pos	=	5
		#We	can	input	it	or	random
		if	nextMove(a,enemy)!=-1:
			defender = nextMove(a,enemy)
			print	"To defence put your coin to the column = "+str(defender)
		if	nextMove(a,player)!=-1	:
			attacker = nextMove(a,player)
			print	"To attack put your coin to the column = "+str(attacker)
		#Start(a)
		r	=	input("Enter the position= ")
		if	a[pos][r]!=0:
			while	a[pos][r]==1	or	a[pos][r]==2:
				if	pos-1>-1:
					if	a[pos-1][r]==1	or	a[pos-1][r]==2:
						pos	=	pos-1
					else:
						a[pos-1][r]	=	player
						line	=	pos	-1
						column	=	r
						break
				else:
					print	"This column is full"
					print	"Please replay"
					step	=	step	-	1
					break
		else	:
			a[5][r]=player
			line	=	5
			column	=	r
		print "   0   1   2   3   4   5   6"
		print	a
		step	=	step+1
		if a[line][column]==player :
			winner	=	checkUpandDown(a,line,column,player)
			if	winner==0:
				winner	=	checkRightandLeft(a,line,column,player)				
				#print	"Right"
				if	winner==0:
					winner	=	checkDiagonalRightUpLeftDown(a,line,column,player)
					if winner==0:
						winner=checkDiagonalLeftUpRightDown(a,line,column,player)
		print "Player " +str(player)+" played at position = "+str(r)
	#Start(a)
	if	winner==1:
		print	"Player 1 wins"
	elif	winner==2:
		print	"Player 2 wins"
	else	:
		print	"Draw"
	Start(a)

