from django.shortcuts import render
from .models import Profile
# Create your views here.
from .forms import Profileform

from django.contrib.auth.decorators import login_required


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user = request.user)

    # Instance is provided to display existing values.
    form  = Profileform(request.POST or None, request.FILES or None, instance=profile)
    # Profile creation confirmation.
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/main.html', context)


