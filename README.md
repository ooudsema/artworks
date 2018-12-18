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

certifi                        2018.11.29
chardet                        3.0.4     
coreapi                        2.3.3     
coreschema                     0.0.4     
defusedxml                     0.5.0     
Django                         2.1.4     
django-allauth                 0.38.0    
django-cors-headers            2.4.0     
django-crispy-forms            1.7.2     
django-filter                  2.0.0     
django-rest-auth               0.9.3     
django-rest-swagger            2.2.0     
django-test-without-migrations 0.6       
djangorestframework            3.9.0     
idna                           2.8       
itypes                         1.1.0     
Jinja2                         2.10      
MarkupSafe                     1.1.0     
mysqlclient                    1.3.13    
numpy                          1.15.1    
oauthlib                       2.1.0     
openapi-codec                  1.3.2     
pandas                         0.23.4    
pip                            18.1      
PyJWT                          1.7.1     
python-dateutil                2.7.3     
python3-openid                 3.1.0     
pytz                           2018.5    
PyYAML                         3.13      
requests                       2.21.0    
requests-oauthlib              1.0.0     
setuptools                     40.6.3    
simplejson                     3.16.0  

```

It also requires a 'secrets.py' file in the 'mysite' directory with the following keys: a django key assigned to the variable SECRET_KEY, a Google Oauth key assigned to the variable SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, and a Google Oauth Secret assigned to the variable SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET. 