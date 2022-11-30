from graphics import *

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
    tri.draw(win)

    

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
    tri.draw(win)
        
def drawPatchB(win, colour, tlPoint):
    """Draw blank patch"""
    brPoint = Point(tlPoint.getX() + 100, tlPoint.getY() + 100)

    drawRect(win, colour, tlPoint, brPoint, 1)

def drawPatchF(win, colour, tlPoint):
    """Draw pattern of final number"""
    brPoint = Point(tlPoint.getX() + 100, tlPoint.getY() + 100)

    drawRect(win, "white", tlPoint, brPoint, 1) # Create box around patch

    for i in range(0,50,5):
        col = colour if (i / 5) % 2 == 0 else "white" # If on even iteration, colour the square as specified, if odd iteration, colour the square white
        drawRect(win, col, Point(tlPoint.getX() + i, tlPoint.getY() + i), Point(brPoint.getX() - i, brPoint.getY() - i))


def drawPatchP(win, colour, tlPoint):
    """Draw pattern of penultimate number"""
    drawRect(win, "white", tlPoint, Point(tlPoint.getX() + 100, tlPoint.getY() + 100), 1) # Create box around patch

    for j in range(0, 5):
        if j % 2 != 0: # If on odd line, draw half triangle on left, 4 full triangles, and then a half triangle on the right
            drawEndTri(win, colour, Point(tlPoint.getX() - 10, tlPoint.getY() + 20 * j), 20, False)

            for i in range(0, 4):
                drawTri(win, colour, Point(tlPoint.getX() + 10 + 20 * i, tlPoint.getY() + 20 * j), 20)

            drawEndTri(win, colour, Point(tlPoint.getX() + 90, tlPoint.getY() + 20 * j), 20, True)
        else: # If on even line, draw 5 full triangles
            for i in range(0, 5):
                drawTri(win, colour, Point(tlPoint.getX() + 20 * i, tlPoint.getY() + 20 * j), 20)

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

def main():
    gridSize, colours = getInput()

    win = GraphWin("up2157117 - Patchwork Coursework", 100 * gridSize, 100 * gridSize)

    for j in range(0, gridSize):
        for i in range(0, gridSize):
            if i == j or i == gridSize - j - 1: # Set colour to the first colour if on the cross in the pattern
                col = colours[0]
            elif i > j and i < gridSize - j - 1: # Set colour to the second colour if in the top triangle
                col = colours[1]
            elif j > i and i > gridSize - j - 1: # Set colour to the second colour if in the bottom triangle
                col = colours[1]
            else: # Set the colour to the third colour if anywhere else (in the left or right triangles)
                col = colours[2]

            tlPoint = Point(100 * i, 100 * j)

            if (i == j or i == gridSize - j - 1) and i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # Draw final pattern patch if on the cross, and not on the outer border of patches
                drawPatchF(win, col, tlPoint)
            elif i > 0 and j > 0 and i < gridSize - 1 and j < gridSize - 1:
                # If within the inner 3x3 or 5x5, draw the penultimate pattern patch
                drawPatchP(win, col, tlPoint)
            else:
                # Everywhere else (the outer ring), draw a blank patch
                drawPatchB(win, col, tlPoint)

    win.getMouse()

main()