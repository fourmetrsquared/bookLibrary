# views.py (additional)
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, AuthorForm, ReviewForm, CollectionForm, Author, Genre
from .models import Book
from django.db.models import Count, Sum


def home(request):
    # Get recently added books (last 8)
    recent_books = Book.objects.select_related('author').order_by('-added_date')[:8]
    
    # Calculate statistics
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_pages = Book.objects.aggregate(total=Sum('pages'))['total'] or 0
    
    # Get top genres
    top_genres = Genre.objects.annotate(num_books=Count('books')).order_by('-num_books')[:5]
    
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_pages': total_pages,
        'top_genres': top_genres,
    }
    
    return render(request, 'home.html', context)

def add_book(request):
	if request.method == 'POST':
		form = BookForm(request.POST, request.FILES)
		if form.is_valid():
			book = form.save(commit=False)
			book.added_by = request.user
			book.save()
			form.save_m2m()  # Save many-to-many relationships
			return redirect('book_detail', slug=book.slug)
	else:
		form = BookForm()
	
	return render(request, 'books/add_book.html', {'form': form})


def book_detail(request, slug):
	book = get_object_or_404(Book, slug=slug)
	reviews = book.reviews.select_related('user').order_by('-created_at')
	
	# Check if the current user has reviewed this book
	user_review = None
	if request.user.is_authenticated:
		try:
			user_review = Review.objects.get(book=book, user=request.user)
		except Review.DoesNotExist:
			pass
	
	# Initialize review form
	review_form = ReviewForm()
	
	context = {
		'book': book,
		'reviews': reviews,
		'user_review': user_review,
		'review_form': review_form,
	}
	return render(request, 'books/book_detail.html', context)

def book_list(request):
	return render(request, 'books/books.html')

def author_list(request):
	pass

def author_detail(request):
	pass

def collection_list(request):
	pass