import vec3
import ray
import hittable
from utils import rand_double
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import texture

class material(ABC):
    @abstractmethod
    def scatter(self, r_in: ray, rec: hittable):
        pass


class lambertian:
    
    def __init__(self, a: texture):
        self.albedo = a
    
    def scatter(self, r_in: ray, rec: hittable):
            scatter_dir = vec3.add(rec.normal, vec3.random_unit_vec())

            # Catch degenerate scatter direction
            if scatter_dir.near_zero():
                scatter_dir = vec3.vec3(rec.normal.x(), rec3.normal.y(),
                 rec3.normal.z())

            scattered = ray.ray(rec.p, scatter_dir)
            
            if isinstance(self.albedo, texture.checker_texture):
                attn = self.albedo.color_value(rec.p)
            elif isinstance(self.albedo, vec3.vec3):
                attn = vec3.vec3(self.albedo.x(), self.albedo.y(), 
                self.albedo.z())
            
            return True, scattered, attn

    def emitted(self, p: vec3):
        return vec3.vec3(0.7, 0.7, 0.7)

class metal:
    def __init__(self, a: vec3, f: float):
       self.albedo = a
       if f < 1:
           self.fuzz = f
       else:
           self.fuzz = 1
    
    def scatter(self, r_in: ray, rec: hittable):
            reflected = vec3.reflect(vec3.norm(r_in.direction()), rec.normal)
            scattered = ray.ray(rec.p, vec3.add(reflected, vec3.elmMul(self.fuzz,
              vec3.random_in_unit_sphere())))
            attn = vec3.vec3(self.albedo.x(), self.albedo.y(), 
            self.albedo.z())
            return vec3.dot(scattered.direction(), rec.normal) > 0, scattered, attn
    
    def emitted(self, p: vec3):
        return vec3.vec3(0.7, 0.7, 0.7)

class dielectric:
    def __init__(self, refract_idx: float):
        self.ir = refract_idx

    @staticmethod
    def reflectance(cosine: float, ref_idx: float):
        # Use Schlick's approximation for reflectance.
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 **= 2
        return r0 + (1 - r0) * ((1 - cosine)**5)

    def scatter(self, r_in: ray, rec: hittable):
        reflected = vec3.reflect(r_in.direction(), rec.normal)
        attn = vec3.vec3(1.0, 1.0, 1.0)
        if (vec3.dot(r_in.direction(), rec.normal) > 0):
            outward_normal = rec.normal.neg()
            refract_ratio = self.ir
            cosine = self.ir * vec3.dot(r_in.direction(), rec.normal) / r_in.direction().len()
        else:
            outward_normal = rec.normal
            refract_ratio = 1.0 / self.ir
            cosine = -vec3.dot(r_in.direction(), rec.normal) / r_in.direction().len()
        ref, refracted = vec3.refract(r_in.direction(), outward_normal, refract_ratio)
        if ref:
            reflect_prob = self.reflectance(cosine, self.ir)
        else:
            scattered = ray.ray(rec.p, reflected)
            reflect_prob = 1.0

        if rand_double() < reflect_prob:
            scattered = ray.ray(rec.p, reflected)
        else:
            scattered = ray.ray(rec.p, refracted)
        return True, scattered, attn
    
    def emitted(self, p: vec3):
        return vec3.vec3(0.7, 0.7, 0.7)

class diffuse_light:
    def __init__(self, a: texture):
        self.emit = a
    
    def scatter(self, r_in: ray, rec: hittable):
        return False, None, None

    
    
    #def emitted(self, p: vec3):
     #   return self.emit.color_value(p)
    

