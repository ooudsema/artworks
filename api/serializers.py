from artworks.models import Artwork, Artist, Subject, Movement, \
	ArtworkSubject, Medium, Era
from rest_framework import response, serializers, status


class EraSerializer(serializers.ModelSerializer):

	class Meta:
		model = Era
		fields = ('era_id', 'era_name')


class MediumSerializer(serializers.ModelSerializer):

	class Meta:
		model = Medium
		fields = ('medium_id', 'medium_name')


class SubjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = Subject
		fields = ('subject_id', 'subject_name')


class MovementSerializer(serializers.ModelSerializer):

	class Meta:
		model = Movement
		fields = ('movement_id', 'movement_name')


class ArtistSerializer(serializers.ModelSerializer):

	class Meta:
		model = Artist
		fields = ('artist_id', 'artist_last_name', 'artist_first_name')




class ArtworkSerializer(serializers.ModelSerializer):
	artwork_title = serializers.CharField(
		allow_blank=True,
		max_length=500
	)
	accession_number = serializers.CharField(
		allow_blank=True
	)
	artwork_date = serializers.CharField(
		allow_blank=True
	)


	artist = serializers.PrimaryKeyRelatedField(
		allow_null=True,
		many=False,
		write_only=True,
		queryset=Artist.objects.all()
	)

	era = serializers.PrimaryKeyRelatedField(
		allow_null=True,
		many=False,
		write_only=True,
		queryset=Era.objects.all()
	)

	movement = serializers.PrimaryKeyRelatedField(
		allow_null=True,
		many=False,
		write_only=True,
		queryset=Movement.objects.all()
	)
	medium = serializers.PrimaryKeyRelatedField(
		allow_null=True,
		many=False,
		write_only=True,
		queryset=Medium.objects.all()
	)

	subject_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Subject.objects.all(),
		source='artworksubject'
	)

	class Meta:
		model = Artwork
		fields = (
			'artwork_id',
			'accession_number',
			'artwork_title',
			'artwork_date',
			'artist',
			'era',
			'movement',
			'medium',
			'subject_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		subjects = validated_data.pop('artworksubject')
		art = Artwork.objects.create(**validated_data)

		if subjects is not None:
			for subject in subjects:
				Subject.objects.create(
					artwork_id=art.artwork_id,
					subject_id=subject.subject_id
				)
		return art

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		artwork_id = instance.artwork_id
		new_subjects = validated_data.pop('artworksubject')

		instance.artwork_title = validated_data.get(
			'artwork_title',
			instance.artwork_title
		)
		instance.accession_number = validated_data.get(
			'accession_number',
			instance.accession_number
		)
		instance.artwork_date = validated_data.get(
			'artwork_date',
			instance.artwork_date
		)
		instance.artist = validated_data.get(
			'artist',
			instance.artist
		)
		instance.era = validated_data.get(
			'era',
			instance.era
		)
		instance.movement = validated_data.get(
			'movement',
			instance.movement
		)
		instance.medium = validated_data.get(
			'medium',
			instance.medium
		)
		instance.subject_id = validated_data.get(
			'subject_id',
			instance.subject_id
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = ArtworkSubject.objects \
			.values_list('subject_id', flat=True) \
			.filter(artwork_id__exact=art_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for subject in new_subjects:
			new_id = subject.subject_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				ArtworkSubject.objects \
					.create(artwork_id=art_id, subject_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				ArtworkSubject.objects \
					.filter(artwork_id=art_id, subject_id=old_id) \
					.delete()

		return instance

class ArtworkSubjectSerializer(serializers.ModelSerializer):
	subject = SubjectSerializer(many=False, read_only=True)
	artwork = ArtworkSerializer(many=False, read_only=True)

	class Meta:
		model = ArtworkSubject
		fields = ('artwork_subject_id', 'artwork', 'subject')