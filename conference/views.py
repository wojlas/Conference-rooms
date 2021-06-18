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
        capacity = request.POST.get('room_capacity')
        projector_yes = request.POST.get('projector_yes')
        projector_no = request.POST.get('projector_no')
        rooms = Room.objects.order_by('id')
        if not name:
            return HttpResponse ('Name field is empty')
        if not Room.objects.get(name=name):
                return HttpResponse (f'Room {name} already exist')

        # if not capacity.min < capacity < capacity.max:
        #     return HttpResponse (f'Capacity must be between {capacity.min} - {capacity.max} ')
        if projector_yes:
            choice = True
        elif projector_no:
            choice = False
        else:
            return HttpResponse ('You must select projector choice')
        Room.objects.create(name=name, capacity=capacity, projector=choice)
        return HttpResponseRedirect(reverse('rooms'))



