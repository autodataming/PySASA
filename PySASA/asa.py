#!python3
# encoding: utf-8

import math
from . import v3
from . import pdbatoms

def calculate_asa(atoms, probe, n_sphere_point):
    sphere_points = generate_sphere_points(n_sphere_point)
    const = 4.0 * math.pi / len(sphere_points)
    areas = []
    result=0
    for i, atom_i in enumerate(atoms):      
        neighbor_indices = find_neighbor_indices(atoms, probe, i)
        n_neighbor = len(neighbor_indices)
        j_closest_neighbor = 0
        radius = probe + atom_i.radius
        
        n_accessible_point = 0
        for point in sphere_points:
            is_accessible = True
            test_point = v3.scale(point, radius) + atom_i.pos
            cycled_indices = list(range(j_closest_neighbor, n_neighbor))
            cycled_indices.extend(range(j_closest_neighbor))
            
            for j in cycled_indices:
                atom_j = atoms[neighbor_indices[j]]
                #溶剂质心到原子j的距离r，溶剂质心接触表面
                r = atom_j.radius + probe
                diff = v3.distance(atom_j.pos, test_point)
                #j的溶剂范围，覆盖了点
                if diff*diff < r*r:
                    j_closest_neighbor = j
                    is_accessible = False
                    break
            if is_accessible:
                n_accessible_point += 1
        
        area = const*n_accessible_point*radius*radius 
        result+=area
        areas.append(area)
    return result

 #   return areas



def find_neighbor_indices(atoms, probe, k):
    """
    Returns list of indices of atoms within probe distance to atom k. 
    """
    neighbor_indices = []
    atom_k = atoms[k]
    radius = atom_k.radius + probe + probe
    indices=[]
    indices =list( range(k))
    indices.extend(range(k+1, len(atoms)))
    for i in indices:
        atom_i = atoms[i]
        dist = v3.distance(atom_k.pos, atom_i.pos)
        if dist < radius + atom_i.radius:
            neighbor_indices.append(i)
    return neighbor_indices



#the radius of the sphere is 1 
def generate_sphere_points(n):
   """
   Returns list of coordinates on a sphere using the Golden-
   Section Spiral algorithm.
   """
   points = []
   inc = math.pi * (3 - math.sqrt(5))
   offset = 2 / float(n)
   for k in range(int(n)):
      y = k * offset - 1 + (offset / 2)
      r = math.sqrt(1 - y*y)
      phi = k * inc
      points.append(v3.vector(math.cos(phi)*r, y, math.sin(phi)*r))
   return points

    