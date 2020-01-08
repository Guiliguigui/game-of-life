"""
Conway's Game of Life

"""
__author__ = "Guillaume Mairesse"

from tkinter import *
import argparse

def showMap():
    """
    Show the map at the launch off the application.

    """
    for row in range(rows):
        for col in range(cols):
            if(data[row][col]):
                ids[row][col] = canvas.create_rectangle(col * cell_size,
                                                        row * cell_size,
                                                        (col + 1) * cell_size,
                                                        (row + 1) * cell_size,
                                                        fill=color_on)
            else:
                ids[row][col] = canvas.create_rectangle(col * cell_size,
                                                        row * cell_size,
                                                        (col + 1) * cell_size,
                                                        (row + 1) * cell_size,
                                                        fill=color_off)

def updateMap():
    """
    Update the map.
    
    """
    for row in range(rows):
        for col in range(cols):
            if(data[row][col]):
                canvas.itemconfig(ids[row][col],fill=color_on)
            else:
                canvas.itemconfig(ids[row][col],fill=color_off)

def click_callback(event):
    """
    Set alive or kill a specific cell.
    
    """
    row = int(event.y / cell_size)
    col = int(event.x / cell_size)
    if(data[row][col]):
        data[row][col] = False
        canvas.itemconfig(ids[row][col], fill=color_off)
    else:
        data[row][col] = True
        canvas.itemconfig(ids[row][col], fill=color_on)

def launch():
    """
    Used to launch the animation.
    
    """
    future_data = [[False for i in range(cols)] for i in range(rows)]
    for row in range(rows):
        for col in range(cols):
            neighbors=[
                [-1,-1],
                [-1,0],
                [-1,1],
                [0,-1],
                [0,1],
                [1,-1],
                [1,0],
                [1,1],
            ]
            k = 0
            for neighbor in  neighbors:
                if(row==0 and neighbor[0]==-1):
                    neighbor[0]=rows-1
                elif(row==rows-1 and neighbor[0]==1):
                    neighbor[0]=0
                else:
                    neighbor[0] = row + neighbor[0]
                if(col==0 and neighbor[1]==-1):
                    neighbor[1]=cols-1
                elif(col==cols-1 and neighbor[1]==1):
                    neighbor[1]=0
                else:
                    neighbor[1] = col + neighbor[1]
                if(data[neighbor[0]][neighbor[1]]):
                    k+=1
            if(data[row][col]):
                if(k==2 or k==3):
                    future_data[row][col] = True
                else:
                    future_data[row][col] = False
            else:
                if(k==3):
                    future_data[row][col] = True
                else:
                    future_data[row][col] = False
    for row in range(rows):
        for col in range(cols):
            data[row][col] = future_data[row][col]
    updateMap()
    btnLaunch.configure(text = "Stop", command=stop)
    global job
    job = root.after(int(duration*1000),launch)

def stop():
    """
    Used to stop the animation.
    
    """
    global job
    if job is not None:
        root.after_cancel(job)
        job = None
    btnLaunch.configure(text = "Launch", command=launch)


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-rows", help="to choose the number of rows (default is 10)", default=10)
    parser.add_argument("-cols", help="to choose the number of columns (default is 10)", default=10)
    parser.add_argument("-duration", help="to choose the duration of the animation (default is 2)", default=1)
    parser.add_argument("-cell_size", help="to choose the size of the cells (default is 35)", default=35)
    parser.add_argument("-color_on", help="to choose the on color (default is black)", default="black")
    parser.add_argument("-color_off", help="to choose the on color  (default is white)", default="white")
    parser.add_argument("-rule", help="to choose the rule (default is 1)",default=1, choices=['1','2',])
    args=parser.parse_args()

    rows = int(args.rows)
    cols = int(args.cols)
    duration= float(args.duration)
    cell_size = int(args.cell_size)
    color_on = args.color_on
    color_off = args.color_off
    rule = int(args.rule)
    global job
    job = None

    root = Tk()
    root.title("Game Of Life")
    root.resizable(width = False, height = False)

    canvas_width = cols * cell_size
    canvas_height = rows * cell_size
    canvas = Canvas(root, width = canvas_width, height = canvas_height)
    canvas.grid(column=0, row=0)

    data = [[False for i in range(cols)] for i in range(rows)]
    ids = [[0 for i in range(cols)] for i in range(rows)]
            
    showMap()

    canvas.bind('<Button-1>',click_callback)
    
    btnLaunch = Button(root, text = "Launch", command = launch)
    btnLaunch.grid(column=0,row=1)

    root.mainloop()
