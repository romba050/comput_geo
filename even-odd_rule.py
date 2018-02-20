import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry import Point


# implements the even-odd rule which determines if a point is inside a polygon
# note that when working with shapely objects, there is also the method object.contains(other) and object.within(other)
# https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
def isPointInPath(x, y, poly):
    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    poly = poly.exterior.coords
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c


monoton_poly = Polygon([(0, 2), (1.5, 6), (3, 4), (1.5, 0), (1, 1)])
myPoint = Point(0, 2)


if isPointInPath(myPoint.x, myPoint.y, monoton_poly):
    print("Point is inside polygon.")
else:
    print("Point is outside polygon.")
print("Note: Point on the border counts as inside.")

#print(is_y_monotone(monoton_poly))

x, y = monoton_poly.exterior.xy
# type of x and y is array 'd', for double point float
print(x, y)

# solid_capstyle = 'round' makes the closing line of the polygon rounded instead of ugly
plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round')

# keyword marker is vital to interprete x and y as point instead of lines, style='rx' won't cut it
plt.plot(myPoint.x, myPoint.y, marker='o', markersize=3, color="red")
plt.show()
