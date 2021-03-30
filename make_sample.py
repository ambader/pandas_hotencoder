import numpy as np
import pandas as pd

num = np.random.randint(5, size=100)
fruit = ["Apple","Banana","Strawberry","Raspberry","Kumquat"]
fruits = []
for i in num:
    fruits.append(fruit[i])
weight = np.round(np.random.rand(100)*100,2)
df = pd.DataFrame(columns=["fruit","weight"])
df.fruit = fruits
df.weight = weight
df.to_csv("sample.csv",index=False)
