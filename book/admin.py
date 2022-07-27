from book.models import Author, Book, Publisher, Store

from django.contrib import admin


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class BooksInline(admin.TabularInline):
    model = Book.authors.through
    extra = 0


class StoreInline(admin.TabularInline):
    model = Store.books.through
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'total_books')
    search_fields = ['name']
    inlines = [BooksInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pages', 'rating', 'price', 'publisher', 'pubdate', 'get_auth', 'get_store')
    search_fields = ['name', 'authors__name', 'publisher__name', 'stores__name']
    inlines = [BooksInline, StoreInline]
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Book information', {'fields': ['pages', 'rating', 'pubdate', 'price'], 'classes': ['collapse']}),
        ('Publisher', {'fields': ['publisher'], 'classes': ['collapse']})
    ]

    @admin.display(description='Authors')
    def get_auth(self, obj):
        return "; ".join([auth.name for auth in obj.authors.all()])

    @admin.display(description='Store')
    def get_store(self, obj):
        return "; ".join([store.name for store in obj.stores.all()])


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_book')
    search_fields = ['name', 'books__name']
    inlines = [BookInline]

    @admin.display(description='Books')
    def get_book(self, obj):
        return "; ".join([book.name for book in obj.books.all()])


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_book')
    filter_vertical = ["books"]
    search_fields = ['name', 'books__name']
    inlines = [StoreInline]

    @admin.display(description='Books')
    def get_book(self, obj):
        return "; ".join([book.name for book in obj.books.all()])
