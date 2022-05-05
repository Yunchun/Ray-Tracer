import vec3
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import math

class texture(ABC):
    @abstractmethod
    def color_value(self, p: vec3):
        pass

class solid_color:
    def __init__(r: float, g: float, b: float):
        self.color_value = vec3.vec3(r, g, b)
    
    def color_value(self, p: vec3):
        return self.color_value

class checker_texture:
    def __init__(self, _even: vec3, _odd: vec3):
        self.odd = _odd
        self.even = _even
    
    def color_value(self, p: vec3):
        sines = math.sin(p.x() * 10)*math.sin(p.y() * 10)*math.sin(p.z() * 10)
        if sines < 0:
            return self.odd
        else:
            return self.even
