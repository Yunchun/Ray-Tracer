import ray
import vec3
import material
from abc import ABC, abstractmethod
from dataclasses import dataclass
import aabb
import typing

if typing.TYPE_CHECKING:
    import material 

class hit_record:
    #def __init__(self, point: vec3, t: float, mat_ptr: material):
    def __init__(self, point: vec3, t: float, mat_ptr: material, u: float, v: float):
        self.p = point
        self.t = t
        self.mat_ptr = mat_ptr
        self.normal = vec3.vec3(0.0, 0.0, 0.0)
        self.front_face = False
        self.u = u
        self.v = v

    def set_face_normal(self, r: ray, outward_normal: vec3):
        front_face = vec3.dot(r.direction(), outward_normal) 
        self.front_face = front_face < 0 
        if front_face:
            self.normal = vec3.vec3(outward_normal.x(), 
            outward_normal.y(), outward_normal.z())
        else:
            self.normal = outward_normal.flipSign()

class hittable(ABC):
    @abstractmethod
    def hit(self, r: ray, t_min: float, t_max: float):
        pass

    @abstractmethod
    def bounding_box(time0: float, time1: float):
        pass

