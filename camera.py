import vec3
import ray 
from utils import degrees_to_radians
import math
class camera:

    def __init__(self, lookfrom: vec3, lookat: vec3, vup: vec3, 
    vfov: float, aspect_ratio: float, aperture: float, focus_dist: float):

        theta = degrees_to_radians(vfov)
        h = math.tan(theta/2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self.w = vec3.norm(vec3.sub(lookfrom, lookat))
        self.u = vec3.norm(vec3.cross(vup, self.w))
        self.v = vec3.cross(self.w, self.u)

        self.origin = vec3.vec3(lookfrom.x(), lookfrom.y(), lookfrom.z())
        self.horizontal = vec3.elmMul(focus_dist * viewport_width, self.u)
        self.vertical = vec3.elmMul(focus_dist * viewport_height, self.v)
        self.lower_left_corner = vec3.sub(vec3.sub(vec3.sub(self.origin,
        vec3.elmDiv(2.0, self.horizontal)), vec3.elmDiv(2.0, self.vertical)),
         vec3.elmMul(focus_dist, self.w))
        self.lens_radius = aperture / 2
        

    def get_ray(self, s: float, t: float):
        rd = vec3.elmMul(self.lens_radius, vec3.random_in_unit_disk())
        offset = vec3.add(vec3.elmMul(rd.x(), self.u), vec3.elmMul(rd.y(), self.v))
        direction = vec3.sub(vec3.sub(vec3.add(vec3.add(self.lower_left_corner,
             vec3.elmMul(s, self.horizontal)), vec3.elmMul(t, self.vertical)), 
             self.origin), offset)
        r = ray.ray(vec3.add(self.origin, offset), direction)

        return r
