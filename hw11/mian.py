# импортируем библиотеки для расчетов

# numpy используем для работы с массивами и подготовки данных для построения графиков.
# Также в некоторых функциях используем возможности векторных расчетов numpy
import numpy as np
# matplotlib используем для построения графиков
import matplotlib.pyplot as plt

# mpmath используем для расчета спец функций и математических операций
from mpmath import *

mp.dps = 5  # здесь задаем желаемую точность расчетов mpmath (количество знаков после запятой)
mp.pretty = True  # здесь задаем вывод функций mpmath в виде чисел, а не объектов

# scipy.special используем как альтернативный вариант расчета специальных функций
import scipy.special as sc
import seaborn as sns

# Решение линейного стока уравнения фильтрации
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


# Решение линейного стока уравнения фильтрации
def pd_ei(rd, td):
  return -1/2*sc.expi(-rd**2 / 4 / td)

n=np.arange(1,100,1)
td = 1000
rr = np.arange(1, 1000, 1)
print(max(rr))
# при построении используем векторный расчет
for i in n:
    td = 1000*i
      # здесь используем расчет заполнения массива с использованием итератора python -
      # не самый быстрый вариант для этой функции, но работает
    plt.plot(rr, [pd_ei(ri,td) for ri in rr])
plt.show()


# td = 1e10
# rr = np.arange(1, 1025, 1)
# # for i in np.arange(1, 2, 1):
# #     t = 1000 * i
# #     plt.plot(rr, [pd_ei_composite(r=ri, t=t) for ri in rr])
#
# # hm_comp = np.array([pd_ei_composite(r=ri, td=td) for ri in rr])
# # sns.heatmap(hm_comp.reshape(32, 32))
# # plt.show()
# # # rr = np.arange(1, 1000, 1)
