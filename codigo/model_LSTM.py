import tensorflow as tf
from tensorflow import keras

from keras.models import Sequential
from keras.layers import Bidirectional,Dense, Dropout,InputLayer
from keras.layers import LSTM
from keras.optimizers import Adam

def modelLSTM_Gen(dim1,dim2):    
    model = Sequential()
    model.add(InputLayer( input_shape=(dim1,dim2)))
    model.add(LSTM(32, activation='relu', return_sequences = False))
    model.add(Dropout(0.2)) 
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model

def modelLSTM_Gen_nodrop(dim1,dim2):    
    model = Sequential()
    model.add(InputLayer( input_shape=(dim1,dim2)))
    model.add(LSTM(32, activation='relu', return_sequences = False))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model

def modelLSTM_Gen_Stacked(dim1,dim2):    
    model = Sequential()
    model.add(InputLayer( input_shape=(dim1,dim2)))
    model.add(LSTM(32, activation='relu', return_sequences = True))
    model.add(LSTM(32, activation='relu', return_sequences = False))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model

def modelLSTM_Gen_Stacked_nodrop(dim1,dim2):    
    model = Sequential()
    model.add(InputLayer( input_shape=(dim1,dim2)))
    model.add(LSTM(32, activation='relu', return_sequences = True))
    model.add(LSTM(32, activation='relu', return_sequences = False))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model


def modelLSTM_Gen_Bidirectional(dim1,dim2):    
    model = Sequential() 
    model.add(Bidirectional(LSTM(32, activation='relu', return_sequences = False), input_shape=(dim1,dim2)))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model

def modelLSTM_Gen_Bidirectional_nodrop(dim1,dim2):    
    model = Sequential()
    model.add(Bidirectional(LSTM(32, activation='relu', return_sequences = False), input_shape=(dim1,dim2)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer = Adam(learning_rate=0.001), loss='mse', metrics=['mae','mse'])
    return model
