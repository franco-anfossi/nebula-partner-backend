from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Employee

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """This method returns all the posts in the database."""

        return Post.objects.all()

    @action(
        detail=False, methods=["get"], url_path="current", url_name="current_user_posts"
    )
    def get_current_user_posts(self, request):
        """This method returns all posts created by the current authenticated user."""

        user = request.user
        if hasattr(user, "employee"):
            posts = Post.objects.filter(creator=user.employee)
        else:
            posts = Post.objects.none()

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """This method ensures that only 'buyer' employees can create posts."""

        user = self.request.user
        if hasattr(user, "employee") and user.employee.employee_type == "buyer":
            serializer.save(creator=user.employee)
        else:
            raise permissions.PermissionDenied(
                "Solo los empleados tipo 'buyer' pueden crear publicaciones."
            )

    @action(
        detail=True,
        methods=["post"],
        url_path="add-seller",
        url_name="add_seller_to_post",
    )
    def add_seller(self, request, pk=None):
        """
        This method allows a 'seller' to add
        themselves to a post as a possibleseller.

        Body: {}
        """

        post = self.get_object()
        # Verificar que el usuario autenticado sea un 'seller'
        if (
            not hasattr(request.user, "employee")
            or request.user.employee.employee_type != "seller"
        ):
            return Response(
                {
                    "detail": (
                        "No autorizado. Solo los 'sellers' "
                        "pueden agregarse a un post."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if post.is_sold:
            return Response(
                {"detail": "No se puede modificar un post ya vendido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if post.creator == request.user.employee:
            return Response(
                {"detail": "No puedes añadirte a tu propio post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user.employee in post.possible_sellers.all():
            return Response(
                {"detail": "Ya estás en la lista de sellers posibles de este post."},
                status=status.HTTP_409_CONFLICT,
            )

        post.possible_sellers.add(request.user.employee)
        post.save()
        return Response(
            {"detail": "Seller añadido exitosamente a la lista de sellers posibles."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False, methods=["get"], url_path="user-posts", url_name="posts-as-seller"
    )
    def posts_as_possible_seller(self, request):
        """
        This method returns all posts where the
        current user is listed as a possible seller.
        """

        user = request.user
        if hasattr(user, "employee") and user.employee.employee_type == "seller":
            posts = Post.objects.filter(possible_sellers=user.employee)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "No autorizado. Solo los 'sellers' pueden ver sus posts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="choose-seller",
        url_name="choose_seller",
    )
    def choose_seller(self, request, pk=None):
        """
        This method allows the 'buyer' to choose a 'seller' for the post.

        Body: {
            "seller_rut": "<rut_del_vendedor>"
        }
        """

        post = self.get_object()

        if (
            post.creator != request.user.employee
            or post.creator.employee_type != "buyer"
        ):
            return Response(
                {"detail": "No autorizado o no eres el comprador de este post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        seller_rut = request.data.get("seller_rut")
        if not seller_rut:
            return Response(
                {"detail": "Se requiere un seller_rut válido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            seller = Employee.objects.get(rut=seller_rut)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Seller no válido o no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if seller.employee_type != "seller":
            return Response(
                {"detail": "Este empleado no es un seller válido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if seller not in post.possible_sellers.all():
            return Response(
                {"detail": "Este seller no es un posible vendedor para este post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.chosen_seller = seller
        post.is_sold = True
        post.save()
        return Response(
            {"detail": "Seller elegido y post marcado como vendido."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="remove-seller",
        url_name="remove_seller",
    )
    def remove_seller(self, request, pk=None):
        """
        This method allows a 'seller' to remove themselves from
        a post, or the 'buyer' to remove a 'seller' from the post.

        Body: {
            "seller_rut": "<rut_del_vendedor>"
        }
        """

        post = self.get_object()
        user = request.user

        seller_rut = request.data.get("seller_rut")

        if post.creator != user.employee and (
            not hasattr(user, "employee")
            or user.employee.employee_type != "seller"
            or user.employee.rut != seller_rut
        ):
            return Response(
                {
                    "detail": (
                        "No autorizado. Solo los 'sellers'pueden eliminarse "
                        "de un post o el 'buyer' puede eliminar un 'seller'."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            seller = Employee.objects.get(rut=seller_rut)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Seller no válido o no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if seller not in post.possible_sellers.all():
            return Response(
                {
                    "detail": (
                        "Este seller no está en la lista "
                        "de posibles sellers de este post."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.possible_sellers.remove(seller)
        post.save()
        return Response(
            {
                "detail": (
                    "El seller ha sido eliminado de "
                    "la lista de posibles sellers de este post."
                )
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk=None):
        """
        This method allows only the creator of the
        post to update the post information.

        Body: {
            "updated_field": "new_value",
            ...
        }
        """

        post = self.get_object()
        user = request.user

        if post.creator != user.employee:
            return Response(
                {
                    "detail": (
                        "No autorizado. Solo el creador del post "
                        "puede actualizar la información del post."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """This method allows only the creator of the post to delete the post."""

        post = self.get_object()
        user = request.user

        if post.creator != user.employee:
            return Response(
                {
                    "detail": (
                        "No autorizado. Solo el creador "
                        "del post puede eliminar el post."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        post.delete()
        return Response(
            {"detail": "Post eliminado correctamente."},
            status=status.HTTP_204_NO_CONTENT,
        )
