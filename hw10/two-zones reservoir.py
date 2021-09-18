import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def p_ss_atma(p_res_atma=250,
              q_liq_sm3day=50,
              mu_cP=1,
              B_m3m3=1.2,
              k_mD=40,
              h_m=10,
              r_e=240,
              r=0.1):
    """
    функция расчета давления в произвольной точке пласта для стационарного решения
    уравнения фильтрации
    p_res_atma - пластовое давление, давление на контуре питания
    q_liq_sm3day - дебит жидкости на поверхности в стандартных условиях
    mu_cP - вязкость нефти (в пластовых условиях)
    B_m3m3 - объемный коэффициент нефти
    k_mD - проницаемость пласта
    h_m - мощность пласта
    r_e - радиус контрура питания
    r - расстояние на котором проводится расчет
    """
    return p_res_atma - 18.41 * q_liq_sm3day * mu_cP * B_m3m3 / k_mD / h_m * np.log(r_e / r)


# r = np.arange(0.1, 100, 1)
# plt.plot(r, p_ss_atma(r=r))
# plt.show()

# first task: two-zones reservoir

def p_ss_atma_two_zones(p_res_atma=250,
                        q_liq_sm3day=50,
                        mu_cP=1,
                        B_m3m3=1.2,
                        h_m=10,
                        r_e=240,
                        r=0.1,
                        r_bound=100,
                        k1_mD=30,
                        k2_mD=10):
    """
    функция, использующая функцию p_ss_atma для расчета композитного двухслойного пласта.
    r_bound - расстояние от скважины до следующей зоны
    k1_mD, k2_mD - проницаемости зон от скважины до контура соответственно
    """
    if r < r_bound:
        k_mD = k1_mD
    else:
        k_mD = k2_mD
    return p_res_atma - 18.41 * q_liq_sm3day * mu_cP * B_m3m3 / k_mD / h_m * np.log(r_e / r)


r = np.arange(0.1, 240, 1)
two_zones = np.array([p_ss_atma_two_zones(r=rr) for rr in r])
# plt.plot(r, two_zones)
# plt.grid()
# plt.show()

# comparison. One-zone reservoir has k = 40 mD meantime two-zone has

one_zone = np.array([p_ss_atma(r=rr) for rr in r])
plt.plot(r, one_zone, r, two_zones)
plt.show()
