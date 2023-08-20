import numpy
import random
import pandas as pd

number = 1000000

names = ['Alexander','Benjamin','Charlotte','David','Emily','Fiona','Gabriel','Hannah','Isabella','Katherine','Nathan','Penelope','Rachel','Taylor','Ulysses','Victoria','William','Xander','Yasmine', 'Zachary']
names = random.choices(names, k = number)
ages = numpy.random.randint(1, 60, number)
heights = numpy.random.randint(120, 200, number)
foot = numpy.random.randint(35, 47, number)
english = random.choices(['A1', 'A2', 'A2+', 'B1', 'B2', 'B2+', 'C1', 'C2'], k = number)
columns = ['names', 'ages', 'heights', 'foot', 'english']
dict = {'id': list(range(1000000)),
       'names': names,
       'ages': ages,
       'heights': heights,
       'foot': foot,
       'english': english}
df = pd.DataFrame(dict)
#df.to_csv('data.csv', sep = ',', encoding = 'utf-8')

df = pd.read_csv('data.csv', index_col = 0)
lists = df.values.tolist()
print(lists)