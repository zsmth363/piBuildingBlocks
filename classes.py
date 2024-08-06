

class Box:
    def __init__(self,x_0,w,v_0,m):
        self.x_pos = x_0
        self.width = w
        self.v = v_0
        self.m = m

    def update_pos(self,t):
        self.x_pos = self.x_pos + self.v*t

    # def edges(self):
    #     l_edge = self.x - self.width/2
    #     r_edge = self.x + self.width/2

class Wall:
    def __init__(self,x_pos):
        self.x_pos = x_pos

class Simulation:
    def __init__(self,timestep):
        self.timestep = timestep
        self.t = 0
        self.t_stop = 5

    # need a method that checks for collisions (both single and double)

    def setup(self):
        r = int(input("How many digits of pi do you want: "))
        m1 = 100**(r - 1)
        self.outer_box = Box(10,1,-0.5,m1)
        self.inner_box = Box(5,1,0,1)
        self.wall = Wall(0)
        self.d_coll = self.outer_box.width/2 + self.inner_box.width/2
        self.d_wall = self.inner_box.width/2
        self.n_collision = 0

    def run(self):
        while self.t < self.t_stop:
            cond1 = self.detect_wall()
            cond2 = self.detect_collision()
            if cond1:
                self.inner_box.v = self.elastic_wall(self.inner_box.v)
                self.n_collision += 1
            if cond1 and cond2:
                self.outer_box.x_pos = self.inner_box.x_pos+self.d_coll
                self.outer_box.v = -1*self.outer_box.v
            elif cond2:
                self.outer_box.v,self.inner_box.v = self.elastic_collision(self.outer_box.m,self.inner_box.m,self.outer_box.v,self.inner_box.v)
                self.n_collision += 1
            else:
                self.update()
            self.stepforward()
        print(f"Mass 1: {self.outer_box.m}")
        print(f"Mass 2: {self.inner_box.m}")
        print(self.n_collision)

    def detect_collision(self):
        # if any two edges occupy the same position.
        x_out = self.outer_box.x_pos+self.outer_box.v*(self.t+self.timestep)
        x_in = self.inner_box.x_pos+self.inner_box.v*(self.t+self.timestep)
        d = x_out-x_in
        if d < self.d_coll:
            self.outer_box.x_pos = self.inner_box.x_pos+self.d_coll
            return True
        else:
            return False

    def detect_wall(self):
        x_in = self.inner_box.x_pos+self.inner_box.v*(self.t+self.timestep)
        d = x_in - self.wall.x_pos
        if d < self.inner_box.width/2:
            self.inner_box.x_pos = self.inner_box.width/2
            return True
        else:
            return False

    def elastic_collision(self,m1,m2,v_1i,v_2i):
        v_1f = ((m1 - m2) / (m1 + m2)) * v_1i + (2 * m2) / (m1 + m2) * v_2i
        v_2f = ((2 * m1) / (m1 + m2)) * v_1i + (m2 - m1) / (m1 + m2) * v_2i
        return v_1f,v_2f

    def elastic_wall(self,v_1i):
        v_1f = -1*v_1i
        return v_1f

    def stepforward(self):
        self.t = self.t + self.timestep

    def update(self):
        self.outer_box.update_pos(self.t)
        self.inner_box.update_pos(self.t)
        # print(f't={self.t}')
        # print(f'x={self.outer_box.x_pos}')



