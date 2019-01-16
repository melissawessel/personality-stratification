import numpy as np
import pandas as pd
import pylab as plt
from scipy.spatial.distance import euclidean,cdist

p = pd.DataFrame(np.load('Pascal_clusters_Nc15_fa_normed_1.npy'),
                columns=['N','E','O','A','C'])
g = pd.read_csv('Gerlach_clusters.csv',index_col=0)

plt.scatter(['N','E','O','A','C'],p.iloc[3], marker='o', color='g',
            facecolors='w',s=50)
plt.scatter(['N','E','O','A','C'],g.loc['Reserved'], marker='o', color='g',s=50)
plt.ylim(-1.25,1.25)
plt.hlines(y=0,xmin='N',xmax='C',linestyles='dashed')

plt.savefig('figRes_noerr.png')
