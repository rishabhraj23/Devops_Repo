from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('user_details', views.user_details, name='user_details'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    
    # Updated watch views
    path('watch', views.watch_list, name='watch'),
    path('add_watch', views.add_watch, name='add_watch'),
    path('watch_form_add_update/', views.watch_form_add_update, name='add_watch'),
    path('watch_form_add_update/<int:id>', views.watch_form_add_update, name='watch_form_add_update'),
    path('delete_watch/<int:id>', views.delete_watch, name='delete_watch'),

    # Orders
    path('orders', views.orders, name='orders'),
    path('history', views.history, name='history'),
    path("place_order", views.place_order, name="place_order"),
    path("cancel_order/<int:id>", views.cancel_order, name="cancel_order"),
    path("complete_order/<int:id>", views.complete_order, name="complete_order"),
]
