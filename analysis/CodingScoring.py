import os,sys
import pandas as pd
import numpy as np
from scipy import stats

def scoreTIPI(df):
    # slice out TIPI section
    dfTIPI = df[['E+','A-','C+','S-','O+','E-','A+','C-','S+','O-']]
    # code
    dfTIPI = dfTIPI.replace(['Disagree strongly','Disagree moderately',
                            'Disagree slightly','Neither agree nor disagree',
                            'Agree slightly','Agree moderately','Agree strongly'],
                            [1,2,3,4,5,6,7])
    #  reverse code
    dfTIPI[['A-','S-','E-','C-','O-']] = 8-dfTIPI[['A-','S-','E-','C-','O-']]
    # score
    TIPI_scored = pd.DataFrame()

    for trait in ['O','C','E','A','S']:
        TIPI_scored[trait] = (dfTIPI['%s+'%trait]+dfTIPI['%s-'%trait])/2

    return TIPI_scored

def normTIPI(df):
    # slice out TIPI section
    dfTIPI = df[['O','C','E','A','S']]

    filename = 'data/External/TIPInorms.csv'
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),filename)
    TIPInorms = pd.read_csv(filepath, index_col=0)
    arrTIPInorms = TIPInorms[['Openness','Conscientiousness','Extraversion',
                            'Agreeableness','Emotional Stability']].values
    arrTIPI = dfTIPI.values

    N_,D_ = np.shape(arrTIPI)
    for d in range(D_):
        x_tmp = arrTIPI[:,d]
        x_mu = arrTIPInorms[0][d]
        x_std = arrTIPInorms[1][d]
        arrTIPI[:,d] = (x_tmp - x_mu)/x_std

    return pd.DataFrame(arrTIPI, columns=['O','C','E','A','S'])

def codeGender(df):
    df['GenderCode']=0
    female = ['Female','F','f','female','FEMALE','Girl','Female ','female ','Woman','woman','femail','Femail',
         'femal','Femal','Females']
    male = ['Male','male','M','m','Male ','MALE','Make', 'Man',' Male','male ']
    df['GenderCode'][df['Gender'].isin(female)] = 1
    df['GenderCode'][df['Gender'].isin(male)] = 2
    return df['GenderCode']

def stratTIPI(df,n_strat):
    if(n_strat==3):
        for trait in ['O','C','E','A','N']:
            df['%s_strat'%trait]=0
            df['%s_strat'%trait].loc[df[trait]<-1] = -1
            df['%s_strat'%trait].loc[df[trait]>1] = 1
#            df['%s_strat'%trait].loc[df['%s_strat'%trait]==0] = 2
    if(n_strat==2):
        for trait in ['O','C','E','A','N']:
            df['%s_bistrat'%trait]=0
            df['%s_bistrat'%trait].loc[df[trait]<0] = -1
            df['%s_bistrat'%trait].loc[df[trait]>0] = 1
    return df

# not mine
def getCronbachAlpha(itemscores):
    itemscores = np.asarray(itemscores)
    itemvars = itemscores.var(axis=1, ddof=1)
    tscores = itemscores.sum(axis=0)
    nitems = len(itemscores)

    return nitems / (nitems-1.) * (1 - itemvars.sum() / tscores.var(ddof=1))
