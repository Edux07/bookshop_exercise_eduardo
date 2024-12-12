from django.urls import path
from .views import UserCreateView, RetrieveUserView, UpdateUserView, DeleteUserView, ListUsersView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='list-users'),  # GET para listar usuarios
    path('users/create/', UserCreateView.as_view(), name='create-user'),  # POST para crear usuario
    path('users/<int:id>/', RetrieveUserView.as_view(), name='retrieve-user'),  # GET para recuperar usuario
    path('users/<int:id>/update/', UpdateUserView.as_view(), name='update-user'),
    path('users/<int:id>/delete/', DeleteUserView.as_view(), name='delete-user'),
]
