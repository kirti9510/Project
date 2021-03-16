from mapping import map_feat
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
def test(mo,y_test_attack):
  test_set = pd.read_csv('Training and Testing Datasets/testing.csv')
  x_columns = pd.read_csv('Training and Testing Datasets/x_columns.csv')
  x = x_columns.to_numpy()
  min_max_scaler = MinMaxScaler()
  fit_x = min_max_scaler.fit(x)
  test_samples = test_set.to_numpy()
  test_sam = fit_x.transform(test_samples)
  testing = test_sam.reshape(test_sam.shape[0], 11, 11, 1)
  rounded=np.argmax(y_test_attack, axis=1)
  from sklearn.metrics import classification_report, confusion_matrix
  y_pred = mo.predict_classes(testing)
  np.savetxt('expected_t.txt', rounded, fmt='%01d')
  np.savetxt('predicted_t.txt', y_pred, fmt='%01d')
  mo.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
  loss, accuracy = mo.evaluate(testing, y_test_attack)
  st.write("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
  st.write(confusion_matrix(rounded,y_pred))
  st.write(classification_report(rounded, y_pred))