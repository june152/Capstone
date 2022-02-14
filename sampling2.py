import random
import pandas as pd

p = 1.0  # 100% of the lines
df = pd.read_csv(
    '/data/label.csv',
    header=0,
    skiprows=lambda i: i > 0 and random.random() >= p
)
df.to_csv('/data/test_sample.csv')