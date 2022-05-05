import vec3
import ray

class aabb:
    def __init__(self, a: vec3, b: vec3):
        self.min = a
        self.max = b

    def getMin(self):
        return self.min
    
    def getMax(self):
        return self.max
        

    def hit(self, r: ray, t_min: float, t_max: float):
        for a in range(0, 3, 1):
            invD = 1.0 / r.direction().e[a]

            t0 = (self.min.e[a] - r.origin().e[a]) * invD
            t1 = (self.max.e[a] - r.origin().e[a]) * invD

            if (invD < 0.0):
                t0, t1 = t1, t0

            t_min = max(t0, t_min)
            t_max = min(t1, t_max)
            if t_max <= t_min:
                return False
        return True

def surrounding_box(box0: aabb, box1: aabb):
    small = vec3.vec3(
            min(box0.min.x(), box1.min.x()),
            min(box0.min.y(), box1.min.y()),
            min(box0.min.z(), box1.min.z()))
    
    big = vec3.vec3(
            max(box0.max.x(), box1.max.x()),
            max(box0.max.y(), box1.max.y()),
            max(box0.max.z(), box1.max.z()))
    
    return aabb(small, big)
    