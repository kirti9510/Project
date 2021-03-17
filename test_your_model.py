from mapping import map_feat
import streamlit as st
import pandas as pd 
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Convolution1D, MaxPooling1D, Flatten, Dropout, Convolution2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from tensorflow.keras.models import load_model
x_columns = pd.read_csv('Training and Testing Datasets/x_columns.csv')
x = x_columns.to_numpy()
min_max_scaler = MinMaxScaler()
fit_x = min_max_scaler.fit(x)
def packet_test(pass_input, pass_mo):
	sample_list = pass_input.columns.tolist()
	del sample_list[-1]
	trace = [] 
	trace = sample_list
	from operator import itemgetter 
	b = [1, 2, 3]
	a = itemgetter(*b)(trace)
	del trace[1:4] 
	L = trace
	modified_L = map_feat(L,a)
	sample_numpy = np.array(modified_L).reshape(1,-1)
	print(sample_numpy.shape)
	print(x.shape)
	sample_norm = fit_x.transform(sample_numpy)
	check_sam = np.array(sample_norm).reshape(1,11,11,1)
	y_pred = (pass_mo.predict(check_sam) > 0.5).astype("int32")
	return y_pred