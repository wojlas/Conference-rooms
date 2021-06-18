from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from conference.models import Room

class RoomList(View):
    def get(self, request):
        rooms = Room.objects.order_by('capacity')
        return render(request, 'conference/index.html', context={'rooms':rooms})

class NewRoom(View):
    def get(self, request):

        return render(request, 'conference/new-room.html')

    def post(self, request):
        name = request.POST.get('room_name')
        capacity = int(request.POST.get('room_capacity'))
        projector_yes = request.POST.get('projector_yes')
        projector_no = request.POST.get('projector_no')
        rooms = Room.objects.order_by('id')
        if not name:
            message = 'Name field is empty'
            return render(request, 'conference/error-page.html', context={'error_code':message})
        for room in rooms:
            if name == room:
                message = f'Name {name} already exist'
                return render(request, 'conference/error-page.html', context={'error_code':message})

        if capacity < 0:
            message = 'Capacity must be bigger than 0'
            return render(request, 'conference/error-page.html', context={'error_code': message})

        if projector_yes:
            choice = True
        elif projector_no:
            choice = False
        else:
            message = 'You must select projectof choice'
            return render(request, 'conference/error-page.html', context={'error_code': message})

        Room.objects.create(name=name, capacity=capacity, projector=choice)
        return HttpResponseRedirect(reverse('rooms'))



