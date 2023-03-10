import pandas as pd
import numpy as np
import openpyxl


xx = pd.read_excel("./uniqZdr.xlsx")
yy = pd.read_excel("./Zdr.xlsx").dropna(axis = 1, how = 'all')

xx.shape
yy.shape
yy.head

df = pd.merge(xx, yy)
df.shape
df.to_excel("./df.xlsx")

df1 = pd.DataFrame(columns=['A', 'B', 'A', 'C', 'C', 'A'], index=range(4))
df2 = pd.DataFrame(np.arange(24).reshape(4,6), columns=['A', 'B', 'C', 'D', 'E', 'F'])

df1
df2

df1.update(df2.reindex(df1.columns, axis=1))

print(df1)