from PIL import Image, ImageDraw
import random

GRID_SIZE = 20
TILE_SIZE = 33  # pixels

START = 0
CROSS = 1
TOP_LEFT = 2
TOP_RIGHT = 3
BOTTOM_LEFT = 4
BOTTOM_RIGHT = 5
END = 6
BLANK = 7

rules = [
    [
        [START, TOP_LEFT, TOP_RIGHT, END, BLANK],
        [CROSS, TOP_LEFT, BOTTOM_LEFT, END],
        [START, BOTTOM_LEFT, BOTTOM_RIGHT, END, BLANK],
        [TOP_LEFT, BOTTOM_LEFT, END, BLANK]
    ],
    [
        [CROSS, BOTTOM_LEFT, BOTTOM_RIGHT],
        [CROSS, TOP_LEFT, BOTTOM_LEFT, END],
        [CROSS, TOP_LEFT, TOP_RIGHT],
        [START, CROSS, TOP_RIGHT, BOTTOM_RIGHT]
    ],
    [
        [CROSS, BOTTOM_LEFT, BOTTOM_RIGHT],
        [START, TOP_RIGHT, BOTTOM_RIGHT, BLANK],
        [START, BOTTOM_LEFT, BOTTOM_RIGHT, END, BLANK],
        [START, CROSS, TOP_RIGHT, BOTTOM_RIGHT]
    ],
    [
        [CROSS, BOTTOM_LEFT, BOTTOM_RIGHT],
        [CROSS, TOP_LEFT, BOTTOM_LEFT, END],
        [START, BOTTOM_LEFT, BOTTOM_RIGHT, END, BLANK],
        [TOP_LEFT, BOTTOM_LEFT, END, BLANK]
    ],
    [
        [START, TOP_LEFT, TOP_RIGHT, END, BLANK],
        [START, TOP_RIGHT, BOTTOM_RIGHT, BLANK],
        [CROSS, TOP_LEFT, TOP_RIGHT],
        [START, CROSS, TOP_RIGHT, BOTTOM_RIGHT]
    ],
    [
        [START, TOP_LEFT, TOP_RIGHT, END, BLANK],
        [CROSS, TOP_LEFT, BOTTOM_LEFT, END],
        [CROSS, TOP_LEFT, TOP_RIGHT],
        [TOP_LEFT, BOTTOM_LEFT, END, BLANK]
    ],
    [
        [START, TOP_LEFT, TOP_RIGHT, END, BLANK],
        [START, TOP_RIGHT, BOTTOM_RIGHT, BLANK],
        [START, BOTTOM_LEFT, BOTTOM_RIGHT, END, BLANK],
        [START, CROSS, TOP_RIGHT, BOTTOM_RIGHT]
    ],
    [
        [START, TOP_LEFT, TOP_RIGHT, END, BLANK],
        [START, TOP_RIGHT, BOTTOM_RIGHT, BLANK],
        [START, BOTTOM_LEFT, BOTTOM_RIGHT, END, BLANK],
        [TOP_LEFT, BOTTOM_LEFT, END, BLANK]
    ]
]


class Tile:
    def __init__(self, _collapsed, _options):
        self.collapsed = _collapsed
        self.options = _options

    def __repr__(self):
        return f"Arr len: {len(self.options)}"


def load_tiles():
    tiles = []
    tiles.append(Image.open("tiles/start_point.png"))
    tiles.append(Image.open("tiles/cross.png"))
    tiles.append(Image.open("tiles/top_left.png"))
    tiles.append(Image.open("tiles/top_right.png"))
    tiles.append(Image.open("tiles/bottom_left.png"))
    tiles.append(Image.open("tiles/bottom_right.png"))
    tiles.append(Image.open("tiles/end_point.png"))
    tiles.append(Image.open("tiles/blank.png"))
    return tiles


def check_valid(arr, valid):
    i = len(arr) - 1
    while i >= 0:
        if arr[i] not in valid:
            arr.pop(i)
        i -= 1


def draw(terrain, tiles, grid):
    grid_copy = grid.copy()
    grid_copy = [a for a in grid_copy if not a.collapsed]
    grid_copy.sort(key=lambda x: len(x.options))

    length = len(grid_copy[0].options)
    stop_index = 0
    for i in range(len(grid_copy)):
        if len(grid_copy[i].options) > length:
            stop_index = i
            break

    if stop_index > 0:
        grid_copy = grid_copy[:stop_index]

    cell = random.choice(grid_copy)
    cell.collapsed = True
    pick = random.choice(cell.options)
    cell.options = [pick]

    x = 0
    y = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[j + i * GRID_SIZE]
            if cell.collapsed:
                index = cell.options[0]
                terrain.paste(tiles[index], (j * TILE_SIZE, i * TILE_SIZE))
            else:
                rectangle = ImageDraw.Draw(terrain)
                rectangle.rectangle(
                    [
                        (j * TILE_SIZE, i * TILE_SIZE),
                        ((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE),
                    ]
                )

    next_grid = [None] * (GRID_SIZE * GRID_SIZE)
    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE):
            index = i + j * GRID_SIZE
            if grid[index].collapsed:
                next_grid[index] = grid[index]
            else:
                options = [
                    START,
                    CROSS,
                    TOP_LEFT,
                    TOP_RIGHT,
                    BOTTOM_LEFT,
                    BOTTOM_RIGHT,
                    END,
                    BLANK,
                ]
                valid_options = []
                # UP
                if j > 0:
                    up = grid[i + (j - 1) * GRID_SIZE]
                    for option in up.options:
                        valid = rules[option][2]
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # RIGHT
                valid_options = []
                if i < GRID_SIZE - 1:
                    right = grid[i + 1 + j * GRID_SIZE]
                    for option in right.options:
                        valid = rules[option][3]
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # DOWN
                valid_options = []
                if j < GRID_SIZE - 1:
                    down = grid[i + (j + 1) * GRID_SIZE]
                    for option in down.options:
                        valid = rules[option][0]
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # LEFT
                valid_options = []
                if i > 0:
                    left = grid[i - 1 + j * GRID_SIZE]
                    for option in left.options:
                        valid = rules[option][1]
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                next_grid[index] = Tile(False, options)

    for i in range(GRID_SIZE * GRID_SIZE):
        grid[i] = next_grid[i]


def init_grid():
    grid = []
    for i in range(GRID_SIZE * GRID_SIZE):
        grid.append(
            Tile(
                False,
                [
                    START,
                    CROSS,
                    TOP_LEFT,
                    TOP_RIGHT,
                    BOTTOM_LEFT,
                    BOTTOM_RIGHT,
                    END,
                    BLANK,
                ],
            )
        )
    return grid


def setup():
    return Image.new("RGB", (GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE), "white")


def show(terrain):
    terrain.show()
    terrain.save("wfc.png")


grid = init_grid()
tiles = load_tiles()
terrain = setup()
for i in range(GRID_SIZE * GRID_SIZE):
    draw(terrain, tiles, grid)
show(terrain)
