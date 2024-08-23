import json
import logging
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)


from core.category.application.use_cases.exceptions import InvalidCategory
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.user_app.repository import ApiClientUserRepository
from src.core.ticket.application.use_cases.create_ticket import (
    CreateTicket,
    CreateTicketRequest,
)
from src.core.ticket.application.use_cases.delete_ticket import DeleteTicket, DeleteTicketRequest
from src.core.ticket.application.use_cases.exceptions import (
    RelatedEntitiesNotFound,
    TicketNotFound,
)
from src.core.ticket.application.use_cases.get_ticket import (
    GetTicket,
    GetTicketRequest,
)

from src.core.ticket.application.use_cases.list_tickets import (
    ListTickets,
    ListTicketsRequest,
    ListTicketsResponse,
)
from src.core.ticket.application.use_cases.update_ticket import UpdateTicket, UpdateTicketRequest
from src.django_project.ticket_app.repository import DjangoORMTicketRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository

from src.django_project.ticket_app.serializers import (
    CreateTicketRequestSerializer,
    CreateTicketResponseSerializer,
    DeleteTicketRequestSerializer,
    ListTicketsResponseSerializer,
    RetrieveTicketRequestSerializer,
    RetrieveTicketResponseSerializer,
    UpdateTicketRequestSerializer,
    
)

class TicketViewSet(viewsets.ViewSet):
    logger = logging.getLogger('tickets-service')
    """
        List Tickets
    """
    @swagger_auto_schema(
        operation_description="Lista todos os tickets do Sistema",
        responses={
            200: ListTicketsResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def list(self, request: Request) -> Response:
        self.logger.debug(request)
        order_by = request.query_params.get("order_by", "title")
        current_page = int(request.query_params.get("current_page", 1))
        per_page = int(request.query_params.get("per_page", 10))

        use_case = ListTickets(ticket_repository=DjangoORMTicketRepository(), category_repository=DjangoORMCategoryRepository())
        output: ListTicketsResponse = use_case.execute(request=ListTicketsRequest(
            order_by=order_by,
            current_page=current_page,
            per_page=per_page
        ))
        response_serializer = ListTicketsResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )
    """
        Get Tickets
    """
    @swagger_auto_schema(
        operation_description="Recupera um ticket pelo id",
        responses={
            200: RetrieveTicketResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        self.logger.debug(request)
        serializer = RetrieveTicketRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetTicketRequest(**serializer.validated_data)
        use_case = GetTicket(ticket_repository=DjangoORMTicketRepository(), category_repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveTicketResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )
    """
        Create Ticket
    """
    @swagger_auto_schema(
        operation_description="Cria um ticket passando os atributos obrigatórios",
        request_body=openapi.Schema(
            title=("Ticket"),
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, example="Ticket 1"),
                'user_create': openapi.Schema(type=openapi.TYPE_NUMBER, description=('ID do usuario criador do Ticket'), example=1),
                'category': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da categoria do Ticket'), example="696868c1-76b5-403b-8774-fa54e9e13123"),
                'subcategory': openapi.Schema(type=openapi.TYPE_STRING, description=('ID da subcategoria do Ticket'), example="696868c1-76b5-403b-8774-fa54e9e13456"), 
                'severity': openapi.Schema(type=openapi.TYPE_NUMBER, description=('Severidade do Ticket'), example=1, enum=[1,2,3,4]), 
                'description': openapi.Schema(type=openapi.TYPE_NUMBER, description=('Descrição do Ticket'), example="Ticket 1 Description"),
                'user_assigned': openapi.Schema(type=openapi.TYPE_STRING, description=('ID do usuario responsável pelo Ticket'), example=0),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description=('Status do Ticket'), example="OPEN", enum=['OPEN', 'IN SERVICE', 'COMPLETED', 'CLOSED'])
            }
        ),
        responses={
            200: RetrieveTicketResponseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def create(self, request: Request) -> Response:
        self.logger.debug(request)
        serializer = CreateTicketRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateTicketRequest(**serializer.validated_data)
        use_case = CreateTicket(            
            ticket_repository=DjangoORMTicketRepository(),
            user_repository=ApiClientUserRepository(),
            category_repository=DjangoORMCategoryRepository())
        
        try:
            output = use_case.execute(request=input)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE}
            )
        return Response(
            status=HTTP_201_CREATED,
            data=CreateTicketResponseSerializer(output).data,
        )
    
    """
        Update Ticket
    """
    @swagger_auto_schema(
        operation_description="Atualiza um ticket passando os atributos obrigatórios",
        request_body=UpdateTicketRequestSerializer,
        responses={
            200: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def update(self, request: Request, pk: UUID = None):
        self.logger.debug(request)
        serializer = UpdateTicketRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        input = UpdateTicketRequest(**serializer.validated_data)
        use_case = UpdateTicket(
            ticket_repository=DjangoORMTicketRepository(),
            user_repository=ApiClientUserRepository(),
            category_repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE}
            )
        
        return Response(status=HTTP_204_NO_CONTENT)

    
    """
        Partial Update Ticket
    """
    @swagger_auto_schema(
        operation_description="Atualiza apenas os atributos desejados do ticket",
        request_body=UpdateTicketRequestSerializer,
        responses={
            200: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def partial_update(self, request, pk: UUID = None):
        self.logger.debug(request)
        serializer = UpdateTicketRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateTicketRequest(**serializer.validated_data)
        
        use_case = UpdateTicket(            
            ticket_repository=DjangoORMTicketRepository(),
            user_repository=ApiClientUserRepository(),
            category_repository=DjangoORMCategoryRepository())
        
        try:
            use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except RelatedEntitiesNotFound as error:
            return Response(
                status=HTTP_406_NOT_ACCEPTABLE,
                data= {'error': error.__str__(), 'status': HTTP_406_NOT_ACCEPTABLE}
            )
        
        return Response(status=HTTP_204_NO_CONTENT)

    """
        Destroy Ticket
    """
    @swagger_auto_schema(
        operation_description="Exclui um ticket",
        request_body=DeleteTicketRequestSerializer,
        responses={
            200: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        }
    )
    def destroy(self, request: Request, pk: UUID = None):
        self.logger.debug(request)
        request_data = DeleteTicketRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteTicketRequest(**request_data.validated_data)
        use_case = DeleteTicket(repository=DjangoORMTicketRepository())
        try:
            use_case.execute(input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)