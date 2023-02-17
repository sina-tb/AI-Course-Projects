
import turtle
import math
import random
from time import sleep
from sys import argv
import time

class Node:
    score = int
    children = []
    next_step = []
    r = []
    b = []
    available = []

    def __init__(self,score,children,next_step,r,b,available):
        self.score = score
        self.children = children
        self.next_step = next_step
        self.r = r
        self.b = b
        self.available = available

class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False
    node_count = 0

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def upgrade_node_count(self,count):
        self.node_count = count

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)

    def generate_minmax_tree(self, depth,player_turn,node):
        if depth == 0:
            return
        for each_child in range((len(node.available))):
            my_copy = node.available.copy()
            red_copy = node.r.copy()
            blue_copy = node.b.copy()
            selection = my_copy.pop(each_child)
            if selection[1] < selection[0]:
                selection = (selection[1], selection[0])
            if player_turn == 'red':
                red_copy.append(selection)
                next_player = 'blue'
            else:
                blue_copy.append(selection)
                next_player = 'red'
            score = self.evaluate(red_copy,blue_copy)
            new_node = Node(score, [], selection, red_copy, blue_copy, my_copy)
            node.children.append(new_node)
            self.generate_minmax_tree(depth-1, next_player, new_node)

    def evaluate(self,red,blue):

       score = self.gameover(red,blue)
       if score == 'blue':
           return -1
       if score == 'red':
           return 1
       if score == 0:
           return 0
    # TODO
    def minimax(self, depth, player_turn, node, answer, count):
        count[0] += 1
        if depth == 0:
            return node.score
        if player_turn == 'red':
            max_score = -2
            for each_child in range(len(node.children)):
                max_score = max(max_score,self.minimax(depth - 1, 'blue', node.children[each_child], answer,count))
            for each_child in range(len(node.children)):
                if max_score == node.children[each_child].score:
                    answer.insert(0,node.children[each_child].next_step)
            return max_score
        else:
            min_score = 2
            for each_child in range(len(node.children)):
                min_score = min(min_score,self.minimax(depth-1, 'red',node.children[each_child], answer,count))
            for each_child in range(len(node.children)):
                if min_score == node.children[each_child].score:
                    answer.insert(0, node.children[each_child].next_step)
            return min_score

    def enemy(self):
        return random.choice(self.available_moves)

    def swap_turn(self, turn):
        if turn == 'red':
            return 'blue'
        else:
            return 'red'

    def play(self):
        self.initialize()
        count = []
        count.append(0)
        while True:
            if self.turn == 'red':
                hey = []
                hey.append(0)
                node = Node(0, [], [], self.red, self.blue, self.available_moves)
                self.generate_minmax_tree(self.minimax_depth,'red',node)
                answer = []
                self.minimax(self.minimax_depth,self.turn, node, answer,count)
                selection = answer[0]
                answer.clear()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self.swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                self.upgrade_node_count(count[0])
                return r

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__ == "__main__":
    depth =int(argv[1])
    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))

    results = {"red": 0, "blue": 0}
    for i in range(1):
        start = time.time()
        results[game.play()] += 1
        end = time.time()
        print("For Depth ",depth)
        print("Total Node Count : ", game.node_count)
        print("The Execution Time : ",end-start,"sec")
    print(results)

