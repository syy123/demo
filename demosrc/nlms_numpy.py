# -*- encoding: utf-8 -*-
# filename: nlms_numpy.py
import numpy as np

# 用Numpy实现的NLMS算法
# x为参照信号，d为目标信号，h为自适应滤波器的初值
# step_size为更新系数
def nlms(x, d, h, step_size=0.5):
    i = len(h)
    size = len(x)
    # 计算输入到h中的参照信号的乘方和
    power = np.sum(x[i:i - len(h):-1] * x[i:i - len(h):-1])# x[i]^2 + x[i-1]^2 +...+x[1],不包括x[0]，为什么？
    u = np.zeros(size, dtype=np.float64)

    while True:
        x_input = x[i:i - len(h):-1]
        u[i] = np.dot(x_input, h)
        e = d[i] - u[i]
        h += step_size * e / power * x_input
        
        power -= x_input[-1] * x_input[-1]  # 减去最早的取样
        i += 1
        if i >= size: 
            return u, h # 迭代了len(x) - len(h)次
        power += x[i] * x[i]  # 增加最新的取样
