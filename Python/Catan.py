from graphics import *
import math


colors = ["black", "red", "blue", "green", "orange", "darkblue", "yellow"]

WIN_SIZE = 800
# WIN_SIZE = 1100


def main():

    win_center = Point(WIN_SIZE//2, WIN_SIZE//2)
    # hex_size = 40
    hex_size = 80
    # hex_size = 120
    # hex_size_short = hex_size * math.sqrt(3) / 2

    scale = Line(Point(WIN_SIZE//2-hex_size/2, 40), Point(WIN_SIZE//2+hex_size/2, 40))
    scale.setWidth(2)
    scale.setOutline("red")
    scale_text = Text(Point(WIN_SIZE//2, 46), "scale")
    scale_text.setTextColor("red")

    done = Circle(Point(20, 20), 15)
    done.setOutline("red")

    board = Board()
    board.place(win_center, hex_size)
    print()
    # print(board)

    win = GraphWin("prototype", WIN_SIZE, WIN_SIZE, autoflush=False)
    done.draw(win)
    scale.draw(win)
    scale_text.draw(win)
    board.draw(win)
    ln = Line(win_center, jump_hex(win_center, hex_size, 1, 1))
    ln.setOutline("purple")
    ln.setWidth(2)
    ln.draw(win)
    win.update()
    win.autoflush = True

    click = win.getMouse()
    while not in_shape(done, click):
        board.get_vertex_click(click, win)
        # board.get_hex_click(click)
        click = win.getMouse()

    win.close()


class Board:
    def __init__(self, rings=2):
        # TODO remove extra hexes when above rings=2
        if rings < 2:
            print("ERROR: Board size too small!")
            return
        rings *= 2
        self.rings = rings * 2

        print('\n')  # DEBUG

        vertices = [[None for i in range(rings*2+1)] for j in range(rings*2+1)]
        num = 0
        for q in range(-rings, rings+1):
            for r in range(max(-rings, -q-rings), min(rings, -q+rings)+1):
                # print("placing V {:2} in {:2} {:2}".format(num, q, r), sep="")  # DEBUG
                if vertices[q][r] is not None:
                    print("DUPLICATE")  # DEBUG
                vertices[q][r] = Vertex(q, r)
                if abs(q-r) % 3 == 0:  # if |q-r| is a multiple of 3
                    hx_q, hx_r = q, r  # CONVERT THIS PROPERLY if want to use separate Hex array
                    # print("hex {:2} at {:2}, {:2}  ->  {:2}, {:2}".format(num, q, r, hx_q, hx_r))  # DEBUG
                    vertices[q][r] = Hex(q, r)

                    num += 1
        rings //= 2
        extra_vertices = [[rings, rings+1], [-rings, 2*rings+1], [-rings-1, 2*rings+1]]
        extra_vertices += [[pair[1], pair[0]] for pair in extra_vertices]
        extra_vertices += [[-qr for qr in pair] for pair in extra_vertices]
        for pair in extra_vertices:
            vertices[pair[0]][pair[1]] = Vertex(pair[0], pair[1])
        self.vertices = vertices
        print("\n")  # DEBUG

    def place(self, center, hex_size):
        self.hex_size = hex_size
        self.center = center
        self.hex_size_short = hex_size * math.sqrt(3) / 2
        # self.vertex_size = (hex_size-hex_size_short)*2 # 3

        for v_row in self.vertices:  # TODO use algorithm as in place()
            for v in v_row:
                if v is not None:
                    v.place(self.center, self.hex_size)

    def move(self, win, center):
        self.center = center
        self.undraw()
        self.place(center, self.hex_size)
        self.draw(win)

    def resize(self, win, hex_size):
        self.hex_size = hex_size
        self.undraw()
        self.place(self.center, hex_size)
        self.draw(win)

    def draw(self, win):  # TODO place() algorithm
        for v_row in self.vertices:
            for v in v_row:
                if v is not None:
                    v.draw(win)

    def undraw(self):  # TODO place() algorithm
        for v_row in self.vertices:
            for v in v_row:
                if v is not None:
                    v.undraw()

    def get_vertex_click(self, click, win):
        # TODO grid bounds check
        poly_size = self.hex_size * math.sqrt(3) / 3
        where = pixel_to_hex(self.center, poly_size, click.x, click.y)
        q, r = where.x, where.y
        # if not ((-self.rings <= q <= self.rings) and (-self.rings <= r <= self.rings)):
        #     print("out of grid")
        #     return

        line = Line(self.center, jump_hex(self.center, self.hex_size, q, r))
        line.setOutline("green")
        line.setWidth(3)
        line.draw(win)
        time.sleep(.2)
        line.undraw()
        if self.vertices[q][r] is not None:
            self.vertices[q][r].setColor("Green")

    def __str__(self):  # TODO use place() algo
        prt = ""
        for q in range(-len(self.vertices)//2+1, len(self.vertices)//2+1):
            for r in range(-len(self.vertices[q])//2+1, len(self.vertices[q])//2+1):
                if self.vertices[q][r] is not None:
                    prt += self.vertices[q][r].__str__() + " "
                else:
                    prt += "   ..   "
            prt += '\n'
        return prt


class Hex:
    def __init__(self, q, r, resource=None):
        self.resource = resource
        self.q, self.r = q, r
        self.text = str(q) + ", " + str(r)
        self.center = None

    def __str__(self):
        return "[{:2},{:2}]".format(self.q, self.r)

    def place(self, grid_center, size):
        self.size = size
        self.size_short = size * math.sqrt(3) / 2
        self.vertex_size = size//4
        self.vertex_size_short = self.vertex_size * math.sqrt(3) / 2
        poly_size = size * math.sqrt(3)/ 3

        self.center = vertex_to_pixel(grid_center, self.size, self.q, self.r)
        self.poly = Polygon(jump_linear(self.center, 0, self.size),  # size
                            jump_linear(self.center, 60, self.size),
                            jump_linear(self.center, 120, self.size),
                            jump_linear(self.center, 180, self.size),
                            jump_linear(self.center, 240, self.size),
                            jump_linear(self.center, 300, self.size))
        self.vpoly = Polygon(jump_linear(self.center, 30, poly_size),  # vertex_size
                             jump_linear(self.center, 90, poly_size),
                             jump_linear(self.center, 150, poly_size),
                             jump_linear(self.center, 210, poly_size),
                             jump_linear(self.center, 270, poly_size),
                             jump_linear(self.center, 330, poly_size))

        self.cir_center = Circle(self.center, 3)
        self.txt = Text(self.center, self.text)
        self.txt.setSize(int(max(min(self.vertex_size, 32), 5)))

    def draw(self, win):
        if self.center is not None:
            self.poly.draw(win)
            self.vpoly.draw(win)
            self.txt.draw(win)

    def undraw(self):
        if self.center is not None:
            self.poly.undraw()
            self.txt.undraw()

    def is_click_in(self, point):
        x, y = point.getX(), point.getY()
        cx, cy = self.center.getX(), self.center.getY()
        # if radius < distance
        if self.size_short**2 > (cx-x)**2 + (cy-y)**2:
            return True
        return False

    def setColor(self, color="black"):
        if self.center is not None:
            self.vpoly.setOutline(color)
            self.txt.setTextColor(color)

    def setText(self, text):
        self.text = text
        self.txt.setText(text)


class Vertex:
    def __init__(self, q, r):
        self.q, self.r = q, r
        self.text = str(q) + ", " + str(r)
        self.directions = [ (+1,  0), (+1, -1), ( 0, -1),
                            (-1,  0), (-1, +1), ( 0, +1)]

    def __str__(self):
        return "({:2},{:2})".format(self.q, self.r)

    def place(self, grid_center, size):
        self.size = size
        self.size_short = size * math.sqrt(3) / 2
        self.vertex_size = size//4
        self.vertex_size_short = self.vertex_size * math.sqrt(3) / 2
        poly_size = size * math.sqrt(3)/ 3

        # self.center = vertex_to_pixel(grid_center, self.size_short*2//3, self.q, self.r)
        self.center = vertex_to_pixel(grid_center, self.size, self.q, self.r)
        # print(str(self) + ", distance = {:3}".format(distance(grid_center, self.center)))  # DEBUG
        self.poly = Polygon(jump_linear(self.center, 30, self.vertex_size),  # vertex_size
                            jump_linear(self.center, 90, self.vertex_size),
                            jump_linear(self.center, 150, self.vertex_size),
                            jump_linear(self.center, 210, self.vertex_size),
                            jump_linear(self.center, 270, self.vertex_size),
                            jump_linear(self.center, 330, self.vertex_size))
        self.cir_center = Circle(self.center, 3)
        self.txt = Text(self.center, self.text)
        self.txt.setSize(int(max(min(self.vertex_size//2, 32), 5)))
        
    def draw(self, win):
        self.poly.draw(win)
        # self.txt.draw(win)
        self.cir_center.draw(win)
    def undraw(self, ):
        self.poly.undraw()
        self.txt.undraw()
        # self.cir_center.undraw()

    def is_click_in(self, point):
        x, y = point.getX(), point.getY()
        cx, cy = self.center.getX(), self.center.getY()
        # if radius < distance
        if self.vertex_size_short**2 > (cx-x)**2 + (cy-y)**2:
            return True
        return False
    def setColor(self, color="black"):
        self.poly.setOutline(color)
    def setText(self, text):
        self.text = text
        self.txt.setText(text)

    def neighbor(self, dir=0):
        return Point(self.q + self.directions[dir][0],
                     self.r + self.directions[dir][1])


def in_shape(cir, point):
    x, y = point.getX(), point.getY()
    cx, cy = cir.getCenter().getX(), cir.getCenter().getY()
    # if radius < distance
    if cir.getRadius()**2 > (cx-x)**2 + (cy-y)**2:
        return True
    return False


def jump_linear(point, angle, distance):
    # Calculates cartesian coordinates of destination,
    # given origin, angle to travel, and distance to travel
    x, y = point.getX(), point.getY()
    x += distance * math.cos(math.radians(angle))
    y -= distance * math.sin(math.radians(angle))
    return Point(x, y)


def jump_hex(point, size, q, r):
    # Calculates cartesian coordinates of destination,
    # given cartesian origin coordinates and a hexagonal travel vector
    x, y = point.getX(), point.getY()
    qr_x = (r * size) + (q * size * 1/2)  # q * sin(30)
    qr_y = q * size * math.sqrt(3)/2  # q * cos(30)
    return Point(x + qr_x, y + qr_y)


def vertex_to_pixel(center, size, q, r):
    x = size * (r + q/2)
    y = q * size * math.sqrt(3) / 2
    return Point(x + center.x, y + center.y)


def pixel_to_hex(center, size, x, y):
    x -= center.x
    y -= center.y

    q_ = y * 2/3 / size
    r_ = (x * math.sqrt(3)/3 - y / 3) / size

    q, r = hex_round(q_, r_)
    print("({:.03},{:.03}) -> ({:2},{:2})".format(q_, r_, q, r))  # DEBUG
    return Point(q, r)


def hex_round(q, r):
    cube_x, cube_y, cube_z = hex_to_cube(q, r)
    round_x, round_y, round_z = cube_round(cube_x, cube_y, cube_z)
    return cube_to_hex(round_x, round_y, round_z)


def cube_to_hex(x, y, z):  # axial
    r = x
    q = z
    return (q, r)


def hex_to_cube(q, r):  # axial
    x = r
    z = q
    y = -x-z
    return (x, y, z)


def cube_round(x, y, z):
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return (rx, ry, rz)


# sorcery of some sort (deep magic)
# doesn't work: doesn't use same axes for q, r
def point_to_hex(center, size, x, y):
    x -= center.x
    y -= center.y

    x /= size * math.sqrt(3)
    y /= size * math.sqrt(3)

    temp = math.floor(x + math.sqrt(3) * y + 1)
    q = math.floor((math.floor(2*x+1) + temp) / 3)
    r = math.floor((temp + math.floor(-x + math.sqrt(3) * y + 1))/3)
    return Point(q, r)


main()
