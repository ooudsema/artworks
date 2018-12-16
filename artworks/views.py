from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from artworks.forms import ArtworkForm
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView
from artworks.filters import ArtworkFilter

from .models import Artwork, Subject, Artist


def index(request):
	return HttpResponse("Hello, world. You're at the Tate Gallery Artworkss index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'artworks/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'artworks/home.html'


class ArtListView(generic.ListView):
	model = Artwork
	context_object_name = 'art'
	template_name = 'artworks/art.html'
	paginate_by = 50

	def get_queryset(self):
		return Artworks.objects.all().select_related('artwork_subject').order_by('artwork_title')

class ArtDetailView(generic.DetailView):
	model = Artwork
	context_object_name = 'art'
	template_name = 'artworks/art_detail.html'

@method_decorator(login_required, name='dispatch')
class SubjectListView(generic.ListView):
	model = Subject
	context_object_name = 'subjects'
	template_name = 'artworks/subject.html'
	paginate_by = 20

	def get_queryset(self):
		return Subject.objects.all().select_related('artwork_subject').order_by('subject_name')
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class SubjectDetailView(generic.DetailView):
	model = Subject
	context_object_name = 'subjects'
	template_name = 'artworks/subject_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ArtworkCreateView(generic.View):
	model = Artwork
	form_class = ArtworkForm
	success_message = "Artwork created successfully"
	template_name = 'artworks/art_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = ArtworkForm(request.POST)
		if form.is_valid():
			art = form.save(commit=False)
			art.save()
			for subject in form.cleaned_data['subject']:
				Artwork_Subject.objects.create(artwork=art, subject=subject)
			return redirect(site) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'artwork/site_new.html', {'form': form})

	def get(self, request):
		form = ArtworkForm()
		return render(request, 'artwork/art_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ArtUpdateView(generic.UpdateView):
	model = Artwork
	form_class = ArtworkForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'art'
	# pk_url_kwarg = 'site_pk'
	success_message = "Artwork updated successfully"
	template_name = 'artworks/art_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		art = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		art.save()

		# # Current country_area_id values linked to site
		# old_ids = Artwork_Subject.objects\
		# 	.values_list('subject_id', flat=True)\
		# 	.filter(artwork_id=art.artwork_id)

		# # New countries list
		# new_subjects = form.cleaned_data['subject']

		# # TODO can these loops be refactored?

		# # New ids
		# new_ids = []

		# # Insert new unmatched country entries
		# for country in new_countries:
		# 	new_id = country.country_area_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.create(heritage_site=site, country_area=country)

		# # Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
		# 			.delete()

		return HttpResponseRedirect(art.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class ArtDeleteView(generic.DeleteView):
	model = Artwork
	success_message = "Artworkdeleted successfully"
	success_url = reverse_lazy('art')
	context_object_name = 'art'
	template_name = 'artworks/art_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		Artwork_Subject.objects \
			.filter(artwork_id=self.object.artwork_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class ArtFilterView(FilterView):
	filterset_class = ArtworkFilter
	template_name = 'artworks/art_filter.html'
	