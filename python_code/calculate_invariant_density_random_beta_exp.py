import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import copy

beta = 1.25
delta = 0.01
n = 10

########### GENERAL STRATEGY

def Tinvbeta(a,b, beta=beta):

    assert a <= b, "a must be smaller than b"

    if a <= 1 and b < 1:
        return [(a/beta,b/beta), ((a+1)/beta,(b+1)/beta)]
    elif a <= 1 and b >= 1:
        return [(a/beta,1/beta), ((a+1)/beta,(b+1)/beta)]
    else:
        return [((a+1)/beta,(b+1)/beta)]

def Linvbeta(a,b, beta=beta):

    assert a <= b, "a must be smaller than b"

    if a <= 1/(beta-1)-1 and b <= 1/(beta-1)-1:
        return [(a/beta,b/beta)]
    elif a <= 1/(beta-1)-1 and b > 1/(beta-1)-1:
        return [(a/beta,b/beta), (1/(beta*(beta-1)),(b+1)/beta)]
    else:
        return [(a/beta,b/beta), ((a+1)/beta,(b+1)/beta)]


def PerronFroboenuisIntegral(Tinv, f, a , b):
    set_int = Tinv(a,b)
    
    result = 0
    for (x,y) in set_int:
        result += quad(f, x ,y)[0]

    return result

def PerronFroboenuisOp(Tinv, f, s, dx = 1e-6):

    F = lambda x: PerronFroboenuisIntegral(Tinv, f, 0, x)

    return (F(s+dx)-F(s))/dx

def Iterate(P,f,s,k):

    if k == 1:
        return P(f,s)
    
    else:
        return P(lambda x: Iterate(P,f,x,k-1),s)


# Pbeta = lambda f, s: 1/2*PerronFroboenuisOp(Tinvbeta, f, s) + 1/2*PerronFroboenuisOp(Linvbeta, f, s)
# f = lambda x: 1

# xx = np.linspace(0,1/(beta-1), 100)
# # yy = [PerronFroboenuisIntegral(Tinvbeta, f, 0, x) for x in xx]
# # yy = [PerronFroboenuisOp(Tinvbeta, f, x) for x in xx]
# yy = [Iterate(Pbeta, f, x, 2) for x in xx]


# plt.plot(xx,yy)
# plt.ylim(0, 1/(beta-1))

# plt.show()



######### PROBLEM SPECIFIC STRATEGY ################

beta = 1.25
alpha = 1/beta
p = 0.5
l = 10
length = (1/(beta-1)-1)/beta
t = 1/beta + 1/2*length

def gaussian(x, sigma, t):
    return np.exp(-(x-t)**2/(2*sigma**2))


random_reals = np.sort(np.random.random(l-1))
# alphas =  1/beta + random_reals * length
alphas = 1/beta + np.linspace(0,1,l)*length

sigma1 = 10
sigma2 = 0.01
probs = gaussian(alphas, sigma1, t)/np.sum(gaussian(alphas, sigma1, t))
q_probs = gaussian(alphas, sigma2, t)/np.sum(gaussian(alphas, sigma2, t))
print(np.sum(probs))
print(np.sum(q_probs))

# plt.plot(alphas,probs)
# plt.plot(alphas,q_probs)
# plt.show()

# probs = np.sort(np.random.random(l))
# probs[-1] = 1

# random_reals = np.random.random(l)
# q_probs = np.zeros((l,))
# q_probs[0] = probs[0] + (1/2 - probs[0])*random_reals[0]
# for i in range(1,l):
#     if probs[i] < 1/2:
#         min_prob = max(probs[i], q_probs[i-1])
#         q_probs[i] = min_prob + (1/2 - min_prob)*random_reals[i]
#     else:
#         break
# q_probs[-1] = 1
# for i in range(l-2,0,-1):
#     # print(i)
#     if q_probs[i+1] > 1/2:
#         min_prob = min(probs[i], q_probs[i+1])
#         q_probs[i] = min_prob - (min_prob - 1/2)*random_reals[i]
#     else:
#         break


def Compare(p,q):

    out = True
    for i in range(len(p)):
        if p[i] < 1/2:
            if p[i] <= q[i] and q[i] <= 1/2:
                pass
            else:
                return False
        else:
            if p[i] >= q[i] and q[i] >= 1/2:
                pass
            else:
                return False
    return out

# probs_diff = probs[1:] - probs[:l-1]
# q_probs_diff = q_probs[1:] - q_probs[:l-1]

# print(alphas, probs, q_probs, Compare(q_probs, probs))

f = lambda x: beta-1

def Einv(y, beta=beta, alpha = alpha):
    if y <= alpha*beta -1 :
        return [y/beta]
    elif y <= alpha*beta :
        return [y/beta,(y+1)/beta]
    else:
        return [(y+1)/beta]

def Eforw(x, beta=beta, alpha = alpha):
    if x<= alpha:
        return beta*x
    else:
        return beta*x - 1
    
def P(f, E, beta=beta):
    return lambda y: 1/beta*np.sum([f(x) for x in E(y)])

def MixP(f, maps, listp, beta=beta):
    return lambda y: np.sum([listp[i]*P(f,lambda x:maps(x,i),beta=beta)(y) for i in range(len(listp))])

def Iterate(f, n):
    if n==0:
        return lambda x:x
    if n==1:
        return lambda x: f(x)
    else:
        return lambda x: Iterate(f, n-1)(f(x))

# def MixPRec(y, f, maps, listp, n, beta=beta):
#     if n==0:
#         return f(y)
#     if n==1:
#         return MixP(y, f, maps, listp, beta=beta)
#     else:
#         return MixPRec(y, lambda x: MixP(x, f, maps, listp, beta=beta), maps, listp, n-1, beta=beta)
       
Tinv = lambda x : Einv(x, alpha = 1/beta)
Linv = lambda x : Einv(x, alpha = 1/(beta*(beta-1)))

AntiMaps = lambda x, n: Einv(x, alpha = alphas[n])
Maps = lambda x, n: Eforw(x, alpha = alphas[n])



xx = np.linspace(0, 1/(beta-1), 1000)
def GenVals(xx, f):
    return [f(x) for x in xx]



# a = alphas[1]
# b = alphas[2]
# for alph in np.linspace(1/beta + 3/4* length, 1/beta + 7/8* length):
#     alphas = [1/beta + 1/4 * length, 1/beta + 1/2* length,alph]
#     list_maps = [(lambda x : Einv(x, alpha=alpha)) for alpha in alphas]
#     # for p in np.linspace(0,1/3,10):
#         # print(quad(lambda x: MixPRec(x,f, list_maps, [p,p,1-2*p], 3, beta=beta), a, b))
#     plt.plot(xx, GenVals(xx, lambda x: MixPRec(x,f, list_maps, [p,1-2*p,p], 1, beta=beta)))


plt.figure()
# for al in alphas:
#     plt.plot(xx,GenVals(xx,lambda x:Eforw(x,alpha = al))) 
#     plt.show()
# for i in range(l):
#     plt.plot(xx,GenVals(xx,lambda x: Maps(x,i))) 
#     plt.show()

AntiMapsTL = lambda x, n: Einv(x, alpha = [1/beta,1/(beta*(beta-1))][n])

# print(probs_diff,q_probs_diff)

Pp = lambda f: MixP(f, AntiMaps, probs)
Pq = lambda f: MixP(f, AntiMaps, q_probs)

p=0.5


PTinv = lambda f : P(f, Tinv)
k = 3

print(alphas[0], alphas[-1])
print(quad(lambda x: Iterate(Pp, k)(f)(x), alphas[0], alphas[-1]))
print(quad(lambda x: Iterate(Pq, k)(f)(x), alphas[0], alphas[-1]))

# plt.plot(xx, GenVals(xx, lambda x: Iterate(Pp, k)(f)(x)))

# plt.plot(xx, GenVals(xx, lambda x: Iterate(Pq, k)(f)(x)))
# plt.show()

# for p in np.linspace(0,1, 10):
#     PTLinv = lambda f: MixP(f, AntiMapsTL, [p,1-p])
#     print(quad(lambda x: Iterate(PTLinv, k)(f)(x), 1/beta, 1/(beta*(beta-1))))

#     plt.plot(xx, GenVals(xx,lambda x: Iterate(PTLinv, k)(f)(x)))
# plt.show()