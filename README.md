# Artworks of the Tate Gallery

## Purpose

This project uses the Tate Collection dataset that is available on [Github](https://github.com/tategallery/collection). It uses Django to create display the artworks and their artists of the Tate in a way that users can browse or filter, by artwork, artists, or subject of the work. 

## Data set

This dataset consists of metadata and image thumbnails for approximately 70,000 works of art owned by the Tate Gallery, and about 3,500 artists.  This project uses the following three files from the Tate's Github dataset: 

* artwork_data.csv with the following headings: id, accession number, artist, artistRole, artistId, title, dateText, medium, creditLine, year, acquisitionYear, dimensions, width, height, depth, units, inscription, thumbnailCopyright, thumbnailUrl, and url

* artist_data.csv

* artists json files 

## Data model

![Artworks Data Model](https://github.com/ooudsema/artworks/blob/master/static/artworkModel.png "Artworks Model")

## Package Dependencies

This app uses the following python packages: 

```python

certifi                        2018.10.15
chardet                        3.0.4
defusedxml                     0.5.0
Django                         2.1.1
django-crispy-forms            1.7.2
django-filter                  2.0.0
django-test-without-migrations 0.6
idna                           2.7
mysqlclient                    1.3.13
numpy                          1.15.1
oauthlib                       2.1.0
pandas                         0.23.4
pip                            18.0
PyJWT                          1.6.4
python-dateutil                2.7.3
python3-openid                 3.1.0
pytz                           2018.5
PyYAML                         3.13
requests                       2.20.0
requests-oauthlib              1.0.0
setuptools                     40.4.3
six                            1.11.0
social-auth-app-django         3.1.0
social-auth-core               2.0.0
urllib3                        1.24.1
wheel                          0.32.0

```