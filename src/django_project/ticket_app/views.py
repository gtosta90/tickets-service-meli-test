from uuid import UUID

from django.shortcuts import render
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
from src.core.ticket.application.use_cases.create_ticket import (
    CreateTicket,
    CreateTicketRequest,
)
from src.core.ticket.application.use_cases.delete_ticket import DeleteTicket, DeleteTicketRequest
from src.core.ticket.application.use_cases.exceptions import (
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
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "title")
        use_case = ListTickets(repository=DjangoORMTicketRepository())
        output: ListTicketsResponse = use_case.execute(request=ListTicketsRequest(
            order_by=order_by,
            current_page=int(request.query_params.get("current_page", 1)),
        ))
        response_serializer = ListTicketsResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        serializer = RetrieveTicketRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetTicketRequest(**serializer.validated_data)
        use_case = GetTicket(repository=DjangoORMTicketRepository())

        try:
            output = use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveTicketResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def create(self, request: Request) -> Response:
        serializer = CreateTicketRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateTicketRequest(**serializer.validated_data)
        use_case = CreateTicket(repository=DjangoORMTicketRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateTicketResponseSerializer(output).data,
        )

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateTicketRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        input = UpdateTicketRequest(**serializer.validated_data)
        use_case = UpdateTicket(repository=DjangoORMTicketRepository())
        try:
            use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk: UUID = None):
        serializer = UpdateTicketRequestSerializer(data={
            **request.data,
            "id": pk,
        }, partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateTicketRequest(**serializer.validated_data)
        use_case = UpdateTicket(repository=DjangoORMTicketRepository())
        try:
            use_case.execute(request=input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteTicketRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteTicketRequest(**request_data.validated_data)
        use_case = DeleteTicket(repository=DjangoORMTicketRepository())
        try:
            use_case.execute(input)
        except TicketNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)