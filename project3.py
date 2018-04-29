#
# CS 177
# Patrick Rewers, Nicole Gillespie, Shelby Nelson
#
# The purpose of this program is to run and display a  maze game
#     where users try to solve the maze in as few members as
#     possible. The game tracks players' names, moves, and scores.
#

# Import Graphics library
from graphics import Point, Rectangle, GraphWin, Line, Entry, Text, Circle, Polygon
from random import random, randint, choice
from datetime import datetime
from time import sleep

# ==================================[ MAIN }===================================


# Define main() function
def main():

    # Draw the Game Panel
    game_panel = drawGamePanel()
    # Define current game settings and set score to 0
    close = False
    in_game = False
    score = 0
    # Create dummy variables to prevent errors before officially defined
    field = ""
    check_second = datetime.now().second

    # Draw initial game panel
    new_player_text, score_box, score_text, phase, scores = drawInitialPanel(game_panel)

    # Loop game functions until user clicks "Exit" button
    while close is False:

        # Get panel location and x and y coordinates of click
        panel, x, y = getClick(game_panel, field, in_game)

        # Check if user clicked "Exit" button
        close = checkExit(panel, x, y)

        # Change score in top score box every second
        second = datetime.now().second
        if second != None and second > check_second:
            changeScores(scores, score_text)
        check_second = second

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
                    player_name_display, player_name, reset_button, reset_text, current_score_text, current_score_display, phase = drawInGamePanel(new_player_text, player_name_entry, game_panel, score)
                    field, pete, sensors, spin_square,blackcenter1, blackcenter2,goodsensors = drawFieldPanel()

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
                field, pete, sensors, spin_square, blackcenter1,blackcenter2,goodsensors = drawFieldPanel()

        # Check if user clicked in field panel
        if panel == "field":
            # Move pete based on click
            pete, pete_center, score = movePete(pete, field, x, y, score, sensors, spin_square, blackcenter1, blackcenter2, goodsensors)
            # Update score with every click during game
            if phase == "in_game":
                # If score is less than 0 (crossing good sensor with a score of
                #   0, set score back to 0)
                if score < 0:
                    score = 0
                current_score_text, current_score_display = updateScore(current_score_text, current_score_display, game_panel, score)
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
    game_panel = GraphWin("Game Panel", 300, 300)
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
    exit_button = Rectangle(Point(250, 260), Point(300, 300))
    exit_button.setFill("red")
    exit_button.draw(game_panel)
    exit_text = Text(Point(275, 281), "EXIT")
    exit_text.setSize(14)
    exit_text.draw(game_panel)

    # Creates green button, which will be used for new player and start options
    green_button = Rectangle(Point(100, 260), Point(200, 300))
    green_button.setFill("green")
    green_button.draw(game_panel)
    return game_panel

# Define drawScoreDisplay() function
def drawScoreDisplay(game_panel):

    # Draws box that serves as the background the score displays
    score_box = Rectangle(Point(50, 155), Point(250, 240))
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
    # Create a text object of the top scores title and players and draw in game
    #  panel
    score_text = Text(Point(150, 198), "\n".join(scores[:6]))
    score_text.draw(game_panel)
    # Return objects
    return (score_box, score_text, scores)

# Define drawPlayerText() function

def drawPlayerText(game_panel):
    # Create and stylize "NEW PLAYER" text over green button
    new_player_text = Text(Point(150, 281), "NEW PLAYER")
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
    reset_button = Rectangle(Point(0, 260), Point(50, 300))
    reset_button.setFill("yellow")
    reset_button.draw(game_panel)
    reset_text = Text(Point(25, 281), "RESET")
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
    goodsensors=[]

    # Initialize loop to create horizontal sensors
    for column in range(10):
        for row in range(10):
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
    x=40
    y=40

    # Initialize loop to create good horizontal sensors
    for column in range(9):
        for row in range(9):

            # Create random number between 0 and 1
            h_chance_border = random()
            v_chance_border = random()

            # Creates 40% chance horizontal sensor will be drawn
            if h_chance_border <= .25:
                # Define, draw, and append location of sensor
                horizontal_sensorgood = Rectangle(Point(x-35.5, y), Point(x-4.5, y))
                horizontal_sensorgood.setWidth(2.5)
                horizontal_sensorgood.setOutline("green")
                h_xg = horizontal_sensorgood.getCenter().getX()
                h_yg = horizontal_sensorgood.getCenter().getY()
                if [h_xg,h_yg] not in sensors:
                    horizontal_sensorgood.draw(field)
                    goodsensors.append([h_xg, h_yg])

            # Creates 40% chance horizontal sensor will be drawn
            if v_chance_border <= 0.25:
                # Define, draw, and append location of sensor
                vertical_sensorgood = Rectangle(Point(x, y-35.5), Point(x, y-4.5))
                vertical_sensorgood.setWidth(2.5)
                vertical_sensorgood.setOutline("green")
                v_xg = vertical_sensorgood.getCenter().getX()
                v_yg = vertical_sensorgood.getCenter().getY()
                if [v_xg,v_yg] not in sensors:
                    vertical_sensorgood.draw(field)
                    goodsensors.append([v_xg, v_yg])

            # Move to next row
            y += 40
        # Set back to first row after finishing final row
        y = 40
        # Move to the next column
        x += 40



    # Draw vertical sensors

    return sensors, goodsensors

# =================================[ PANELS }==================================


# Define DrawInitialPanel()
def drawInitialPanel(game_panel):
    # Draw score display, "NEW PLAYER" text on green button
    score_box, score_text, scores = drawScoreDisplay(game_panel)
    new_player_text = drawPlayerText(game_panel)
    # Set game panel phase to "initial"
    phase = "initial"
    # Return objects
    return new_player_text, score_box, score_text, phase, scores

# Define DrawNewPlayerPanel() function
def drawNewPlayerPanel(new_player_text, score_box, score_text, game_panel, phase):
    # Set green button text to "START!", remove Initial conditions, and draw New
    #   Player entry
    new_player_text.setText("START!")
    player_name_text, player_name_entry = drawPlayerNameEntry(game_panel)
    # Set game panel phase to "new_player"
    phase = "new_player"
    # Return objects
    return player_name_text, player_name_entry, phase

# Define DrawInGamePanel() function
def drawInGamePanel(new_player_text, player_name_entry, game_panel, score):
    # Set green button text to "NEW PLAYER", finalize player name, creat reset
    #   button, and draw score display
    new_player_text.setText("NEW PLAYER")
    player_name_display, player_name = drawPlayerNameDisplay(
        player_name_entry, game_panel)
    reset_button, reset_text = drawResetButton(game_panel)
    current_score_text, current_score_display = drawCurrentScore(game_panel, score)
    # Set game panel phase to "in_game"
    phase = "in_game"
    # Return objects
    return player_name_display, player_name, reset_button, reset_text, current_score_text, current_score_display, phase

# Define DrawResetPanel()
def drawResetPanel(reset, game_panel, reset_button, reset_text, current_score_text, current_score_display, player_name_text, player_name_display):
    # Remove reset button, set back to inital phase
    #   * Game panel phase not set to inital because drawInitialPanel() is called
    undrawResetButton(reset_button, reset_text)
    undrawScoreDisplay(current_score_text, current_score_display)
    undrawPlayerNameDisplay(player_name_text, player_name_display)
    new_player_text, score_box, score_text, phase, scores = drawInitialPanel(game_panel)
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

    # Draw black holes
    blackcenter1, blackcenter2 = blackholes(field)

    # Create spin square Rectangle
    while True:
        # Make sure spin square is not drawn on top of black holes, and repeat
        #   location process if it is on top of a black hole
        spin_x = randint(2, 9) * 40 - 20
        spin_y = randint(2, 9) * 40 - 20
        spin_square = Rectangle(Point(spin_x-17, spin_y-17), Point(spin_x+17, spin_y+17))
        if spin_x != blackcenter1.getX() and spin_y != blackcenter1.getY() or spin_x != blackcenter2.getX() and spin_y != blackcenter2.getY():
            break
    spin_square.setFill("blue")
    spin_square.draw(field)
    spin_text = Text(Point(spin_x, spin_y), "SPIN")
    spin_text.setTextColor("white")
    spin_text.draw(field)

    # Create initial Pete Rectangle
    pete = Rectangle(Point(4, 4), Point(36, 36))
    pete.setFill("gold")
    pete.draw(field)

    # Draw and return sensors
    sensors, goodsensors = drawSensors(field)

    # Return objects
    return field, pete, sensors, spin_square, blackcenter1, blackcenter2, goodsensors

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
        click = game_panel.checkMouse()
        if click is not None:
            panel = "game_panel"
        else:
            panel = "none"

    # When game is played, check panel and return result and click location
    else:
        panel, click = checkPanel(game_panel, field)
    # Get the coordinates of the click, regardless of panel
    try:
        x, y = clickCoords(click)
    except AttributeError:
        x = 0
        y = 0

    # Return objects
    return panel, x, y

# ================================[ CHECKS }==================================


# Define checkPanel() function
def checkPanel(game_panel, field):

    # Until a click occurs, check panels for a click
    click1 = game_panel.checkMouse()
    click2 = field.checkMouse()

    # When user clicks in the game panel, return "game" and click location
    if click1 is not None:
        return "game_panel", click1

    # When user clicks in field panel, return "field" and click location
    elif click2 is not None:
        return "field", click2
    else:
        return "none", click1

# Define checkExit() function
def checkExit(panel, x, y):
    # If user clicks in game panel on red exit button, return True
    if panel == "game_panel" and x >= 250 and y >= 260:
        return True
    else:
        return False

# Define checkGreenButton() function
def checkGreenButton(panel, x, y):
    # If user clicks in game panel on green button, return True
    if panel == "game_panel" and x >= 100 and x <= 200 and y >= 260:
        return True
    else:
        return False

# Define checkResetButton() function
def checkResetButton(panel, phase, x, y):
    # If reset button exists, and user clicks on it in the game panel, return True
    if panel == "game_panel" and phase == "in_game" and x <= 50 and y >= 260:
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

# Define checkSensor() function
def checkSensor(direction, sensors, score, peteX, peteY, goodsensors):

    # Define Pete's location as a set of coordinates to check against
    coordinate = [peteX, peteY]

    # Check sensors related to Pete moving up
    if direction == "up":
        if [coordinate[0], coordinate[1] + 20] in sensors:
            score += 3
        elif [coordinate[0], coordinate[1]+20] in goodsensors:
            score -= 1
        else:
            score += 1

    # Check sensors related to Pete moving down
    if direction == "down":
        if [coordinate[0], coordinate[1] - 20] in sensors:
            score += 3
        elif [coordinate[0], coordinate[1]-20] in goodsensors:
            score -= 1
        else:
            score += 1

    # Check sensors related to Pete moving left
    if direction == "left":
        if [coordinate[0] + 20, coordinate[1]] in sensors:
            score += 3
        elif [coordinate[0]+20, coordinate[1]] in goodsensors:
            score -= 1
        else:
            score += 1

    # Check sensors related to Pete moving right
    if direction == "right":
        if [coordinate[0] - 20, coordinate[1]] in sensors:
            score += 3
        elif [coordinate[0]-20, coordinate[1]] in goodsensors:
            score -= 1
        else:
            score += 1

    # Check sensors related to Pete moving diagonally up and left
    if direction == "up,left":
        if [coordinate[0], coordinate[1] + 20] in sensors:
            score += 3
        if [coordinate[0] + 20, coordinate[1]] in sensors:
            score += 3
        if [coordinate[0] + 20, coordinate[1] + 40] in sensors:
            score += 3
        if [coordinate[0] + 40, coordinate[1] + 20] in sensors:
            score += 3
        if [coordinate[0], coordinate[1] + 20] not in sensors and [coordinate[0] + 20, coordinate[1]] not in sensors and [coordinate[0] + 20, coordinate[1] + 40] not in sensors and [coordinate[0] + 40, coordinate[1] + 20] not in sensors:
            score += 1

        #Check for goodsensors
        if [coordinate[0], coordinate[1] + 20] in goodsensors:
            score -= 1
        if [coordinate[0] + 20, coordinate[1]] in goodsensors:
            score -= 1
        if [coordinate[0] + 20, coordinate[1] + 40] in goodsensors:
            score -= 1
        if [coordinate[0] + 40, coordinate[1] + 20] in goodsensors:
            score -= 1

    # Check sensors related to Pete moving diagonally up and right
    if direction == "up,right":
        if [coordinate[0], coordinate[1] + 20] in sensors:
            score += 3
        if [coordinate[0] - 20, coordinate[1]] in sensors:
            score += 3
        if [coordinate[0] - 20, coordinate[1] + 40] in sensors:
            score += 3
        if [coordinate[0] - 40, coordinate[1] + 20] in sensors:
            score += 3
        if [coordinate[0], coordinate[1] + 20] not in sensors and [coordinate[0] - 20, coordinate[1]] not in sensors and [coordinate[0] - 20, coordinate[1] + 40] not in sensors and [coordinate[0] - 40, coordinate[1] + 20] not in sensors:
            score += 1

        #Check for goodsensors
        if [coordinate[0], coordinate[1] + 20] in goodsensors:
            score -= 1
        if [coordinate[0] - 20, coordinate[1]] in goodsensors:
            score -= 1
        if [coordinate[0] - 20, coordinate[1] + 40] in goodsensors:
            score -=1
        if [coordinate[0] - 40, coordinate[1] + 20] in goodsensors:
            score -= 1

    # Check sensors related to Pete moving diagonally down and left
    if direction == "down,left":

        # Check if Pete crossed a penalty sensor
        if [coordinate[0], coordinate[1] - 20] in sensors:
            score += 3
        if [coordinate[0] + 20, coordinate[1]] in sensors:
            score += 3
        if [coordinate[0] + 20, coordinate[1] - 40] in sensors:
            score += 3
        if [coordinate[0] + 40, coordinate[1] - 20] in sensors:
            score += 3
        if [coordinate[0], coordinate[1] - 20] not in sensors and [coordinate[0] + 20, coordinate[1]] not in sensors and [coordinate[0] + 20, coordinate[1] - 40] not in sensors and [coordinate[0] + 40, coordinate[1] - 20] not in sensors:
            score += 1

        # Check if Pete crossed a good sensor
        if [coordinate[0], coordinate[1] - 20] in goodsensors:
            score -= 1
        if [coordinate[0] + 20, coordinate[1]] in goodsensors:
            score -= 1
        if [coordinate[0] + 20, coordinate[1] - 40] in goodsensors:
            score -= 1
        if [coordinate[0] + 40, coordinate[1] - 20] in goodsensors:
            score -= 1

    # Check sensors related to Pete moving diagonally down and right
    if direction == "down,right":

        # Check if Pete crossed a penalty sensor
        if [coordinate[0], coordinate[1] - 20] in sensors:
            score += 3
        if [coordinate[0] - 20, coordinate[1]] in sensors:
            score += 3
        if [coordinate[0] - 20, coordinate[1] - 40] in sensors:
            score += 3
        if [coordinate[0] - 40, coordinate[1] - 20] in sensors:
            score += 3
        if [coordinate[0], coordinate[1] - 20] not in sensors and [coordinate[0] - 20, coordinate[1]] not in sensors and [coordinate[0] - 20, coordinate[1] - 40] not in sensors and [coordinate[0] - 40, coordinate[1] - 20] not in sensors:
            score += 1

        # Check if Pete crossed a good sensor
        if [coordinate[0], coordinate[1] - 20] in goodsensors:
            score -= 1
        if [coordinate[0] - 20, coordinate[1]] in goodsensors:
            score -= 1
        if [coordinate[0] - 20, coordinate[1] - 40] in goodsensors:
            score -= 1
        if [coordinate[0] - 40, coordinate[1] - 20] in goodsensors:
            score -= 1

    # If user did not move, do nothing
    if direction == "none":
        pass

    # Return score after any changes
    return score

# ===========================[ FIELD METHODS ]=================================


# Define movePete() function
def movePete(pete, field, x, y, score, sensors, spin_square,blackcenter1, blackcenter2, goodsensors):

    # Find the location of Pete and spin square, and derive the edges of Pete
    pete_center = pete.getCenter()
    clickX = x
    clickY = y
    peteX, peteY = clickCoords(pete_center)
    spinX, spinY = clickCoords(spin_square.getCenter())

    # Define bounds of Pete object
    peteUpperX = peteX + 20
    peteLowerX = peteX - 20
    peteUpperY = peteY + 20
    peteLowerY = peteY - 20

    # Undraw Pete object so it can be re-drawn
    pete.undraw()

    # Check if Pete is on spin square, and randomly move him in a direction
    #   that is not a wall
    if peteX == spinX and peteY == spinY:
        direction = {'-1,-1':'up,left', '-1,0':'left', '-1,1':'down,left',
        '0,-1':'up', '0,0':'none', '0,1':'down',
        '1,-1':'up,right', '1,0':'right', '1,1':'down,right'}
        x_movement = randint(-1, 1)
        y_movement = randint(-1, 1)
        peteX += x_movement * 40
        peteY += y_movement * 40
        direction_key = str(x_movement) + "," + str(y_movement)
        direction_value = direction[direction_key]
        score = checkSensor(direction_value, sensors, score, peteX, peteY, goodsensors)

    # If not on spin tile, perform a normal action
    else:

        # Create list of directions
        direction = []

        # Move Pete up if the user clicks above him
        if clickY < peteLowerY:
            peteY -= 40
            direction.append("up")

        # Move Pete down if the user clicks below him
        if clickY > peteUpperY:
            peteY += 40
            direction.append("down")

        # Move Pete left if the user clicks left of him
        if clickX < peteLowerX:
            peteX -= 40
            direction.append("left")

        # Move Pete right if the user clicks to the right of him
        if clickX > peteUpperX:
            peteX += 40
            direction.append("right")
        direction = ",".join(direction)
        score = checkSensor(direction, sensors, score, peteX, peteY, goodsensors)

    # Define and re-draw Pete Rectangle object
    pete = Rectangle(Point(peteX-16, peteY-16), Point(peteX+16, peteY+16))
    pete.setFill("gold")
    pete.draw(field)

    # Return the center of Pete so the victory condition can be checked
    pete_center = pete.getCenter()

    #Get the center of Pete
    petecenter=pete.getCenter()
    #If center of Pete matches blackcenter1, move him to blackcenter2
    if petecenter.getX()==blackcenter1.getX() and petecenter.getY()==blackcenter1.getY():
        pete.undraw()
        petecenter=blackcenter2
        pete=Rectangle(Point(blackcenter2.getX()-20,blackcenter2.getY()-20),Point(blackcenter2.getX()+20,blackcenter2.getY()+20))
        pete.setFill('gold')
        pete.draw(field)

    #If center of Pete matches blackcenter2, move him to blackcenter1
    elif petecenter.getX()==blackcenter2.getX() and petecenter.getY()==blackcenter2.getY():
        pete.undraw()
        petecenter=blackcenter1
        pete=Rectangle(Point(blackcenter1.getX()-20,blackcenter1.getY()-20),Point(blackcenter1.getX()+20,blackcenter1.getY()+20))
        pete.setFill('gold')
        pete.draw(field)

    # Return objects
    return pete, pete_center, score

# Define updateScore() function
def updateScore(current_score_text, current_score_display, game_panel, score):
    # Update score by re-drawing objects
    undrawCurrentScore(current_score_text, current_score_display)
    current_score_text, current_score_display = drawCurrentScore(game_panel, score)
    # Return objects
    return current_score_text, current_score_display

# Define endGame() function
def endGame(field, game_panel, player_name, score):

    # Let the user know the game is finished
    end_game_text = Text(Point(200, 200), "Finished! Click to close")
    end_game_text.draw(field)

    # Draw graphic objects at different places that represent balloons with a
    # string connected to it.
    balloon_1 = Circle(Point(145,110),18)
    balloon_1.setFill("red")
    balloon_1.setOutline("red")
    balloon_1.draw(field)
    triangle_1 = Polygon(Point(137,135),Point(145,128),Point(153,135))
    triangle_1.setFill("red")
    triangle_1.setOutline('red')
    triangle_1.draw(field)
    string_1 = Line(Point(145,135),Point(145,180))
    string_1.draw(field)

    balloon_2 = Circle(Point(340,300),18)
    balloon_2.setFill("red")
    balloon_2.setOutline("red")
    balloon_2.draw(field)
    triangle_2 = Polygon(Point(332,325),Point(340,318),Point(348,325))
    triangle_2.setFill("red")
    triangle_2.setOutline('red')
    triangle_2.draw(field)
    string_2 = Line(Point(340,325),Point(340,370))
    string_2.draw(field)

    balloon_3 = Circle(Point(75,275),18)
    balloon_3.setFill("red")
    balloon_3.setOutline("red")
    balloon_3.draw(field)
    triangle_3 = Polygon(Point(67,300),Point(75,293),Point(83,300))
    triangle_3.setFill("red")
    triangle_3.setOutline('red')
    triangle_3.draw(field)
    string_3 = Line(Point(75,300),Point(75,345))
    string_3.draw(field)

    # Create a while loop that moves the objets every 0.05 seconds upwards to
    # make it appear as if they are floating
    while True:
        sleep(0.05)
        balloon_1.move(0,-10)
        triangle_1.move(0,-10)
        string_1.move(0,-10)
        balloon_2.move(0,-10)
        triangle_2.move(0,-10)
        string_2.move(0,-10)
        balloon_3.move(0,-10)
        triangle_3.move(0,-10)
        string_3.move(0,-10)

        # If a click is detetced in the field, the window will close even if the
        # balloons are still moving in the while loop
        click = field.checkMouse()
        if click != None:
            break

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
    # Return top scores in list form
    return top_scores

# Define changeScores() function
def changeScores(scores, score_text):
    scores.append(scores.pop(2))
    score_text.setText("\n".join(scores[:6]))

# Define blackholes() function
def blackholes(field):
    #create a list of numbers that could be X and Y coordinates
    numbers=[]
    for i in range (60,360,40):
        numbers.append(i)
    #From that list, select a pair to be the location of the black holes
    #Create first blackhole coordinates
    blackX1=int(choice(numbers))
    blackY1=int(choice(numbers))
    #Create second blackhole coordinates
    blackX2=int(choice(numbers))
    blackY2=int(choice(numbers))
    #Draw black holes
    black1=Circle(Point(blackX1,blackY1), 5)
    black1.setFill('black')
    black1.draw(field)
    black2=Circle(Point(blackX2,blackY2), 5)
    black2.setFill('black')
    black2.draw(field)
    #Get the centers of the circles and return them
    blackcenter1=black1.getCenter()
    blackcenter2=black2.getCenter()

    return blackcenter1, blackcenter2

# ==============================[ CALL MAIN }==================================


# Call main() function
main()
