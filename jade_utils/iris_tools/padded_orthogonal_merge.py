"""
Experimental cube merging that trys to create a single cube from a list of cubes along defined orthogonal coordinates
and uses masked arrays to fill in any 'holes' that there isn't data for in the cube list.
"""

import iris

def padded_orthogonal_merge(cube_list, orthogonal_coords):
    # TODO: should we always use the first cube as a template?
    # TODO: check that all cubes have the required orthogonal_coords as scalar coords and filter those that don't?
    cubes = _flatten(cube_list)
    missing_cubes = []
    for point in _get_missing_points_in_coord_space(cubes, orthogonal_coords):
        missing_cubes.append(_make_masked_cube_for_point(cubes[0], orthogonal_coords, point))
    cubes += missing_cubes
    return cubes.merge_cube()



def _make_masked_cube_for_point(template_cube, coord_names, point):
        c = template_cube.copy()
        constraints = {}
        for name in coord_names:
            constraints[name] = c.coord(name).points[0]
        constraint = iris.Constraint(**constraints)
        new_cube = c.extract(constraint)
        for i, coord_name in enumerate(coord_names):
            new_cube.coord(coord_name).points = (point[i],)
        lazy_data = new_cube.lazy_data()
        data = np.ma.masked_all(lazy_data.shape, dtype=lazy_data.dtype)
        np.ma.set_fill_value(data, lazy_data.fill_value)
        new_cube.data = data
        return new_cube


def _flatten(cube_list):
    flattened = []
    reject = []
    for cube in cube_list:
        for flat_cube in cube.slices(['latitude', 'longitude']): # Why lat long, should we use the orthag coords?
            flattened.append(flat_cube)
    return iris.cube.CubeList(flattened)


def _get_missing_points_in_coord_space(flat_cube_list, dims):
    # go through all cubes to find all the points in the problem space dims
    points = []
    dim_point_sets = {dim:set() for dim in dims}
    for cube in flat_cube_list:
        point = []
        for dim in dims:
            dim_value = cube.coord(dim).points[0]
            point.append(dim_value)
            dim_point_sets[dim].add(dim_value)
        points.append(point)

    # Place a True value in the problem space if we have that point
    # TODO: could use dic and rev dic to speed up the problem/real space conversion
    space_map = {dim:list(dim_point_sets[dim]) for dim in dims}
    def to_prob_space(point):
        return tuple(space_map[dims[i]].index(point[i]) for i in range(len(dims)))

    def to_real_space(indexs):
        return tuple(space_map[dims[i]][indexs[i]] for i in range(len(dims)))

    problem_space = np.zeros([len(space_map[dim]) for dim in dims], dtype=bool)

    for point in points:
        problem_space[to_prob_space(point)] = True

    missing = []
    # Find all the missing points in the problem space and convert back in to cube space
    for missing_point_in_problem_space in zip(*np.where(problem_space == False)):
        missing.append(to_real_space(missing_point_in_problem_space))

    return missing
