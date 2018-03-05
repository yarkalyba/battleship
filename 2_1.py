import string


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


print(ship_size(data, ("E", 1)))


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

