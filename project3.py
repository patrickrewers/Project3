#
# CS 177
# Patrick Rewers, Nicole Gillespie, Shelby Nelson
#
# The purpose of this program is to run and display a  maze game
#     where users try to solve the maze in as few members as
#     possible. The game tracks players' names, moves, and scores.
#

# Import Graphics library
from graphics import Point, Rectangle, GraphWin, Line, Entry, Text
from random import random

# ==================================[ MAIN }===================================


# Define main() function
def main():

    # Draw the Game Panel
    game_panel = drawGamePanel()
    # Define current game settings and set score to 0
    close = False
    in_game = False
    score = 0
    # Create dummy variable before called
    field = ""

    # Draw initial game panel
    new_player_text, score_box, score_text, phase = drawInitialPanel(game_panel)

    # Loop game functions until user clicks "Exit" button
    while close is False:

        # Get panel location and x and y coordinates of click
        panel, x, y = getClick(game_panel, field, in_game)
        # Check if user clicked "Exit" button
        close = checkExit(panel, x, y)

        # Check if user clicked in game panel
        if panel == "game_panel":
            # Whenever user presses the green button, change the game mode
            if checkGreenButton(panel, x, y) is True:
                # Clicks in Initial panel change panel to New Player
                if phase == "initial":
                    player_name_text, player_name_entry, phase = drawNewPlayerPanel(
                        new_player_text, score_box, score_text, game_panel, phase)
                # Clicks in New Player panel launch the game
                elif phase == "new_player":
                    in_game = True
                    player_name_display, player_name, reset_button, reset_text, current_score_text, current_score_display, phase = drawInGamePanel(
                        new_player_text, player_name_entry, game_panel, score)
                    field, pete, sensors = drawFieldPanel()
                # Clicks while in game close the game and revert panel to New
                #   Player panel
                elif phase == "in_game":
                    if in_game is True:
                        field.close()
                        score = 0
                        player_name_display.undraw()
                        current_score_display.undraw()
                        in_game = False
                    player_name_text, player_name_entry, phase = drawNewPlayerPanel(
                        new_player_text, score_box, score_text, game_panel, phase)
            # Whenever the user presses the reset button, close the game and
            #    draw Initial panel
            if checkResetButton(panel, phase, x, y) is True:
                field.close()
                score = 0
                current_score_text, current_score_display = updateScore(current_score_text, current_score_display, game_panel, score)
                field, pete, sensors = drawFieldPanel()

        # Check if user clicked in field panel
        if panel == "field":
            # Move pete based on click
            pete, pete_center, score = movePete(pete, field, x, y, score, sensors)
            # Update score with every click during game
            if phase == "in_game":
                current_score_text, current_score_display = updateScore(
                    current_score_text, current_score_display, game_panel, score)
            # Check if user won game, and set close to the result
            if checkWinGame(pete_center) is True:
                close = endGame(field, game_panel, player_name, score)

    # When user close condition is true, close both panels
    game_panel.close()
    if in_game is True:
        field.close()

# =========================[ GAME PANEL ELEMENTS ]=============================


# Define gamePanel() function
def drawGamePanel():

    # Creates gray Game Panel window
    game_panel = GraphWin("Game Panel", 300, 200)
    game_panel.setBackground("gray")

    # Creates title text with background
    title_background = Rectangle(Point(0, 0), Point(300, 40))
    title_background.setFill("white")
    title_background.draw(game_panel)
    title_text = Text(Point(150, 20), "BoilerMazer")
    title_text.setSize(30)
    title_text.setStyle("bold")
    title_text.draw(game_panel)

    # Creates exit button and text
    exit_button = Rectangle(Point(250, 160), Point(300, 200))
    exit_button.setFill("red")
    exit_button.draw(game_panel)
    exit_text = Text(Point(275, 181), "EXIT")
    exit_text.setSize(14)
    exit_text.draw(game_panel)

    # Creates green button, which will be used for new player and start options
    green_button = Rectangle(Point(100, 160), Point(200, 200))
    green_button.setFill("green")
    green_button.draw(game_panel)
    return game_panel

# Define drawScoreDisplay() function


def drawScoreDisplay(game_panel):

    # Draws box that serves as the background the score displays
    score_box = Rectangle(Point(50, 60), Point(250, 145))
    score_box.setFill("white")
    score_box.draw(game_panel)

    # Call readScores() function, and store top 4 scores from topscores.txt
    top_scores = readScores()
    # Print title for top scores table
    scores = ["TOP SCORES", "=========="]
    # For each of the top scores, create a string with the name and score
    for element in top_scores:
        # Convert tuple to list
        element = list(element)
        # Loop through name and score for each player
        for item in element:
            # Assign name to name
            if type(item) == str:
                name = item
            # Convert score to int and assign to score
            elif type(item) == int:
                score = str(item)
        # Create a string from the name and score with space between elements
        string = name + "      " + str(score)
        # Add player to scores list
        scores.append(string)
    # Join the elements of the score string to create a string with newline
    #   characters between each player
    scores = "\n".join(scores)
    # Create a text object of the top scores title and players and draw in game
    #  panel
    score_text = Text(Point(150, 103), scores)
    score_text.draw(game_panel)
    # Return objects
    return (score_box, score_text)

# Define undrawScoreDisplay() function


def undrawScoreDisplay(score_box, scores_text):
    # Undraw score background box and text
    score_box.undraw()
    scores_text.undraw()

# Define drawPlayerText() function


def drawPlayerText(game_panel):
    # Create and stylize "NEW PLAYER" text over green button
    new_player_text = Text(Point(150, 181), "NEW PLAYER")
    new_player_text.setSize(14)
    new_player_text.draw(game_panel)
    # Return objects
    return (new_player_text)

# Define drawPlayerNameEntry() function


def drawPlayerNameEntry(game_panel):
    # Creates text prompting user for player name
    player_name_text = Text(Point(80, 70), "Player Name:")
    player_name_text.setStyle("bold")
    player_name_text.setSize(14)
    player_name_text.draw(game_panel)
    # Provides an entry box for user to enter player name
    player_name_entry = Entry(Point(195, 70), 18)
    player_name_entry.setFill("white")
    player_name_entry.draw(game_panel)
    # Return objects
    return player_name_text, player_name_entry

# Define drawPlayerNameDisplay() function


def drawPlayerNameDisplay(player_name_entry, game_panel):
    # Takes player name from entry box and creates Text object with it
    player_name = player_name_entry.getText()
    player_name_entry.undraw()
    player_name_display = Text(Point(195, 70), player_name)
    player_name_display.setSize(14)
    player_name_display.draw(game_panel)
    # Return objects
    return player_name_display, player_name

# Define undrawPlayerNameDisplay() function


def undrawPlayerNameDisplay(player_name_text, player_name_display):
    # Undraws player name Text objects
    player_name_text.undraw()
    player_name_display.undraw()

# Define drawCurrentScore() function


def drawCurrentScore(game_panel, score):
    # Draws and decorates score Text objects
    current_score_text = Text(Point(102, 120), "Score:")
    current_score_text.setStyle("bold")
    current_score_text.setSize(14)
    current_score_text.draw(game_panel)
    current_score_display = Text(Point(195, 120), score)
    current_score_display.setStyle("bold")
    current_score_display.setSize(14)
    current_score_display.draw(game_panel)
    # Return objects
    return current_score_text, current_score_display

# Define undrawCurrentScore() function


def undrawCurrentScore(current_score_text, current_score_display):
    # Undraws score Text objects
    current_score_text.undraw()
    current_score_display.undraw()

# Define drawResetButton() function


def drawResetButton(game_panel):
    # Creates yellow reset button to create new game with same player
    reset_button = Rectangle(Point(0, 160), Point(50, 200))
    reset_button.setFill("yellow")
    reset_button.draw(game_panel)
    reset_text = Text(Point(25, 181), "RESET")
    reset_text.setSize(14)
    reset_text.draw(game_panel)
    # Return objects
    return reset_button, reset_text

# Define undrawResetButton() function


def undrawResetButton(reset_button, reset_text):
    # Undraws the reset button
    reset_button.undraw()
    reset_text.undraw()

# Define drawSensors() function


def drawSensors(field):
    # Set initial coordinates to potentially draw sensors and empty list
    #   of sensor locations
    x = 40
    y = 40
    sensors = []

    # Initialize loop to create horizontal sensors
    for column in range(9):
        for row in range(9):
            # Create random number between 0 and 1
            h_chance_border = random()
            v_chance_border = random()
            # Creates 40% chance horizontal sensor will be drawn
            if h_chance_border >= 0.6:
                # Define, draw, and append location of sensor
                horizontal_sensor = Rectangle(Point(x-35.5, y), Point(x-4.5, y))
                horizontal_sensor.setWidth(2.5)
                horizontal_sensor.setOutline("orange")
                horizontal_sensor.draw(field)
                h_x = horizontal_sensor.getCenter().getX()
                h_y = horizontal_sensor.getCenter().getY()
                sensors.append([h_x, h_y])
            # Creates 40% chance horizontal sensor will be drawn
            if v_chance_border >= 0.6:
                # Define, draw, and append location of sensor
                vertical_sensor = Rectangle(Point(x, y-35.5), Point(x, y-4.5))
                vertical_sensor.setWidth(2.5)
                vertical_sensor.setOutline("orange")
                vertical_sensor.draw(field)
                v_x = vertical_sensor.getCenter().getX()
                v_y = vertical_sensor.getCenter().getY()
                sensors.append([v_x, v_y])
            # Move to next row
            y += 40
        # Set back to first row after finishing final row
        y = 40
        # Move to the next column
        x += 40

    # Draw vertical sensors
    return sensors

# =================================[ PANELS }==================================


# Define DrawInitialPanel()
def drawInitialPanel(game_panel):
    # Draw score display, "NEW PLAYER" text on green button
    score_box, score_text = drawScoreDisplay(game_panel)
    new_player_text = drawPlayerText(game_panel)
    # Set game panel phase to "initial"
    phase = "initial"
    # Return objects
    return new_player_text, score_box, score_text, phase

# Define DrawNewPlayerPanel() function


def drawNewPlayerPanel(new_player_text, score_box, score_text, game_panel, phase):
    # Set green button text to "START!", remove Initial conditions, and draw New
    #   Player entry
    new_player_text.setText("START!")
    undrawScoreDisplay(score_box, score_text)
    player_name_text, player_name_entry = drawPlayerNameEntry(game_panel)
    # Set game panel phase to "new_player"
    phase = "new_player"
    # Return objects
    return player_name_text, player_name_entry, phase

# Define DrawInGamePanel() function


def drawInGamePanel(new_player_text, player_name_entry, game_panel, score):
    # Set green button text to "NEW PLAYER", finalize player name, creat reset button,
    #   and draw score display
    new_player_text.setText("NEW PLAYER")
    player_name_display, player_name = drawPlayerNameDisplay(
        player_name_entry, game_panel)
    reset_button, reset_text = drawResetButton(game_panel)
    current_score_text, current_score_display = drawCurrentScore(
        game_panel, score)
    # Set game panel phase to "in_game"
    phase = "in_game"
    # Return objects
    return player_name_display, player_name, reset_button, reset_text, current_score_text, current_score_display, phase

# Define DrawResetPanel()


def drawResetPanel(reset, game_panel, reset_button, reset_text,
                   current_score_text, current_score_display, player_name_text,
                   player_name_display):
    # Remove reset button, set back to inital phase
    #   * Game panel phase not set to inital because drawInitialPanel() is called
    undrawResetButton(reset_button, reset_text)
    undrawScoreDisplay(current_score_text, current_score_display)
    undrawPlayerNameDisplay(player_name_text, player_name_display)
    new_player_text, score_box, score_text, phase = drawInitialPanel(game_panel)
    # Return objects
    return new_player_text, score_box, score_text, phase

# Define fieldPanel() function


def drawFieldPanel():
    # Create Field panel
    field = GraphWin("The Field", 400, 400)
    # Create vertical and horizontal lines on Field panel
    for i in range(9):
        v_field_line = Line(Point(40*(i+1), 0), Point(40*(i+1), 400))
        v_field_line.setOutline("light gray")
        v_field_line.draw(field)
        h_field_line = Line(Point(0, 40*(i+1)), Point(400, 40*(i+1)))
        h_field_line.setOutline("light gray")
        h_field_line.draw(field)
    # Color start and end squares
    start = Rectangle(Point(0, 0), Point(40, 40))
    start.setFill("green")
    start.setOutline("light gray")
    start.draw(field)
    end = Rectangle(Point(360, 360), Point(400, 400))
    end.setFill("red")
    end.setOutline("light gray")
    end.draw(field)
    # Create initial Pete Rectangle
    pete = Rectangle(Point(4, 4), Point(36, 36))
    pete.setFill("gold")
    pete.draw(field)
    # Draw and return sensors
    sensors = drawSensors(field)
    # Return objects
    return field, pete, sensors

# ================================[ CLICK }====================================

# Define clickCoords() function


def clickCoords(click):
    # Separate click Point into x and y coordinates
    x = click.getX()
    y = click.getY()
    # Return coordinates
    return (x, y)

# Define getClick() function


def getClick(game_panel, field, in_game):
    # When not in game, get click from game panel
    if in_game is False:
        click = game_panel.getMouse()
        panel = "game_panel"
    # When game is played, check panel and return result and click location
    else:
        panel, click = checkPanel(game_panel, field)
    # Get the coordinates of the click, regardless of panel
    x, y = clickCoords(click)
    # Return objects
    return panel, x, y

# ================================[ CHECKS }==================================

# Define checkPanel() function


def checkPanel(game_panel, field):
    # Until a click occurs, check panels for a click
    while True:
        click1 = game_panel.checkMouse()
        click2 = field.checkMouse()
        # When user clicks in the game panel, return "game" and click location
        if click1 is not None:
            return "game_panel", click1
            # End loop
            break
        # When user clicks in field panel, return "field" and click location
        elif click2 is not None:
            return "field", click2
            # End loop
            break

# Define checkExit() function


def checkExit(panel, x, y):
    # If user clicks in game panel on red exit button, return True
    if panel == "game_panel" and x >= 250 and y >= 160:
        return True
    else:
        return False

# Define checkGreenButton() function


def checkGreenButton(panel, x, y):
    # If user clicks in game panel on green button, return True
    if panel == "game_panel" and x >= 100 and x <= 200 and y >= 160:
        return True
    else:
        return False

# Define checkResetButton() function


def checkResetButton(panel, phase, x, y):
    # If reset button exists, and user clicks on it in the game panel, return True
    if panel == "game_panel" and phase == "in_game" and x <= 50 and y >= 160:
        return True
    else:
        return False

# Define checkWinGame() function


def checkWinGame(pete_center):
    # If Pete Rectangle is located in the center of the red Rectangle that
    #   represents the goal, return True
    peteX, peteY = clickCoords(pete_center)
    if peteX == 380.0 and peteY == 380.0:
        return True
    else:
        return False

# ===========================[ FIELD METHODS ]=================================

# Define movePete() function


def movePete(pete, field, x, y, score, sensors):
    # Find the location of Pete, and derive the edges
    pete_center = pete.getCenter()
    clickX = x
    clickY = y
    peteX, peteY = clickCoords(pete_center)
    peteUpperX = peteX+20
    peteLowerX = peteX-20
    peteUpperY = peteY+20
    peteLowerY = peteY-20
    # Undraw Pete object so it can be re-drawn
    pete.undraw()
    # Move down
    #   If user clicks below Pete in the same column, move Pete down one square
    if clickX >= peteLowerX and clickX <= peteUpperX and clickY > peteUpperY:
        peteY += 40
        # If Pete crossed a sensor border, add a penalty of 2
        for coordinate in sensors:
            if peteX == coordinate[0] and (peteY-20) == coordinate[1]:
                score += 2
        # Increment score for moving
        score += 1
    # Move up
    #   If user clicks above Pete in the same column, move Pete up one square
    elif clickX >= peteLowerX and clickX <= peteUpperX and clickY < peteLowerY:
        peteY -= 40
        # If Pete crossed a sensor border, add a penalty of 2
        for coordinate in sensors:
            if peteX == coordinate[0] and (peteY+20) == coordinate[1]:
                score += 2
        # Increment score for moving
        score += 1
    # Move right
    #   If user clicks to the right of Pete in the same row, move Pete right one square
    elif clickY >= peteLowerY and clickY <= peteUpperY and clickX > peteUpperX:
        peteX += 40
        # If Pete crossed a sensor border, add a penalty of 2
        for coordinate in sensors:
            if (peteX-20) == coordinate[0] and peteY == coordinate[1]:
                score += 2
        # Increment score for moving
        score += 1
    # Move left
    #   If user clicks to the left of Pete in the same row, move Pete left one square
    elif clickY >= peteLowerY and clickY <= peteUpperY and clickX < peteLowerX:
        peteX -= 40
        # If Pete crossed a sensor border, add a penalty of 2
        for coordinate in sensors:
            if (peteX+20) == coordinate[0] and peteY == coordinate[1]:
                score += 2
    # Move up-left
    elif clickY < peteLowerY and clickX < peteLowerX:
        peteX -= 40
        peteY -= 40
        # If Pete crossed a sensor border, add a penalty of 2
        for coordinate in sensors:
            if (peteX+20) == coordinate[0] and peteY == coordinate[1]:
                score += 2
    # Move up-right
    # Move down-left
    # Move down-right
        # Increment score for moving
        score += 1
    # Define and re-draw Pete rectangle object
    pete = Rectangle(Point(peteX-16, peteY-16), Point(peteX+16, peteY+16))
    pete.setFill("gold")
    pete.draw(field)
    # Return the center of Pete so the victory condition can be checked
    pete_center = pete.getCenter()
    # Return objects
    return pete, pete_center, score


# Define updateScore() function
def updateScore(current_score_text, current_score_display, game_panel, score):
    # Update score by re-drawing objects
    undrawCurrentScore(current_score_text, current_score_display)
    current_score_text, current_score_display = drawCurrentScore(game_panel,
                                                                 score)
    # Return objects
    return current_score_text, current_score_display


# Define endGame() function
def endGame(field, game_panel, player_name, score):
    # Let the user know the game is finished, and close after they click
    end_game_text = Text(Point(200, 200), "Finished! Click to close")
    end_game_text.draw(field)
    # Wait for user mouse input
    field.getMouse()
    # Add player score to top_scores.txt
    writeScores(player_name, score)
    # Set close condition to True
    close = True
    # Return close condition
    return close

# ===========================[ SCORE METHODS ]=================================


# Define writeScores() function
def writeScores(name, score):
    # Open top_scores.txt in appending mode
    score_file = open("top_scores.txt", 'a')
    # Create new score String using Player entered information
    new_score = name+","+str(score)+"\n"
    # Output String object to file
    score_file.write(new_score)
    # Close text file
    score_file.close()


# Define readScores() function
def readScores():
    # Create empty list of top scores
    top_scores = []
    # Open top_scores.txt in read mode
    score_file = open("top_scores.txt", 'r')
    # For each line of top_scores.txt, strip the newline character, split into
    #   name and score, convert score to an integer, and append to list
    for line in score_file.readlines():
        line = line[:-1]
        name, score = line.split(",")
        score = int(score)
        top_scores.append((name, score))
    # Close text file
    score_file.close()
    # Sort list by score component
    top_scores.sort(key=lambda s: s[1])
    # Retain only top four scores of list
    top_scores = top_scores[:4]
    # Return top scores in list form
    return top_scores

# ==============================[ CALL MAIN }==================================


# Call main() function
main()
