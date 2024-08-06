

class Box:
    # Box (or block) with initial attributes: initial position, width, initial velocity, mass
    def __init__(self,x_0,w,v_0,m):
        self.x_pos = x_0
        self.width = w
        self.v = v_0
        self.m = m

    def update_pos(self,t):
    # updates the position for a given time
        self.x_pos = self.x_pos + self.v*t

    # def edges(self):
    #     l_edge = self.x - self.width/2
    #     r_edge = self.x + self.width/2

class Wall:
    # Creates a wall at x_pos. 
    def __init__(self,x_pos):
        self.x_pos = x_pos

class Simulation:
    def __init__(self,timestep):
        # Simulation steps from t=0 to t=t_stop with stepsize = timestep
        self.timestep = timestep
        self.t = 0
        self.t_stop = 5

    def setup(self):
        # Setup function to create two boxes, a wall, collision distances, and get how many digits of pi the user wants.
        r = int(input("How many digits of pi do you want: "))
        m1 = 100**(r - 1)
        self.outer_box = Box(10,1,-0.5,m1)
        self.inner_box = Box(5,1,0,1)
        self.wall = Wall(0)
        self.d_coll = self.outer_box.width/2 + self.inner_box.width/2 # Box collision distance
        self.d_wall = self.inner_box.width/2 # Inner box and wall collision distance
        self.n_collision = 0

    def run(self):
        # Right now it runs to a specified stopping time. 
        # Need to change the stopping condition. 
        while self.t < self.t_stop:
            cond1 = self.detect_wall() # Boolean condition 
            cond2 = self.detect_collision() #Boolean condition
            if cond1: # Does inner box hit wall
                self.inner_box.v = self.elastic_wall(self.inner_box.v)
                self.n_collision += 1
            if cond1 and cond2 # does inner box hit wall and outer box hit inner box
                self.outer_box.x_pos = self.inner_box.x_pos+self.d_coll
                self.outer_box.v = -1*self.outer_box.v
            elif cond2: # does outer box hit inner box 
                self.outer_box.v,self.inner_box.v = self.elastic_collision(self.outer_box.m,self.inner_box.m,self.outer_box.v,self.inner_box.v)
                self.n_collision += 1
            else: # no collisions
                self.update()
            self.stepforward()
        print(f"Mass 1: {self.outer_box.m}")
        print(f"Mass 2: {self.inner_box.m}")
        print(self.n_collision)

    def detect_collision(self):
        # If the distance between two boxes is less than the sum of their half-widths a collision occurs. 
        # The position of the outer box is set to be exactly the collision distance away from the inner box. 
        x_out = self.outer_box.x_pos+self.outer_box.v*(self.t+self.timestep)
        x_in = self.inner_box.x_pos+self.inner_box.v*(self.t+self.timestep)
        d = x_out-x_in
        if d < self.d_coll:
            self.outer_box.x_pos = self.inner_box.x_pos+self.d_coll
            return True
        else:
            return False

    def detect_wall(self):
        # If the distance between the inner boxe is less than its half-width a collision occurs with the wall. 
        # The position of the inner box is set to be its half-width. 
        x_in = self.inner_box.x_pos+self.inner_box.v*(self.t+self.timestep)
        d = x_in - self.wall.x_pos
        if d < self.inner_box.width/2:
            self.inner_box.x_pos = self.inner_box.width/2
            return True
        else:
            return False

    def elastic_collision(self,m1,m2,v_1i,v_2i):
        # Perfectly elastic collision momentum and kinetic energy equations rearranged to find final velocities.
        v_1f = ((m1 - m2) / (m1 + m2)) * v_1i + (2 * m2) / (m1 + m2) * v_2i
        v_2f = ((2 * m1) / (m1 + m2)) * v_1i + (m2 - m1) / (m1 + m2) * v_2i
        return v_1f,v_2f

    def elastic_wall(self,v_1i):
        # Perfectly elastic collision with a wall of infinite mass
        v_1f = -1*v_1i
        return v_1f

    def stepforward(self):
        self.t = self.t + self.timestep

    def update(self):
        # Update the position of the boxes
        self.outer_box.update_pos(self.t)
        self.inner_box.update_pos(self.t)
        # print(f't={self.t}')
        # print(f'x={self.outer_box.x_pos}')



