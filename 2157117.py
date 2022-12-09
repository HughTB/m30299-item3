from graphics import *;
import time; # Needed only for the challenge

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

    if outlineThickness == 0: # This is required to hide the outline as polygons do not seem to support an outline thickness of 0
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

    if outlineThickness == 0: # This is required to hide the outline as polygons do not seem to support an outline thickness of 0
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

    shapes.extend(drawBorder(win, "black", tlPoint, 100, 1)) # Draw outline around patch, after the patch is drawn

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

    shapes.extend(drawBorder(win, "black", tlPoint, 100, 1)) # Draw outline around patch, after the patch is drawn

    return shapes

def getColour(x, y, colours, gridSize):
    """Using the coordinates of the patch, determine which colour the patch should be"""
    if x == y or x == gridSize - y - 1: # Set colour to the first colour if on the cross in the pattern
        colour = colours[0]
    elif x > y and x < gridSize - y - 1: # Set colour to the second colour if in the top triangle
        colour = colours[1]
    elif y > x and x > gridSize - y - 1: # Set colour to the second colour if in the bottom triangle
        colour = colours[1]
    else: # Set the colour to the third colour if anywhere else (in the left or right triangles)
        colour = colours[2]

    return colour

def getValidOptionString(optionArray):
    """Get a string containing the valid options stored in an array"""
    optionString = ""

    for i in range(0, len(optionArray) - 2):
        optionString += str(optionArray[i]) + ", "

    optionString += str(optionArray[-2]) + " and " + str(optionArray[-1])

    return optionString

def getInput():
    """Get user input for the size of the grid, and the colours which should be used"""
    gridSize = -1
    colours = []
    validColours = ["red", "green", "blue", "purple", "orange", "cyan"]
    validSizes = [5, 7]

    print("===== up2157117 - Patchwork Coursework =====")

    while gridSize == -1:
        inValue = input("Please enter the size of the patchwork: ")

        if inValue.isnumeric() and int(inValue) in validSizes:
            gridSize = int(inValue) # Set gridSize to input number, only if it is 5 or 7
        else:
            print("Invalid patchwork size. Valid sizes are {}".format(getValidOptionString(validSizes)))

    for i in range(1, 4):
        colour = input(f"Please enter colour {i}: ")

        while colour not in validColours: # If colour is invalid, print message containing the valid colours and ask the user to try again
            print("Not a valid colour. Valid colours are {}".format(getValidOptionString(validColours)))
            colour = input(f"Please enter colour {i}: ")

        colours.append(colour) # After checking that the colour is valid, add it to the list of colours to be used

    return gridSize, colours

def drawLine(win, colour, point1, point2, thickness):
    """Draw line between point1 and point2 with the specified colour and thickness"""
    l = Line(point1, point2)
    l.setOutline(colour)
    l.setWidth(thickness)
    l.draw(win)

    return l

def drawBorder(win, colour, tlPoint, size, thickness = 1):
    """Draw a border of given thickness (rectangles cannot have a transparent fill colour)"""
    brPoint = Point(tlPoint.getX() + size, tlPoint.getY() + size)

    lines = []

    lines.append(drawLine(win, colour, tlPoint, Point(brPoint.getX(), tlPoint.getY()), thickness))
    lines.append(drawLine(win, colour, tlPoint, Point(tlPoint.getX(), brPoint.getY()), thickness))
    lines.append(drawLine(win, colour, brPoint, Point(tlPoint.getX(), brPoint.getY()), thickness))
    lines.append(drawLine(win, colour, brPoint, Point(brPoint.getX(), tlPoint.getY()), thickness))

    return lines

# Functions for challenge (As stated in the documentation, code quality does not matter here)
def undrawItem(itemArray):
    for i in range(0, len(itemArray)):
        itemArray[i].undraw()

def drawOutline(win, colour, tlPoint, size, thickness):
    brPoint = Point(tlPoint.getX() + size, tlPoint.getY() + size)

    lines = []

    lines.append(drawLine(win, colour, Point(tlPoint.getX() - thickness / 2, tlPoint.getY()), Point(brPoint.getX() + thickness / 2, tlPoint.getY()), thickness))
    lines.append(drawLine(win, colour, tlPoint, Point(tlPoint.getX(), brPoint.getY() + thickness / 2), thickness))
    lines.append(drawLine(win, colour, Point(brPoint.getX() + thickness / 2, brPoint.getY()), Point(tlPoint.getX(), brPoint.getY()), thickness))
    lines.append(drawLine(win, colour, brPoint, Point(brPoint.getX(), tlPoint.getY()), thickness))

    return lines

def redrawItem(win, itemArray):
    for i in range(0, len(itemArray)):
        itemArray[i].undraw()
        itemArray[i].draw(win)

def moveItem(itemArray, xDist, yDist, animTime):
    for t in range(0, 10):
        for i in range(0, len(itemArray)):
            itemArray[i].move(xDist / 10, yDist / 10)

        time.sleep(animTime / 10)

def challengeFunc(win, gridSize, patchArray, colours):
    clickPos = win.getMouse()

    x = int(clickPos.getX() / 100)
    y = int(clickPos.getY() / 100)

    patchIndex = x + y * gridSize

    outline = drawOutline(win, "black", Point(x * 100, y * 100), 100, 5)

    selected = True
    while selected:
        key = win.getKey()

        if key == "d":
            undrawItem(patchArray[patchIndex])
            patchArray[patchIndex] = []
        elif key == "1" and len(patchArray[patchIndex]) == 0: # If the patch is empty, draw a new patch depending upon the key pressed, else do nothing (Yes there are better ways of doing this, but code quality does not matter here)
                patchArray[patchIndex] = drawPatchB(win, colours[0], Point(x * 100, y * 100))
        elif key == "2" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchB(win, colours[1], Point(x * 100, y * 100))
        elif key == "3" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchB(win, colours[2], Point(x * 100, y * 100))
        elif key == "4" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchP(win, colours[0], Point(x * 100, y * 100))
        elif key == "5" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchP(win, colours[1], Point(x * 100, y * 100))
        elif key == "6" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchP(win, colours[2], Point(x * 100, y * 100))
        elif key == "7" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchF(win, colours[0], Point(x * 100, y * 100))
        elif key == "8" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchF(win, colours[1], Point(x * 100, y * 100))
        elif key == "9" and len(patchArray[patchIndex]) == 0:
                patchArray[patchIndex] = drawPatchF(win, colours[2], Point(x * 100, y * 100))
        elif key == "Up": # Check if patch in specified direction is empty, if true move the patch, else do nothing
            moveIndex = x + (y - 1) * gridSize

            if moveIndex > 0 and len(patchArray[moveIndex]) == 0:
                moveItem(patchArray[patchIndex], 0, -100, 1)

                patchArray[moveIndex] = patchArray[patchIndex]
                patchArray[patchIndex] = []
        elif key == "Down":
            moveIndex = x + (y + 1) * gridSize

            if moveIndex < (gridSize ** 2) and len(patchArray[moveIndex]) == 0:
                moveItem(patchArray[patchIndex], 0, 100, 1)

                patchArray[moveIndex] = patchArray[patchIndex]
                patchArray[patchIndex] = []
        elif key == "Left":
            moveIndex = (x - 1) + y * gridSize

            if moveIndex > (y * gridSize) and len(patchArray[moveIndex]) == 0:
                moveItem(patchArray[patchIndex], -100, 0, 1)

                patchArray[moveIndex] = patchArray[patchIndex]
                patchArray[patchIndex] = []
        elif key == "Right":
            moveIndex = (x + 1) + y * gridSize

            if moveIndex < ((y + 1) * gridSize) and len(patchArray[moveIndex]) == 0:
                moveItem(patchArray[patchIndex], 100, 0, 1)

                patchArray[moveIndex] = patchArray[patchIndex]
                patchArray[patchIndex] = []
        elif key == "Escape": # If escape is pressed, de-select the patch and end the loop
            selected = False

        redrawItem(win, outline)

    undrawItem(outline)
# End of functions for challenge

def main():
    gridSize, colours = getInput()

    win = GraphWin("up2157117 - Patchwork Coursework", 100 * gridSize, 100 * gridSize)
    win.setBackground("white")

    patchArray = [] # All patches are stored in this array, so that they can be moved, deleted or changed in the challenge

    # Draw the initial grid
    for j in range(0, gridSize):
        for i in range(0, gridSize):
            colour = getColour(i, j, colours, gridSize) # Get the colour for the patch, given a position

            tlPoint = Point(100 * i, 100 * j)

            if (i == j or i == gridSize - j - 1) and i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # Draw final pattern patch if on the cross, and not on the outer border of patches
                patchArray.append(drawPatchF(win, colour, tlPoint))
            elif i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # If within the inner 3x3 or 5x5, draw the penultimate pattern patch
                patchArray.append(drawPatchP(win, colour, tlPoint))
            else:
                # Everywhere else (the outer ring), draw a blank patch
                patchArray.append(drawPatchB(win, colour, tlPoint))

    # Infinite loop for challenge, documentation does not specify how the program should be closed
    while True:
        challengeFunc(win, gridSize, patchArray, colours)

main()