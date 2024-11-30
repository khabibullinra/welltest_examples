"""
тестовые функции

"""

import numpy as np
import scipy.special as sp
import scipy.constants as sc
import anaflow 

pi_ = sc.pi
tiny = 0.00000001
gamma = 0.577215664901533

"""

' Radial source solution
Function Pd_lapl_source(z As Double, ByVal R_d As Double, _
                        Optional ByVal WellModel = 2) As Double
'z - laplace space variable
'r_d - dimensionless distance from center of wellbore
' WellModel - well model
        ' 1 - line source solution (default)
        ' 2 - finite well radius solution


   Dim Pd As Double

   If Sqr(z) * R_d > 700 Then
        Pd_lapl_source = 0
   Else
        Select Case WellModel
        Case 1
            Pd = 1 / (2 * pi_) * BesselK(Sqr(z) * R_d, 0)
        Case 2
            Pd = 1 / (2 * pi_) * BesselK(Sqr(z) * R_d, 0) / Sqr(z) / BesselK(Sqr(z), 1)
        End Select
        
        Pd_lapl_source = Pd
    
   End If

End Function
"""


def tst(x:float)->float:
    return x * x



