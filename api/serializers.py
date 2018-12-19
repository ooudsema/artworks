from artworks.models import Artwork, Subject, ArtworkSubject
from rest_framework import response, serializers, status



class SubjectSerializer(serializers.ModelSerializer):

	subject_name = serializers.CharField(
		allow_blank=False,
		max_length=250
	)

	class Meta:
		model = Subject
		fields = ('subject_id', 'subject_name')



	def create(self, validated_data):

	# subjects = validated_data.pop('artworksubject')
		subject = Subject.objects.create(**validated_data)

		# if subjects is not None:
		# 	for subject in subjects:
		# 		Subject.objects.create(
		# 			subject_id=subject.subject_id,
		# 			subject_name=subject.subject_name
		# 		)
		return subject

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		subject_id = instance.subject_id
		# new_subjects = validated_data.pop('artworksubject')

		# )

		instance.subject_name = validated_data.get(
			'subject_name',
			instance.subject_name
		)

		instance.save()

		# # If any existing country/areas are not in updated list, delete them
		# new_ids = []
		# old_ids = Subject.objects \
		# 	.values_list('subject_id', flat=True) \
		# 	.filter(subject_id__exact=subject_id)

		# # TODO Insert may not be required (Just return instance)

		# # Insert new unmatched country entries
		# for subject in new_subjects:
		# 	new_id = subject.subject_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		ArtworkSubject.objects \
		# 			.create(artwork_id=art_id, subject_id=new_id)

		# # Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		ArtworkSubject.objects \
		# 			.filter(artwork_id=art_id, subject_id=old_id) \
		# 			.delete()

		return instance

# class ArtworkSubjectSerializer(serializers.ModelSerializer):
# 	subject = SubjectSerializer(many=False, read_only=True)
# 	artwork = ArtworkSerializer(many=False, read_only=True)

# 	class Meta:
# 		model = ArtworkSubject
# 		fields = ('artwork_subject_id', 'artwork', 'subject')