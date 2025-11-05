"""
simple welltest functions
ver 0.2 from 20/01/2022
Khabibullin Rinat
"""
import numpy as np
import scipy.special as sp
#from scipy.special import  expi
import anaflow 


# Define functions for converting dimensional variables into dimensionless variables and vice versa
# to be used later for graphing and calculations

# Naming functions, we'll keep following conventions
# first comes the name of what we're looking at
# at the end comes result dimension, if appropriate


def q_from_qd_sm3day(qd, q_ref_sm3day=1):
    """
    Перевод безразмерного дебита скважины в размерный
    qd - безразмерный дебит скважины
    q_ref_sm3day - референсный дебит
    """
    return  qd * q_ref_sm3day / 2 / np.pi

def qd_from_q(q_sm3day, q_ref_sm3day=1):
    """
    Перевод размерного дебита в безразмерные
    q_sm3day -  дебит скважины, ст. м3/сут
    q_ref_sm3day - референсный дебит
    """
    return 2 * np.pi * q_sm3day / q_ref_sm3day

def r_from_rd_m(rd, rw_m=0.1):
    """
    translate dimensionless distance into dimensional distance
    rd - dimensionless distance
    rw_m - well radius, m
    """
    return rd*rw_m

def rd_from_r(r_m, rw_m=0.1):
    """
    translate dimensional distance to dimensionless distance
    r_m - dimensional distance, m
    rw_m - well radius, m
    """
    return r_m/rw_m

def t_from_td_hr(td, k_mD=10, phi=0.2, mu_cP=1, ct_1atm=1e-5, rw_m=0.1):
    """
    conversion of dimensionless time to dimensional time, result in hours
    td - dimensionless time
    k_mD - formation permeability, mD
    phi - porosity, fractions of units
    mu_cP - dynamic fluid viscosity, cP
    ct_1atm - total compressibility, 1/atm
    rw_m - well radius, m
    """
    return td * phi * mu_cP * ct_1atm * rw_m * rw_m / k_mD / 0.00036

def td_from_t(t_hr, k_mD=10, phi=0.2, mu_cP=1, ct_1atm=1e-5, rw_m=0.1):
    """
    dimension time conversion to dimensionless time
    t_hr - dimensional time, hour
    k_mD - formation permeability, mD
    phi - porosity, fractions of units
    mu_cP - dynamic fluid viscosity, cP
    ct_1atm - total compressibility, 1/atm
    rw_m - well radius, m
    """
    return 0.00036 * t_hr * k_mD / (phi * mu_cP * ct_1atm * rw_m * rw_m) 

def p_from_pd_atma(pd, k_mD=10, h_m=10, q_sm3day=20, b_m3m3=1.2, mu_cP=1, pi_atma=250):
    """
    conversion of dimensionless pressure to dimensional pressure, result in absolute atmospheres
    pd - dimensionless pressure
    k_mD - formation permeability, mD
    h_m - reservoir thickness, m
    q_sm3day - flow rate at the surface, m3 /day in s.c.
    fvf_m3m3 - oil volumetric ratio, m3/m3
    mu_cP - dynamic viscosity of fluid, cP
    pi_atma - initial pressure, absolute atm
    """
    return pi_atma - pd * 18.42 * q_sm3day * b_m3m3 * mu_cP / k_mD / h_m 

def pd_from_p(p_atma, k_mD=10, h_m=10, q_sm3day=20, b_m3m3=1.2, mu_cP=1, pi_atma=250):
    """
    translate dimensional pressure into dimensionless pressure
    p_atma - pressure
    k_mD - formation permeability, mD
    h_m - reservoir thickness, m
    q_sm3day - flow rate at the surface, m3/day in s.c.
    fvf_m3m3 - oil volumetric ratio, m3/m3
    mu_cP - dynamic viscosity of fluid, cP
    pi_atma - initial pressure, absolute atm
    """
    return (pi_atma - p_atma) / (18.42 * q_sm3day * b_m3m3 * mu_cP) * k_mD * h_m 

# ==========================================================
#
# ==========================================================

# Решение линейного стока уравнения фильтрации
def pd_line_source_ei(td, rd, qd=1, skin=0):
    """
    Решение линейного стока уравнения фильтрации
    rd - безразмерное расстояние
    td - безразмерное время
    qd - безразмерный дебит
    skin - величина скин-фактора
    """
    # оценим приведенный радиус скважины
    rd_eff = np.exp(-skin) * np.heaviside(-skin, 0) + np.heaviside(skin, 1)
    # преобразуем входные радиусы в приведенные с учетом величины скин-фактора
    rd_calc = rd * np.heaviside(rd - rd_eff, 0) + np.exp(-skin) * np.heaviside(rd_eff - rd, 1)
    # исключим нулевые величины времени, чтобы избежать деления на ноль
    td_safe = 100 * np.heaviside(-td, 1) + td * np.heaviside(td, 0)
    pd = - qd / 2 / np.pi * ( 1 / 2  * sp.expi(-rd_calc**2 / 4 / td_safe)  )
    # в конце обнулим результаты для нулевых моментов времени
    return  pd * np.heaviside(td, 0)


def pd_ss(rd, r_ed=2500, qd=1, skin=0):
    # оценим приведенный радиус скважины
    rd_eff = np.exp(-skin) * np.heaviside(-skin, 0) + np.heaviside(skin, 1)
    # преобразуем входные радиусы в приведенные с учетом величины скин-фактора
    rd_calc = rd * np.heaviside(rd - rd_eff, 0) + np.exp(-skin) * np.heaviside(rd_eff - rd, 1)

    return qd / 2 / np.pi * (np.log(r_ed/rd_calc) )

def pd_ss_(rd, r_ed=2500, qd=1, skin=0):
    skin_eff = skin * np.heaviside(1 - rd, 1)
    rd_eff = rd * np.heaviside(rd - 1, 1) + np.heaviside(1 - rd, 0)
    return qd / 2 / np.pi * (np.log(r_ed/rd_eff) + skin_eff)


def pd_line_source_ei_build_up(td, td_p, rd, qd=1, skin=0):
    """
    расчет давления для запуска и последующей остановки скважины
    td - время после запуска
    td_p - время безразмерное - которое скважина работала до остановки
    rd - расстояния от скважины
    qd - безразмерный дебит
    skin - величина скин-фактора
    """
    
    # применение функции Хевисайда здесь делает расчет корректным
    # для входных векторов td
    return pd_line_source_ei(td, rd, qd, skin) - np.heaviside(td-td_p,1) * pd_line_source_ei(td-td_p, rd, qd, skin)

def p_line_source_ei_atma(t_hr, r_m, q_sm3day, 
                          k_mD=10, h_m=10, phi=0.2, mu_cP=1, b_m3m3=1.2, ct_1atm=1e-5, rw_m=0.1, p_init_atma=250, skin=0):
    """
    Функция расчета перепада давления в произвольной точке пласта 
    на расстоянии r_m от центра скважины для решения линейного стока
    
    - r_m - расстояние на котором проводится расчет, м
    - q_sm3day - дебит жидкости на поверхности в стандартных условиях
    - k_mD
    - h_m
    - phi
    - mu_cP - вязкость нефти (в пластовых условиях)
    - b_m3m3 - объемный коэффициент нефти 
    - ct_1atm 
    - rw_m - радиус скважины, м
    - p_init_atma
    - skin - скин фактор
    """ 
    q_ref_sm3day = 1
    td = td_from_t(t_hr, k_mD=k_mD, phi=phi, mu_cP=mu_cP, ct_1atm=ct_1atm, rw_m=rw_m)
    rd = rd_from_r(r_m, rw_m=rw_m)
    qd = qd_from_q(q_sm3day, q_ref_sm3day=q_ref_sm3day)
    pd = pd_line_source_ei(td, rd, qd, skin)
    return p_from_pd_atma(pd, k_mD=k_mD, h_m=h_m, q_sm3day=q_ref_sm3day, b_m3m3=b_m3m3, mu_cP=mu_cP, pi_atma=p_init_atma)

# ====================================================================================


# Определим функции для расчета стационарного решения
def dp_ss_atm(q_liq_sm3day = 50,
              mu_cP = 1,
              b_m3m3 = 1.2,
              kh_mDm = 40,
              r_e_m = 240,
              r_w_m = 0.1,
              r_m = 0.1, 
              skin = 0):
  """
  Функция расчета перепада давления в произвольной точке пласта 
  на расстоянии r_m от центра скважины для стационарного решения
 
  - q_liq_sm3day - дебит жидкости на поверхности в стандартных условиях
  - mu_cP - вязкость нефти (в пластовых условиях)
  - B_m3m3 - объемный коэффициент нефти 
  - kh_mDm - kh пласта
  - r_e_m - радиус контрура питания, м  
  - r_w_m - радиус скважины, м
  - r_m - расстояние на котором проводится расчет, м
  - skin - скин фактор
  """
  r_eff_m = np.where(skin < 0, r_w_m * np.exp(-skin), r_w_m)
  mult = 18.42 * q_liq_sm3day * mu_cP * b_m3m3/ kh_mDm
  dp = np.where(r_m <= r_eff_m, 
                mult * (np.log(r_e_m/r_w_m) + skin),
                mult * (np.log(r_e_m/r_m)))

  return dp

def p_ss_atma(p_res_atma = 250,
              q_liq_sm3day = 50,
              mu_cP = 1,
              b_m3m3 = 1.2,
              k_mD = 40,
              h_m = 10,
              r_e_m = 240,
              r_w_m = 0.1,
              r_m = 0.1, 
              skin = 0):
  """
  функция расчета давления в произвольной точке пласта 
  на расстоянии r_m от центра скважины для стационарного решения 

  - p_res_atma - пластовое давление, давление на контуре питания
  - q_liq_sm3day - дебит жидкости на поверхности в стандартных условиях
  - mu_cP - вязкость нефти (в пластовых условиях)
  - B_m3m3 - объемный коэффициент нефти 
  - k_mD - проницаемость пласта
  - h_m - мощность пласта, м
  - r_e_m - радиус контрура питания, м  
  - r_m - расстояние на котором проводится расчет, м
  """
  return p_res_atma - dp_ss_atm(q_liq_sm3day = q_liq_sm3day,
                                mu_cP = mu_cP,
                                b_m3m3 = b_m3m3,
                                kh_mDm = k_mD * h_m,
                                r_e_m = r_e_m,
                                r_w_m = r_w_m,
                                r_m = r_m,
                                skin = skin)

# =================================================================================

# пример функции реализующий расчет решения в пространстве Лапласа
def pd_lapl_line_source(u, rd=1.):
    """
    расчет решения линейного стока для безразмерного давления в пространстве Лапласа
    u - переменная пространства Лапласа
    rd- безразмерное расстояние от центра скважины
    """
    return np.divide(sp.kn(0, rd * u**0.5) , u)

# функция расчета безразмерного давления с использованием алгоритма Стефеста
# для численного обратного преобразования Лапласа
def pd_line_source_inv(td, rd=1.):
    """
    расчет решения линейного стока для безразмерного давления
    на основе численного обратного преобразования Лапласа (алгоритм Стефеста)
    td - безразмерное давление, число или numpy массив
    rd - безразмерный радиус, по умолчанию rd=1 - соответствует давлению на забое
         должно быть числом
    результат массив массивов давления от времени
    """
    pd_inv = anaflow.get_lap_inv(pd_lapl_line_source, rd=rd)
    return pd_inv(td)

    # пример функции реализующий расчет решения в пространстве Лапласа
def pd_lapl_finite_rw(u, rd=1.):
    """
    расчет решения c конечным радиусом скважины для безразмерного давления в пространстве Лапласа
    u - переменная пространства Лапласа
    rd- безразмерное расстояние от центра скважины
    """
    # полезно учесть, что при u>5e5 выражение kn(1, u05) обратится в ноль и будет деление на ноль
    # но если принудительно сделать там выражение равное нулу, обратное преобразование Лапласа
    # может выдавать очень странные результаты, поэтому лучше пока оставить как есть
    u05 = u**0.5
    return np.divide(sp.kn(0, rd * u05) , (u * u05 *  sp.kn(1, u05)))


# функция расчета безразмерного давления с использованием алгоритма Стефеста
# для численного обратного преобразования Лапласа
def pd_finite_rw_inv(td, rd=1.):
    """
    расчет решения c конечным радиусом скважины для безразмерного давления
    на основе численного обратного преобразования Лапласа (алгоритм Стефеста)
    td - безразмерное давление, число или numpy массив
    rd - безразмерный радиус, по умолчанию rd=1 - соответствует давлению на забое
    результат массив массивов давления от времени
    """
    pd_inv = anaflow.get_lap_inv(pd_lapl_finite_rw, rd=rd)
    return pd_inv(td)