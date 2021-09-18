import numpy as np
import matplotlib.pyplot as plt
from mpmath import *
import scipy.special as sc


mp.dps = 5  # здесь задаем желаемую точность расчетов mpmath (количество знаков после запятой)
mp.pretty = True  # здесь задаем вывод функций mpmath в виде чисел, а не объек
def pd_ei_composite(t=10,
          r=1,
          r_w = 0.1,
          k_mD=40,
          k1_mD=30,
          k2_mD=10,
          por=0.3,
          mu_cP=1.2,
          ct=1,
          r_bound=100):
    if r<r_bound:
        k_mD = k1_mD
    else:
        k_mD = k2_mD
    rd = r/r_w
    td = 0.00036*k_mD*t/(por*mu_cP*ct*r_w**2)
    return -1 / 2 * sc.expi(-rd ** 2 / 4 / td)


td = 1000
rr = np.arange(1, 1000, 1)
for i in np.arange(98, 100, 1):  # 100 solutions, i.e. 100 graphs
    t = 1000 * i
    plt.plot(rr, [pd_ei_composite(r=ri, t=t) for ri in rr])
plt.show()