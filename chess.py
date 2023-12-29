import pygame

pygame.init()
Width = 800
Height = 800
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont("comicsansms", 20)
big_font = pygame.font.SysFont("comicsansms", 40)
timer = pygame.time.Clock()
fps = 60

# game variables and images
white = [
    "rook",
    "knight",
    "bishop",
    "queen",
    "king",
    "bishop",
    "knight",
    "rook",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
]
white_coordinates = [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
]
black = [
    "rook",
    "knight",
    "bishop",
    "queen",
    "king",
    "bishop",
    "knight",
    "rook",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
    "pawn",
]

black_coordinates = [
    (0, 7),
    (1, 7),
    (2, 7),
    (3, 7),
    (4, 7),
    (5, 7),
    (6, 7),
    (7, 7),
    (0, 6),
    (1, 6),
    (2, 6),
    (3, 6),
    (4, 6),
    (5, 6),
    (6, 6),
    (7, 6),
]
captured_white = []
captured_black = []
current_phase = 0
selection = 100
valid_moves = []
isInCheck = False
# pieces
black_queen = pygame.image.load("images/black-queen.png")
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load("images/black-king.png")
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load("images/black-rook.png")
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load("images/black-bishop.png")
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load("images/black-knight.png")
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load("images/black-pawn.png")
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load("images/white-queen.png")
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load("images/white-king.png")
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load("images/white-rook.png")
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load("images/white-bishop.png")
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load("images/white-knight.png")
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load("images/white-pawn.png")
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [
    white_pawn,
    white_queen,
    white_king,
    white_knight,
    white_rook,
    white_bishop,
]
small_white_images = [
    white_pawn_small,
    white_queen_small,
    white_king_small,
    white_knight_small,
    white_rook_small,
    white_bishop_small,
]
black_images = [
    black_pawn,
    black_queen,
    black_king,
    black_knight,
    black_rook,
    black_bishop,
]
small_black_images = [
    black_pawn_small,
    black_queen_small,
    black_king_small,
    black_knight_small,
    black_rook_small,
    black_bishop_small,
]
piece_list = ["pawn", "queen", "king", "knight", "rook", "bishop"]
# check variables
counter = 0


def drawBoard():
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
                pygame.draw.rect(screen, "White", (i * 80, j * 80, 80, 80))
            else:
                pygame.draw.rect(screen, "dark gray", (i * 80, j * 80, 80, 80))
        if isInCheck == True:
            screen.blit(big_font.render("King is in check", True, "red"), (20, 680))
        else:
            screen.blit(
                big_font.render(status[current_phase], True, "Black"), (20, 680)
            )


def drawPieces():
    for i in range(len(white)):
        index = piece_list.index(white[i])
        if white[i] == "pawn":
            screen.blit(
                white_images[index],
                (white_coordinates[i][0] * 80 + 5, white_coordinates[i][1] * 80),
            )
        else:
            screen.blit(
                white_images[index],
                (white_coordinates[i][0] * 80, white_coordinates[i][1] * 80),
            )
        if current_phase < 2:
            if selection == i:
                pygame.draw.rect(
                    screen,
                    "red",
                    (
                        white_coordinates[i][0] * 80,
                        white_coordinates[i][1] * 80,
                        80,
                        80,
                    ),
                    5,
                )

    for i in range(len(black)):
        index = piece_list.index(black[i])
        if black[i] == "pawn":
            screen.blit(
                black_images[index],
                (black_coordinates[i][0] * 80 + 5, black_coordinates[i][1] * 80),
            )
        else:
            screen.blit(
                black_images[index],
                (black_coordinates[i][0] * 80, black_coordinates[i][1] * 80),
            )
        if current_phase >= 2:
            if selection == i:
                pygame.draw.rect(
                    screen,
                    "blue",
                    (
                        black_coordinates[i][0] * 80,
                        black_coordinates[i][1] * 80,
                        80,
                        80,
                    ),
                    5,
                )


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


def Check():
    global isInCheck
    if current_phase < 2:
        king_index = white.index("king")
        king_location = white_coordinates[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                isInCheck = True
                if counter < 15:
                    pygame.draw.rect(
                        screen,
                        "red",
                        [
                            white_coordinates[king_index][0] * 80 + 1,
                            white_coordinates[king_index][1] * 80 + 1,
                            80,
                            80,
                        ],
                        5,
                    )
    else:
        king_index = black.index("king")
        king_location = black_coordinates[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                isInCheck = True
                if counter < 15:
                    pygame.draw.rect(
                        screen,
                        "blue",
                        [
                            black_coordinates[king_index][0] * 80 + 1,
                            black_coordinates[king_index][1] * 80 + 1,
                            80,
                            80,
                        ],
                        5,
                    )


# function to check all pieces valid options on board


def gameOver():
    if isGameOver:
        pygame.draw.rect(screen, "Black", [80, 180, 480, 200], border_radius=30)
        screen.blit(big_font.render(f"{winner} Wins", True, "White"), (210, 200))
        screen.blit(big_font.render(f"Press enter to reset", True, "White"), (140, 270))


def check_options(pieces, coordinates, phase):
    moveList = []
    allMovesList = []
    for i in range(len(pieces)):
        coordinate = coordinates[i]
        piece = pieces[i]
        if piece == "pawn":
            moveList = check_pawn(coordinate, phase)
        elif piece == "rook":
            moveList = check_rook(coordinate, phase)
        elif piece == "knight":
            moveList = check_knight(coordinate, phase)
        elif piece == "bishop":
            moveList = check_bishop(coordinate, phase)
        elif piece == "queen":
            moveList = check_queen(coordinate, phase)
        elif piece == "king":
            moveList = check_king(coordinate, phase)

        allMovesList.append(moveList)
    return allMovesList


def check_pawn(pos, color):
    moves_list = []
    if color == "White":
        if (
            (pos[0], pos[1] + 1) not in white_coordinates
            and (
                pos[0],
                pos[1] + 1,
            )
            not in black_coordinates
            and pos[1] < 7
        ):
            moves_list.append((pos[0], pos[1] + 1))
        if (
            (pos[0], pos[1] + 2) not in white_coordinates
            and (
                pos[0],
                pos[1] + 2,
            )
            not in black_coordinates
            and pos[1] == 1
            and (pos[0], pos[1] + 1) not in white_coordinates
            and (pos[0], pos[1] + 1) not in black_coordinates
        ):
            moves_list.append((pos[0], pos[1] + 2))

        if (pos[0] + 1, pos[1] + 1) in black_coordinates:
            moves_list.append((pos[0] + 1, pos[1] + 1))

        if (pos[0] - 1, pos[1] + 1) in black_coordinates:
            moves_list.append((pos[0] - 1, pos[1] + 1))

    else:
        if (
            (pos[0], pos[1] - 1) not in white_coordinates
            and (
                pos[0],
                pos[1] - 1,
            )
            not in black_coordinates
            and pos[1] > 0
        ):
            moves_list.append((pos[0], pos[1] - 1))
        if (
            (pos[0], pos[1] - 2) not in white_coordinates
            and (
                pos[0],
                pos[1] - 2,
            )
            not in black_coordinates
            and pos[1] == 6
            and (pos[0], pos[1] - 1) not in white_coordinates
            and (pos[0], pos[1] - 1) not in black_coordinates
        ):
            moves_list.append((pos[0], pos[1] - 2))

        if (pos[0] + 1, pos[1] - 1) in white_coordinates:
            moves_list.append((pos[0] + 1, pos[1] - 1))

        if (pos[0] - 1, pos[1] - 1) in white_coordinates:
            moves_list.append((pos[0] - 1, pos[1] - 1))
    return moves_list


def check_rook(pos, color):
    moves_list = []
    if color == "White":
        enemy_list = black_coordinates
        friends_list = white_coordinates
    else:
        enemy_list = white_coordinates
        friends_list = black_coordinates
    for i in range(4):  # up,down,left,right
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0

        while path:
            if (
                (pos[0] + (chain * x), pos[1] + (chain * y)) not in friends_list
                and 0 <= pos[0] + chain * x <= 7
                and 0 <= pos[1] + chain * y <= 7
            ):
                moves_list.append((pos[0] + chain * x, pos[1] + chain * y))
                if (pos[0] + (chain * x), pos[1] + (chain * y)) in enemy_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list


def check_knight(pos, color):
    moves_list = []
    if color == "White":
        enemy_list = black_coordinates
        friends_list = white_coordinates
    else:
        enemy_list = white_coordinates
        friends_list = black_coordinates
    for i in range(8):
        if i == 0:
            x = 1
            y = 2
        elif i == 1:
            x = 2
            y = 1
        elif i == 2:
            x = 2
            y = -1
        elif i == 3:
            x = 1
            y = -2
        elif i == 4:
            x = -1
            y = -2
        elif i == 5:
            x = -2
            y = -1
        elif i == 6:
            x = -2
            y = 1
        else:
            x = -1
            y = 2
        if (
            (pos[0] + x, pos[1] + y) not in friends_list
            and 0 <= pos[0] + x <= 7
            and 0 <= pos[1] + y <= 7
        ):
            moves_list.append((pos[0] + x, pos[1] + y))
    return moves_list


def check_bishop(pos, color):
    moves_list = []
    if color == "White":
        enemy_list = black_coordinates
        friends_list = white_coordinates
    else:
        enemy_list = white_coordinates
        friends_list = black_coordinates
    for i in range(4):  # up,down,left,right
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = 1
        elif i == 1:
            x = 1
            y = -1
        elif i == 2:
            x = -1
            y = 1
        else:
            x = -1
            y = -1

        while path:
            if (
                (pos[0] + (chain * x), pos[1] + (chain * y)) not in friends_list
                and 0 <= pos[0] + chain * x <= 7
                and 0 <= pos[1] + chain * y <= 7
            ):
                moves_list.append((pos[0] + chain * x, pos[1] + chain * y))
                if (pos[0] + (chain * x), pos[1] + (chain * y)) in enemy_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list


def check_queen(pos, color):
    moves_list = []
    moves_list.extend(check_rook(pos, color))
    moves_list.extend(check_bishop(pos, color))
    return moves_list


def check_king(pos, color):
    moves_list = []
    if color == "White":
        enemy_list = black_coordinates
        friends_list = white_coordinates
    else:
        enemy_list = white_coordinates
        friends_list = black_coordinates
    for i in range(8):
        if i == 0:
            x = 1
            y = 1
        elif i == 1:
            x = 1
            y = -1
        elif i == 2:
            x = -1
            y = 1
        elif i == 3:
            x = -1
            y = -1
        elif i == 4:
            x = 1
            y = 0
        elif i == 5:
            x = 0
            y = 1
        elif i == 6:
            x = -1
            y = 0
        else:
            x = 0
            y = -1
        if (
            (pos[0] + x, pos[1] + y) not in friends_list
            and 0 <= pos[0] + x <= 7
            and 0 <= pos[1] + y <= 7
        ):
            moves_list.append((pos[0] + x, pos[1] + y))
    return moves_list


def draw_valid(moves):
    if current_phase < 2:
        color = "red"
    else:
        color = "blue"
    for i in range(len(moves)):
        pygame.draw.circle(
            screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5
        )


def check_valid_moves():
    if current_phase < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


black_options = check_options(black, black_coordinates, "Black")
white_options = check_options(white, white_coordinates, "White")

run = True
isGameOver = False

while run:
    pygame.display.update()
    if not isGameOver:
        timer.tick(fps)
        if counter < 30:
            counter += 1
        else:
            counter = 0
        screen.fill("gray")
        isInCheck = False
        Check()
        drawBoard()
        drawPieces()
        drawCaptured()
        Check()
    if selection != 100 and not isGameOver:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[0] // 80, event.pos[1] // 80
            click_coordinates = (x, y)
            if current_phase < 2:
                if click_coordinates in white_coordinates:
                    selection = white_coordinates.index(click_coordinates)
                    current_phase = 1
                if click_coordinates in valid_moves and selection != 100:
                    white_coordinates[selection] = click_coordinates
                    if click_coordinates in black_coordinates:
                        black_piece = black_coordinates.index(click_coordinates)
                        captured_black.append(black[black_piece])
                        black.pop(black_piece)
                        black_coordinates.pop(black_piece)
                    black_options = check_options(black, black_coordinates, "Black")
                    white_options = check_options(white, white_coordinates, "White")
                    current_phase = 2
                    selection = 100
                    valid_moves = []
            if current_phase > 1:
                if click_coordinates in black_coordinates:
                    selection = black_coordinates.index(click_coordinates)
                    if current_phase == 2:
                        current_phase = 3
                if click_coordinates in valid_moves and selection != 100:
                    black_coordinates[selection] = click_coordinates
                    if click_coordinates in white_coordinates:
                        white_piece = white_coordinates.index(click_coordinates)
                        captured_white.append(white[white_piece])
                        white.pop(white_piece)
                        white_coordinates.pop(white_piece)
                    black_options = check_options(black, black_coordinates, "Black")
                    white_options = check_options(white, white_coordinates, "White")
                    current_phase = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and isGameOver:
            if event.key == pygame.K_RETURN:
                print("test")
                isGameOver = False
                white = [
                    "rook",
                    "knight",
                    "bishop",
                    "king",
                    "queen",
                    "bishop",
                    "knight",
                    "rook",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                ]
                white_coordinates = [
                    (0, 0),
                    (1, 0),
                    (2, 0),
                    (3, 0),
                    (4, 0),
                    (5, 0),
                    (6, 0),
                    (7, 0),
                    (0, 1),
                    (1, 1),
                    (2, 1),
                    (3, 1),
                    (4, 1),
                    (5, 1),
                    (6, 1),
                    (7, 1),
                ]
                black = [
                    "rook",
                    "knight",
                    "bishop",
                    "king",
                    "queen",
                    "bishop",
                    "knight",
                    "rook",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                    "pawn",
                ]
                black_coordinates = [
                    (0, 7),
                    (1, 7),
                    (2, 7),
                    (3, 7),
                    (4, 7),
                    (5, 7),
                    (6, 7),
                    (7, 7),
                    (0, 6),
                    (1, 6),
                    (2, 6),
                    (3, 6),
                    (4, 6),
                    (5, 6),
                    (6, 6),
                    (7, 6),
                ]
                captured_white = []
                captured_black = []
                current_phase = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black, black_coordinates, "Black")
                white_options = check_options(white, white_coordinates, "White")
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
