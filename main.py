import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_ema(fileValue, number, index):
    alpha = 2/(number+1)
    numerator = fileValue[index]
    denominator = 1
    iterator = 1
    for j in range(index+number-1, index-1, -1):
        factor = (1-alpha)**(iterator)
        numerator += factor*fileValue[j]
        denominator += factor
        iterator += 1
    return numerator/denominator

file = pd.read_csv("wig20g.csv")
floatValues = []
macdValues = []
signalValues = []
fund = 1000
stocks = 0
for i in range(1035):
    floatValues.append(file['Otwarcie'][i])
for i in range(1009):
    macdValues.append(get_ema(floatValues, 13, i+13)-get_ema(floatValues, 26, i))
for i in range(1000):
    signalValues.append(get_ema(macdValues, 9, i))
for i in range(9):
    macdValues.pop()


xtab = []
for i in range(1000):
    xtab.append(i)

positive = True
if macdValues[0] - signalValues [0] < 0:
    positive = False
intersectionpointsxSELL = []
intersectionpointsxBUY = []
intersectionpointsySELL = []
intersectionpointsyBUY = []
for i in range(1, 1000):
    if positive == True and macdValues[i] - signalValues [i] < 0:
        stocks += fund / floatValues[i + 25]
        fund = 0
        positive = False
        intersectionpointsxSELL.append(i)
        intersectionpointsySELL.append((macdValues[i]+signalValues[i])/2)
    elif positive == False and macdValues[i] - signalValues[i] > 0:
        if fund != 10000:
            fund += stocks * floatValues[i + 25]
            stocks = 0
        positive = True
        intersectionpointsxBUY.append(i)
        intersectionpointsyBUY.append((macdValues[i]+signalValues[i])/2)

if fund == 0:
    fund += stocks*floatValues[1034]
    stocks = 0

for i in range(0, 35):
    floatValues.pop()

print(f"Funds: {fund}")
print(f"Stocks: {stocks}")
x = np.array(xtab)
for i in range(0, len(intersectionpointsxSELL)):
    intersectionpointsySELL[i] = floatValues[intersectionpointsxSELL[i]]
for i in range(0, len(intersectionpointsxBUY)):
    intersectionpointsyBUY[i] = floatValues[intersectionpointsxBUY[i]]


plt.plot(x, floatValues, '-', label="stock")
plt.scatter(intersectionpointsxBUY, intersectionpointsyBUY, label="buy points", color="green", s=15, zorder=3)
plt.scatter(intersectionpointsxSELL, intersectionpointsySELL, label="sell points", color="red", s=15, zorder=3)
plt.ylabel("Values")
plt.xlabel("Dni")
plt.legend(bbox_to_anchor=(1.1, 1.15), loc='upper right')

plt.show()