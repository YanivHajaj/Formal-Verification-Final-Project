# Formal-Verification-Final-Project
Formal Verification Project - This project implements a solver for the Sokoban puzzle using Formal Methods. It generates SMV models with Python, checks them using nuXmv, and evaluates BDD and SAT Solver performance. The solution includes iterative approaches for complex boards. All code, boards, models, and a report are included.


Explanation_PDF about the code:
https://github.com/YanivHajaj/Formal-Verification-Final-Project/blob/main/Explanation_PDF_Formal_Verification_Final_Project.pdf


## Usage
This project includes several functions. Here's a breakdown of each one:  
**•	print_board(board):**  
this function prints the XSB format of the board.  
**•	createSMVfile(board):**  
This function checks all the conditions related to the change of the board by moving the player and the boxes, and creates an SMV file from them with an initial state, a table of transitions, a winning state and a temporal logical expression.  
In this function you must refer to the following variables:  
  &ensp;o	In the PATH variable, enter the address where you want to save the file.  
  &ensp;o	In the FILENAME variable, enter the name you want to call the file.  
**•	run_nuxmv(model_filename, engine=None, k=None):**  
This function runs the nuXmv model checker on a given model file.   
The arguments of this function:   
<ins>model_filename:</ins> This is the path to the model file you want to check. It should be a string representing a valid file path. For example, sokoban.smv'.  
<ins>engine:</ins> This is the type of engine you want to use for the model checking. It can be either 'SAT' or 'BDD'. If no engine is specified, the function will run nuXmv in its default mode.  
<ins>k:</ins> This is the maximum length of the counterexample you want to find. It should be an integer. This argument is only used if the engine is 'SAT'.  
In this function you must refer to the following:  
  &ensp;o	os.chdir- enter the address where you saved the file.  
**•	print_solution(filename, mode):**  
this function reads the solution from the out file and prints it.  
The arguments of this function:  
<ins>filename:</ins> This is the path to the file that contains the solution. It should be a string representing a valid file path. For example, 'sokoban.out.  
<ins>mode:</ins> This is the mode in which the solution was found. It can be any string, but typically it would be 'SAT' or 'BDD'.  
**•	iterative_solving(board):**  
this function solves a sokoban board iteratively. In each iteration a new goal is added.     
In the main function change the path to the address of the board file.    
