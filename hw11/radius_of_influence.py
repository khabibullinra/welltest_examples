import numpy as np
import matplotlib.pyplot as plt

from mpmath import *
import scipy.special as sc

mp.dps = 5  # здесь задаем желаемую точность расчетов mpmath (количество знаков после запятой)
mp.pretty = True  # здесь задаем вывод функций mpmath в виде чисел, а не объектов


# Решение линейного стока уравнения фильтрации
def pd_ei(rd, td):
    return -1 / 2 * sc.expi(-rd ** 2 / 4 / td)


n = np.arange(1, 100, 1)
td = 1000
rr = np.arange(1, 1000, 1)
# for i in n:
#     td = 1000 * i
#     # здесь используем расчет заполнения массива с использованием итератора python -
#     # не самый быстрый вариант для этой функции, но работает
#     x = rr
#     y = [pd_ei(ri, td) for ri in rr]
min_cone = [pd_ei(ri, td=1000) for ri in rr]
max_cone = [pd_ei(ri, td=100000) for ri in rr]
plt.plot(rr, min_cone)
plt.plot(rr, max_cone)
plt.show()
influence = []
for i in range(len(rr)):
    x = rr[i]
    y_max = max_cone[i]
    y_min = min_cone[i]
    influence.append(y_max-y_min)

tdd = np.arange(1000, 100000, 100)
for i in range(1, len(tdd)):
    influence.append(pd_ei(ri, td=tdd[i]))

#
# plt.plot(rr, influence)
# plt.show()
# for i in n:
#     td = 1000 * i
#     x = rr
#     y1 = [pd_ei(ri, td) for ri in rr]
#     print(y)


    # rad_infl.append(y)
# print(sqrt((rr[-1]-rr[0])**2+(y[-1]-y[0])**2))


# print(np.argmax((pd)))
# plt.show()
