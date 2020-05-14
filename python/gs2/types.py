from ctypes import Structure
from ctypes import c_int
from ctypes import c_double
from ctypes import c_void_p
from ctypes import POINTER
from ctypes import CFUNCTYPE

import ctypes

class MemoryRequirements(Structure):
    _fields_ = [
        ('mxc', c_int),
        ('mxt', c_int),
        ('maxnn', c_int),
        ('maxne', c_int),
        ('ns1', c_int),
        ('kns1', c_int),
        ('maxm4', c_int),
        ('maxm5', c_int),
        ('maxeep', c_int),
        ('maxbw', c_int),
        ('maxbw2', c_int),
        ('maxm1', c_int),
        ('maxm2', c_int),
        ('maxs', c_int),
        ('mx', c_int)
    ]

class Array(Structure):
    _fields_ = [
        ('elements', POINTER(c_double)),
        ('size', c_int)
    ]

class Matrix(Structure):
    _fields_ = [
        ('elements', POINTER(POINTER(c_double))),
        ('rows', c_int),
        ('columns', c_int)
    ]


class State(Structure):
    _fields_ = [
        ('memoryRequirements', MemoryRequirements),
        ('input', c_void_p),
        ('output', c_void_p),
        ('tape7', c_void_p),
        ('tape8', c_void_p),
        ('tape2', Matrix),
        ('tape4', Array),
        ('tape11', Matrix),
        ('tape13', Matrix),
        ('s', Matrix),
        ('p', Array),
        ('w', Array),
        ('cfq', Array),
        ('conc', Array),
        ('conci', Array),
        ('fq', Array),
        ('klc', Array),
        ('klr', Array),
        ('lc', Array),
        ('lr', Array),
        ('phi', Array),
        ('phii', Array),
        ('x', Array),
        ('y', Array),
        ('alpha', Array),
        ('elong', Array),
        ('etrans', Array),
        ('fmobx', Array),
        ('fmoby', Array),
        ('kd', Array),
        ('kf', Array),
        ('_lambda', Array),
        ('por', Array),
        ('rho', Array),
        ('tta', Array),
        ('_in', Matrix),
        ('ie', Matrix),
        ('type', c_int),
        ('chng', c_double),
        ('tdr', c_double),
        ('stat', c_double),
        ('statp', c_double),
        ('oldt', c_double),
        ('delt', c_double),
        ('dprdt', c_double),
        ('betap', c_double),
        ('clos1', c_double),
        ('delp', c_double),
        ('difusn', c_double),
        ('pchng', c_double),
        ('vmax', c_double),
        ('stime', c_double),
        ('ssec', c_double),
        ('h1', c_double),
        ('h2', c_double),
        ('pl', c_double),
        ('coefi', c_double),
        ('ei', c_double),
        ('initialDelt', c_double),
        ('ne', c_int),
        ('np', c_int),
        ('nk', c_int),
        ('nseep', c_int),
        ('inc', c_int),
        ('me', c_int),
        ('igo', c_int),
        ('kod1', c_int),
        ('kod2', c_int),
        ('kod3', c_int),
        ('kod4', c_int),
        ('kod7', c_int),
        ('kod8', c_int),
        ('kod9', c_int),
        ('kod10', c_int),
        ('kod11',c_int),
        ('kod12', c_int),
        ('itmax', c_int),
        ('itchng', c_int),
        ('iter1', c_int),
        ('wk', Array),
        ('xk', Matrix),
        ('xm', Matrix),
        ('xpsi', Matrix),
        ('ckt', Matrix * 3),
        ('ctt', Matrix * 3),
        ('psio', Array),
        ('ispl', Array),
        ('nn', c_int),
        ('mm', c_int),
        ('km', c_int),
        ('it', c_int),
        ('nsdn', c_int),
        ('nb', c_int),
        ('knb', c_int),
        ('knb2', c_int),
        ('istop', c_int),
        ('mb', c_double),
        ('mb2', c_double),
        ('kmb', c_double),
        ('kmb2', c_double),
        ('pe', Matrix),
        ('se', Matrix),
        ('f', Matrix),
        ('dx', Matrix),
        ('dy', Matrix),
        ('q', Array),
        ('detj', Array),
        ('cphi', Array),
        ('vkx', Array),
        ('vky', Array),
        ('dpordt', Array),
        ('d0', Array),
        ('dk', Array),
        ('dh', Array),
        ('srcrt', Array),
        ('ff', Array),
        ('dgx', Array),
        ('dgy', Array),
        ('srcr', Array)
    ]


CallbackType = CFUNCTYPE(c_int, State)