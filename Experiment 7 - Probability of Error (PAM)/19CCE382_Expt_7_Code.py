import matplotlib.pyplot as plt # Provides an implicit way of plotting
import numpy as np # Support for large, multi-dimensional arrays and matrices
import math # Provides access to the mathematical functions defined by the C standard

t = []
xt = np.random.normal(0, 1, 10000)
for i in range(len(xt)):
    if i>0.5:
        t.append(i)
    elif i<=0.5:
        t.append(0)

y = []
for i in t:
    if i==0:
        y.append(1)
    else:
        y.append(-1)

x = np.arange(0, len(y), 1); plt.step(x, y)
plt.xlim(0, 100); plt.show()

l = p = []
for num in range(1,11):
    
    final = error = rt = []
    sigma = (10*10**(-num/10)/2)
    print("\n" + str(num) + " - Sigma Value: " + str(sigma))
    
    noise = np.random.normal(0,sigma,10000)
    count, bins, ignored = plt.hist(noise, 1000, density=True)
    plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
    plt.show()
    
    rt = y + noise    
    plt.plot(rt); plt.title("Signal with Noise")
    plt.xlim(0,100); plt.show()
    
    for i in range(len(rt)):
        if rt[i]>0:
            final.append(1)
        else:
            final.append(-1)
    
    error_count = 0
    for i in range(len(rt)):
        if final[i] != y[i]:
            error_count += 1
    print("    Error Count: " + str(error_count)); error.append(error_count)
    
    plt.stem(final)
    plt.xlabel("Sequence"); plt.ylabel("Ampltiude"); plt.title("Demodulated Signal")
    plt.xlim(0,100); plt.show()
    
    for i in range(len(error)):
        l.append(error[i]/10000)
    p.append(math.erfc(np.sqrt(num)*np.sqrt(2))) # Returns the complementary error function of a number
    
plt.semilogx(p); plt.semilogy(l)
plt.xlabel("SNR in dB"); plt.ylabel("Probability of Error (PAM)")
plt.show()
