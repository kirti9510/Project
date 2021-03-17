from test_your_model import packet_test
from test_analysis import test
from test_analysis_1 import test_1
import streamlit as st
import pandas as pd
from PIL import Image
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
	features = [
	'duration','src_bytes','dst_bytes','land','wrong_fragment','urgent','hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root','num_file_creations' ,
	'num_shells','num_access_files','is_host_login','is_guest_login','count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate',
	'srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate',
	'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate','protocol_type_icmp','protocol_type_tcp','protocol_type_udp','service_IRC','service_X11','service_Z39_50','service_aol',
	'service_auth','service_bgp','service_courier','service_csnet_ns','service_ctf','service_daytime','service_discard','service_domain','service_domain_u','service_echo','service_eco_i','service_ecr_i',
	'service_efs','service_exec','service_finger','service_ftp','service_ftp_data','service_gopher','service_harvest','service_hostnames','service_http','service_http_2784','service_http_443',
	'service_http_8001','service_imap4','service_iso_tsap','service_klogin','service_kshell','service_ldap','service_link','service_login','service_mtp','service_name','service_netbios_dgm',
	'service_netbios_ns','service_netbios_ssn','service_netstat','service_nnsp','service_nntp','service_ntp_u','service_other','service_pm_dump','service_pop_2','service_pop_3','service_printer',
	'service_private','service_red_i','service_remote_job','service_rje','service_shell','service_smtp','service_sql_net','service_ssh','service_sunrpc','service_supdup','service_systat','service_telnet',
	'service_tftp_u','service_tim_i','service_time','service_urh_i','service_urp_i','service_uucp','service_uucp_path','service_vmnet','service_whois','flag_OTH','flag_REJ','flag_RSTO','flag_RSTOS0',
	'flag_RSTR','flag_S0','flag_S1','flag_S2','flag_S3','flag_SF','flag_SH'
	  # 'class_anomaly
	  # 'class_normal
	]
	packet_head = pd.DataFrame(columns = features)
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
	mo.add(Dense(5, activation="softmax"))
	mo.compile(loss="categorical_crossentropy", optimizer="adam",metrics=['accuracy'])
	mo.load_weights("Models/cnn_conv2d.h5")
	#prediction = mo.predict((check_sam))
	x = pd.DataFrame()
	y = pd.DataFrame()
	st.title("IDS")
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
				task = st.selectbox("Get into the software",["Dataset details and Pre-processed output","Analyze Training Phase","Result Analysis","Lets check the Detector"])
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
						x_des = pd.read_csv('Samples and Details/x_des.csv')
						st.write(' ### x (Features) Description')
						st.write(x_des)
						y_des = pd.read_csv('Samples and Details/y_des.csv')
						st.write(' ### y (Labels) Description')
						st.write(y_des)
				elif task == "Result Analysis":
					st.subheader("Results")
					testdata = pd.read_csv('Training and Testing Datasets/Modified Test.csv')
					y_attack = pd.get_dummies(testdata['attack_type'])
					outcom = y_attack.columns
					num_class = len(outcom)
					y_test_attack = y_attack.values
					testdata = testdata.drop(columns=['attack_type'])
					testdata_list = testdata.values.tolist()
					print(len(testdata_list[0]))
					acc = Image.open('accuracy.PNG')
					st.image(acc, caption='Training v/s Validation Accuracy')
					loss = Image.open('loss.PNG')
					st.image(loss, caption='Training v/s Validation Loss')
					st.write("Training Results:")
					test_1(mo)
					st.write("Testing Results:")
					test(mo,y_test_attack)
				elif task == "Lets check the Detector":
					st.subheader("Test the Model")
					test_attack = st.button('Test attack sample')
					test_normal = st.button('Test normal sample')
					if test_attack:
						input_df = pd.read_csv('Training and Testing Datasets/Attack sample.csv')
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[1 0 0 0 0]]':
							st.warning('Its Denial of Service attack')
						if np.array_str(output) == '[[0 0 0 0 1]]':
							st.warning('Its User to Root attack')
						if np.array_str(output) == '[[0 0 1 0 0]]':
							st.warning('Its Probe attack')
						if np.array_str(output) == '[[0 0 0 1 0]]':
							st.warning('Its Root to Local attack')
					if test_normal:
						input_df = pd.read_csv('Training and Testing Datasets/Normal sample.csv')
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[0 1 0 0 0]]':
							st.success('Yes Its normal')
						else:
							st.warning('Its some type of attack')
					upload_file = st.sidebar.file_uploader("Upload your input CSV file (single row)", type=["csv"])
					if upload_file is not None:
						input_df = pd.read_csv(upload_file)
						output = packet_test(input_df, mo)
						if np.array_str(output) == '[[1 0 0 0 0]]':
							st.warning('Denial of Service packet')
						if np.array_str(output) == '[[0 0 0 0 1]]':
							st.warning('User to Root packet')
						if np.array_str(output) == '[[0 0 1 0 0]]':
							st.warning('Probe packet')
						if np.array_str(output) == '[[0 0 0 1 0]]':
							st.warning('Root to Local packet')
						if np.array_str(output) == '[[0 1 0 0 0]]':
							st.success('Normal')
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