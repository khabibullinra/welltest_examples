

import numpy as np
from numpy.typing import ArrayLike
from typing import Union, Callable
import scipy.special as sp
import scipy.constants as sc
from anaflow import get_lap_inv 

from dataclasses import dataclass

FloatArray = Union[float, np.ndarray]

# константы
pi_ = sc.pi
tiny = 0.00000001
gamma = 0.577215664901533


@dataclass
class WellModel:
    name: str
    dept: str
    salary: int


# базовые решения уравнения фильтрации


def pd_line_source_ei(td:FloatArray, 
                      rd:FloatArray=1.)->np.ndarray:
    """
    Решение линейного стока уравнения фильтрации
    Радиальный приток к вертикальной скважине бесконечно малого 
    радиуса в бесконечном пласте

    td - безразмерное время, число или numpy массив, больше нуля
    rd - безразмерное расстояние, 
         по умолчанию rd=1 - соответствует давлению на забое, 
         число или numpy массив
    
    результат давление от времени
    """

    td = np.array(td, dtype = float)
    rd = np.array(rd, dtype = float)
    return np.multiply(-0.5, 
                       sp.expi(np.divide(-rd**2 / 4 , 
                                          td, 
                                          out=np.zeros_like(td), 
                                          where=td!=0)), 
                       out=np.zeros_like(td), 
                       where=td!=0)


def pd_superposition(td:FloatArray, 
                     rd:FloatArray = 1.,
                     td_hist:FloatArray = 0., 
                     qd_hist:FloatArray = 1.,
                     pd_func:Callable = pd_line_source_ei)->np.ndarray:
    """
    calculation of dimensionless pressure for the sequence of dimensionless flow rates
    td - calculation time after startup, dimensionless
    td_hist - array of well operation mode change times, dimensionless
    qd_hist - array of flow rates set after regime change, dimensionless
    rd - radius dimensionless, distance from well
    """
    # forcibly add zeros to the input arrays to account for well startup
    qdh = np.hstack([0, qd_hist])
    tdh = np.hstack([0, td_hist])
    # plot the virtual wells' flow rates - the differences of the real flow rates at switching
    delta_qd = np.hstack([0, np.diff(qdh)])
    # reference dimensionless flow rate is 1
    
    # vector magic - time can be a vector and switching flow rates is also a vector
    # we must arrange sum over times, each of which is a sum over switches
    # we do it by means of meshgrid calculation and searching for accumulated sums
    qd_v, td_v =np.meshgrid(delta_qd, td)
    # use cumulative sum numpy to sum the results
    dpd = np.cumsum(qd_v * pd_func((td_v - tdh), rd=rd) * np.heaviside((td_v - tdh), 1), 1)
    # the last column is the full sum, which is needed as a result
    return dpd[:,-1]


def lpd_line_source(u:FloatArray, 
                    rd:float=1.)->np.ndarray:
    """
    расчет решения линейного стока для безразмерного давления 
    в пространстве Лапласа
    u - переменная пространства Лапласа
    rd- безразмерное расстояние от центра скважины
    """
    return  np.divide(sp.k0(rd * np.sqrt(u)) , u)


def lpd_finite_rw(u:FloatArray, 
                  rd:float=1.)->np.ndarray:
    """
    расчет решения c конечным радиусом скважины для безразмерного
    давления в пространстве Лапласа
    u - переменная пространства Лапласа
    rd- безразмерное расстояние от центра скважины
    """ 
    # полезно учесть, что при u>5e5 выражение kn(1, u05) обратится 
    # в ноль и будет деление на ноль, но если принудительно сделать 
    # там выражение равное нулю, обратное преобразование Лапласа
    # может выдавать очень странные результаты, поэтому лучше пока 
    # оставить как есть
    
    u05 = np.sqrt(u)
    return np.divide(sp.k0(rd * u05) , 
                    (u * u05 *  sp.k1(u05)))


def lpd_circle_boundary(u:FloatArray, 
                         rd:float=1., 
                         rd_external:float = 1000.,
                         finite_radius:bool=True,
                         boundary_no_flow:bool=False):
    """
    решения для кругового пласта в пространстве Лапласа.
    u - переменная пространства Лапласа
    rd - безразмерное расстояние от центра скважины
    rd_external - внешний радиус кругового пласта
    finite_radius - флаг - True решение для конечного радиуса
                         - False решение линейного стока
    boundary_no_flow - флаг True замкнутая граница
                            False постоянное давление на границе               
    """
    u05 = np.sqrt(u)
    
    #Select values of derivative normalizing coefficients u * K1(sqrt(u)) and -u * I1(sqrt(u))
    #in accordance with model - line source of finite radius
    if finite_radius:
         zK1 = u05 * sp.k1(u05)
         zI1 = u05 * sp.i1(u05)
    else:
         zK1 = 1
         zI1 = 0

    k1rde = sp.k1(u05 * rd_external)
    i1rde = sp.i1(u05 * rd_external)
    k0rde = sp.k0(u05 * rd_external)
    i0rde = sp.i0(u05 * rd_external)
    k0rd = sp.k0(u05 * rd)
    i0rd = sp.i0(u05 * rd)
    
    if boundary_no_flow:
        #no flow
        Lpd =  (i1rde * k0rd + k1rde * i0rd) / (i1rde * zK1 - k1rde * zI1)
    else:
        #constant pressure
        Lpd =  (i0rde * k0rd - k0rde * i0rd) / (i0rde * zK1 + k0rde * zI1)
    return Lpd / u 


def lpd_circle_boundary_const_press(u:FloatArray, 
                                     rd:float=1., 
                                     rd_external:float = 1000.):
    """
    решения для кругового пласта с постоянным давлением
    на границе в пространстве Лапласа.
    u - переменная пространства Лапласа
    rd - безразмерное расстояние от центра скважины
    r_ed - внешний радиус кругового пласта
    """
    
    u05 = np.sqrt(u)
    rd_u05 = rd * u05
    rd_external_u05 = rd_external * u05 
    return ((-sp.i0(rd_u05) * sp.k0(rd_external_u05) + sp.i0(rd_external_u05) * sp.k0(rd_u05)) / 
            (u**(3/2) * (sp.i0(rd_external_u05) * sp.k1(np.sqrt(u)) + 
                       sp.i1(np.sqrt(u)) * sp.k0(rd_external_u05))))



def lpd_func(u, rd, func, *arg, **kwarg):
    mask = np.sqrt(u) * rd > 700
    u = np.array(u)
    lpd = np.zeros_like(u)
    lpd[mask] = func(u[mask], rd, *arg, **kwarg)
    lpd[~mask] = lpd_line_source(u[mask], rd)
    return lpd



# функция расчета безразмерного давления на основе
# численного обратного преобразования Лапласа
def pd_lapl_inv(td:FloatArray, 
                rd:FloatArray=1.,
                lpd_func:Callable = lpd_line_source)->np.ndarray:
    """
    расчет решения линейного стока для безразмерного давления
    на основе численного обратного преобразования Лапласа 
    (алгоритм Стефеста)
    t_d - безразмерное давление, число или numpy массив
    rd - безразмерный радиус, по умолчанию rd=1 - соответствует
         давлению на забое, должно быть числом
    результат массив массивов давления от времени
    """
    pd_inv = get_lap_inv(lpd_func, rd=rd)
    return pd_inv(td)

