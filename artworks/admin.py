from django.contrib import admin
import artworks.models as models


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
	fields = [
		'artist_last_name',
		'artist_first_name'
	]

	list_display = [
		'artist_last_name',
		'artist_first_name'
	]

	list_filter = ['artist_first_name', 'artist_last_name']


@admin.register(models.Era)
class EraAdmin(admin.ModelAdmin):
	fields = ['era_name']
	list_display = ['era_name']
	ordering = ['era_name']

# admin.site.register(models.DevStatus)


@admin.register(models.Artwork)
class ArtworkAdmin(admin.ModelAdmin):
	fields = [
				'artwork_title',
				'accession_number',
				'artwork_date',
				'artist',
				'era',
				'movement',
				'medium'
]

	list_display = (
		'artwork_title',
		'accession_number',
		'artwork_date',
		'artist',
		'era',
		'movement',
		'medium'
	)

	list_filter = (
		'medium',
		'artwork_date'
	)


@admin.register(models.ArtworkSubject)
class ArtworkSubjectAdmin(admin.ModelAdmin):
	fields = ['artwork', 'subject']
	list_display = ['artwork', 'subject']
	ordering = ['artwork', 'subject']


@admin.register(models.Medium)
class MediumAdmin(admin.ModelAdmin):
	fields = ['medium_name']
	list_display = ['medium_name']
	ordering = ['medium_name']

@admin.register(models.Movement)
class MovementAdmin(admin.ModelAdmin):
	fields = ['movement_name']
	list_display = ['movement_name']
	ordering = ['movement_name']


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
	fields = ['subject_name']
	list_display = ['subject_name']
	ordering = ['subject_name']
