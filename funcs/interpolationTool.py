import numpy as np

def GenericBresenhamLine(x1, y1, x2, y2, shape):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    # 根据直线的走势方向，设置变化的单位是正是负
    s1 = 1 if ((x2 - x1) > 0) else -1
    s2 = 1 if ((y2 - y1) > 0) else -1
    # 根据斜率的大小，交换dx和dy，可以理解为变化x轴和y轴使得斜率的绝对值为[0,1]
    boolInterChange = False
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        boolInterChange = True
    # 初始误差
    e = 2 * dy - dx
    x = x1
    y = y1
    points = [[x, y]]
    for i in range(0, int(dx + 1)):
        if e >= 0:
            # 此时要选择横纵坐标都不同的点，根据斜率的不同，让变化小的一边变化一个单位
            if boolInterChange:
                x += s1
            else:
                y += s2
            e -= 2 * dx
        # 根据斜率的不同，让变化大的方向改变一单位，保证两边的变化小于等于1单位，让直线更加均匀
        if boolInterChange:
            y += s2
        else:
            x += s1
        if x >=0 and x < shape[1] and y >=0 and x < shape[1]:
            points.append([x, y])
        e += 2 * dy
    return points

def interpolationPoints(points, shape):
    length = len(points)
    n_points = []
    for i in range(0, length - 1):
        tmp = GenericBresenhamLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1], shape)
        n_points.extend(tmp)
    return n_points

