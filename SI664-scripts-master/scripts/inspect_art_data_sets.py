import logging
import os
import pandas as pd
import sys as sys


def main(argv=None):
	"""
	Utilize Pandas library to read in both UNSD M49 country and area .csv file
	(tab delimited) as well as the UNESCO heritage site .csv file (tab delimited).
	Extract regions, sub-regions, intermediate regions, country and areas, and
	other column data.  Filter out duplicate values and NaN values and sort the
	series in alphabetical order. Write out each series to a .csv file for inspection.
	"""
	if argv is None:
		argv = sys.argv

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Read in Artworks Data set (tabbed separator)
	art_csv = './input/csv/artwork_data_a.csv'
	art_data_frame = read_csv(art_csv)

	# Read in Artists Data set (tabbed separator)
	artist_csv = './input/csv/artist_data.csv'
	artist_data_frame = read_csv(artist_csv, '\t')


	# Write countries to a .csv file.
	country = extract_filtered_series(artist_data_frame, 'birthCountry')
	country_csv = './output/country.csv'
	write_series_to_csv(country, country_csv)
	
	# Write artists to a .csv file.
	artist = extract_filtered_series(art_data_frame, 'artist')
	artist_csv = './output/artistCleaned.csv'
	write_series_to_csv(artist, artist_csv)



	# Write mediums to a .csv file.
	medium = extract_filtered_series(art_data_frame, 'medium')
	medium_csv = 'output/art_medium2.csv'
	write_series_to_csv(medium, medium_csv)







def extract_filtered_series(data_frame, column_name):
	"""
	Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
	Duplicate values and NaN or blank values are dropped from the result set which is
	returned sorted (ascending).
	:param data_frame: Pandas DataFrame
	:param column_name: column name string
	:return: Panda Series one-dimensional ndarray
	"""
	return data_frame[column_name].drop_duplicates().dropna().sort_values()


def read_csv(path, delimiter=','):
	"""
	Utilize Pandas to read in *.csv file.
	:param path: file path
	:param delimiter: field delimiter
	:return: Pandas DataFrame
	"""
	return pd.read_csv(path, sep=delimiter, engine='python')


def write_series_to_csv(series, path, delimiter=',', row_name=True):
	"""
	Write Pandas DataFrame to a *.csv file.
	:param series: Pandas one dimensional ndarray
	:param path: file path
	:param delimiter: field delimiter
	:param row_name: include row name boolean
	"""
	series.to_csv(path, sep=delimiter, index=row_name)


if __name__ == '__main__':
	sys.exit(main())