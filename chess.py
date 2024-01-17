import pygame
from init import (
    white,
    WhiteCoordinates,
    black,
    BlackCoordinates,
    piece_list,
    white_images,
    black_images,
    small_white_images,
    small_black_images,
    piece_list,
    pieces,
)

pygame.init()
Width = 800
Height = 800
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont("comicsansms", 20)
big_font = pygame.font.SysFont("comicsansms", 40)
timer = pygame.time.Clock()
fps = 60

counter = 0
captured_white = []
captured_black = []
current_phase = 0
selection = 100
valid_moves = []
isInCheck = False


# draws the boards and handles
def drawBoard(screen, big_font):
    global isInCheck
    pygame.draw.rect(screen, "Black", (0, 0, 640, 640), 5)
    pygame.draw.line(screen, "Black", (0, 640), (640, 640), 10)
    pygame.draw.line(screen, "Black", (640, 0), (640, 800), 10)
    status = [
        "White: It is your turn",
        "White: Select a field to move to",
        "Black: It is your turn",
        "Black: Select a field to move to",
    ]
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), (i * 80, j * 80, 80, 80))
            else:
                pygame.draw.rect(screen, (45, 98, 177, 255), (i * 80, j * 80, 80, 80))
        if isInCheck == True:
            screen.blit(big_font.render("King is in check", True, "red"), (20, 680))
        else:
            screen.blit(
                big_font.render(status[current_phase], True, "Black"), (20, 680)
            )


# draw pieces
def drawWhite():
    for i in range(len(white)):
        index = piece_list.index(white[i])
        if white[i] == "pawn":
            screen.blit(
                white_images[index],
                (WhiteCoordinates[i][0] * 80 + 5, WhiteCoordinates[i][1] * 80 + 5),
            )
        else:
            screen.blit(
                white_images[index],
                (WhiteCoordinates[i][0] * 80, WhiteCoordinates[i][1] * 80),
            )
        if current_phase < 2:
            if selection == i:
                pygame.draw.rect(
                    screen,
                    "red",
                    (
                        WhiteCoordinates[i][0] * 80,
                        WhiteCoordinates[i][1] * 80,
                        80,
                        80,
                    ),
                    5,
                )


def drawBlack():
    for i in range(len(black)):
        index = piece_list.index(black[i])
        if black[i] == "pawn":
            screen.blit(
                black_images[index],
                (BlackCoordinates[i][0] * 80 + 5, BlackCoordinates[i][1] * 80 + 5),
            )
        else:
            screen.blit(
                black_images[index],
                (BlackCoordinates[i][0] * 80, BlackCoordinates[i][1] * 80),
            )
        if current_phase >= 2:
            if selection == i:
                pygame.draw.rect(
                    screen,
                    "blue",
                    (
                        BlackCoordinates[i][0] * 80,
                        BlackCoordinates[i][1] * 80,
                        80,
                        80,
                    ),
                    5,
                )


def drawPieces():
    drawBlack()
    drawWhite()


# draw pieces to the side
def drawCaptured():
    for i in range(len(captured_white)):
        index = piece_list.index(captured_white[i])
        screen.blit(
            small_white_images[index],
            (645, i * 45),
        )
    for i in range(len(captured_black)):
        index = piece_list.index(captured_black[i])
        screen.blit(
            small_black_images[index],
            (750, i * 45),
        )


# render warning when king in check
def Check():
    global isInCheck
    if current_phase < 2:
        king_index = white.index("king")
        king_location = WhiteCoordinates[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                isInCheck = True
                if counter < 15:
                    pygame.draw.rect(
                        screen,
                        "red",
                        [
                            WhiteCoordinates[king_index][0] * 80 + 1,
                            WhiteCoordinates[king_index][1] * 80 + 1,
                            80,
                            80,
                        ],
                        5,
                    )
    else:
        king_index = black.index("king")
        king_location = BlackCoordinates[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                isInCheck = True
                if counter < 15:
                    pygame.draw.rect(
                        screen,
                        "blue",
                        [
                            BlackCoordinates[king_index][0] * 80 + 1,
                            BlackCoordinates[king_index][1] * 80 + 1,
                            80,
                            80,
                        ],
                        5,
                    )


# render game over screen
def gameOver():
    if isGameOver:
        pygame.draw.rect(screen, "Black", [80, 180, 480, 200], border_radius=30)
        screen.blit(big_font.render(f"{winner} Wins", True, "White"), (210, 200))
        screen.blit(big_font.render(f"Press enter to reset", True, "White"), (140, 270))


# calculate valid moves
def validMoves(pieces, coordinates, phase):
    moveList = []
    allMovesList = []
    for i in range(len(pieces)):
        coordinate = coordinates[i]
        piece = pieces[i]
        if piece == "pawn":
            moveList = Pawn(coordinate, phase)
        elif piece == "rook":
            moveList = Rook(coordinate, phase)
        elif piece == "knight":
            moveList = Knight(coordinate, phase)
        elif piece == "bishop":
            moveList = Bishop(coordinate, phase)
        elif piece == "queen":
            moveList = Queen(coordinate, phase)
        elif piece == "king":
            moveList = King(coordinate, phase)
        allMovesList.append(moveList)
    return allMovesList


def Pawn(pos, color):
    Move = []
    direction = 0
    startingPositon = 0
    coords = WhiteCoordinates
    enemycoords = BlackCoordinates
    if color == "White":
        direction = 1
        startingPositon = 1
    else:
        direction = -1
        startingPositon = 6
        coords = BlackCoordinates
        enemycoords = WhiteCoordinates

    if (
        (pos[0], pos[1] + direction) not in coords
        and (
            pos[0],
            pos[1] + direction,
        )
        not in enemycoords
        and (pos[1] < 6 if color == "White" else pos[1] > 1)
    ):
        Move.append((pos[0], pos[1] + direction))
    if (
        (pos[0], pos[1] + 2 * direction) not in coords
        and (
            pos[0],
            pos[1] + 2 * direction,
        )
        not in enemycoords
        and pos[1] == startingPositon
        and (pos[0], pos[1] + direction) not in coords
        and (pos[0], pos[1] + direction) not in enemycoords
    ):
        Move.append((pos[0], pos[1] + 2 * direction))

    if (pos[0] + 1, pos[1] + direction) in enemycoords:
        Move.append((pos[0] + 1, pos[1] + direction))

    if (pos[0] - 1, pos[1] + direction) in enemycoords:
        Move.append((pos[0] - 1, pos[1] + direction))
    return Move


def checkDirectionForRook(pos, dir, player, opponent):
    moveInDirection = []
    isValidPath = True
    chain = 1
    while isValidPath:
        if (
            (pos[0] + (chain * dir[0]), pos[1] + (chain * dir[1])) not in player
            and 0 <= pos[0] + chain * dir[0] <= 7
            and 0 <= pos[1] + chain * dir[1] <= 7
        ):
            moveInDirection.append((pos[0] + chain * dir[0], pos[1] + chain * dir[1]))
            if (pos[0] + (chain * dir[0]), pos[1] + (chain * dir[1])) in opponent:
                isValidPath = False
            chain += 1
        else:
            isValidPath = False
    return moveInDirection


def Rook(pos, color):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    Move = []
    opponent = BlackCoordinates if color == "White" else WhiteCoordinates
    player = WhiteCoordinates if color == "White" else BlackCoordinates

    for direction in directions:
        Move.extend(checkDirectionForRook(pos, direction, player, opponent))

    return Move


def Knight(pos, color):
    knight_moves = [
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
        (-2, 1),
        (-1, 2),
    ]
    Move = []
    player = WhiteCoordinates if color == "White" else BlackCoordinates

    for move in knight_moves:
        x, y = pos[0] + move[0], pos[1] + move[1]
        if (x, y) not in player and 0 <= x <= 7 and 0 <= y <= 7:
            Move.append((x, y))

    return Move


def checkDirectionForBishop(pos, dir, player, opponent):
    moveInDirection = []
    isValidPath = True
    chain = 1
    while isValidPath:
        x, y = pos[0] + chain * dir[0], pos[1] + chain * dir[1]
        if (x, y) not in player and 0 <= x <= 7 and 0 <= y <= 7:
            moveInDirection.append((x, y))
            if (x, y) in opponent:
                isValidPath = False
            chain += 1
        else:
            isValidPath = False
    return moveInDirection


def Bishop(pos, color):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    Move = []
    opponent = BlackCoordinates if color == "White" else WhiteCoordinates
    player = WhiteCoordinates if color == "White" else BlackCoordinates

    for direction in directions:
        Move.extend(checkDirectionForBishop(pos, direction, player, opponent))
    return Move


def Queen(pos, color):
    Move = []
    Move.extend(Rook(pos, color))
    Move.extend(Bishop(pos, color))
    return Move


def checkDirectionForKing(pos, dir, player):
    moveInDirection = []
    x, y = pos[0] + dir[0], pos[1] + dir[1]
    if (x, y) not in player and 0 <= x <= 7 and 0 <= y <= 7:
        moveInDirection.append((x, y))
    return moveInDirection


def King(pos, color):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
    Move = []
    player = WhiteCoordinates if color == "White" else BlackCoordinates

    for direction in directions:
        Move.extend(checkDirectionForKing(pos, direction, player))

    return Move


def drawValidMoves(moves):
    color = "red" if current_phase < 2 else "light blue"
    for move in moves:
        pygame.draw.circle(screen, color, (move[0] * 80 + 40, move[1] * 80 + 40), 5)


def check_valid_moves():
    if current_phase < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


def handle_mouse_click(event):
    x, y = event.pos[0] // 80, event.pos[1] // 80
    click_coordinates = (x, y)
    if current_phase < 2:
        handle_white_move(click_coordinates)
    elif current_phase > 1:
        handle_black_move(click_coordinates)


def handle_white_move(click_coordinates):
    global current_phase, selection, valid_moves
    if click_coordinates in WhiteCoordinates:
        selection = WhiteCoordinates.index(click_coordinates)
        current_phase = 1
    if click_coordinates in valid_moves and selection != 100:
        make_move(
            click_coordinates, WhiteCoordinates, BlackCoordinates, black, captured_black
        )
        current_phase = 2
        selection = 100
        valid_moves = []


def handle_black_move(click_coordinates):
    global current_phase, selection, valid_moves
    if click_coordinates in BlackCoordinates:
        selection = BlackCoordinates.index(click_coordinates)
        if current_phase == 2:
            current_phase = 3
    if click_coordinates in valid_moves and selection != 100:
        make_move(
            click_coordinates, BlackCoordinates, WhiteCoordinates, white, captured_white
        )
        current_phase = 0
        selection = 100
        valid_moves = []


def make_move(
    click_coordinates,
    player_coordinates,
    opponent_coordinates,
    opponent_pieces,
    captured_pieces,
):
    player_coordinates[selection] = click_coordinates
    if click_coordinates in opponent_coordinates:
        opponent_piece = opponent_coordinates.index(click_coordinates)
        captured_pieces.append(opponent_pieces[opponent_piece])
        opponent_pieces.pop(opponent_piece)
        opponent_coordinates.pop(opponent_piece)
    update_options()


def update_options():
    global black_options, white_options
    black_options = validMoves(black, BlackCoordinates, "Black")
    white_options = validMoves(white, WhiteCoordinates, "White")


def reset_game():
    global isGameOver, white, WhiteCoordinates, black, BlackCoordinates, captured_white, captured_black, current_phase, selection, valid_moves, black_options, white_options
    isGameOver = False
    white = pieces.copy()
    WhiteCoordinates = [(i % 8, i // 8) for i in range(16)]
    black = pieces.copy()
    BlackCoordinates = [(i % 8, 7 - i // 8) for i in range(16)]
    captured_white = []
    captured_black = []
    current_phase = 0
    selection = 100
    valid_moves = []
    update_options()


run = True
isGameOver = False

black_options = validMoves(black, BlackCoordinates, "Black")
white_options = validMoves(white, WhiteCoordinates, "White")

while run:
    pygame.display.update()
    if not isGameOver:
        timer.tick(fps)
        counter = (counter + 1) % 30
        screen.fill("gray")
        isInCheck = False
        Check()
        drawBoard(screen, big_font)
        drawPieces()
        drawCaptured()
        Check()
    if selection != 100 and not isGameOver:
        valid_moves = check_valid_moves()
        drawValidMoves(valid_moves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_mouse_click(event)
        if event.type == pygame.KEYDOWN and isGameOver and event.key == pygame.K_RETURN:
            reset_game()
    if captured_black.count("king") == 1:
        winner = "White"
        isGameOver = True
        gameOver()
    elif captured_white.count("king") == 1:
        isGameOver = True
        winner = "Black"
        gameOver()

pygame.display.flip()
pygame.quit()
