from graphics import *
from time import sleep

def drawRect(win, colour, tlPoint, brPoint, outlineThickness = 0):
    """Draw a rectangle using the specified colour between points tlPoint and brPoint"""
    rect = Rectangle(tlPoint, brPoint)
    rect.setFill(colour)
    rect.setWidth(outlineThickness)
    rect.draw(win)

    return rect

def drawTri(win, colour, tlPoint, size, outlineThickness = 0):
    """Draw a triangle using the specified colour and size at point tlPoint"""
    topPoint = Point(tlPoint.getX() + size / 2, tlPoint.getY())
    leftPoint = Point(tlPoint.getX(), tlPoint.getY() + size)
    rightPoint = Point(tlPoint.getX() + size, tlPoint.getY() + size)

    tri = Polygon([topPoint, leftPoint, rightPoint])
    tri.setFill(colour)
    tri.setWidth(outlineThickness)

    if outlineThickness == 0: # This is required, as polygons do not support having an outline of 0 thickness :P
        tri.setOutline(colour)

    tri.draw(win)

    return tri

def drawEndTri(win, colour, tlPoint, size, mirror = False, outlineThickness = 0):
    """Draw a half triangle using the specified colour and size at point tlPoint, optionally mirrored"""
    topPoint = Point(tlPoint.getX() + size / 2, tlPoint.getY()) # Top point is always the same

    if mirror: # If drawing mirrored, the right point should be in line with the top point
        leftPoint = Point(tlPoint.getX(), tlPoint.getY() + size)
        rightPoint = Point(tlPoint.getX() + size / 2, tlPoint.getY() + size)
    else: # If not mirrored, the left point should be in line with the top point
        leftPoint = Point(tlPoint.getX() + size / 2, tlPoint.getY() + size)
        rightPoint = Point(tlPoint.getX() + size, tlPoint.getY() + size)

    tri = Polygon([topPoint, leftPoint, rightPoint])
    tri.setFill(colour)
    tri.setWidth(outlineThickness)

    if outlineThickness == 0: # This is required, as polygons do not support having an outline of 0 thickness :P
            tri.setOutline(colour)

    tri.draw(win)

    return tri
        
def drawPatchB(win, colour, tlPoint):
    """Draw blank patch"""
    brPoint = Point(tlPoint.getX() + 100, tlPoint.getY() + 100)

    return [drawRect(win, colour, tlPoint, brPoint, 1)]

def drawPatchF(win, colour, tlPoint):
    """Draw pattern of final number"""
    shapes = []

    brPoint = Point(tlPoint.getX() + 100, tlPoint.getY() + 100)

    for i in range(0,50,5):
        col = colour if (i / 5) % 2 == 0 else "white" # If on even iteration, colour the square as specified, if odd iteration, colour the square white
        shapes.append(drawRect(win, col, Point(tlPoint.getX() + i, tlPoint.getY() + i), Point(brPoint.getX() - i, brPoint.getY() - i)))

    shapes.extend(drawOutline(win, "black", tlPoint, 100, 1)) # Draw outline around patch, after the patch is drawn

    return shapes


def drawPatchP(win, colour, tlPoint):
    """Draw pattern of penultimate number"""
    shapes = []

    for j in range(0, 5):
        if j % 2 != 0: # If on odd line, draw half triangle on left, 4 full triangles, and then a half triangle on the right
            shapes.append(drawEndTri(win, colour, Point(tlPoint.getX() - 10, tlPoint.getY() + 20 * j), 20, False))

            for i in range(0, 4):
                shapes.append(drawTri(win, colour, Point(tlPoint.getX() + 10 + 20 * i, tlPoint.getY() + 20 * j), 20))

            shapes.append(drawEndTri(win, colour, Point(tlPoint.getX() + 90, tlPoint.getY() + 20 * j), 20, True))
        else: # If on even line, draw 5 full triangles
            for i in range(0, 5):
                shapes.append(drawTri(win, colour, Point(tlPoint.getX() + 20 * i, tlPoint.getY() + 20 * j), 20))

    shapes.extend(drawOutline(win, "black", tlPoint, 100, 1)) # Draw outline around patch, after the patch is drawn

    return shapes

def getColour(x, y, colours, gridSize):
    if x == y or x == gridSize - y - 1: # Set colour to the first colour if on the cross in the pattern
        colour = colours[0]
    elif x > y and x < gridSize - y - 1: # Set colour to the second colour if in the top triangle
        colour = colours[1]
    elif y > x and x > gridSize - y - 1: # Set colour to the second colour if in the bottom triangle
        colour = colours[1]
    else: # Set the colour to the third colour if anywhere else (in the left or right triangles)
        colour = colours[2]

    return colour

def getInput():
    gridSize = -1
    colours = []
    validColours = ["red", "green", "blue", "purple", "orange", "cyan"]

    while gridSize == -1:
        inValue = input("Please enter the size of the patchwork: ")

        if inValue.isnumeric():
            inValue = int(inValue) # If input is a valid number, convert to integer

        if inValue == 5 or inValue == 7:
            gridSize = int(inValue) # Set gridSize to input number, only if it is 5 or 7
        else:
            print("Invalid patchwork size. Valid sizes are 5 and 7")

    for i in range(1, 4):
        col = input(f"Please enter colour {i}: ")

        while col not in validColours:
            print(f"Not a valid colour. Valid colours are red, green, blue, purple, orange or cyan")
            col = input(f"Please enter colour {i}: ")

        colours.append(col) # After checking that the colour is valid, add it to the list of colours to be used

    return gridSize, colours

def undrawItem(itemArray):
    for i in range(0, len(itemArray)):
        itemArray[i].undraw()

def drawOutline(win, colour, tlPoint, size, thickness):
    brPoint = Point(tlPoint.getX() + size, tlPoint.getY() + size)

    l1 = Line(tlPoint, Point(tlPoint.getX() + size, tlPoint.getY()))
    l2 = Line(tlPoint, Point(tlPoint.getX(), tlPoint.getY() + size))
    l3 = Line(brPoint, Point(brPoint.getX() - size, brPoint.getY()))
    l4 = Line(brPoint, Point(brPoint.getX(), brPoint.getY() - size))

    l1.setOutline(colour)
    l2.setOutline(colour)
    l3.setOutline(colour)
    l4.setOutline(colour)

    l1.setWidth(thickness)
    l2.setWidth(thickness)
    l3.setWidth(thickness)
    l4.setWidth(thickness)

    l1.draw(win)
    l2.draw(win)
    l3.draw(win)
    l4.draw(win)

    return [l1, l2, l3, l4]

def redrawItem(win, itemArray):
    for i in range(0, len(itemArray)):
        itemArray[i].undraw()
        itemArray[i].draw(win)

def moveItem(itemArray, xDist, yDist, time):
    for t in range(0, 10):
        for i in range(0, len(itemArray)):
            itemArray[i].move(xDist / 10, yDist / 10)

        sleep(time / 10)        

def main():
    gridSize, colours = getInput()

    win = GraphWin("up2157117 - Patchwork Coursework", 100 * gridSize, 100 * gridSize)
    win.setBackground("white")

    cells = []

    # Draw the initial grid
    for j in range(0, gridSize):
        for i in range(0, gridSize):
            colour = getColour(i, j, colours, gridSize)

            tlPoint = Point(100 * i, 100 * j)

            if (i == j or i == gridSize - j - 1) and i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # Draw final pattern patch if on the cross, and not on the outer border of patches
                cells.append(drawPatchF(win, colour, tlPoint))
            elif i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # If within the inner 3x3 or 5x5, draw the penultimate pattern patch
                cells.append(drawPatchP(win, colour, tlPoint))
            else:
                # Everywhere else (the outer ring), draw a blank patch
                cells.append(drawPatchB(win, colour, tlPoint))

    # Get user input (Challenge, code quality rapidly deteriorates but it says in the instructions that this does not matter)
    while True:
        clickPos = win.getMouse()

        x = int(clickPos.getX() / 100)
        y = int(clickPos.getY() / 100)

        patchIndex = x + y * gridSize

        outline = drawOutline(win, "black", Point(x * 100, y * 100), 100, 10)

        selected = True
        while selected:
            key = win.getKey()

            match key: # Yes this is horrible. Could I have done it in a better way? Possibly. Does it work? Yes
                case "d":
                    undrawItem(cells[patchIndex])
                    cells[patchIndex] = []
                case "1":
                    if len(cells[patchIndex]) == 0: # If the cell is empty, draw into it, else do nothing
                        cells[patchIndex] = drawPatchB(win, colours[0], Point(x * 100, y * 100))
                case "2":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchB(win, colours[1], Point(x * 100, y * 100))
                case "3":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchB(win, colours[2], Point(x * 100, y * 100))
                case "4":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchP(win, colours[0], Point(x * 100, y * 100))
                case "5":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchP(win, colours[1], Point(x * 100, y * 100))
                case "6":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchP(win, colours[2], Point(x * 100, y * 100))
                case "7":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchF(win, colours[0], Point(x * 100, y * 100))
                case "8":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchF(win, colours[1], Point(x * 100, y * 100))
                case "9":
                    if len(cells[patchIndex]) == 0:
                        cells[patchIndex] = drawPatchF(win, colours[2], Point(x * 100, y * 100))
                case "Up":
                    moveIndex = x + (y - 1) * gridSize

                    if len(cells[moveIndex]) == 0:
                        moveItem(cells[patchIndex], 0, -100, 1)

                        cells[moveIndex] = cells[patchIndex]
                        cells[patchIndex] = []
                case "Down":
                    moveIndex = x + (y + 1) * gridSize

                    if len(cells[moveIndex]) == 0:
                        moveItem(cells[patchIndex], 0, 100, 1)

                        cells[moveIndex] = cells[patchIndex]
                        cells[patchIndex] = []
                case "Left":
                    moveIndex = (x - 1) + y * gridSize

                    if len(cells[moveIndex]) == 0:
                        moveItem(cells[patchIndex], -100, 0, 1)

                        cells[moveIndex] = cells[patchIndex]
                        cells[patchIndex] = []
                case "Right":
                    moveIndex = (x + 1) + y * gridSize

                    if len(cells[moveIndex]) == 0:
                        moveItem(cells[patchIndex], 100, 0, 1)

                        cells[moveIndex] = cells[patchIndex]
                        cells[patchIndex] = []
                case "Escape":
                    selected = False

            redrawItem(win, outline)
    
        undrawItem(outline)

main()