import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry import Point, LineString

from itertools import tee, islice, chain


# source: https://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop
# (modified to loop over)
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([some_iterable[-1]], prevs)
    nexts = chain(islice(nexts, 1, None), [some_iterable[0]])
    return zip(prevs, items, nexts)


# my_list = [1, 2, 3, 4, 5]
# for prev, item, nxt in previous_and_next(my_list):
#     print(f"prev = {prev}, item = {item}, nxt = {nxt}")


def intersect(y, linesegment):
    """return True if infinity line defined by y intersects linesegment, and otherwise False
    linesegment: LineString
    [Point(a, b), Point(c, d)]"""
    minx, miny, maxx, maxy = linesegment.bounds
    #max_y = max(linesegment[0][1], linesegment[1][1])
    #min_y = min(linesegment[0][1], linesegment[1][1])
    if miny <= y <= maxy:
        return True
    else:
        return False


def count_intersect(y, segment_list):
    """ this method assumes that no 2 points have the same y-coord,
    i.e. if 2 segments share a point with the same y-coord, the x-coord is also the same,
    because the two segments join each other"""
    count = 0
    # test if y is the y-coord of a beginning or endpoint of any segment in the list, if so, remove those segments from the list and add
    # hits/2 to the count
    segment_list_ = [seg for seg in segment_list if seg.coords[0][1] != y and seg.coords[1][1] != y]
    # we have as half as many points on the line as segments filtered out
    points_on_line = (len(segment_list)-len(segment_list_))/2
    count += points_on_line
    for seg in segment_list_:
        if intersect(y, seg):
            count += 1
    # print(f"At sweep line y={y}:\nPoints on line: {points_on_line}\nTotal polygon crossings: {count}\n")
    return count


def crossing_left_edges(sweepline, polygon):
    """given a polygon and a sweepline, return all left edges of the polygon that the sweepline crosses"""
    polygon = make_ccw(polygon)
    edges = get_edges(polygon)
    crossing_left_edges = []
    for e in edges:
        if intersect(sweepline, e):
            # e is a left edge if first point above second point, first and second being determined by ccw polygon order
            # [1] for y coord
            assert(len(e) == 2)
            if list(e.coords)[0][1] > list(e.coords)[1][1]:
                crossing_left_edges.append(e)
    return crossing_left_edges


def get_edges(polygon):
    """
    :param polygon: a Polygon object
    :return: edges, a list of Linestrings
    """
    edges = []
    vertex_iter = polygon.exterior.coords
    # since Polygon object automatically repeats first point at the end
    # in order to close the circuit, we have to remove one of them
    i = 0
    for v_minus, v, v_plus in previous_and_next(vertex_iter):
        if i != len(vertex_iter)-1:
            e = LineString([v, v_plus])
            edges.append(e)
            i += 1
        else:
            return edges
    return edges


def is_y_monotone(polygon):
    # each polygon has "Component rings" attributes "interior" and "exterior"
    vertices = polygon.exterior.coords
    edges = get_edges(polygon)
    for v in vertices:
        v = Point(v)
        if count_intersect(v.y, edges) > 2:
            return False
    return True

# TODO: fix bug that causes monotone_poly to be "inverted"
# cause of bug: polygon ends with same point as it starts, LineString ethods assumes this makes it not ccw
def make_ccw(polygon):
    """test if poylgon is ccw, if not, return ccw copy of polygon"""
    linear_ring = LinearRing(polygon.exterior.coords)
    if linear_ring.is_ccw:
        print(f"{polygon} is already ccw")
        return polygon
    else:
        print(f"{polygon} was made ccw")
        return Polygon(list(linear_ring.coords)[::-1])

def y_monotonize(polygon):
    pass


# patch = Point(0.0, 0.0).buffer(10.0)
# print(patch.area)

poly = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
poly = make_ccw(poly)
print(poly)


monotone_poly = Polygon([(0, 2), (1.5, 6), (3, 4), (1.5, 0), (1, 1)])
poly = make_ccw(monotone_poly)
print(monotone_poly)


myPoint = Point(1, 2)

#my_edges = get_edges(monotone_poly)
# plt.plot()
# plt.savefig("edges_poly.png")
# plt.close()
#print(is_y_monotone(monotone_poly))


#print(x, y)
x, y = poly.exterior.xy
# solid_capstyle = 'round' makes the closing line of the polygon rounded instead of ugly
plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round')
plt.savefig("readme_images/poly.png")
plt.close()

x, y = monotone_poly.exterior.xy
# solid_capstyle = 'round' makes the closing line of the polygon rounded instead of ugly
plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round')
# keyword marker is vital to interprete x and y as point instead of lines, style='rx' won't cut it
plt.plot(myPoint.x, myPoint.y, marker='o', markersize=3, color="red")
plt.savefig("readme_images/monotone_poly_w_point.png")
plt.close()

print(f"Poly is y-monotone: {is_y_monotone(poly)}")
print(f"Monotone_poly is y-monotone: {is_y_monotone(monotone_poly)}")
