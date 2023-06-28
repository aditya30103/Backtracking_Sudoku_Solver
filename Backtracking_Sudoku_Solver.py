from typing import Tuple, List
# No other imports allowed

# PART OF THE DRIVER CODE

def input_sudoku() -> List[List[int]]:
	"""Function to take input a sudoku from stdin and return
	it as a list of lists.
	Each row of sudoku is one line.
	"""
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	"""Helper function to print sudoku to stdout
	Each row of sudoku in one line.
	"""
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

# You have to implement the functions below

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes a parameter position and returns
	the block number of the block which contains the position.
	"""
	a=pos[0]-1
	b=pos[1]-1

	row_val=(a-a%3)+1
	col_val=b//3
	block_no=row_val+col_val
	return block_no

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes parameter position
	and returns the index of the position inside the corresponding block.
	"""
	a=pos[0]-1
	b=pos[1]-1
	block_num=get_block_num(sudoku,(a+1,b+1))

	up_i=a-a%3
	block_position=((a-up_i)*3)+(b%3)+1
	return block_position

def get_block(sudoku:List[List[int]], x: int) -> List[int]:
	"""This function takes an integer argument x and then
	returns the x^th block of the Sudoku. Note that block indexing is
	from 1 to 9 and not 0-8.
	"""
	a=x-1
	row=[]
	col=[]
	block=[]

	# Getting Row Indices
	m=a//3
	row = [3*m,3*m+1,3*m+2]							

	# Getting Column Indices
	n=a%3
	col = [3*n,3*n+1,3*n+2]							

	for i in row:
		for j in col:
			block.append(sudoku[i][j])				

	return block
	
def get_row(sudoku:List[List[int]], i: int)-> List[int]:
	"""This function takes an integer argument i and then returns
	the ith row. Row indexing have been shown above.
	"""
	row=[]
	row_index=i-1
	row=sudoku[row_index]
	return row

def get_column(sudoku:List[List[int]], x: int)-> List[int]:
	"""This function takes an integer argument i and then
	returns the ith column. Column indexing have been shown above.
	"""
	col=[]
	col_index=x-1

	for i in sudoku:
		col.append(i[col_index])
	return col

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:
	"""This function returns the first empty position in the Sudoku. 
	If there are more than 1 position which is empty then position with lesser
	row number should be returned. If two empty positions have same row number then the position
	with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
	"""
	for i in sudoku:
		for j in i:
			if j==0:
				return (sudoku.index(i)+1,i.index(j)+1)
	
	return (-1,-1)

def valid_list(lst: List[int])-> bool:
	"""This function takes a lists as an input and returns true if the given list is valid. 
	The list will be a single block , single row or single column only. 
	A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
	"""
	
	# Create a Clone of lst in order to preserve Sudoku list
	clone_lst=lst.copy()
	clone_lst.sort()

	for i in range(0,8):
		if clone_lst[i]==clone_lst[i+1] and clone_lst[i]!=0:
			return False
	return True

def valid_sudoku(sudoku:List[List[int]])-> bool:
	"""This function returns True if the whole Sudoku is valid.
	"""
	
	# Checking validity of rows
	for i in range(1,10):	
		if valid_list(get_row(sudoku,i))== False:
			return False
	
	# Checking validity of columns
	for i in range(1,10):	
		if valid_list(get_column(sudoku,i))== False:
			return False
	
	# Checking validity of blocks
	for i in range(1,10):	
		if valid_list(get_block(sudoku,i))== False:
			return False

	return True

def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
	"""This function takes position as argument and returns a list of all the possible values that 
	can be assigned at that position so that the sudoku remains valid at that instant.
	"""
	candy=[]
	occupy_cond=[]
	a=pos[0]
	b=pos[1]

	occupied=get_row(sudoku,a)+get_column(sudoku,b)+get_block(sudoku,get_block_num(sudoku,(a,b)))
	occupied.sort()

	# Condensing List Occupied
	for i in occupied:
		if i not in occupy_cond:
			occupy_cond.append(i)

	for i in range(1,10):
		if i not in occupy_cond:
			candy.append(i)
	return candy

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
	"""This function fill `num` at position `pos` in the sudoku and then returns
	the modified sudoku.
	"""
	a=pos[0]-1
	b=pos[1]-1

	sudoku[a][b]=num
	return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):
	"""This function fills `0` at position `pos` in the sudoku and then returns
	the modified sudoku. In other words, it undoes any move that you 
	did on position `pos` in the sudoku.
	"""
	a=pos[0]-1
	b=pos[1]-1

	sudoku[a][b]=0
	return sudoku

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
	""" This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
	true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
	It return them in a tuple i.e. `(True, solved_sudoku)`.

	However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
	"""
	# your code goes here

	# to complete this function, you may define any number of helper functions.
	# However, we would be only calling this function to check correctness.

	if (find_first_unassigned_position(sudoku))!=(-1,-1) and len(get_candidates(sudoku,find_first_unassigned_position(sudoku)))!=0:						# If Sudoku has empty spaces
		
		unassigned_pos=find_first_unassigned_position(sudoku)
		#print("Position:",unassigned_pos)
		candidates=get_candidates(sudoku,unassigned_pos)
		#print("Candidates:",candidates)
		
		for i in candidates:
			make_move(sudoku,unassigned_pos,i)
			#print_sudoku(sudoku)
			#print("\n")

			if (find_first_unassigned_position(sudoku))!=(-1,-1) and len(get_candidates(sudoku,find_first_unassigned_position(sudoku)))!=0:	
				sudoku_solver(sudoku)
			
			if (find_first_unassigned_position(sudoku))==(-1,-1) and valid_sudoku(sudoku)==True:	
				return (True, sudoku)
	
			else:
				#print("Move Undo at",unassigned_pos)
				undo_move(sudoku,unassigned_pos)
				#print_sudoku(sudoku)

	return (False, sudoku)
	
# PLEASE NOTE:
# We would be importing your functions and checking the return values in the autograder.
# However, note that you must not print anything in the functions that you define above before you 
# submit your code since it may result in undefined behaviour of the autograder.

def in_lab_component(sudoku: List[List[int]]):
	print("Testcases for In Lab evaluation")
	print("Get Block Number:")
	print(get_block_num(sudoku,(4,4)))
	print(get_block_num(sudoku,(7,2)))
	print(get_block_num(sudoku,(2,6)))
	print("Get Block:")
	print(get_block(sudoku,3))
	print(get_block(sudoku,5))
	print(get_block(sudoku,9))
	print("Get Row:")
	print(get_row(sudoku,3))
	print(get_row(sudoku,5))
	print(get_row(sudoku,9))

# Following is the driver code
# you can edit the following code to check your performance.
if __name__ == "__main__":

	# Input the sudoku from stdin
	sudoku = input_sudoku()

	# Try to solve the sudoku
	possible, sudoku = sudoku_solver(sudoku)

	"""Clarify For Submission Of Lab Code"""
	# The following line is for the in-lab component
	# in_lab_component(sudoku) 			
	# Show the result of the same to your TA to get your code evaulated

	# Check if it could be solved
	if possible:
		print("Found a valid solution for the given sudoku :)")
		print_sudoku(sudoku)

	else:
		print("The given sudoku cannot be solved :(")
		print_sudoku(sudoku)