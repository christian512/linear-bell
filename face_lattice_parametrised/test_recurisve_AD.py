from linearbell.utils import get_deterministic_behaviors, get_configs, get_parametrisation_configs, parametrise_behavior
import numpy as np
from polytope import ParamPolytope

inputs = range(3)
outputs = range(2)
configs = get_configs(inputs, inputs, outputs, outputs)
configs_param = get_parametrisation_configs(inputs, inputs, outputs, outputs)

# dict to store all polytopes
all_polys = {}

# Generate vertices and it's permutations for the bell polytope
vertices = get_deterministic_behaviors(inputs, inputs, outputs)
vertices_param = np.array(
    [parametrise_behavior(p, configs, configs_param, inputs, inputs, outputs, outputs) for p in vertices])
permutations_vertices = np.loadtxt('../data/relabels_dets/{}{}{}{}.gz'.format(3, 3, 2, 2)).astype(int)

# Generate Bell polytope
bell_polytope = ParamPolytope(vertices_param, permutations_vertices)


def get_all_face_classes(polytope, level=0):
    """Function that returns all classes of faces for a polytope"""
    # if max recursion depth is reached, use Double Description to get all classes
    if level > 1:
        return polytope.get_all_classes()

    # get a single face
    face = polytope.get_single_face()
    # generate classes
    classes = [face]
    new_classes = [face]
    while new_classes:
        c = new_classes.pop()
        for r in get_all_face_classes(c, level + 1):
            res = c.rotate(r)
            if not res.equiv_under_parent(classes):
                classes.append(res)
                new_classes.append(res)
                if level == 0:
                    print('number of classes')
    return classes

classes = get_all_face_classes(bell_polytope)
