import sys
import operator
import copy
import time

since=time.time()

f=open('input.txt','r')
array=[]
for line in f:
	array.append(line.rstrip('\n'))
for i in range(len(array)):
	array[i]=array[i].split(',')
arrayindex=0

row=(int)(array[0][0])
col=(int)(array[0][1])
arrayindex+=1

wall=[]
for i in range((int)(array[arrayindex][0])):
	wall.append(array[i+arrayindex+1])
arrayindex+=len(wall)+1

terminal=[]
for i in range((int)(array[arrayindex][0])):
	terminal.append(array[i+arrayindex+1])
arrayindex+=len(terminal)+1
probability=[]
probability.append(array[arrayindex])
pw=(float)(probability[0][0])
pr=(float)(probability[0][1])
arrayindex+=1

reward=[]
reward.append(array[arrayindex])
rw=(float)(reward[0][0])
rr=(float)(reward[0][1])

gamma=(float)(array[len(array)-1][0])

grid_u0=[[0 for i in range(col)] for j in range(row)]
grid_action=copy.deepcopy(grid_u0)

for i in range(len(wall)):
	r=(int)(wall[i][0])
	c=(int)(wall[i][1])
	grid_u0[r-1][c-1]="wall"

termi_dict={}
termi_index=[]
for i in range(len(terminal)):
	r=(int)(terminal[i][0])
	c=(int)(terminal[i][1])
	termi_index.append([r-1,c-1])
	index=(str)(r-1)+(str)(c-1)
	termi_dict[index]=(float)(terminal[i][2])
	grid_u0[r-1][c-1]='T'
#grid_u1=copy.deepcopy(grid_u0)
print termi_dict
print termi_index

def transition(grid_u0, index,category, action):
	trans=[]
	if category==1:
		if action=="Walk Up":
			if index[0]==row-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+1,index[1]])
			if index[1]==col-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+1])
			if index[1]==0:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-1])
		elif action=="Walk Down":

			if index[0]==0:

				trans.append([index[0],index[1]])
			else:

				if grid_u0[index[0]-1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-1,index[1]])
			if index[1]==col-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+1])
			if index[1]==0:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-1])
		elif action=="Walk Right":
			if index[1]==col-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+1])
			if index[0]==row-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+1,index[1]])
			if index[0]==0:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]-1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-1,index[1]])
		else:
			if index[1]==0:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-1])
			if index[0]==row-1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+1,index[1]])
			if index[0]==0:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]-1][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-1,index[1]])
	else:
		if action=="Run Up":
			if index[0]>=row-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall" or grid_u0[index[0]+2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+2,index[1]])
			if index[1]>=col-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall" or grid_u0[index[0]][index[1]+2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+2])
			if index[1]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall" or grid_u0[index[0]][index[1]-2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-2])
		elif action=="Run Down":
			if index[0]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]-1][index[1]]=="wall" or grid_u0[index[0]-2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-2,index[1]])
			if index[1]>=col-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall" or grid_u0[index[0]][index[1]+2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+2])
			if index[1]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall" or grid_u0[index[0]][index[1]-2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-2])
		elif action=="Run Right":
			if index[1]>=col-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]+1]=="wall" or grid_u0[index[0]][index[1]+2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]+2])
			if index[0]>=row-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall" or grid_u0[index[0]+2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+2,index[1]])
			if index[0]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]-1][index[1]]=="wall" or grid_u0[index[0]-2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-2,index[1]])
		else:
			if index[1]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]][index[1]-1]=="wall" or grid_u0[index[0]][index[1]-2]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0],index[1]-2])
			if index[0]>=row-2:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]+1][index[1]]=="wall" or grid_u0[index[0]+2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]+2,index[1]])
			if index[0]<=1:
				trans.append([index[0],index[1]])
			else:
				if grid_u0[index[0]-1][index[1]]=="wall" or grid_u0[index[0]-2][index[1]]=="wall":
					trans.append([index[0],index[1]])
				else:
					trans.append([index[0]-2,index[1]])
	return trans


actions=[["Run Right","Run Left","Run Down","Run Up"],["Walk Right","Walk Left","Walk Down","Walk Up"]]
'''for x in range(len(actions)):
	for y in range(len(actions[x])):
		print transition(grid_u0, [4,4],x, actions[x][y])'''
walk_and_run=[]
for a in range(row):
	walk_and_run_idx = []
	for b in range(col):
		walk_and_run_idx_idx=[]
		for i in range(len(actions)):
			walk_and_run_idx_idx_idx=[]
			for j in range(len(actions[i])):
				trans = transition(grid_u0, [a,b], i, actions[i][j])
				walk_and_run_idx_idx_idx.append(trans)
			walk_and_run_idx_idx.append(walk_and_run_idx_idx_idx)
		walk_and_run_idx.append(walk_and_run_idx_idx)
	walk_and_run.append(walk_and_run_idx)

def compute_value(grid_u0, index,delta):
	heigest=float('-inf')
	action=""
	
	if grid_u0[index[0]][index[1]]=="wall":
		grid_action[index[0]][index[1]]="None"
		return delta
	elif grid_u0[index[0]][index[1]]=='T':
		delta=max(delta,0)
		grid_action[index[0]][index[1]]="Exit" 
		return delta
	else:
		for i in range(len(actions)):
			for j in range(len(actions[i])):
				total=0
				ftotal=0
				trans=walk_and_run[index[0]][index[1]][i][j]
				#print trans
				#print trans,index,actions[i][j]
				if i==1:
					for z in range(len(trans)):
						if z==0:
							if grid_u0[trans[z][0]][trans[z][1]]!='T':
								#print pw
								total+=pw*grid_u0[trans[z][0]][trans[z][1]]
							else:
								#print termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
								total+=pw*termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
								#print "total",total
						else:
							if grid_u0[trans[z][0]][trans[z][1]]!='T':
								total+=0.5*(1-pw)*grid_u0[trans[z][0]][trans[z][1]]
							else:
								#print termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
								total+=0.5*(1-pw)*termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
						
					
					ftotal=rw+gamma*total
					if heigest<=ftotal:
						heigest=ftotal
						action=actions[i][j]
						#if index[0]==4 and index[1]==5:
							#print heigest, actions[i][j]	
				else:
					for z in range(len(trans)):
						if z==0:
							if grid_u0[trans[z][0]][trans[z][1]]!='T':
								total+=pr*grid_u0[trans[z][0]][trans[z][1]]
							else:
								#print termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]

								total+=pr*termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
								#print total, actions[i][j],index
						else:
							if grid_u0[trans[z][0]][trans[z][1]]!='T':
								#print grid_u0[trans[z][0]][trans[z][1]]
								
								total+=0.5*(1-pr)*grid_u0[trans[z][0]][trans[z][1]]
							else:
								#print termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
								#print trans[z][0],trans[z][1]
								total+=0.5*(1-pr)*termi_dict[(str)(trans[z][0])+(str)(trans[z][1])]
					#print total, actions[i][j],index
					ftotal=rr+gamma*total
					#print ftotal,total, actions[i][j],index
					if heigest<=ftotal:
						heigest=ftotal
						action=actions[i][j]
						#if index[0]==4 and index[1]==5:
						#	print heigest, actions[i][j]
	grid_action[index[0]][index[1]]=action
	delta=max(delta,abs(heigest-grid_u0[index[0]][index[1]]))
	#print delta,"delta1"
	grid_u0[index[0]][index[1]]=heigest
	return delta

def value_iteration(grid_u0,epsilon):
	global forloop
	forloop=0
	#print x1,x2,y1,y2
	while True:
		print len(termi_index), "length"
		delta=float('-inf')
		for i in range(len(termi_index)):
			#print i,"i"
			
			#print delta
			x1=termi_index[i][0]
			y1=termi_index[i][1]
			x2=termi_index[i][0]+1
			y2=termi_index[i][1]+1

			while(x1>=0 or x2<=row-1):
				#print x1
				if x1>=0:
					y1=termi_index[i][1]
					while(y1>=0):
						#print y1
						index=[x1,y1]
						#print index
						delta=compute_value(grid_u0, index,delta)
						#print delta
						y1-=1
					y2=termi_index[i][1]+1
					while(y2<=col-1):
						#print y2
						index=[x1,y2]
						#print index
						delta=compute_value(grid_u0, index,delta)
						#print delta
						#print grid_u1,"grid_u1"
						y2+=1
					x1-=1
				if x2<=row-1:
					y1=termi_index[i][1]
					while(y1>=0):
						index=[x2,y1]
						#print index
						delta=compute_value(grid_u0, index,delta)
						#print delta
						#print grid_u1,"grid_u1"
						y1-=1
					y2=termi_index[i][1]+1
					while(y2<=col-1):
						index=[x2,y2]
						#print index
						delta=compute_value(grid_u0, index,delta)
						#print delta,"delta"
						y2+=1
					x2+=1
			forloop+=1
			print forloop
			print delta,epsilon*(1-gamma)/gamma
			if delta<=epsilon*(1-gamma)/gamma:
				return grid_u0

#print walk_and_run
value_iteration(grid_u0,0)

'''x=0
for i in range(row):
	for j in range(col):
		index=[]
		index.append(i)
		index.append(j)
		compute_value(grid_u0, index)
grid_u0=copy.deepcopy(grid_u1)
#print grid_u0,"grid_u0"
#print grid_u1,"grid_u1"
x+=1
print grid_u1,"grid_u1"'''
#print grid_action
for i in range(row):
	print grid_u0[i]
# for i in range(row):
#  	print grid_action[i]
'''final=grid_action
for i in range(len(grid_action)-1,-1,-1):
	final[i]=grid_action[i]
print final,"final"'''
f1=open('output.txt',"w")
for i in range(len(grid_action)-1,-1,-1):
   s=(str(grid_action[i])).replace('[',"").replace("]","").replace("\'","").replace(", ",",")
   f1.write(s)
   f1.write("\n")
f1.close()

time_e=time.time()-since
print('Training complete in {:.0f}m {:.0f}s'.format(time_e // 60, time_e % 60))