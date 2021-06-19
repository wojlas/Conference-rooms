from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.views import View

from conference.models import Room


class RoomList(View):
    def get(self, request):
        rooms = Room.objects.order_by('capacity')
        return render(request, 'conference/index.html', context={'rooms': rooms})


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
        room = Room.objects.get(pk=int(id))
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
        if not new_name or new_cap or choice:
            message = 'Some field is empty'
            return render(request, 'conference/error-page.html', context={'error_code': message})
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
            return HttpResponseRedirect (reverse('rooms'))

class RoomDetails(View):
    def get(self, request, id):
        room = Room.objects.filter(pk=id)
        return render(request, 'conference/room_details.html', context={'rooms':room})