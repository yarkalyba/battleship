import string


def generate_field():
    import random
    borders = ((0, 0), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))
    field = [[" "] * 10 for i in range(10)]
    all_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    ship_borders = []
    for i in all_ships:
        horizontal = random.choice([False, True])  # false
        if horizontal:
            while True:
                tries = 0
                column = random.choice(range(10 - i))
                row = random.choice(range(10))
                for length in range(i):
                    for p in borders:
                        if [row+p[0], column + length + p[1]] in ship_borders:
                            tries += 1
                if tries == 0:
                    break
            for j in range(i):
                field[row][column + j] = "*"
                ship_borders.append([row, column+j])
        else:
            while True:
                tries = 0
                column = random.choice(range(10))
                row = random.choice(range(10-i))
                for length in range(i):
                    for p in borders:
                        if [row+length+p[0], column + p[1]] in ship_borders:
                            tries += 1
                if tries == 0:
                    break
            for j in range(i):
                field[row+j][column] = "*"
                ship_borders.append([row + j, column])
    return field

def write_field():
    with open("kek", "w") as file:
        field = generate_field()
        for i in range(len(field)):
            if len(field)-1 != i:
                file.write("".join(field[i]) + "\n")
            else:
                file.write("".join(field[i]))

write_field()


def read_field(filename):
    """
    (str) -> (data)
    :param filename: str(name of the file)
    :return: list of lists
    """
    lst = []
    with open(filename) as file:
        for i in range(10):
            line = file.readline().rstrip()
            lst_line = list(line)
            while len(lst_line) < 10:
                lst_line.append(" ")
            lst.append(lst_line)
    return lst


data = read_field("field.txt")


def has_ship(data, coord):
    """
    (data, coord) -> bool
    """
    if data[coord[1] - 1][
        string.ascii_lowercase.index(coord[0].lower())] == "*":
        return True
    return False


def ship_size(data, coord):
    if not has_ship(data, coord):
        return (0, 0)
    horiz = 1
    ver = 1
    board_range = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    j = 0

    for i in range(4):
        new_coord = (string.ascii_lowercase[string.ascii_lowercase.index(
            (coord[0].lower())) + board_range[i][j]],
                     coord[1] + board_range[i][j + 1])
        while True:
            if string.ascii_lowercase.index(
                    (new_coord[0].lower())) < 0 and i == 1:
                break
            try:
                if has_ship(data, new_coord):
                    new_coord = (
                        string.ascii_lowercase[string.ascii_lowercase.index(
                            (new_coord[0].lower())) + board_range[i][j]],
                        new_coord[1] + board_range[i][j + 1])
                    if i < 2:
                        horiz += 1
                    else:
                        ver += 1
                else:
                    break
            except IndexError:
                break

    return (ver, horiz)


def is_valid(data):
    count = 0
    for line in data:
        for element in line:
            if element == "*":
                count += 1
    if count != 20:
        return False
    for i in list(string.ascii_lowercase)[:10]:
        for j in range(10):
            coord = (i, j)
            if ship_size(data, coord)[0] > 4 or ship_size(data, coord)[1] > 4:
                return False
            if ship_size(data, coord)[0] > 1 and ship_size(data, coord)[1] > 1:
                return False
            if ship_size(data, coord)[1] > 1 and ship_size(data, coord)[0] > 1:
                return False
    return True
