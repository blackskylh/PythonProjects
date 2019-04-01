# -*- coding: utf-8 -*- 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import random


def create_point():
    x = np.random.random(100) * 100  # 随机产生100个平均值为2，方差为1.2的浮点数，即第一簇点的x轴坐标
    y = np.random.random(100) * 100  # 随机产生100个平均值为2，方差为1.2的浮点数，即第一簇点的x轴坐标
    return x, y


def make_pic(x, y):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # matplotlib画图中中文显示会有问题，需要这两行设置默认字体

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(right=100, left=0)
    plt.ylim(top=100, bottom=0)
    # 画两条（0-9）的坐标轴并设置轴标签x，y
    area = np.pi * 2 ** 2  # 点面积
    # 画散点图
    colors = 'blue'
    plt.scatter(x, y, s=area, c=colors, alpha=0.4)
    plt.show()
    return plt


def get_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def create_vpoint(point, k):
    x = []
    y = []
    for i in range(k):
        count = 0
        x_all = 0
        y_all = 0
        for key, value in point.items():
            if value == i:
                count += 1
                x_all += key[0]
                y_all += key[1]
        if count != 0:
            x.append(x_all / count)
            y.append(y_all / count)
    return list(zip(x, y))


def k_means(k, point, v_point, flag1, distance):
    print(v_point)
    if flag1 == 0:
        return
    flag1 = 0
    di = -1
    for key, value in point.items():
        di += 1
        for i in range(k):
            d = get_distance(key[0], key[1], v_point[i][0], v_point[i][1])
            if d < distance[di]:
                distance[di] = d
                if value != i:
                    point[key] = i
                    if flag1 != 1:
                        flag1 = 1
    if flag1 == 1:
        v_point = create_vpoint(point, k)
    return k_means(k, point, v_point, flag1, distance)


def initVale(n):
    l = []
    for i in range(k - 1):
        l.extend([i] * int(n / k))
    if n % k == 0:
        l.extend([k - 1] * int(n / k))
    else:
        l.extend([k - 1] * int(n / k + 1))
    return l


def show_div(point, k, plt):
    colors = random.sample(list(matplotlib.colors.cnames), k)
    area = np.pi * 2 ** 2  # 点面积
    for i in range(k):
        listX = []
        listY = []
        for key, value in point.items():
            if value == i:
                listX.append(key[0])
                listY.append(key[1])
                plt.scatter(listX, listY, s=area, c=colors[i], alpha=0.4)
    plt.show()


if __name__ == '__main__':
    (x, y) = create_point()
    plt = make_pic(x, y)
    point = list(zip(x, y))
    k = int(input("请输入种类个数："))
    v_point = random.sample(point, k)
    n = len(point)
    point = dict(zip(point, initVale(n)))
    flag = 1
    distance = [999999] * n
    k_means(k, point, v_point, flag, distance)
    show_div(point, k, plt)
