import streamlit as st
from mapping import map_feat
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
def test_1(mo):
	traindata = pd.read_csv('Training and Testing Datasets/Modified Train.csv')
	x_columns = pd.read_csv('Training and Testing Datasets/x_columns.csv')
	oh_train_x = pd.get_dummies(traindata, columns = ['protocol_type', 'service', 'flag'])
	oh_train_y = pd.get_dummies(traindata['attack_type'])
	x_columns = oh_train_x.drop(columns=['attack_type'])
	x = x_columns.to_numpy()

	outcomes = oh_train_y.columns
	num_classes = len(outcomes)
	y = oh_train_y.values
	min_max_scaler = MinMaxScaler()
	fit_x = min_max_scaler.fit(x)
	x = fit_x.transform(x)
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
	x_test = x_test.reshape(x_test.shape[0], 11, 11, 1)
	rounded_labels=np.argmax(y_test, axis=1)
	print(rounded_labels)
	from sklearn.metrics import classification_report, confusion_matrix
	y_pred = mo.predict_classes(x_test)

	np.savetxt('expected_tr.txt', rounded_labels, fmt='%01d')
	np.savetxt('predicted_tr.txt', y_pred, fmt='%01d')
	mo.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
	loss, accuracy = mo.evaluate(x_test, y_test)
	st.write("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
	st.write(confusion_matrix(rounded_labels,y_pred))
	st.write(classification_report(rounded_labels, y_pred))