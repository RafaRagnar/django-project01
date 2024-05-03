import os
from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.conf import settings
from PIL import Image
from tag.models import Tag


class Category(models.Model):
    """Class representing category"""
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')


class Recipe(models.Model):
    """Class representing recipes"""
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    preparation_time = models.IntegerField(verbose_name=_('preparation time'))
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_('preparation time unit'))
    servings = models.IntegerField(verbose_name=_('servings'))
    servings_unit = models.CharField(
        max_length=65, verbose_name=_('servings unit'))
    preparation_steps = models.TextField(verbose_name=_('preparation steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name=_('preparation steps is html'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    update_at = models.DateTimeField(
        auto_now=True, verbose_name=_('update at'))
    is_published = models.BooleanField(
        default=False, verbose_name=_('is published'))
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='', verbose_name=_('cover'))
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None, verbose_name=_('category')
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))

    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name=_('tags'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def generate_unique_slug(self):
        slug = slugify(self.title)
        count = 1
        while Recipe.objects.filter(slug=slug).exists():
            slug = slugify(self.title) + '-' + str(count)
            count += 1
        return slug

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title')

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
