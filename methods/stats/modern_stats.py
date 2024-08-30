import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from scipy.stats import linregress



os.chdir("../..")

modern_data = pd.read_csv('data/modern/NPacific_modern_02.csv')

fig, ax = plt.subplots(
)

selected_modern_data = modern_data.loc[(modern_data.Depth > 1010) & (modern_data.Depth < 5000)]

ax.scatter(selected_modern_data.d18O, selected_modern_data.Depth)
ax.set(xlabel='d18O', ylabel='Depth', ylim = [0, 4500])
ax.invert_yaxis()

result = linregress(selected_modern_data.Depth, selected_modern_data.d18O)

y = np.arange(1000, 5000, 1)
x = y * result.slope + result.intercept

x_min = y * (result.slope - result.stderr) + (result.intercept - result.intercept_stderr)
x_max = y * (result.slope + result.stderr) +  (result.intercept + result.intercept_stderr)



ax.plot(x, y)
ax.fill_betweenx(y, x_min, x_max, alpha=0.2)

print(result.slope * 1000, result.stderr * 1000)
print(result)

print(selected_modern_data.d18O.mean())  # -0.10846153846153846
print(selected_modern_data.d18O.std())  # 0.035365536244289494

print(selected_modern_data.d18O.mean() - (2 * selected_modern_data.d18O.std()), selected_modern_data.d18O.mean() + (2 * selected_modern_data.d18O.std()))


plt.show()