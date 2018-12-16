import django_filters
from artworks.models import Artwork, Artist, Subject, ArtworkSubject


class ArtworkFilter(django_filters.FilterSet):
	artwork_title = django_filters.CharFilter(
		field_name='artwork_title',
		label='Artwork Title',
		lookup_expr='icontains'
	)

# 	date = django_filters.CharFilter(
# 		field_name='artwork_date',
# 		label='Date',
# 		lookup_expr='icontains'
# 	)

# 	subject = django_filters.ModelChoiceFilter(
# 		field_name='subject',
# 		label='Subject',
# 		queryset=Subject.objects.all().order_by('subject_name'),
# 		lookup_expr='exact'
# 	)

	class Meta:
		model = Artwork
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []