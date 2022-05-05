from utils import rand_double, random_double
import numpy as np

class vec3:

    def __init__(self, e0: float, e1: float, e2: float):
        self.e = [e0, e1, e2]

    def x(self):
        return self.e[0]
    
    def y(self):
        return self.e[1]
    
    def z(self):
        return self.e[2]

    def neg(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def near_zero(self):
        # Return true if the vector is close to zero in all dimensions.
        s = 1e-8
        return ((abs(self.e[0]) < s) and (abs(self.e[1]) < s)) and (
            abs(self.e[2]) < s)

    def index(self, i: int):
        return self.e[i]

    def add(self, v):
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self.e

    def mul(self, t: float):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t

    def div(self, t: float):
        self.e[0] /= t
        self.e[1] /= t
        self.e[2] /= t 
    
    def sqLen(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]
    
    def len(self):
        return self.sqLen()**0.5
    
"""
point3 = vec3(1.0, 2.0, 3.0)
color = vec3(3.0, 4.0, 5.0)
minus = point3.flipSign()
print(point3.x(), point3.y(), point3.z())
print(color.x(), color.y(), color.z())
print(minus.x(), minus.y(), minus.z())
print(point3.index(1))
point3.add(vec3(1.0,2.0,3.0))
print(point3.x(), point3.y(), point3.z())
point3.mul(0.5)
print(point3.x(), point3.y(), point3.z())
point3.div(0.5)
print(point3.x(), point3.y(), point3.z())
print(point3.sqLen())
print(point3.len())
"""

def out(v: vec3):
    return str(v.e[0]) + ' ' + str(v.e[1]) + ' ' + str(v.e[2]) + ' '
    
def add(u: vec3, v: vec3):
    return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2])

def sub(u: vec3, v: vec3):
    return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2]) 

def mul(u: vec3, v: vec3):
    return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2]) 

def div(u: vec3, v: vec3):
    return vec3(u.e[0] / v.e[0], u.e[1] / v.e[1], u.e[2] / v.e[2]) 

def elmMul(t: float, v: vec3):
    return vec3(t * v.e[0], t * v.e[1], t * v.e[2])

def elmDiv(t: float, v: vec3):
    return vec3(v.e[0]/t, v.e[1]/t, v.e[2]/t)

def dot(u: vec3, v: vec3):
    return u.e[0]*v.e[0] + u.e[1]*v.e[1] + u.e[2]*v.e[2]

def cross(u: vec3, v: vec3):
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
            u.e[2] * v.e[0] - u.e[0] * v.e[2],
            u.e[0] * v.e[1] - u.e[1] * v.e[0])

def norm(v: vec3):
    l = v.len()
    return elmDiv(l, v)

def reflect(v: vec3, n: vec3):
    return sub(v, elmMul(2 * dot(v, n), n))

def rand():
    return vec3(rand_double(), rand_double(), rand_double())

def random(min: float, max: float):
    return vec3(random_double(min, max), random_double(min, max),
    random_double(min, max))

def random_in_unit_sphere():
    while True:
        p = random(-1, 1)
        if p.sqLen() >= 1:
            continue
        else:
            return p

def random_in_unit_disk():
    while True:
        p = vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.sqLen() >= 1:
            continue
        else:
            return p

def random_unit_vec():
    return norm(random_in_unit_sphere())

def random_in_hemisphere(normal: vec3):
    in_unit_sphere = random_in_unit_sphere()
    # In the same hemisphere as the normal
    if dot(in_unit_sphere, normal) > 0.0:
        return in_unit_sphere
    else:
        return in_unit_sphere.neg()

def refract(v: vec3, n: vec3, refract_ratio: float):
    uv = norm(v)
    dt = dot(uv, n)
    discriminant = 1.0 - refract_ratio * refract_ratio * (1 - dt**2)
    if discriminant > 0:
        refracted = sub(elmMul(refract_ratio, sub(uv, elmMul(dt, n))), elmMul(
            np.sqrt(discriminant), n))
        return True, refracted
    else:
        return False, None


"""
uv = vec3(2.0, -1.0, -1.0)
n = vec3(-1.0, 0.0, 1.0)
print(out(refract(uv, n, 1.0)))
"""
"""
print(out(point3))
new_vec3 = add(point3, color)
print(out(new_vec3))
new_vec3 = sub(point3, color)
print(out(new_vec3))
new_vec3 = mul(point3, color)
print(out(new_vec3))
new_vec3 = div(point3, color)
print(out(new_vec3))
new_vec3 = elmMul(3, color)
print(out(new_vec3))
new_vec3 = dot(point3, color)
print(new_vec3)
new_vec3 = cross(vec3(1.0,1.0,1.0), vec3(1.0,0.0,0.0))
print(out(new_vec3))
print(out(norm(vec3(1.0,1.0,1.0))))
"""