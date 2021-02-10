from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
from tinymce.models import HTMLField
from django.shortcuts import reverse
# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(
        'Название тэга', max_length=30, null=False, blank=False)
    tag_eng_name = models.CharField(
        'Название тэга eng', max_length=30, null=True, blank=True)
    tag_ru_name = models.CharField(
        'Название тэга ru', max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return str(self.tag_name)


class Proposition(models.Model):
    title = models.CharField(
        'Заголовок', max_length=80, null=False, blank=False)
    title_eng = models.CharField(
        'Заголовок eng', max_length=80, null=True, blank=True)
    title_ru = models.CharField(
        'Заголовок ru', max_length=80, null=True, blank=True)

    tag = models.ManyToManyField(Tag)
    date_added = models.DateField(auto_now=True)
    proposition_photo = models.ImageField(blank=True, null=True)
    description = HTMLField()
    description_eng = HTMLField(null=True, blank=True)
    description_ru = HTMLField(null=True, blank=True)
    slug = models.SlugField()

    def short_description(self):
        return mark_safe(self.description)[:20]

    def prop_preview_photo(self):
        return mark_safe('<img src="{}" width="100" /'.format(self.proposition_photo.url))

    def get_absolute_url(self):
        return reverse("proposition:single_proposition", kwargs={
            'slug': self.slug
        })

    prop_preview_photo.short_description = 'Превью'
    prop_preview_photo.allow_tags = True
    short_description.allow_tags = True

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
