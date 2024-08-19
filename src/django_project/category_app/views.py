from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_201_CREATED,
)

from django_project._shared import meta_serializer

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    RelatedEntitiesNotFound,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)

from src.core.category.application.use_cases.list_categories import (
    ListCategories,
    ListCategoriesRequest,
    ListCategoriesResponse,
)
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.category_app.repository import DjangoORMCategoryRepository

from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoriesResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
    
)

class CategoryViewSet(viewsets.ViewSet):
    """
        List Categories
    """
    @swagger_auto_schema(
        operation_description="Lista todos as categorias do Sistema",
        responses={
            200:openapi.Schema(
                title=("Categorias"),
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_ARRAY, description=('Lista de categorias'),
                        items=openapi.Schema(type=openapi.TYPE_OBJECT, description=('Objeto de Categoria'),
                                properties= {
                                    'id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria'), example="696868c1-76b5-403b-8774-fa54e9e13123"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome da categoria'), example="Categoria 1"), 
                                    'display_name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome para exibição da categoria'), example="Cat1"), 
                                    'relationship_id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria que possui um relacionamento'), example="696868c1-76b5-403b-8774-fa54e9e13456"),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de criação da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de atualização da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description=('Flag de ativação/desativação da categoria'), example=True),
                                    'subcategories': openapi.Schema(type=openapi.TYPE_ARRAY, description=('Lista de subcategorias'),
                                                                items=openapi.Schema(                        
                                                                        type=openapi.TYPE_OBJECT,
                                                                        description=('Objeto de subcategoria'),
                                                                        properties={
                                                                                'id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria'), example="696868c1-76b5-403b-8774-fa54e9e13123"),
                                                                                'name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome da categoria'), example="Categoria 1"), 
                                                                                'display_name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome para exibição da categoria'), example="Cat1"), 
                                                                                'relationship_id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria que possui um relacionamento'), example="696868c1-76b5-403b-8774-fa54e9e13456"),
                                                                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de criação da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                                                                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de atualização da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                                                                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description=('Flag de ativação/desativação da categoria'), example=True),
                                                                                'subcategories': openapi.Schema(type=openapi.TYPE_ARRAY, description=('Lista de subcategorias'),
                                                                                                                items=openapi.Schema(type=openapi.TYPE_OBJECT, description=('Objeto de subcategoria (recursivo)'), example=""),
                                                                                                                )
                                                                            }
                                                                        ),
                                                                    )
                                    }
                            )
                        ),
                    'meta': openapi.Schema(
                        type=openapi.TYPE_OBJECT, 
                        description=('Meta Info Object'), 
                        properties={
                                'current_page': openapi.Schema(type=openapi.TYPE_INTEGER, description=('Pagina Atual'), example=1),
                                'per_page': openapi.Schema(type=openapi.TYPE_INTEGER, description=('Items por pagina'), example=10),
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER, description=('Total de itens'), example=20)
                            }
                        )
                }
            ),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        use_case = ListCategories(repository=DjangoORMCategoryRepository())
        output: ListCategoriesResponse = use_case.execute(request=ListCategoriesRequest(
            order_by=order_by,
            current_page=int(request.query_params.get("current_page", 1)),
        ))
        response_serializer = ListCategoriesResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )
    """
        Get Category
    """
    @swagger_auto_schema(
        operation_description="Busca uma categoria pelo ID",
        responses={
            200:openapi.Schema(
                title=("Categoria"),
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT, description=('Obejto de categoria'),
                        properties= {
                            'id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria'), example="696868c1-76b5-403b-8774-fa54e9e13123"),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome da categoria'), example="Categoria 1"), 
                            'display_name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome para exibição da categoria'), example="Cat1"), 
                            'relationship_id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria que possui um relacionamento'), example="696868c1-76b5-403b-8774-fa54e9e13456"),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de criação da categoria'), example="2024-08-14T20:33:41.919341Z"),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de atualização da categoria'), example="2024-08-14T20:33:41.919341Z"),
                            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description=('Flag de ativação/desativação da categoria'), example=True),
                            'subcategories': openapi.Schema(type=openapi.TYPE_ARRAY, description=('Lista de subcategorias'),
                                items=openapi.Schema(                        
                                        type=openapi.TYPE_OBJECT,
                                        description=('Objeto de subcategoria'),
                                        properties={
                                                'id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria'), example="696868c1-76b5-403b-8774-fa54e9e13123"),
                                                'name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome da categoria'), example="Categoria 1"), 
                                                'display_name': openapi.Schema(type=openapi.TYPE_STRING, description=('Nome para exibição da categoria'), example="Cat1"), 
                                                'relationship_id': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria que possui um relacionamento'), example="696868c1-76b5-403b-8774-fa54e9e13456"),
                                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de criação da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description=('Data de atualização da categoria'), example="2024-08-14T20:33:41.919341Z"),
                                                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description=('Flag de ativação/desativação da categoria'), example=True),
                                                'subcategories': openapi.Schema(type=openapi.TYPE_ARRAY, description=('Lista de subcategorias'),
                                                                                items=openapi.Schema(type=openapi.TYPE_OBJECT, description=('Objeto de subcategoria (recursivo)'), example=""),
                                                                                )
                                            }
                                        ),
                                    )
                            }
                        )
                }
            ),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCategoryRequest(**serializer.validated_data)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveCategoryResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )
    """
        Create Category
    """
    @swagger_auto_schema(
        operation_description="Cria uma categoria passando os atributos obrigatórios",
        request_body=CreateCategoryRequestSerializer,
        responses={
            200: CreateCategoryResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=input)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE})

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(output).data,
        )
    """
        Update Category
    """
    @swagger_auto_schema(
        operation_description="Atualiza uma categoria passando os atributos obrigatórios",
        request_body=UpdateCategoryRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE})

        return Response(status=HTTP_204_NO_CONTENT)

    """
        Update Category
    """
    @swagger_auto_schema(
        operation_description="Atualiza apenas os atributos desejados da categoria",
        request_body=UpdateCategoryRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def partial_update(self, request, pk: UUID = None):
        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE})

        return Response(status=HTTP_204_NO_CONTENT)
    """
        Destroy Category
    """
    @swagger_auto_schema(
        operation_description="Exclui uma categoria passando o ID",
        request_body=DeleteCategoryRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteCategoryRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteCategoryRequest(**request_data.validated_data)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)