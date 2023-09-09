import pandas as pd
from matplotlib import pyplot as plt, font_manager

import pynimate as nim
import matplotlib
from matplotlib.font_manager import FontProperties
import os

matplotlib.use("TkAgg")


merged_data = pd.read_csv('m.csv')
merged_data = merged_data.set_index('time')
print(merged_data)

plt.rcParams['font.sans-serif']=['SimHei']

ip_freq = None
cnv = nim.Canvas()
bar = nim.Barplot(merged_data, "%Y-%m-%d", "1m")
bar.set_time(callback=lambda i, datafier: datafier.data.index[i].strftime("%b, %Y"))
cnv.add_plot(bar)
cnv.animate()
plt.show()
print(merged_data)
# df = pd.DataFrame(
#     {
#         "time": ["1960-01-01", "1961-01-01", "1962-01-01"],
#         "Afghanistan": [100000, 200000, 300000],
#         "Angola": [200000, 300000, 400000],
#         "Albania": [100000, 200000, 500000],
#         "USA": [500000, 300000, 400000],
#         "Argentina": [100000, 400000, 500000],
#     }
# ).set_index("time")
#
# cnv = nim.Canvas()
# bar = nim.Barhplot.from_df(df, "%Y-%m-%d", "2d")
# bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
# cnv.add_plot(bar)
# cnv.animate()
# plt.show()