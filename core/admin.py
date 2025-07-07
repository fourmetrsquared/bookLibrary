from django.contrib import admin
from .models import Book, Author, Genre, ReadingSession, Review, Collection


class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'get_genres', 'pages', 'added_date')
	list_filter = ('status', 'format', 'genre')
	search_fields = ('title', 'author__name', 'description')
	prepopulated_fields = {'slug': ('title',)}
	
	def get_genres(self, obj):
		return ", ".join([g.name for g in obj.genre.all()])
	
	get_genres.short_description = 'Genres'


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'birth_date', 'death_date')
	search_fields = ('name', 'bio')


class GenreAdmin(admin.ModelAdmin):
	list_display = ('name', 'color')
	search_fields = ('name',)


class CollectionAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_by', 'created_at', 'is_public')
	filter_horizontal = ('books',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ReadingSession)
admin.site.register(Review)
admin.site.register(Collection, CollectionAdmin)