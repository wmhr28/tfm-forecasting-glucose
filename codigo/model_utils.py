import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codigo
from codigo import utils
from sklearn import metrics

def GenDataSet(df,features,pacientesId,min,train_share,val_share,lag,n_ahead,scalerHours,scalerMin,scalerGlucosa,scalerPodId,scalerLevelId,fillNullData=True): 
    
    dfCopy = df.copy()

    dfGen=pd.DataFrame()

    array_Xtrain=np.reshape([], (0, lag, len(features)))
    array_Ytrain=np.reshape([], (0,1))

    array_Xval=np.reshape([], (0, lag, len(features)))
    array_Yval=np.reshape([], (0,1))

    array_Xtest=np.reshape([], (0, lag, len(features)))
    array_Ytest=np.reshape([], (0,1))

    strMin=str(min)+'min'
    
    for pacienteID in pacientesId: 
        data=utils.getDataPatient(dfCopy,pacienteID,strMin,False)

        data['level_label'] = data['Glucose level'].apply(utils.label_LevelBG)         
        data['level_id'] = data['level_label'].apply(utils.id_LevelBG)        
        data['level_id'] = scalerLevelId.transform(data[['level_id']].values)
        data['Glucose level'] = scalerGlucosa.transform(data[['Glucose level']].values) 
        if(fillNullData):
            data=utils.fillNullData(data,'interpolate_linear')

        data=utils.generateNewColumns(data,scalerHours,scalerMin)
        data['pod_id'] = scalerPodId.transform(data[['pod_id']].values)  

        select_data=data[features].to_numpy()
        
        if(len(data['Glucose level'])>=lag):
            X, Y = create_X_Y(select_data, lag=lag, n_ahead=n_ahead)
            
            Xtrain, Ytrain = X[0:int(X.shape[0] * train_share)], Y[0:int(X.shape[0] * train_share)]
            Xval, Yval = X[int(X.shape[0] * train_share):int(X.shape[0] * val_share)], Y[int(X.shape[0] * train_share):int(X.shape[0] * val_share)]
            Xtest, Ytest = X[int(X.shape[0] * val_share):], Y[int(X.shape[0] * val_share):]

            array_Xtrain=np.concatenate((array_Xtrain, Xtrain))
            array_Ytrain=np.concatenate((array_Ytrain, Ytrain))

            array_Xval=np.concatenate((array_Xval, Xval))
            array_Yval=np.concatenate((array_Yval, Yval))

            array_Xtest=np.concatenate((array_Xtest, Xtest))
            array_Ytest=np.concatenate((array_Ytest, Ytest))

            dfGen = pd.concat([dfGen, data[features]])
    
    return dfGen,array_Xtrain,array_Ytrain,array_Xval,array_Yval,array_Xtest,array_Ytest

#using the MachineLearningMastery formula for splitting up the dataset to predictors and target
#reference: https://towardsdatascience.com/single-and-multi-step-temperature-time-series-forecasting-for-vilnius-using-lstm-deep-learning-b9719a0009de
def create_X_Y(ts: np.array, lag=1, n_ahead=1, target_index=0) -> tuple:
    """
    A method to create X and Y matrix from a time series array for the training of 
    deep learning models 
    """
    # Extracting the number of features that are passed from the array 
    n_features = ts.shape[1]
    
    # Creating placeholder lists
    X, Y = [], []

    if len(ts) - lag <= 0:
        X.append(ts)
    else:
        for i in range(len(ts) - lag - n_ahead):
            Y.append(ts[(i + lag):(i + lag + n_ahead), target_index])
            X.append(ts[i:(i + lag)])

    X, Y = np.array(X), np.array(Y)

    # Reshaping the X array to an LSTM input shape 
    X = np.reshape(X, (X.shape[0], lag, n_features))

    return X, Y

def predictionOverPrediction(Xtest,model):
    test_predictions = []

    current_batch = Xtest[0]
    current_batch=current_batch.reshape((1, Xtest.shape[1], Xtest.shape[2]))
    for i in range(len(Xtest)):
        # get the prediction value for the first batch
        current_pred = model.predict(current_batch)[0][0]

        # append the prediction into the array
        test_predictions.append(current_pred) 

        # use the prediction to update the batch and remove the first value
        if(Xtest.shape[2]>1):
            current_batch = np.append(current_batch[:,1:,:],[[np.append(current_pred,Xtest[i][Xtest.shape[1]-1][1:])]],axis=1)
        else:
            current_batch = np.append(current_batch[:,1:,:],[[[current_pred]]],axis=1)        
    return test_predictions

def modelEvaluateTraining(model,history,Xtest, Ytest):
    results = model.evaluate(Xtest, Ytest)
    print("test loss, test acc:", results)
    hist=history.history
    loss_per_epoch =hist['loss']
    plt.plot(range(len(loss_per_epoch)),loss_per_epoch)
    plt.show()
    
    plt.plot(hist['loss'], label='Training loss')
    plt.plot(hist['val_loss'], label = 'Validation loss')
    plt.legend()
    plt.show()    
    
    
    plt.plot(hist['mae'], label='Training Mae')
    plt.plot(hist['val_mae'], label = 'Validation Mae')
    plt.legend()
    plt.show()

def forecast_accuracy(forecast, Ytest):
    mae=metrics.mean_absolute_error(Ytest, forecast)
    mse=metrics.mean_squared_error(Ytest, forecast, squared=False)
    rmse=metrics.mean_squared_error(Ytest, forecast, squared=True)
    return({'mae': mae,'mse': mse,  'rmse':rmse})

def plotPredicted(yhat,Ytest):
    pred_n_ahead = pd.DataFrame(yhat)
    actual_n_ahead = pd.DataFrame(Ytest)

    plt.figure(figsize=(15, 8))
    plt.plot(pred_n_ahead, color='C0', marker='o', label='Predicted')
    plt.plot(actual_n_ahead, color='C1', marker='o', label='True', alpha=0.6)
    plt.title('Predicted vs True')
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.legend()
    plt.show()

