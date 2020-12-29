from test_your_model import packet_test
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from tensorflow.keras.layers import Dense, Activation, Convolution1D, MaxPooling1D, Flatten, Dropout, Convolution2D, MaxPooling2D
from tensorflow.keras.models import load_model
import numpy as np

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""CNN Detector"""
	from tensorflow.keras.models import load_model
	mo = Sequential()
	mo.add(Convolution2D(20, 4, padding="valid",activation="relu",input_shape=(11,11,1)))
	mo.add(MaxPooling2D(pool_size=2, strides=2))
	mo.add(Convolution2D(10, 3, padding="valid",activation="relu"))
	mo.add(MaxPooling2D(2, 2))
	mo.add(Flatten())
	mo.add(Dense(50, activation="relu"))
	mo.add(Dropout(0.2))
	mo.add(Dense(20, activation="relu"))
	mo.add(Dropout(0.2))
	mo.add(Dense(2, activation="softmax"))
	mo.compile(loss="binary_crossentropy", optimizer="adam",metrics=['accuracy'])
	mo.load_weights("Models/cnn_conv2d.h5")
	#prediction = mo.predict((check_sam))
	x = pd.DataFrame()
	y = pd.DataFrame()
	st.title("CNN Detector!")
	menu = ["Home","Login","SignUp","Profiles"]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Home":
		st.subheader("Home")
		st.write("Hey *There!!!*:sunglasses:")
		st.write(" ### Go to Menu to proceed furthuer!")
	elif choice == "Login":
		st.subheader("Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Get into the software",["Dataset details and Pre-processed output","Analyze Training Phase","Lets check the Detector"])
				if task == "Dataset details and Pre-processed output":
					st.subheader('Dataset')
					st.write('NSL-KDD')
					input_df = pd.read_csv('Samples and Details/Sample NSL-KDD.csv')
					st.write(' ### Sample NSL-KDD')
					st.write(input_df)
					st.write('Features')
					fea = pd.read_csv('Samples and Details/fea.csv')
					st.write(' ### The Features Set')
					st.write(fea)
					st.markdown("""[NSL-KDD loaded from here!](https://www.unb.ca/cic/datasets/nsl.html)""")
					pre = st.button('Pre-processing Results')
					if pre:
						st.write(' ### Pre-processed features set (5 rows)')
						x_head = pd.read_csv('Samples and Details/x.csv')
						st.write(x_head)
						st.write(' ### Pre-processed label set (5 rows)')
						y_head = pd.read_csv('Samples and Details/y.csv')
						st.write(y_head)
				elif task == "Analyze Training Phase":
					st.subheader("Will observe Training Phase now")
					train_model = st.button('Analyze the Training')
					if train_model:
						st.balloons()
						x_des = pd.read_csv('Samples and Details/x_des.csv')
						st.write(' ### x (Features) Description')
						st.write(x_des)
						y_des = pd.read_csv('Samples and Details/y_des.csv')
						st.write(' ### y (Labels) Description')
						st.write(y_des)
				elif task == "Lets check the Detector":
					st.subheader("Test the Model")
					test_attack = st.button('Test attack sample')
					test_normal = st.button('Test normal sample')
					if test_attack:
						input_df = pd.read_csv('Training and Testing Datasets/Attack sample.csv')
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[0 1]]':
							st.success('Its normal')
						else:
							st.warning('Its an attack')
					if test_normal:
						input_df = pd.read_csv('Training and Testing Datasets/Normal sample.csv')
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[0 1]]':
							st.success('Its normal')
						else:
							st.warning('Its an attack')
					upload_file = st.sidebar.file_uploader("Upload your input CSV file (single row)", type=["csv"])
					if upload_file is not None:
						input_df = pd.read_csv(upload_file)
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[0 1]]':
							st.success('Your packet is normal')
						else:
							st.warning('Your packet is attack')
			else:
				st.warning("Incorrect Username/Password")
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
	elif choice == "Profiles":
		st.subheader("Below mentioned users are signed up here:")
		user_result = view_all_users()
		clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
		st.dataframe(clean_db)


if __name__ == '__main__':
	main()