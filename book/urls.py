from book.views import AuthDetailView, AuthView, BookDetailView, BooksView, PubDetailView, \
    PublisherView, StoreDetailView, StoreView, index

from django.urls import path


app_name = 'book'
urlpatterns = [
    path('', index, name='index'),
    path('publishers_books/', BooksView.as_view(), name='publishers_book'),
    path('publishers_books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('best_pub/', PublisherView.as_view(), name='best_pub'),
    path('best_pub/<int:pk>/', PubDetailView.as_view(), name='pub_detail'),
    path('auth_list/', AuthView.as_view(), name='auth_list'),
    path('auth_list/<int:pk>/', AuthDetailView.as_view(), name='auth_detail'),
    path('store_list/', StoreView.as_view(), name='store_list'),
    path('store_list/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
]
