import vec3
import hittable
import ray
import material
import numpy as np
import aabb
import math
from utils import pi

class sphere:

    def __init__(self, cen: vec3, r: float, m: material):
        self.center = cen
        self.radius = r
        self.mat_ptr = m

    
    def get_sphere_uv(self, p: vec3):
        neg_p = p.neg()
        theta = math.acos(neg_p.y())
        phi = math.atan2(neg_p.z(), p.x()) + pi
        
        u = phi / (2 * pi)
        v = theta / pi

        return u, v
    

    def hit(self, r: ray, t_min: float, t_max: float):

        oc = vec3.sub(r.origin(), self.center)
        a = r.direction().sqLen()
        half_b = vec3.dot(oc, r.direction())
        c = oc.sqLen() - self.radius**2

        discriminant = half_b**2 - a*c

        
        if discriminant < 0:
            return False, None
        sqrtd = discriminant**0.5

        # Find the nearest root that lies in the acceptable range.
        root = (-half_b - sqrtd) / a
        if (root < t_min or t_max < root):
            root = (-half_b + sqrtd) / a
            if (root < t_min or t_max < root):
                return False, None
        
        
        p = r.at(root)
        #rec = hittable.hit_record(p, root, self.mat_ptr)

        outward_normal = vec3.elmDiv(self.radius, vec3.sub(p, self.center))
        u, v = self.get_sphere_uv(outward_normal)
        rec = hittable.hit_record(p, root, self.mat_ptr, u, v)
        rec.set_face_normal(r, outward_normal)

        return True, rec

    def bounding_box(self, time0: float, time1: float):
        #rad = vec3.vec3(self.radius, self.radius, self.radius)
        output_box = aabb.aabb(
            vec3.sub(self.center, vec3.vec3(self.radius, self.radius, self.radius)),
            vec3.add(self.center, vec3.vec3(self.radius, self.radius, self.radius))
        )
        return output_box
    