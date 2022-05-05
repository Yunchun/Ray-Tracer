import hittable
import hittable_list
from utils import random_int
import ray
import vec3
import aabb

class bvh_node:
    def __init__(self, scr_objects: hittable_list, time0: float, time1: float):
        # Create a modifiable array of the source scene objects
        self.obj_lst = scr_objects
        self.left = None
        self.right = None
        self.time0 = time0
        self.time1 = time1
        self.box = None
        
        #objects = scr_objects
        axis = random_int(0, 2)
        
        object_span = len(self.obj_lst)
        if object_span == 1:
            self.left = self.obj_lst[0]
            self.right = self.obj_lst[0]

        elif object_span == 2:
            if self.box_compare(scr_objects[0], scr_objects[1], axis):
                self.left = scr_objects[0]
                self.right = scr_objects[1]
            else:
                self.left = scr_objects[1]
                self.right = scr_objects[0]

        else:
            self.obj_lst.sort(key=lambda x: x.bounding_box(time0, time1).getMin().e[axis])
            mid = object_span//2
            self.left = bvh_node(self.obj_lst[:mid], time0, time1)
            self.right = bvh_node(self.obj_lst[mid:], time0, time1)
        #print('left',self.left)
        #print('right', self.right)

        box_lt = self.left.bounding_box(time0, time1)
        box_rt = self.right.bounding_box(time0, time1)

        #print(box_lt is None)
        #print(box_rt is None)

        if box_lt is None or box_rt is None:
            return

        #print('box_lt', box_lt)
        #print('box_rt', box_rt)
        
        self.box = aabb.surrounding_box(self.left.bounding_box(time0, time1), 
        self.right.bounding_box(time0, time1))
        

    def hit(self, r: ray, t_min: float, t_max: float):
        if not self.box.hit(r, t_min, t_max):
            return False, None
        hit_lt, rec_lt = self.left.hit(r, t_min, t_max)
        if hit_lt:
            hit_rt, rec_rt = self.right.hit(r, t_min, rec_lt.t)
        else:
            hit_rt, rec_rt = self.right.hit(r, t_min, t_max)
        
        if hit_rt:
            return True, rec_rt
        if hit_lt:
            return True, rec_lt
        return False, None

    def bounding_box(self, time0: float, time1: float):
        output_box = self.box
        #print('box',self.box)
        return output_box
    
    def box_compare(self, a: hittable, b: hittable, axis: int):
        box_a = a.bounding_box(0, 0)
        box_b = b.bounding_box(0, 0)
        
        if box_a is None or box_b is None:
            return
        
        return box_a.getMin().e[axis] < box_b.getMin().e[axis]