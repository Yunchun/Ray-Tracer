import hittable
import sphere
import ray
import vec3
import aabb

class hittable_list:

    def __init__(self):
        self.objects = []
    
    def add(self, obj: sphere):
        self.objects.append(obj)

    
    def clear(self):
        self.objects = []
    
    def hit(self, r: ray, t_min: float, t_max: float):
        hit_anything = False
        closest_so_far = t_max
        rec = None

        for obj in self.objects:
            hit, temp_rec = obj.hit(r, t_min, closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything, rec
    
    def sort(self, key:callable):
        self.objects.sort(key=key)

    def bounding_box(time0: float, time1: float):
        if len(self.objects) == 0:
            return False, None

        output_box = None
        first_box = True

        for obj in self.objects:
            temp_box = obj.bounding_box(time0, time1)
            if temp_box is not None:
                return False, None
            if first_box:
                output_box = temp_box
            else:
                output_box = aabb.surrounding_box(output_box, temp_box)
            first_box = False
        
        return output_box