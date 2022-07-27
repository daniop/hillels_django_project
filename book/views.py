from django.db.models import Avg, Count, Max, Min, Prefetch, Sum
from django.db.models.functions import Round
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, Publisher, Store


def index(request):
    return render(request, 'book/index.html')


class BooksView(generic.ListView):
    template_name = 'book/publishers_books.html'
    context_object_name = 'publishers_books'

    def get_queryset(self):
        return Book.objects.filter(rating__gte=9).select_related('publisher').\
            prefetch_related('authors').order_by('-rating')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['store_total'] = self.object.stores.all().count()
        return context


class PublisherView(generic.ListView):
    template_name = 'book/best_pub.html'
    context_object_name = 'best_pub'

    def get_queryset(self):
        return Publisher.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.filter(rating__gte=9)))


class PubDetailView(generic.DetailView):
    model = Publisher
    template_name = 'book/pub_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PubDetailView, self).get_context_data(**kwargs)
        context['book_list'] = self.object.books.all().order_by('-rating')
        return context


class AuthView(generic.ListView):
    template_name = 'book/auth_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return Author.objects.annotate(rating=Round(Avg('books__rating'), 2),
                                       total=Count('books')).\
            order_by('-rating')


class AuthDetailView(generic.DetailView):
    model = Author
    template_name = 'book/auth_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AuthDetailView, self).get_context_data(**kwargs)
        context['average'] = self.object.books.aggregate(average=Avg('price'), total_pages=Sum('pages'))
        return context


class StoreView(generic.ListView):
    template_name = 'book/store_list.html'
    context_object_name = 'stores'

    def get_queryset(self):
        return Store.objects.annotate(min=Min('books__price'), max=Max('books__price'))


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'book/store_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context['youngest_auth'] = self.object.books.aggregate(youngest=Min('authors__age'))
        return context
