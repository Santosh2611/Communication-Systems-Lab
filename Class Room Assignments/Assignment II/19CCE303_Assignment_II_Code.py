binary_data = [1,0,0,1,0,1,1,1,0,1,1,0]
print("\nBinary Data Sequence, {dk}: ", binary_data)

# Precodes it for a duobinary pulse transmission system to produce the sequence, {pk}: -
pn =[]; pn.append(0); m = 2
for i in range(len(binary_data)):
    pn.append((binary_data[i] - pn[i]) % m)
print("Precoded and Produced Sequence, {pk}: ", pn)

# Maps the precoded sequence into the transmitted amplitude levels, {ak}: -
an = []
for i in range(0,len(pn)):
    an.append(2*pn[i] - (m-1))
print("Transmitted Amplitude Levels, {ak}: ", an)

# Received noise-free sequences, {bk}: -
bn = []
for i in range(1,len(pn)):
    bn.append(an[i] + an[i-1])
print("Received Noise-Free Sequences, {bk}: ", bn)

# Recover the original data sequence: -
dn = []
for i in range(len(bn)):
    dn.append(int((((bn[i]/2) + (m-1)) % m)))
print("Recovered Original Data Sequence: ", dn)
