import pandas as pd
import numpy as np

def getDataPatient(df,id,frequency='15min',includeID=False,includeDate=False):
    dfCopy = df.copy()
    ret = dfCopy[dfCopy['ID'] == id]
    
    ret.index = pd.to_datetime(ret.Date)
    
    ret= ret.resample(frequency).mean()
    if(includeID):
        ret['ID']=id
    
    if(includeDate):
        ret['Date']=ret.index
    
    return ret
def generateNewColumns(df,scalerHours,scalerMin):
    ret = df.copy()
    ret['Gt']=ret['Glucose level'].shift(1)
    ret['Gt+r']=ret['Glucose level']
    ret['Yt']=ret['Gt+r']-ret['Gt']
    ret['Gt'][0]=0
    ret['Yt'][0]=0
 
    ret['hour']=ret.index.hour
    ret['pod_label'] = ret['hour'].apply(label_partOfDay)
    ret['pod_id'] = ret['pod_label'].apply(id_partOfDay)

    ret['hour'] = scalerHours.transform(ret[['hour']].values)
    
    ret['min']=ret.index.minute    
    ret['min'] = scalerMin.transform(ret[['min']].values)    
    
        
    return ret
def transformScaler(x,scaler):
    return scaler.transform([[x]])[0][0]

def inverse_transformScaler(x,scaler):
    return scaler.inverse_transform([[x]])[0][0]

def fillNullData(df,fill_method):
    ret = df.copy()   
    if(fill_method=='-1'):
        ret['Glucose level']= ret['Glucose level'].fillna(-1)    
    if(fill_method=='ffill'):
        ret['Glucose level']= ret['Glucose level'].fillna(method='ffill')
    if(fill_method=='bfill'):
        ret['Glucose level']= ret['Glucose level'].fillna(method='bfill')
    if(fill_method=='interpolate_linear'):
        ret['Glucose level']= ret['Glucose level'].interpolate(method='linear')
        
    return ret

def label_partOfDay(x):
    if (x > 4) and (x <= 8):
        return 'Early Morning'
    elif (x > 8) and (x <= 12 ):
        return 'Morning'
    elif (x > 12) and (x <= 16):
        return 'Noon'
    elif (x > 16) and (x <= 20) :
        return 'Eve'
    elif ((x > 20) and (x <= 24) or x==1):
        return 'Night'
    elif (x <= 4):
        return 'Late Night'
    
def id_partOfDay(x):    
    if (x=='Early Morning'):
        resp= 1;
    elif (x=='Morning'):
        resp= 2;
    elif (x=='Noon'):
        resp= 3;
    elif (x=='Eve'):
        resp= 4;
    elif (x=='Night'):
        resp= 5;
    elif (x=='Late Night'):
        resp= 6;
    return resp;

def id_partOfDay_inverse_transform(x,scaler):   
    x=int(inverse_transformScaler(x,scaler))
    
    if (x==1):
        return 'Early Morning';
    elif (x==2):
        return 'Morning';
    elif (x==3):
        return 'Noon';
    elif (x==4):
        return 'Eve';
    elif (x==5):
        return 'Night';
    elif (x==6):
        return 'Late Night';
		
def label_LevelBG(x):
    if  (x < 70):
        return 'hypoglycemia'
    elif (x > 180 ):
        return 'hyperglycemia'
    else: 
        ## target range (e.g., 70–180 mg/ dL)
        return 'normal'
    
def id_LevelBG(x):
    if (x=='hypoglycemia'):
        resp= -1;
    elif (x=='hyperglycemia'):
        resp= 1;
    elif (x=='normal'):
        resp= 0;
    return resp;

def id_LevelBG_transform(x):
    if (x==-1):
        return 'hypoglycemia';
    elif (x==1):
        return 'hyperglycemia';
    elif (x==0):
        return 'normal';

def id_LevelBG_inverse_transform(x,scaler):
    x=int(inverse_transformScaler(x,scaler))
    if (x==-1):
        return 'hypoglycemia';
    elif (x==1):
        return 'hyperglycemia';
    elif (x==0):
        return 'normal';
        
def plotRangeDates(df,ObjRangeDateStart,ObjRangeDateEnd):
    df.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(figsize=(20, 10))
    
def plotTwoDf(df1,df2,ObjRangeDateStart,ObjRangeDateEnd):
    ax = df1.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(color='red', marker='.', linestyle='dotted')
    df2.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(ax=ax,color='blue', marker='.',figsize=(20, 10))