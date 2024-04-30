from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.text import slugify
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
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = GenericRelation(Tag, related_query_name='recipes')

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        return super().save(*args, **kwargs)
