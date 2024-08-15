from django.contrib import admin

from django_project.ticket_app.models import Ticket

class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)