
import copy
import sys
import random

#justify reasonable
def Judge(pot,confederation):
	for line in pot:
		if(len(line)>group_num):
			return False
	for line in confederation:
		if(line[0]!="UEFA" and len(line)>group_num):
			return False
		elif(line[0]=='UEFA'):
			x=0
			if len(line)%2!=0:
				x=1;
			num=len(line)/2+x
			if num>group_num:
				return False
	return True

def find_confederation(city):
		for i in range(len(confederation)):
			for j in range(1,len(confederation[i])):
				if(confederation[i][j]==city):
					return confederation[i][0]


def min_conflicts(country,group):
	res=0
	count_UEFA=0

	for i in range (len(group)):

		if(group[i][1]==country[1]):
			res+=1
		if(group[i][2]==country[2]):
			res+=1
		if(group[i][2]=='UEFA'):
			count_UEFA+=1
	if(count_UEFA==1 and country[2]=='UEFA'):
		res-=1
	return res


def buildgroups(countries,groups):

	country_boolean=[False for i in range(len(countries))]
	for i in range(len(countries)):

		for j in range(len(groups)):
			each_con=min_conflicts(countries[i],groups[j])
			if each_con==0 and not country_boolean[i]:
				groups[j].append(countries[i])
				country_boolean[i]=True

	return groups,country_boolean

def country_conflict(c1,c2):
	res=0
	if(c1[1]==c2[1]):
		res+=1
	if(c1[2]==c2[2]):
		res+=1
	return res

def country_replace(groups,rest_first_country,rest_country,index,i):
	rest_country.append(groups[index][i])
	rest_country.remove(rest_first_country)
	groups[index][i]=rest_first_country
	return groups,rest_country

def exchange(rest_country,groups):
	count=0
	while(count<10):

		rest_first_country=random.choice(rest_country)

		min_conflict_val=[]
		minimax_conflict=sys.maxint
		index=0
		for i in range(len(groups)):
			min_value=min_conflicts(rest_first_country,groups[i])
			min_conflict_val.append(min_value)
			if(min_conflict_val[i]<minimax_conflict):
				index=i
				minimax_conflict=min_conflict_val

		for i in range(len(groups[index])):

			res=min_conflicts(rest_first_country,groups[index][0:i])+min_conflicts(rest_first_country,groups[index][i+1:len(groups[index])])
			country_con=country_conflict(rest_first_country,groups[index][i])
			if(country_con==2):
				continue
			if country_con==1 and res==0:
				groups,rest_country=country_replace(groups,rest_first_country,rest_country,index,i)
				groups,country_boolean=buildgroups(rest_country,groups)
				rest_country=[]
				for i in range(len(country_boolean)):
					if(not country_boolean[i]):
						rest_country.append(countries[i])
		count+=1
	if len(rest_country)==0:
		return groups
	else:
		return 'No'


f=open('input1.txt','r')
array=[]
for line in f:
	array.append(line.rstrip('\n'))
group_num=array[0];
pot_num=array[1];
pot=[]
for line in range(2,2+(int)(pot_num)):
	list1=array[line].split(',')
	pot.append(list1)
confederation=[]
for line in range(2+(int)(pot_num),len(array)):
	list1=array[line].replace(':',',').split(',')
	confederation.append(list1)
for i in range(len(pot)):
	for j in range(len(pot[i])):
		pot[i][j]=pot[i][j].rstrip()
for i in range(len(confederation)):
	for j in range(len(confederation[i])):
		confederation[i][j]=confederation[i][j].rstrip()

boolean=Judge(pot, confederation)
if(not boolean):
	f1=open('output.txt','w')
	f1.write('No')
	f1.close()
else:

	countries=[]
	for i in range(len(pot)):
		for j in range(len(pot[i])):
			temp=[]
			temp.append(pot[i][j])
			temp.append(i)
			conf=find_confederation(pot[i][j])
			temp.append(conf)
			countries.append(temp)

	groups=[]
	for i in range(int(group_num)):
		groups.append([])

	groups,country_boolean=buildgroups(countries,groups)

	rest_country=[]
	for i in range(len(country_boolean)):
		if(not country_boolean[i]):
			rest_country.append(countries[i])

	if len(rest_country)==0:
		decision='Yes'
		results=groups

	else:
		results=exchange(rest_country,groups)
		if results!='No':
			decision='Yes'

		else:
			decision=results

	if decision=='No':
		f1=open('output.txt','w')
		f1.write(decision)
		f1.close()
	else:
		f1=open('output.txt','w')
		f1.write(decision)
		f1.write('\n')
		for i in range(len(results)):
			temp=''
			for j in range(len(results[i])):
				temp+=results[i][j][0]
				if(j!=len(results[i])-1):
					temp+=','
			if(len(results[i])==0):
				temp='None'
			f1.write(temp)
			f1.write('\n')
		f1.close()
