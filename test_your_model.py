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

def pre_test(temp):
		trace = []
		trace = [val for sublist in temp for val in sublist]
		L=[]
		from operator import itemgetter 
		b = [1, 2, 3]
		a = itemgetter(*b)(trace)
		del trace[1:4] 
		L=trace
		modified_L = map_feat(L,a)
		#applying min_max_normalization
		LL=[]
		i=0
		for i in range(121):
			LL.append((float(modified_L[i]) - x_columns[features[i]].min())/(x_columns[features[i]].max() - x_columns[features[i]].min()))
		check_sam = np.array(LL).reshape(1,11,11,1)
		#Measure accuracy of single packet by loading the model (CNN)
		return check_sam
def packet_test(pass_input, pass_mo):
	temp = pass_input.values.tolist()
	testing_sample = pre_test(temp)
	y_pred = (pass_mo.predict(testing_sample) > 0.5).astype("int32")
	return y_pred