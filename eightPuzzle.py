#Natalie Carlson
#Linda Lee
#William de Schweinitz

#CSCE 405 AI
#Due: Sept 19, 2019
#Assignment 1: 8-state


import queue
import time

##################################################
#Main method
##################################################
def main():
	
	searchMethod = 0 #hold user desired search method
	repeat = 'x' #give user option to repeat program

##############################################################
#Get user input for start and goal states
#	state = 'a'
#	while not state.isdigit() or len(state) != 9:
#		state = input("\nEnter initial state in the form 012345678, use 0 for the blank tile: ")
#	initialState = list(map(int, state))
#	
#	state = 'a'
#	while not state.isdigit() or len(state) != 9:
#		state = input("\nEnter goal state in the form 012345678, use 0 for the blank tile: ")
#	goalState = list(map(int, state))
#		
#	#Verify user input for start and goal states
#	inputCheck = 'x' #verify user entry is correct
#	while (inputCheck != 'y' and inputCheck != 'n'):
#		print("\nYou entered:\nInitial state: ", initialState, "\nGoal state: ", goalState)
#		inputCheck = input("Is this correct?\nYes: enter y\nNo: enter n\n")
#		if inputCheck == 'y':	
#			continue
#		elif inputCheck == 'n':
#			print("Let's try again.")
#			main()
#		else:
#			print("Invalid entry.")

####################################################
#Test cases (comment out "#Get user input for start and goal states" section above)

	#D4
#	initialState = [0,1,3,4,2,5,7,8,6]
#	goalState = [1,2,3,4,5,6,7,8,0]
	#D7
#	initialState = [1,2,3,5,6,8,4,0,7]
#	goalState = [1,2,3,4,5,6,7,8,0]
	#D9 Slide
#	initialState = [2,0,6,1,3,4,7,5,8]
#	goalState = [1,2,3,4,5,6,7,8,0]
	#D26
#	initialState = [7,2,4,5,0,6,8,3,1]
#	goalState = [0,1,2,3,4,5,6,7,8]
	#D31
	initialState = [8,0,6,5,4,7,2,3,1]
	goalState = [0,1,2,3,4,5,6,7,8]
#####################################################
	
	again = 'y'
	while (again == 'y'):
		#check parity and if match continue on to solve puzzle
		if parityCheck(initialState) == parityCheck(goalState):	
			root = Node(initialState, None, 0, 0) #create root node
			
			#Get user input for search method
			while (searchMethod < 1 or searchMethod > 4 ):
				searchMethod = int(input("\nSelect a search method.\nBreadth-First Search: enter 1\nMisplace Tiles heuristic: enter 2\nManhattan Distance heuristic: enter 3\nGaschnig heuristic: enter 4\nSelection: "))
			
				if searchMethod == 1:
					start = time.time()
					root.h = getH(root.state, goalState, 1)
					solution = breadthFirst(root, goalState)
					end = time.time()
					t = end - start
					print("Time elapse: ", t)
					printSolution(solution)
				
				elif searchMethod == 2:
					start = time.time()
					root.h = getH(root.state, goalState, 2)
					solution = aStarSearch(root, goalState, 2)
					end = time.time()
					t = end - start
					print("Time elapse: ", t)
					printSolution(solution)
					
				elif searchMethod == 3:
					start = time.time()
					root.h = getH(root.state, goalState, 3)
					solution = aStarSearch(root, goalState, 3)
					end = time.time()
					t = end - start
					print("Time elapse: ", t)
					printSolution(solution)

				elif searchMethod == 4:
					start = time.time()
					root.h = getH(root.state, goalState, 4)
					solution = aStarSearch(root, goalState, 4)
					end = time.time()
					t = end - start
					print("Time elapse: ", t)
					printSolution(solution)
				else:
					print("Invalid entry.")
					
		else:
			print("Parity of puzzles do not match.  No solution possible.\n")
		
		again = input("\nWould you like to repeat the puzzle with a different search method?\nYes: enter y\nNo: enter n\n")
		searchMethod = 0 #re-set
		
	#Give user option to re-start program
	while (repeat != 'n' and repeat != 'y'):
		repeat = input("\nWould you like to start a new state?\nYes: enter y\nNo: enter n\n")
		if repeat == 'y':
			main() #restart
		elif repeat == 'n':
			print("Good-bye")
			exit
		else:
			print("Invalid entry.")

#########################################################
#Node Class
#########################################################
class Node:
	
	#Node variables
	def __init__(self, state, parentNode, g, h):
	
		self.state = state
		self.parentNode = parentNode
		self.g = g #number of steps it took to get to this state from initial state
		self.h = h #hueristic weight
		self.childList = [] #create empty list to store child Nodes
		
	#This method creates child nodes of a current node
	def createChildren(self, nodeDict, goal, search):
		
		h = 0		
		
		#find space('0') tile
		blankIndex = 0
		for i in range(0,9):
			if self.state[i] == 0:
				blankIndex = i
		
		#find child states
		childStatesList = [] #temporary list to hold child states
		#right child
		rightList = [0,1,3,4,6,7]
		if blankIndex in rightList:		
			childState = swap(self.state, blankIndex, blankIndex + 1)
			childStatesList.append(childState)
		#down child
		if blankIndex < 6: 		
			childState = swap(self.state, blankIndex, blankIndex + 3)
			childStatesList.append(childState)					
		#left child
		leftList = [1,2,4,5,7,8]
		if blankIndex in leftList: 
			childState = swap(self.state, blankIndex, blankIndex - 1)
			childStatesList.append(childState)
		#up child
		if blankIndex > 2:		
			childState = swap(self.state, blankIndex, blankIndex - 3)
			childStatesList.append(childState)
		
		#create children from childStatesList
		for childState in childStatesList:	
			h = getH(childState, goal, search)
			childKey = ','.join(map(str, childState))
			if childKey not in nodeDict: #only add if new state
				self.childList.append(Node(childState, self, self.g + 1, h)) #create child and connect to current node
				nodeDict.update({childKey : None}) #add to dict					


#################################################################################
#Search Methods
#################################################################################

#BreadthFirst search method
def breadthFirst(root, goal):
	
	expanded = 0 #closed count
	searchSpace = 0 #max open count
		
	if root.state == goal:#goal check
		print("\nMax search space: ", searchSpace, " Total Nodes expanded: ", expanded)
		return root
	
	nodeDict = {} #create dictionary of discovered nodes/states
	q = queue.Queue() #create queue
	q.put(root)  #add node to back of queue
	while(1):  #repeat until solution found
		if q.qsize() > searchSpace: #update max open count
			searchSpace = q.qsize()
		currentNode = q.get() #remove node at front of queue		
		nodeDict.update({(','.join(map(str, currentNode.state))) : None}) #add node/state to dict
		currentNode.createChildren(nodeDict, goal, 1) #expand node
		expanded += 1 #increase expanded count
		
		for child in currentNode.childList:
				if child.state == goal: #goal check
					print("\nMax search space: ", searchSpace, " Total Nodes expanded: ", expanded)
					return child
				q.put(child) #add child node to back of queue

#A* search method				
def aStarSearch(root, goal, searchCode):

	expanded = 0
	searchSpace = 0
	#goal check
	if root.state == goal:
		print("\nMax search space: ", searchSpace, " Total Nodes expanded: ", expanded)
		return root
	
	nodeDict = {} #create dictionary
	pq = queue.PriorityQueue() #create queue
	entry = pqEntry(root.g + root.h, root) #create pq entry object, set f(n)
	pq.put(entry) #add entry to queue
	while(1):
		if pq.qsize() > searchSpace: #update max queue size
			searchSpace = pq.qsize()
		best = pq.get() #remove entry with lowest priority
		currentNode = best.node
		nodeDict.update({currentNode : None}) #add to list of visited nodes
		currentNode.createChildren(nodeDict, goal, searchCode) #expand node
		expanded += 1 #increase expanded count
		
		for child in currentNode.childList:
				if child.state == goal:
					print("\nMax search space: ", searchSpace, " Total Nodes expanded: ", expanded)
					return child
				entry = pqEntry(child.g + child.h, child) #create pq entry object, set f(n)
				pq.put(entry) #add child entry to queue	
	
################################################
#Huerisitc methods
################################################

#This method directs the state to the proper hueristic method based on the users selection
def getH(state, goal, search):

	if search == 1: #breadthFirst(non-hueristic)
		h = 0
	if search == 2:
		h = misplacedTiles(state, goal)
	if search == 3:
		h = manhattanDistance(state, goal)
	if search == 4:
		h = gaschnigHeuristic(state, goal)
	return h

#This hueristic method calculates the number of out of order tiles
def misplacedTiles(state, goal):
	
	h = 0
	for i in range (1,9):
		if state[i] != goal[i]:
			h += 1
	return h

#This hueristic method calculates the step distance of each tile between current state and goal state
def manhattanDistance(state, goal):
	
	h = 0
	stepChart = [
	[0,1,2,1,2,3,2,3,4],
	[1,0,1,2,1,2,3,2,3],
	[2,1,0,3,2,1,4,3,2],
	[1,2,3,0,1,2,1,2,3],
	[2,1,2,1,0,1,2,1,2],
	[3,2,1,2,1,0,3,2,1],
	[2,3,4,1,2,3,0,1,2],
	[3,2,3,2,1,2,1,0,1],
	[4,3,2,3,2,1,2,1,0]]
	
	for i in range(0,9):
		if state[i] != 0:
			h += stepChart[i][goal.index(state[i])]
	return h		

#This hueristic method calculates the number of swaps with the blank space between currentState and goal state
def gaschnigHeuristic(state, goal):
	
	h = 0
	pList = state[:]#state #current permutation
	bList = [] #holds index numbers of pList from element of goal
	while (1):
		if (pList == goal):
			return h
		
		for num in goal: #get element from goal
			bList.append(pList.index(num))#find corresponding index in pList
		
		if (pList.index(0) == bList[pList.index(0)]): #blank is in correct spot
			i = 0
			while pList[i] == goal[i] and i < 8: #search for element out of place
				i += 1
			pList = swap(pList, pList.index(0), i) #swap blank with correct value for index
			
		else:
			pList = swap(pList, pList.index(0), bList[pList.index(0)]) #swap blank with correct value for index
		
		h += 1 #increase h count
		bList.clear()#empty array to start over


#########################################################
#Helper Methods
#########################################################

#This class supplements Priority Queue by limiting comparison to the first element only
class pqEntry(object):
	
	def __init__(self, priority, node):
		self.priority = priority
		self.node = node
	
	def __lt__(self, other):
		return self.priority < other.priority


#This method checks if the puzzle has an odd or even parity
def parityCheck(state):

	count = 0 #hold number of unordered pairs
	for i in range(9):
		if state[i] != 0:
			for j in range(i, 9):
				if state[j] != 0 and state[i] > state[j]:
					count += 1

	if count % 2 == 0:
		return "Even"
	else:
		return "Odd"

#This method takes a list, swaps two of the elements and returns a new modified list
def swap(currentState, indexA, indexB):
	
	newState = currentState[:] #copy starting state
	newState[indexA], newState[indexB] = newState[indexB], newState[indexA] #swap elements
	return newState
	
#This method prints the pathway from solution to root
def printSolution(node):

	pathway = []
	pathway.insert(0,node)
	while node.parentNode != None:
		node = node.parentNode
		pathway.insert(0,node)
	
	print("Pathway from initial state to goal state:")
	for n in pathway:
		print("state: ", n.state, " g: ", n.g, " h: ", n.h)
		
		

############################################
#Run Program
############################################

if __name__ == '__main__':
	main()