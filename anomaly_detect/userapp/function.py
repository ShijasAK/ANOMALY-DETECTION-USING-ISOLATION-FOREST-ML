from django.shortcuts import render,redirect
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest
mpl.rcParams['figure.figsize'] = (10 , 8)
mpl.rcParams['axes.grid'] = False
from .forms import UserRegisterForm
import warnings
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from pathlib import Path
from django.core.files import File

def Anomally(dataset,title,request):

	obj = Anomally_Detect.objects.create(user=request.user,title=title)

	df = pd.read_csv(dataset,encoding= 'unicode_escape')
	df['timestamp']=pd.to_datetime(df['timestamp'])
	df=df.set_index('timestamp').resample("H").mean().reset_index()
	fig = px.line(df.reset_index(), x='timestamp', y='value', title=title)
	fig.update_xaxes(rangeslider_visible=True)
	df['hour'] = df.timestamp.dt.hour
	df['weekday']=pd.Categorical(df.timestamp.dt.strftime('%A'), categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
	df[['value','hour']].groupby('hour').mean().plot()
	plt.close()
	df[['value','weekday']].groupby('weekday').mean().plot()
	plt.close()

	df.groupby(['hour','weekday']).mean()['value'].unstack().plot()
	plt.savefig('userapp/static/image/anomaly_detect/'+str(title)+'ano.png')
	plt.close()

	path = Path('userapp/static/image/anomaly_detect/'+str(title)+'ano.png')
	with path.open(mode='rb') as f:
		obj.weekday_plot = File(f, name=path.name)
		obj.save()


	df_final=df.join(df.groupby(['hour','weekday'])['value'].mean(), on=['hour','weekday'],rsuffix='_avg')
	df_final['day']=df.timestamp.dt.weekday
	data= df_final[['value','hour','day']]
	model=IsolationForest(contamination=0.005,max_features=3,max_samples=0.8,n_estimators=200)
	model.fit(data)
	df_final['outliers']=pd.Series(model.predict(data)).apply(lambda x: 'yes' if (x== -1) else 'no')
	df_final.query('outliers=="yes"')
	fig = px.scatter(df_final, x='timestamp', y='value',color='outliers',hover_data=['weekday','hour','value_avg'], title="New York Taxi Demand")

	fig.update_xaxes(rangeslider_visible=True)

	# score=model.decision_function(data)
	# plt.hist(score, bins=50)
	# plt.show()

	score = model.decision_function(data)
	plt.hist(score, bins=50)
	plt.savefig('userapp/static/image/hist/'+str(title)+'_hist.png')

	path = Path('userapp/static/image/hist/'+str(title)+'_hist.png')
	with path.open(mode='rb') as f:
		obj.hist_img = File(f, name=path.name)
		obj.save()


	df_final['scores']=score
	df_final.to_csv('userapp/static/data/final/'+str(title)+'_final.csv')
	path = Path('userapp/static/data/final/'+str(title)+'_final.csv')
	with path.open(mode='rb') as f:
		obj.final = File(f, name=path.name)
		obj.save()

	df_final = df_final.query('scores<-0.02')
	# df_final.to_csv(df.csv, sep='\t', encoding='utf-8')
	df_final.to_csv('userapp/static/data/anomally/'+str(title)+'_anomaly.csv')
	path = Path('userapp/static/data/anomally/'+str(title)+'_anomaly.csv')
	with path.open(mode='rb') as f:
		obj.outliers = File(f, name=path.name)
		obj.save()

	geeks_object = df_final.to_html(classes='data', header="true")
	params={'geek': geeks_object}
	return obj