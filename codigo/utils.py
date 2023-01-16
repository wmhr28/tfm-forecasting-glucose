import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import matplotlib.dates as md
import random

def getDataPatient(df,id,frequency='15min',includeID=False,includeDate=False,resample=True):
    dfCopy = df.copy()
    ret = dfCopy[dfCopy['ID'] == id]
    
    ret.index = pd.to_datetime(ret.Date)
    if(resample):
        ret= ret.resample(frequency).mean()
    if(includeID):
        ret['ID']=id
    
    if(includeDate):
        ret['Date']=ret.index
    
    return ret
    
def setMasking(x,glucose):
    if(glucose==-1):
        return -1
    else:
        return x


def generateNewColumns(df,scalerLevelId,scalerHours,scalerMin,scalerPodId,scalerGlucose,normalized=True):
    ret = df.copy() 
    
    ret['level_label'] = ret['Glucose level'].apply(label_LevelBG)         
    ret['level_id'] = ret['level_label'].apply(id_LevelBG)      
    
    ret['hour']=ret.index.hour
    
    ret['min']=ret.index.minute        
    
    ret['pod_label'] = ret['hour'].apply(label_partOfDay)
    ret['pod_id'] = ret['pod_label'].apply(id_partOfDay)    

    if(normalized):
        ret['level_id'] = scalerLevelId.transform(ret[['level_id']].values)
        ret['hour'] = scalerHours.transform(ret[['hour']].values)
        ret['min'] = scalerMin.transform(ret[['min']].values)    
        ret['pod_id'] = scalerPodId.transform(ret[['pod_id']].values)      
        ret['Glucose level'] = scalerGlucose.transform(ret[['Glucose level']].values)  
        
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
    ## target range (e.g., 70–180 mg/ dL)
    if  (x <= 70):
        resp= 'hypoglycemia'
    elif (x >= 180 ):
        resp= 'hyperglycemia'
    else: 
        resp= 'euglycemia'
    return resp;
    
def id_LevelBG(x):
    if (x=='hypoglycemia'):
        resp= -1;
    elif (x=='hyperglycemia'):
        resp= 1;
    elif (x=='euglycemia'):
        resp= 0;
    return resp;

def id_LevelBG_transform(x):
    if (x==-1):
        return 'hypoglycemia';
    elif (x==1):
        return 'hyperglycemia';
    elif (x==0):
        return 'euglycemia';

def id_LevelBG_inverse_transform(x,scaler):
    x=int(inverse_transformScaler(x,scaler))
    if (x==-1):
        return 'hypoglycemia';
    elif (x==1):
        return 'hyperglycemia';
    elif (x==0):
        return 'euglycemia';
        
def plotRangeDates(df,ObjRangeDateStart,ObjRangeDateEnd):
    df.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(figsize=(20, 10))
    
def plotTwoDf(df1,df2,ObjRangeDateStart,ObjRangeDateEnd):
    ax = df1.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(color='red', marker='.', linestyle='dotted')
    df2.loc[ObjRangeDateStart:ObjRangeDateEnd].plot(ax=ax,color='blue', marker='.',figsize=(20, 10))

def genDataset(df,pacientesId,min,includeID,includeDate):
    dfCopy = df.copy()
    dfGen=pd.DataFrame()
    strMin=str(min)+'min'
    for pacienteID in pacientesId:         
        data=getDataPatient(dfCopy,pacienteID,strMin,includeID,includeDate)        
        dfGen = pd.concat([dfGen, data])
    return dfGen
def plotDayAllPatients(df,pacientesId,title,plt,date):
    dfCopy = df.copy()    
    
    plt.figure(figsize=(10, 5), dpi=150)
    plt.axhline(y=69, color='black', linestyle=':')
    plt.axhline(y=181, color='black', linestyle=':')
    eventosFijos=[' 04:00:00',' 08:00:00',' 13:30:00',' 19:00:00',' 23:00:00']
    for evento in eventosFijos: 
        plt.axvline(pd.Timestamp(date+evento), color='black', linestyle=':') 
    for pacienteID in pacientesId:
        dfCopy[dfCopy['ID'] == pacienteID]['Glucose level'].plot(label=pacienteID)
    ax = plt.gca()
    ax.xaxis.set_major_locator(md.HourLocator(interval = 1))
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
    plt.title(title)    
    plt.legend()
    plt.show()
    
def restarMinutos(strDatetime,formato,minutos):
    datetime_object = datetime.strptime(strDatetime, formato)
    totalMin = timedelta(minutes=minutos)
    return (datetime_object-totalMin).strftime(formato)

def downsamplingByLabel(X,Y,Y_label,percent,obj_label,debug=False,minLen=0):
    if(debug):
        print('DEBUGING')
    filtered = [item for item in Y_label if item==obj_label] 
    lenFilter=len(filtered)
    if(debug):
        print('lenFilter',lenFilter)

    if(percent>1):
        return X, Y,Y_label

    if(minLen>0):
        r_times=lenFilter-minLen
    else:
        r_times=int(lenFilter*percent)
    
    if(debug):
        print('r_times',r_times)
    i = 0
    index=0
    while i < r_times:  
        lenX=len(X)-1              
        irandom = random.randint(0,3)
        index+=irandom        
        if(debug):            
            print('irandom ',irandom) 
            print('index ',index)   
        
        if(index<=lenX):          
            if(Y_label[index]==obj_label):                            
                if(debug):
                    print('SI')  
                X=np.delete(X, index, 0)
                Y=np.delete(Y, index, 0)
                Y_label=np.delete(Y_label, index, 0)
                i += 1               
            else:
                if(debug):
                    print('NO, segundo intento') 
                    print('index ',index)  
                index+=1
                if(index<=lenX):
                    if(Y_label[index]==obj_label):                            
                        if(debug):
                            print('SI')  
                        X=np.delete(X, index, 0)
                        Y=np.delete(Y, index, 0)
                        Y_label=np.delete(Y_label, index, 0)   
                        i += 1
                    else:                        
                        if(debug):
                            print('NO')  
                else:
                    if(debug):
                        print('FUERA DE RANGO')
                        index=0      
        else:
            if(debug):
                print('FUERA DE RANGO')
                index=0

    return X, Y,Y_label