# Bresenham Generation
def GenericBresenhamLine(x1, y1, x2, y2, shape):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    # find the line direction
    s1 = 1 if ((x2 - x1) > 0) else -1
    s2 = 1 if ((y2 - y1) > 0) else -1
    # keep the slope value with in [0,1]
    changeDirectFlag = False
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        changeDirectFlag = True
    # initial error
    e = 2 * dy - dx
    x = x1
    y = y1
    points = [[x, y]]
    for i in range(0, int(dx + 1)):
        if e >= 0:
            # make one unit change to the end with a smaller change
            if changeDirectFlag:
                x += s1
            else:
                y += s2
            e -= 2 * dx
        # make one unit change to the end with a larger change to smooth the line
        if changeDirectFlag:
            y += s2
        else:
            x += s1
        if 0 <= x < shape[1] and y >= 0 and x < shape[1]:
            points.append([x, y])
        e += 2 * dy
    return points

# Point interpolation function
def interpolationPoints(points, shape):
    length = len(points)
    n_points = []
    for i in range(0, length - 1):
        tmp = GenericBresenhamLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], shape)
        n_points.extend(tmp)
    return n_points
