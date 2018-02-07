import csv
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from itertools import izip
import collections as cts

app = Flask(__name__)

@app.route('/')
#root
def index():
	#render the homepage with the form
	return render_template('index.html')

@app.route('/datafetch', methods= ['POST'])
def read_data():
	df_county = pd.read_csv("Counties__OSi.csv", sep=",", usecols = ['X', 'Y', 'County']) #Reads csv file, specific columns
	df_town = pd.read_csv("Townlands__OSi.csv", sep = ",", usecols = ['X', 'Y', 'County', 'English_Name']) #Reads csv file
	place_cord = {'County':[], 'Town':[], 'X-Coordinate':[], 'Y-Coordinate':[]}
	with open('addresses.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter = ',')
		for row in csvreader:
			if (row != ['Address']):
					for element in row:	
						for inner in reversed(element.split(',')):
							inner = inner.replace('Co.', '')
							if (len(place_cord['County']) <= len(place_cord['Town']) and df_town[df_town.County == inner.lstrip().upper()].shape[0] != 0):
								place_cord['County'].append(inner.lstrip().upper())
							elif (len(place_cord['County']) > len(place_cord['Town']) and df_town[df_town['English_Name'] == inner.lstrip().upper()].shape[0] != 0):
								place_cord['Town'].append(inner.lstrip().upper())
								break
						if (len(place_cord['County']) > len(place_cord['Town'])):
								place_cord['Town'].append('NULL')
	for val_c, val_t in izip(place_cord['County'],place_cord['Town']):
		if (val_t == 'NULL') or (df_town.loc[(df_town.County == val_c) & (df_town['English_Name'] == val_t),['X', 'Y']].shape[0] == 0) or (df_town.loc[(df_town.County == val_c) & (df_town['English_Name'] == val_t),['X', 'Y']].shape[0] > 1):
			place_cord['X-Coordinate'].append(df_county.loc[df_county.County == val_c, ['X']].values.item(0))
			place_cord['Y-Coordinate'].append(df_county.loc[df_county.County == val_c, ['Y']].values.item(0))
		else:
			place_cord['X-Coordinate'].append(df_town.loc[(df_town.County == val_c) & (df_town['English_Name'] == val_t),['X']].values.item(0))
			place_cord['Y-Coordinate'].append(df_town.loc[(df_town.County == val_c) & (df_town['English_Name'] == val_t),['Y']].values.item(0))
	return render_template('view.html', vars = cts.OrderedDict(sorted(place_cord.items(), key=lambda idx: idx[0])))

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
	app.run(debug = True)		 # Please remove debug = True before publishing.
