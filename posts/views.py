from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from users.models import Employee
from rest_framework.decorators import action

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employee'):
            return Post.objects.filter(creator=user.employee)
        return Post.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'employee') and user.employee.employee_type == 'buyer':
            serializer.save(creator=user.employee)
        else:
            raise permissions.PermissionDenied("Solo los empleados tipo 'buyer' pueden crear publicaciones.")
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_seller(self, request, pk=None):
        post = self.get_object()
        # Verificar que el usuario autenticado sea un 'seller'
        if not hasattr(request.user, 'employee') or request.user.employee.employee_type != 'seller':
            return Response({"detail": "No autorizado. Solo los 'sellers' pueden agregarse a un post."}, status=status.HTTP_403_FORBIDDEN)

        # Añadir el 'seller' a possible_sellers si aún no está vendido y no es el creador
        if post.is_sold:
            return Response({"detail": "No se puede modificar un post ya vendido."}, status=status.HTTP_400_BAD_REQUEST)

        if post.creator == request.user.employee:
            return Response({"detail": "No puedes añadirte a tu propio post."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.employee in post.possible_sellers.all():
            return Response({"detail": "Ya estás en la lista de sellers posibles de este post."}, status=status.HTTP_409_CONFLICT)

        post.possible_sellers.add(request.user.employee)
        post.save()
        return Response({"detail": "Seller añadido exitosamente a la lista de sellers posibles."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def choose_seller(self, request, pk=None):
        post = self.get_object()
    
        if post.creator != request.user.employee or post.creator.employee_type != 'buyer':
            return Response({"detail": "No autorizado o no eres el comprador de este post."}, status=status.HTTP_403_FORBIDDEN)

        seller_id = request.data.get('seller_id')
        if not seller_id:
            return Response({"detail": "Se requiere un seller_id válido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            seller = Employee.objects.get(id=seller_id)
        except Employee.DoesNotExist:
            return Response({"detail": "Seller no válido o no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if seller.employee_type != 'seller':
            return Response({"detail": "Este empleado no es un seller válido."}, status=status.HTTP_400_BAD_REQUEST)

        if seller not in post.possible_sellers.all():
            return Response({"detail": "Este seller no es un posible vendedor para este post."}, status=status.HTTP_400_BAD_REQUEST)

        post.chosen_seller = seller
        post.is_sold = True
        post.save()
        return Response({"detail": "Seller elegido y post marcado como vendido."}, status=status.HTTP_200_OK)
