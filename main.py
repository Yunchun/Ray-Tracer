import vec3
import ray
import hittable_list
import hittable
import sphere
from utils import clamp, rand_double, random_double, infinity
import camera
import material
import math
import bvh_node
import texture

def write_color(pixel_color: vec3, samples_per_pixel: int):
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    # Divide the color by the number of samples and gamma-correct for gamma=2.0.
    scale = 1.0 / samples_per_pixel
    r = (scale * r)** 0.5
    g = (scale * g)** 0.5
    b = (scale * b)** 0.5

    output = "{} {} {}\n".format(int(256 * clamp(r, 0.0, 0.999)), 
    int(256 * clamp(g, 0.0, 0.999)),
    int(256 * clamp(b, 0.0, 0.999)))

    return output

def hit_sphere(center: vec3, radius: float, r: ray):
    oc = vec3.sub(r.origin(), center)
    a = r.direction().sqLen()
    half_b = vec3.dot(oc, r.direction())
    c = oc.sqLen() - radius*radius
    discriminant = half_b*half_b - a*c

    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - discriminant**0.5) / a

#def ray_color(r: ray, background: vec3, world: hittable_list, depth: int):
def ray_color(r: ray, world: hittable_list, depth: int):
    if depth <= 0:
        return vec3.vec3(0.0, 0.0, 0.0)

    hit, rec = world.hit(r, 0.001, infinity)

    if hit:

        sc, scattered, attn = rec.mat_ptr.scatter(r, rec)

        if sc: 
            return vec3.mul(attn, ray_color(scattered, world, depth - 1))

        return vec3.vec3(0.0, 0.0, 0.0)
    
    unit_dir = vec3.norm(r.direction())
    t = 0.5 * (unit_dir.y() + 1.0)
    init_color = vec3.elmMul(1.0 - t, vec3.vec3(1.0, 1.0, 1.0))
    delta_color = vec3.elmMul(t, vec3.vec3(0.5, 0.7, 1.0))
    return vec3.add(init_color, delta_color)

def random_scene():
    # World
    world = hittable_list.hittable_list()

    c1 = vec3.vec3(1.0, 140.0/255.0, 0)
    c2 = vec3.vec3(0.8, 1.0, 0.8)
    checker = texture.checker_texture(c1, c2)
    mat_grd = material.lambertian(checker)
    world.add(sphere.sphere(vec3.vec3(0, -1000, 0), 1000, mat_grd))

    mat_lt = material.metal(vec3.vec3(1.0, 1.0, 1.0), 0.0)
    world.add(sphere.sphere(vec3.vec3(-1000, 0, 0), 1000, mat_lt))

    mat2 = material.metal(vec3.vec3(0.98, 0.2, 0.2), 0.2)
    world.add(sphere.sphere(vec3.vec3(1, 0.4, -1), 0.4, mat2))
    
    mat3 = material.dielectric(1.5)
    world.add(sphere.sphere(vec3.vec3(2, 0.7, -2), 0.7, mat3))


    # metal & lambertian objects
    
    spheres = hittable_list.hittable_list()
    
    for a in range(-4, 4, 1):
        for b in range(-4, 4, 1):

            choose_mat = rand_double()
            center = vec3.vec3(a + 0.9 * rand_double(),
             0.3, b + 0.9 * rand_double()) 

            if choose_mat < 0.4:
                # Diffuse
                albedo = vec3.mul(vec3.rand(), vec3.rand())
                sphere_mat = material.lambertian(albedo)
                spheres.add(sphere.sphere(center, 0.3, sphere_mat))
            elif choose_mat < 0.7:
                # Metal
                albedo = vec3.random(0.3, 0.6)
                fuzz = random_double(0, 0.3)
                sphere_mat = material.metal(albedo, fuzz)
                spheres.add(sphere.sphere(center, 0.2, sphere_mat))
            else:
                # Glass
                sphere_mat = material.dielectric(1.6)
                spheres.add(sphere.sphere(center, 0.2, sphere_mat))
    
    world.add(bvh_node.bvh_node(spheres.objects, 0, 1))
    """
    for i in range(30):
        z = random_double(-7, 12)
        while -1.3 < z and z < 1.3:
            z = random_double(-7, 12)
        center = vec3.vec3(random_double(-0.3, 5), 0.1, z)
        choose_mat = rand_double()
        
        if choose_mat < 0.6:
            # Diffuse
            albedo = vec3.mul(vec3.rand(), vec3.rand())
            sphere_mat = material.lambertian(albedo)
            spheres.add(sphere.sphere(center, 0.2, sphere_mat))

        elif choose_mat < 0.8:
            # Metal
            albedo = vec3.random(0.3, 0.6)
            fuzz = random_double(0, 0.3)
            sphere_mat = material.metal(albedo, fuzz)
            spheres.add(sphere.sphere(center, 0.3, sphere_mat))

        else:
            # Glass
            sphere_mat = material.dielectric(1.3)
            spheres.add(sphere.sphere(center, 0.15, sphere_mat))


    world.add(bvh_node.bvh_node(spheres.objects, 0, 1))
    
    mat1 = material.dielectric(2.0)
    world.add(sphere.sphere(vec3.vec3(0, 1, 0), 1, mat1))

    mat2 = material.lambertian(vec3.vec3(0.3, 0.3, 0.3))
    world.add(sphere.sphere(vec3.vec3(-4, 1, 0), 1, mat2))


    mat3 = material.metal(vec3.vec3(0.82, 0.34, 0.9), 0)
    world.add(sphere.sphere(vec3.vec3(4, 1, 0), 1, mat3))
    """
    return world


def main():
    # Image
    aspect_ratio = 4.0 / 3.0
    image_width = 700
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 50

    # World
    world = random_scene()

    # Camera
    lookfrom = vec3.vec3(5, 2, 10)
    lookat = vec3.vec3(0, 0, -1)
    vup = vec3.vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1
    background = vec3.vec3(0.7, 0.8, 1.0)
    cam = camera.camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

    print('P3\n' + str(image_width) + ' ' + str(image_height) + '\n255\n')

    for j in range(image_height - 1, -1, -1):
        for i in range(0, image_width, 1):
            pixel_color = vec3.vec3(0.0, 0.0, 0.0)
            for s in range(0, samples_per_pixel, 1):
                u = (i + rand_double()) / (image_width - 1)
                v = (j + rand_double()) / (image_height-1)
                r = cam.get_ray(u, v)
                pixel_color.add(ray_color(r, world, max_depth))
                
            print(write_color(pixel_color, samples_per_pixel))


main()