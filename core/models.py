from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Author(models.Model):
	name = models.CharField(max_length=100)
	bio = models.TextField(blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)
	death_date = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='authors/', blank=True, null=True)
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('author_detail', kwargs={'pk': self.pk})


class Genre(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	color = models.CharField(max_length=7, default='#0A84FF')  # Vision UI accent color
	
	def __str__(self):
		return self.name


class Book(models.Model):
	STATUS_CHOICES = [
		('unread', 'Unread'),
		('reading', 'Currently Reading'),
		('completed', 'Completed'),
	]
	
	FORMAT_CHOICES = [
		('physical', 'Physical'),
		('ebook', 'E-Book'),
		('audiobook', 'Audiobook'),
	]
	
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True, blank=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
	genre = models.ManyToManyField(Genre, related_name='books')
	description = models.TextField(blank=True, null=True)
	pages = models.PositiveIntegerField(blank=True, null=True)
	publication_date = models.DateField(blank=True, null=True)
	isbn = models.CharField(max_length=20, blank=True, null=True)
	cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
	added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_books')
	added_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
	format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='physical')
	rating = models.FloatField(blank=True, null=True)
	read_start_date = models.DateField(blank=True, null=True)
	read_end_date = models.DateField(blank=True, null=True)
	
	class Meta:
		ordering = ['-added_date']
		indexes = [
			models.Index(fields=['-added_date']),
			models.Index(fields=['title']),
		]
	
	def __str__(self):
		return f"{self.title} by {self.author.name}"
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)
	
	def get_absolute_url(self):
		return reverse('book_detail', kwargs={'slug': self.slug})
	
	def reading_time(self):
		"""Estimate reading time in hours"""
		if self.pages:
			# Average reading speed: 200 words per page, 200 wpm reading speed
			words = self.pages * 200
			minutes = words / 200
			return round(minutes / 60, 1)
		return None


class ReadingSession(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_sessions')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_sessions')
	start_page = models.PositiveIntegerField()
	end_page = models.PositiveIntegerField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	notes = models.TextField(blank=True, null=True)
	
	def duration(self):
		return self.end_time - self.start_time
	
	def pages_read(self):
		return self.end_page - self.start_page


class Review(models.Model):
	RATING_CHOICES = [
		(1, '★'),
		(2, '★★'),
		(3, '★★★'),
		(4, '★★★★'),
		(5, '★★★★★'),
	]
	
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
	rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ['book', 'user']
	
	def __str__(self):
		return f"{self.user.username}'s review of {self.book.title}"


class Collection(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	books = models.ManyToManyField(Book, related_name='collections')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
	created_at = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=True)
	
	def __str__(self):
		return self.name
	
	def book_count(self):
		return self.books.count()