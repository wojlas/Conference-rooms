from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.views import View

from conference.models import Room, Book


class RoomList(View):
    def get(self, request):
        rooms = Room.objects.order_by('capacity')
        return render(request, 'conference/index.html', context={'rooms': rooms})

    def post(self, request):
        rooms = Room.objects.order_by('capacity')
        date = request.POST.get('date_choice')
        all_rooms = Room.objects.all()
        for room in all_rooms:
            for room in Book.objects.all():
                book_date = str(room.date)
                format_date = datetime.strptime(book_date, '%Y-%m-%d').date()
                date_int = int(format_date.strftime('%Y-%m-%d'))
            all_rooms.reserved = datetime.date(date) in format_date


        return render(request, 'conference/index.html', context={'rooms':all_rooms, 'date':date})




class NewRoom(View):
    def get(self, request):

        return render(request, 'conference/new-room.html')

    def post(self, request):
        name = request.POST.get('room_name')
        capacity = request.POST.get('room_capacity')
        projector_yes = request.POST.get('projector_yes')
        projector_no = request.POST.get('projector_no')

        if projector_yes:
            choice = True
        elif projector_no:
            choice = False
        else:
            message = 'You must select projector choice'
            return render(request, 'conference/error-page.html', context={'error_code': message})
        if not (name or capacity or choice):
            message = 'Some field is empty'
            return render(request, 'conference/error-page.html', context={'error_code': message})
        if name in Room.objects.all():
            message = f'Name {name} already exist'
            return render(request, 'conference/error-page.html', context={'error_code': message})
        if int(capacity) < 0:
            message = 'Capacity must be bigger than 0'
            return render(request, 'conference/error-page.html', context={'error_code': message})

        Room.objects.create(name=name, capacity=capacity, projector=choice)
        return HttpResponseRedirect(reverse('rooms'))


class DeleteRoom(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        room.delete()
        return HttpResponseRedirect(reverse('rooms'))


class ModifyRoom(View):
    def get(self, request, id):
        room = Room.objects.filter(pk=id)
        return render(request, 'conference/modify-room.html', context={'rooms': room})

    def post(self, request, id):
        new_name = request.POST.get('new_name')
        new_cap = request.POST.get('new_capacity')
        projector_yes = request.POST.get('projector_yes')
        projector_no = request.POST.get('projector_no')
        room = Room.objects.get(pk=id)

        if projector_yes:
            choice = True
        elif projector_no:
            choice = False
        else:
            message = 'You must select projectof choice'
            return render(request, 'conference/error-page.html', context={'error_code': message})
        # if not new_name or new_cap or choice:
        #     message = 'Some field is empty'
        #     return render(request, 'conference/error-page.html', context={'error_code': message})
        if new_name == room.name:
            message = 'Name already exist'
            return render(request, 'conference/error-page.html', context={'error_code': message})

        for name in Room.objects.all():
            if new_name == name.name:
                message = 'New name already exist in base'
                return render(request, 'conference/error-page.html', context={'error_code': message})

        else:
            room.name = str(new_name)
            room.capacity = int(new_cap)
            room.projector = choice
            return HttpResponseRedirect(reverse('rooms'))


class RoomDetails(View):
    def get(self, request, id):
        room = Room.objects.filter(pk=id)
        return render(request, 'conference/room_details.html', context={'rooms': room})


class ReserveRoom(View):
    def get(self, request, id):
        room = Room.objects.filter(pk=id)
        return render(request, 'conference/reserve-room.html', context={'room': room})

    def post(self, request, id):
        try:
            date_now = datetime.today()
            date_now_int = int(date_now.strftime('%Y%m%d'))
            room = Room.objects.get(pk=id)
            comment = request.POST.get('comment')
            date = request.POST.get('date')
            format_date = datetime.strptime(date, '%Y-%m-%d')
            date_int = int(format_date.strftime('%Y%m%d'))

            # if format_date in Book.date:
            #     message = 'Room is busy'
            #     return render(request, 'conference/error-page.html', context={'error_code': message})
            if date_int < date_now_int:
                message = 'Wrong date'
                url = f'/room/reserve/{id}'
                return render(request, 'conference/error-page.html', context={'error_code': message, 'url':url})
            if comment == ' ':
                message = 'Comment is empty'
                url = f'/room/reserve/{id}'
                return render(request, 'conference/error-page.html', context={'error_code': message, 'url': url})
            Book.objects.create(date=date_int, room_id_id=room.id ,comment=comment)
            return HttpResponseRedirect (reverse('rooms'))
        except AttributeError as e:
            return HttpResponse(e)
            # url = f'/room/reserve/{id}'
            # return render(request, 'conference/error-page.html', context={'error_code':'Room not in database', 'url':url})
        except ValueError:
            url = f'/room/reserve/{id}'
            return render(request, 'conference/error-page.html',
                          context={'error_code': 'The date must be set', 'url': url})