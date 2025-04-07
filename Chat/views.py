from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from .models import Room

def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            try:
                room = Room.objects.get(name=name)
                return HttpResponseRedirect(reverse("room", args=[room.pk]))
            except Room.DoesNotExist:
                pass
            room = Room.objects.create(name=name, host=request.user)
            return HttpResponseRedirect(reverse("room", args=[room.pk]))
    return render(request, 'Chat/index.html')

def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'Chat/room.html', {
        "room":room,
    })