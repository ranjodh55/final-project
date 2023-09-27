from django.urls import path
from accounts.views import login_user, signup, activate_email, logout_user, add_to_cart, cart, remove_from_cart, forgot_password, reset_pass, remove_all_from_cart, order,cart_is_empty
urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('signup/', signup, name='signup'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('logout/', logout_user, name='logout_user'),
    path('add-to-cart/<id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<cart_item_id>/',
         remove_from_cart, name='remove_from_cart'),
    path('remove-all-from-cart/<cart_id>/',
         remove_all_from_cart, name='remove_all_from_cart'),
    path('order/<cart_id>/', order, name='order'),
    path('forgot', forgot_password, name='forgot_password'),
    path('reset/<forgot_token>/', reset_pass, name='reset_pass'),
    path('empty-cart/',cart_is_empty,name='cart_is_empty'),
    path('cart/', cart, name='cart')

]
