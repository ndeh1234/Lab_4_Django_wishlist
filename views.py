from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

# This view renders the list of places that have not been visited yet.
@login_required
def place_list(request):

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

# This view renders the places_visited page.
@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

# This view will either 404 or update the place.visited value.
@login_required
def place_was_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk = pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request):
    pk = request.POST.get('pk')
    place = get_object_or_404(Place, pk=pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()