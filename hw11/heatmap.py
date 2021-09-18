import numpy as np
import matplotlib.pyplot as plt
from mpmath import *
import scipy.special as sc
import seaborn as sns

mp.dps = 5  # здесь задаем желаемую точность расчетов mpmath (количество знаков после запятой)
mp.pretty = True  # здесь задаем вывод функций mpmath в виде чисел, а не объек


# Решение линейного стока уравнения фильтрации
def pd_ei(rd, td):
    return -1 / 2 * sc.expi(-rd ** 2 / 4 / td)


def pd_ei_composite(t=10,
                    r=1,
                    r_w=0.1,
                    k_mD=40,
                    k1_mD=30,
                    k2_mD=10,
                    por=0.3,
                    mu_cP=1.2,
                    ct=1,
                    r_bound=100,
                    td=None):
    if r<r_bound:
        k_mD = k1_mD
    else:
        k_mD = k2_mD
    rd = r/r_w
    if not td:
        td = 0.00036*k_mD*t/(por*mu_cP*ct*r_w**2)
    return -1 / 2 * sc.expi(-rd ** 2 / 4 / td)


td = 1e10
rr = np.arange(1, 1025, 1)

# homogeneous stratum

hm_homo = np.array([pd_ei(ri, td=td) for ri in rr])
sns.heatmap(hm_homo.reshape(32,32))
plt.show()

# composite stratum

hm_comp = np.array([pd_ei_composite(r=ri, td=td) for ri in rr])
sns.heatmap(hm_comp.reshape(32, 32))
plt.show()
