# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'
        ordering = ['subject_name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.subject_name


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_last_name = models.CharField(max_length=300, blank=True, null=True)
    artist_first_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist'
        ordering = ['artist_last_name']
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __str__(self):
        return self.artist_last_name + ", " + self.artist_first_name


class Artwork(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    accession_number = models.CharField(max_length=250, blank=True, null=True)
    artwork_title = models.CharField(max_length=500, blank=True, null=True)
    artwork_date = models.CharField(max_length=200, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)
    era = models.ForeignKey('Era', models.DO_NOTHING, blank=True, null=True)
    movement = models.ForeignKey('Movement', models.DO_NOTHING, blank=True, null=True)
    medium = models.ForeignKey('Medium', models.DO_NOTHING, blank=True, null=True)
    subject = models.ManyToManyField(Subject, through='ArtworkSubject')

    class Meta:
        managed = False
        db_table = 'artwork'
        ordering = ['artwork_title']
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'

    def __str__(self):
        return self.artwork_title

    def get_absolute_url(self):
        return reverse('art_detail', kwargs={'pk': self.pk})

    @property
    def subject_names(self):
        subjects = self.subject.order_by('subject.subject_name')

        names = []
        for subject in subjects:
            name = subject.subject_name
            if name is None:
                continue
            if name not in names:
                names.append(name)

        return ', '.join(names)

class ArtworkSubject(models.Model):
    artwork_subject_id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey('Artwork', models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artwork_subject'
        ordering = ['artwork', 'subject']
        verbose_name = 'Arwork Subject'
        verbose_name_plural = 'Artwork Subjects'


class Era(models.Model):
    era_id = models.AutoField(primary_key=True)
    era_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'era'
        ordering = ['era_name']
        verbose_name = 'Era'
        verbose_name_plural = 'Eras'

    def __str__(self):
        return self.era_name


class Medium(models.Model):
    medium_id = models.AutoField(primary_key=True)
    medium_name = models.CharField(unique=True, max_length=250)

    class Meta:
        managed = False
        db_table = 'medium'
        ordering = ['medium_name']
        verbose_name = 'Medium'
        verbose_name_plural = 'Mediums'

    def __str__(self):
        return self.medium_name

class Movement(models.Model):
    movement_id = models.AutoField(primary_key=True)
    movement_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'movement'
        ordering = ['movement_name']
        verbose_name = 'Movement'
        verbose_name_plural = 'Movements'

    def __str__(self):
        return self.movement_name




