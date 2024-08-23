from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)

from src.core.user.application.use_cases.exceptions import (
    UserNotFound,
)
from src.core.user.application.use_cases.get_user import (
    GetUser,
    GetUserRequest,
)

from src.core.user.application.use_cases.list_user import (
    ListUsers,
    ListUsersRequest,
    ListUsersResponse,
)
from src.django_project.permissions import IsAdmin, IsAuthenticated
from src.django_project.user_app.repository import ApiClientUserRepository

from src.django_project.user_app.serializers import (
    ListUsersResponseSerializer,
    RetrieveUserRequestSerializer,
    RetrieveUserResponseSerializer,
)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """
        List Users
    """
    @swagger_auto_schema(
        operation_description="Lista todos os usuários do Sistema",
        responses={
            200: ListUsersResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "id")
        per_page = int(request.query_params.get("per_page", 10))
        current_page = int(request.query_params.get("current_page", 1))

        use_case = ListUsers(repository=ApiClientUserRepository())
        output: ListUsersResponse = use_case.execute(request=ListUsersRequest(
            order_by=order_by,
            current_page=current_page,
            per_page=per_page
        ))
        response_serializer = ListUsersResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )
    """
        Get User
    """
    @swagger_auto_schema(
        operation_description="Recupera um usuário pelo ID",
        responses={
            200: RetrieveUserResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        serializer = RetrieveUserRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        # import ipdb; ipdb.set_trace()
        input = GetUserRequest(**serializer.validated_data)
        use_case = GetUser(repository=ApiClientUserRepository())

        try:
            output = use_case.execute(request=input)
        except UserNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveUserResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )