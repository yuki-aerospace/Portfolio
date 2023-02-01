import numpy as np
import tkinter as tk
from tkinter import messagebox
#* black=1, white=-1, empty=0

# Initialize the board to start new game
def init_board():
    global board
    global turn
    
    turn = -1  
    board =[
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,-1,1,0,0,0],
        [0,0,0,1,-1,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    set_board(board)

# Create board
def set_board(board):
    global turn
    turn *= -1 # change turn  

    for column in range(8):
        for row in range(8):
            # Create renctangles with the size of 45*45
            X = column * 45
            Y = row * 45
            canvas.create_rectangle(X, Y, X+45, Y+45, outline="black")

            # Create cirlcles correspond to the board situation
            #if turnable(column,row,turn)[0]>0: #! this line doesn't work
                #canvas.create_oval(X+2, Y+2, X+43, Y+43, fill="red") # put a black piece
            if board[row][column] == 1: 
                canvas.create_oval(X+2, Y+2, X+43, Y+43, fill="black") # put a black piece
            if board[row][column] == -1: 
                canvas.create_oval(X+2, Y+2, X+43, Y+43, fill="white", outline="white") # put a white piece
                
    # execute click() when board is clicked
    canvas.bind('<ButtonRelease-1>', click)

# get the event info 
def click(event): 
    clicked_row = event.y//45
    clicked_column = event.x//45

    global board
    if board[clicked_row][clicked_column] != 0:
        messagebox.showerror("Error", "You can't put your piece there!")
    else: 
        flip(clicked_column, clicked_row, turn)

# go through all the 8 directions and check if there is a piece that can be turned
def turnable(clicked_column, clicked_row, turn):
    total = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            count = 0 # number of pices to flip
            x = clicked_column 
            y = clicked_row
            while True:
                x += dx
                y += dy
                    
                # if it is out of board, break
                if x<0 or x>7 or y<0 or y>7:
                    break
                # if there is nothing to flip, break
                if board[y][x]==0:
                    break
                
                # if there is opponent's piece, add count and keep going
                if board[y][x]==turn*(-1):
                    count += 1      
            
                # if there is user's piece, flip pieces 
                if board[y][x]==turn:
                    for i in range(count): #! there should be better way to do this
                        total += 1
                        x -= dx
                        y -= dy
                        board[y][x] = turn
                    break                    
    return total, board

# flip pieces
def flip(clicked_column, clicked_row, turn):
    # if there is nothing to turn, show error
    if turnable(clicked_column, clicked_row, turn)[0]==0:
        messagebox.showerror("Error", "You can't put your piece there!")
    else:
        board = turnable(clicked_column, clicked_row, turn)[1]
        board[clicked_row][clicked_column] = turn                
        set_board(board)      
        

if __name__ == '__main__':
    root = tk.Tk() 
    root.title("Reversi")
    root.geometry("365x365")
    canvas = tk.Canvas(root, height=360, width=361, bg= "#1A7F2B")
    canvas.pack()
    init_board()
    root.mainloop()

# show result after click()is called 64 times