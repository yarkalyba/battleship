class Ship:
    def __init__(self, length, bow, horizontal):
        self.__length = length
        self.bow = bow
        self.horizontal = horizontal
        self.__hit = [False] * length

    def shoot_at(self, cords):
        if self.horizontal:
            for i in range(self.__length):
                if (self.bow[0] + i, self.bow[1]) == cords:
                    self.__hit[i] = True
                    return True
        else:
            for i in range(self.__length):
                if (self.bow[0], self.bow[1] + i) == cords:
                    self.__hit[i] = True
                    return True
        return False


class Field:
    def __init__(self):
        self.__ships = self.generate_field()

    def shoot_at(self, cords):
        if self.__ships[cords[0]][cords[1]] == " " or self.__ships[cords[0]][cords[1]] == "*":
            self.__ships[cords[0]][cords[1]] = "*"
            return False
        else:
            self.__ships[cords[0]][cords[1]] = "×"
            return True

    def field_without_ships(self):
        import copy
        battlefield = copy.deepcopy(self.__ships)
        for row in range(len(battlefield)):
            for column in range(len(battlefield)):
                if battlefield[row][column] == "*" or battlefield[row][column] == "×":
                    pass
                else:
                    battlefield[row][column] = " "
        return self.beautiful_board(battlefield)

    def field_with_ships(self):
        import copy
        battlefield = copy.deepcopy(self.__ships)
        for row in range(len(battlefield)):
            for column in range(len(battlefield)):
                if battlefield[row][column] == "*" or battlefield[row][column] == "×" or battlefield[row][column] == ' ':
                    pass
                else:
                    battlefield[row][column] = "□"
        return self.beautiful_board(battlefield)

    def generate_field(self):
        import random
        borders = ((0, 0), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))
        field = [[" "] * 10 for i in range(10)]
        all_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        ship_borders = []
        for i in all_ships:
            horizontal = random.choice([False, True])  # false
            if not horizontal:
                while True:
                    tries = 0
                    row = random.choice(range(10 - i))
                    column = random.choice(range(10))
                    for length in range(i):
                        for p in borders:
                            if [column + p[0], row + length + p[1]] in ship_borders:
                                tries += 1
                    if tries == 0:
                        break
                ship = Ship(i, (column, row), False)
                for j in range(i):
                    field[column][row + j] = ship
                    ship_borders.append([column, row + j])
            else:
                while True:
                    tries = 0
                    row = random.choice(range(10))
                    column = random.choice(range(10 - i))
                    for length in range(i):
                        for p in borders:
                            if [column + length + p[0], row + p[1]] in ship_borders:
                                tries += 1
                    if tries == 0:
                        break
                ship = Ship(i, (column, row), True)
                for j in range(i):
                    field[column + j][row] = ship
                    ship_borders.append([column + j, row])
        return field

    @staticmethod
    def beautiful_board(field):
        import copy
        battlefield = copy.deepcopy(field)
        for i in range(len(battlefield)-1):
            battlefield[i].insert(0, str(i + 1)+" ")
        battlefield[9].insert(0, "10")

        battlefield.insert(0, ["  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
        for i in range(len(battlefield)):
            for j in range(11):
                battlefield[i][j] = battlefield[i][j]+"│"
        for i in range(1, len(battlefield)+10,2):
            battlefield.insert(i, "──┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤")
        battlefield.append("──┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘")
        return battlefield

class Player:
    def __init__(self, name):
        self.__name = name

    def read_position(self):
        import string
        a = list(input())
        a[0] = string.ascii_lowercase.index(a[0].lower())
        two_char = ""
        for i in range(1,len(a)):
            two_char = two_char + a[i]
        two_char = int(two_char)-1
        return (two_char, a[0])

    def __str__(self):
        return self.__name


class Game:
    def __init__(self, name1, name2):
        self.__field = [Field(), Field()]
        self.__players = [Player(name1), Player(name2)]
        self.__current_player = 0

    def read_position(self):
        return self.__players[self.__current_player - 1].read_position()

    def field_with_ships(self, player):
        return self.__field[player].field_with_ships()

    def field_without_ships(self, player):
        return self.__field[player].field_without_ships()

    def play(self):
        def opponent(index):
            if index == 0:
                return 1
            return 0

        print("Welcome in Battleships")
        while True:
            print("{}'s field:".format(self.__players[opponent(self.__current_player)]))
            for i in self.__field[opponent(self.__current_player)].field_without_ships():
                print("".join(i))
            print("{} make a shot:".format(self.__players[self.__current_player]))
            cords = self.read_position()

            hit = self.__field[opponent(self.__current_player)].shoot_at(cords)
            if hit:
                print("Good job, you can shoot one more time!")
                continue
            print("You missed, your opponent turn")

            print("{}'s field:".format(self.__players[self.__current_player]))
            for i in self.__field[self.__current_player].field_without_ships():
                print("".join(i))
            print("{} make a shot:".format(self.__players[opponent(self.__current_player)]))
            cords = self.read_position()

            hit = self.__field[self.__current_player].shoot_at(cords)
            if hit:
                print("Good job, you can shoot one more time!")
                continue
            print("You missed, your opponent turn")

            if self.is_winner():
                print("Congrats! {} wins!".format(self.__players[self.__current_player]))
                break

    def is_winner(self):
        for i in range(10):
            for j in range(10):
                if "□" in self.__field[self.__current_player].field_with_ships()[i][j]:
                    return False
        return True


game = Game("Arman", "Rybka")
game.play()
