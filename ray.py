import vec3
class ray:

    def __init__(self, origin: vec3, direction: vec3):
        self.orig = origin
        self.dir = direction

    def origin(self):
        return self.orig
    
    def direction(self):
        return self.dir
    
    def at(self, t:float):
        return vec3.add(self.orig, vec3.elmMul(t, self.dir))

"""
origin = vec3.vec3(1.0, 2.0, 0.0)
direction = vec3.vec3(0.0, 1.0, 0.0)
ray1 = ray(origin, direction)
print(vec3.out(ray1.origin()))
print(vec3.out(ray1.direction()))
print(vec3.out(ray1.at(0.5)))
"""


        