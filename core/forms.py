# forms.py
from django import forms
from .models import Book, Author, Genre, Review, Collection


class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = [
			'title', 'author', 'genre', 'description', 'pages',
			'publication_date', 'isbn', 'cover', 'status',
			'format', 'rating'
		]
		widgets = {
			'publication_date': forms.DateInput(attrs={'type': 'date'}),
			'description': forms.Textarea(attrs={'rows': 4}),
			'genre': forms.CheckboxSelectMultiple(),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['author'].queryset = Author.objects.order_by('name')


class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['name', 'bio', 'birth_date', 'death_date', 'photo']
		widgets = {
			'birth_date': forms.DateInput(attrs={'type': 'date'}),
			'death_date': forms.DateInput(attrs={'type': 'date'}),
			'bio': forms.Textarea(attrs={'rows': 4}),
		}


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['rating', 'content']
		widgets = {
			'content': forms.Textarea(attrs={'rows': 4}),
		}


class CollectionForm(forms.ModelForm):
	class Meta:
		model = Collection
		fields = ['name', 'description', 'books', 'is_public']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3}),
			'books': forms.CheckboxSelectMultiple(),
		}
	
	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['books'].queryset = Book.objects.filter(
			added_by=user
		).order_by('-added_date')