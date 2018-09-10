import numpy as np
z = 1.96
def estimate_ratio(file, request_type, n=10000):
    """
    function computes estimation of proportion of mobile device requests and delta for confidence 0.95 interval of this estimation
    and also total number of occurences
    """
    total = 0
    mobile = 0
    with open(file, 'r') as f:
        #actually here it is better to read random lines, 
        #becouse if they're dependent(e.g. lines are in chronological order), this will work poorly
        for i, line in enumerate(f):
            if i > n:
                break
            tmp = line.split(',')
            if tmp[1] == request_type:
                total += 1
                mobile += int(tmp[2]) == 1
    delta = z/total*np.sqrt(mobile*(total - mobile)/total)
    return mobile*1.0/total, delta, total

def test(file, n):
    p1, delta1, n1 = estimate_ratio(file, '/index', n)
    p2, delta2, n2 = estimate_ratio(file, '/test', n)
    p = (p1*n1 + p2*n2)*1.0/(n1 + n2)
    Z = (p1 - p2)/(np.sqrt(p*(1 - p)*(1.0/n1 + 1.0/n2)))
    return Z, np.abs(Z) > z