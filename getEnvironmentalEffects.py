import numpy as np
import math


def getEnvEffects(param):

    factor = 1

    p = param.split(":")
    
    if p[0] == 'i':
        factor1 = 0.6
    elif p[0] == 'o':
        factor1 = 1.0
    elif p[0] == 'u':
        factor1 = 0.0
    else:
        factor1 = 0.0
        
    if p[1] == 'u':
        factor2 = 0.75
    elif p[1] == 's':
        factor2 = 1.0
    elif p[1] == 'd':
        factor2 = 1.0
    elif p[1] == 'f':
        factor2 = 0.9
    elif p[1] == 'r':
        factor2 = 1.0
    else:
        factor2 = 0.95

    if p[2] == 'n':
        factor3 = 1.0
    elif p[2] == 'l':
        factor3 = 0.8
    elif p[2] == 'm':
        factor3 = 0.6
    else:
        factor3 = 0.4

    if p[3] == 'n':
        factor4 = 1.0
    elif p[3] == 'l':
        factor4 = 0.8
    elif p[3] == 'm':
        factor4 = 0.6
    else:
        factor4 = 0.4
    
    f = factor1 * factor2 * factor3 * factor4

    return f

