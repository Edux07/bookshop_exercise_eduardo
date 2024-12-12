from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class UserCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Validar datos requeridos
        required_fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f'El campo {field} es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que las contraseñas coincidan
        if data['password'] != data['confirm_password']:
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar que el usuario no exista
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Ya existe un usuario con este correo electrónico.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario
        try:
            user = User.objects.create(
                email=data['email'],
                username=data['email'],  # Se usa el email como username
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=make_password(data['password']),
            )
            return Response({'message': 'Usuario creado exitosamente.', 'user_id': user.id},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al crear el usuario: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveUserView(APIView):
    """
    Maneja la recuperación de un usuario específico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if not id:
            return Response({'error': 'El parámetro id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserView(APIView):
    """
    Maneja la actualización de un usuario existente.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # Actualizar datos del usuario
        for field in ['first_name', 'last_name', 'email']:
            if field in data and data[field]:
                setattr(user, field, data[field])

        # Actualizar contraseña si se proporciona
        if 'password' in data:
            if data['password'] != data.get('confirm_password', ''):
                return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(data['password'])

        try:
            user.save()
            return Response({'message': 'Usuario actualizado exitosamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al actualizar el usuario: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({'message': 'Usuario eliminado exitosamente.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar el usuario: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
