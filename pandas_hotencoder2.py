import numpy as np
import pandas as pd

def pandas_type(inp):
    if str(type(inp)) != "<class 'pandas.core.frame.DataFrame'>":
        print("Use pandas DataFrame")
        return False
    else:
        if np.any(inp.isnull()==True)==True:
            print("Your data is a mess")
            return False
        else:
            pass
    
def pandas_enc_str(inp,m_co_var=True):
    out = pd.DataFrame()
    zw = inp.astype
    try:
        zzw = zw.unique()
    except:
        zw = pd.Series(inp)
        zzw = zw.unique()
    if m_co_var == True:
        for i in zzw[1:]:
            try:
                bin_ = eval('zw=='+str(i)).replace({True : 1 , False : 0})
            except:
                bin_ = eval('zw=="'+str(i)+'"').replace({True : 1 , False : 0})
            out[i]=bin_
        return out
    else:
        for i in zzw:
            try:
                bin_ = eval('zw=='+str(i)).replace({True : 1 , False : 0})
            except:
                bin_ = eval('zw=="'+str(i)+'"').replace({True : 1 , False : 0})
            out[i]=bin_
        return out
    
def get_split_len(inp):
    nn1 = str(np.float32(np.mean(inp))-min(inp)).split(".")[0]
    nn2 = str(np.float32(min(inp))).split(".")[1]
    if nn1 != "0":
        return -len(nn1)+3
    else:
        return len(nn2)

def categorize_cat(inp,bins):
    nn = get_split_len(inp)
    leng = (max(inp)-min(inp))/bins
    cats = []
    for i in range(bins):
        cats.append(min(inp)+leng*(i+1))
    return np.around(cats,nn)

def categorize_(inp,bins):
    out = inp.values
    bins_ = categorize_cat(inp,bins)
    zw = np.ones(len(out))*bins_[0]
    for i in range(len(bins_[:-1])):
        for j in range(len(zw)):
            if out[j] > bins_[i]:
                zw[j]=bins_[i+1]
    return zw

def cat_str(inp):
    zw = pd.Series(inp)
    zzw = np.sort(zw.unique())
    cat_dic={}
    for i in range(1,len(zzw)-1):
        cat_dic.update({zzw[i] : str(zzw[i])+"-"+str(zzw[i+1])})
    cat_dic.update({zzw[-1] : "> "+str(zzw[-1])})
    cat_dic.update({zzw[0] : " <"+str(zzw[0])})
    return pd.Series(zw),cat_dic

def pandas_enc(inp,col,bins=5,m_co_var=True):
    out1 = inp[inp.columns[inp.columns!=col]]
    zw = inp[col]
    if pandas_type(inp)!=False:
        pass
    else:
        return None
    if zw.dtype==float:
        zw = categorize_(zw,bins)
        zw,cat_dic = cat_str(zw)
        out2 = pandas_enc_str(zw,m_co_var)
        out2 = out2[np.sort(out2.columns)]
        out2 = out2.rename(columns=cat_dic)
    elif zw.dtype==int:
        zw = categorize_(zw,bins)
        zw,cat_dic = cat_str(zw)
        out2 = pandas_enc_str(zw,m_co_var)
        out2 = out2[np.sort(out2.columns)]
        out2 = out2.rename(columns=cat_dic)
    elif zw.dtype==int:
        print("Specify: str or float")
    elif zw.dtype=="O":
        zw=str(col)+"_"+zw
        out2 = pandas_enc_str(zw,m_co_var)
    else:
        print("Strange dtype")
    return pd.concat([out1,out2], axis=1)

def pandas_multi_enc(inp,col,bins=5,m_co_var=True):
    out = inp.copy()
    for i in col:
        out = pandas_enc(out,str(i))
    return out
