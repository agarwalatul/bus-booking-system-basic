from django.db import transaction, DatabaseError
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from booking_system.models import Trip, TripSeatStatus, BookingStatus, Ticket
from booking_system.serializer import TripSerializer, TripSeatStatusSerializer, TicketSerializer
from user.models import User


class TripList(APIView):
    def get(self, request, format=None):
        trips = Trip.objects.all()
        return Response([TripSerializer(trip).data for trip in trips])

    def post(self, request, format=None):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripDetail(APIView):

    def get_object(self, pk):
        try:
            return Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        trip = self.get_object(pk)
        trip_seats = TripSeatStatus.objects.filter(trip=trip)
        return Response([TripSeatStatusSerializer(ts).data for ts in trip_seats])

    def put(self, request, pk, format=None):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        match = user.check_password(password)
        trip = self.get_object(pk)
        trip_seat_status = request.data['id']
        seat_exists = TripSeatStatus.objects.filter(id=trip_seat_status, status=BookingStatus.AVAILABLE.value).exists()
        if not seat_exists:
            return Response(data={'reason': 'other user trying to booking/Already booked the ticket'},
                            status=status.HTTP_409_CONFLICT)

        try:
            with transaction.atomic():
                tss = TripSeatStatus.objects.select_for_update(nowait=True).get(id=trip_seat_status)
                ticket = Ticket.objects.create(user=user, trip=trip, seat=tss.seat)
                tss.status = BookingStatus.BOOKED.value
                ticket.save()
                tss.save()
                return Response(status=status.HTTP_201_CREATED)
        except DatabaseError as db_err:
            print(db_err)
            # increment db_err metric
            return Response(data={'reason': 'other user trying to booking'}, status=status.HTTP_409_CONFLICT)
        except TripSeatStatus.DoesNotExist as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TicketList(APIView):
    def get(self, request, format=None):
        tickets = Ticket.objects.all()
        return Response([TicketSerializer(ticket).data for ticket in tickets])
