"""ConferenceRooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from conference.views import NewRoom, RoomList, DeleteRoom, ModifyRoom, RoomDetails, ReserveRoom, SearchRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', RoomList.as_view(), name='rooms'),
    path('room/new', NewRoom.as_view(), name='new_room'),
    path('room/delete/<int:id>', DeleteRoom.as_view(), name='delete_room'),
    path('room/modify/<int:id>', ModifyRoom.as_view(), name='modify_room'),
    path('room/details/<int:id>', RoomDetails.as_view(), name='details'),
    path('room/reserve/<int:id>', ReserveRoom.as_view(), name='reserve'),
    path('search', SearchRoom.as_view(), name='search')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
