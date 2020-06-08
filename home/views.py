from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from course.models import Registration


@login_required
def home(request):
    registrations = Registration.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    context = {"registrations": registrations}
    return render(request, "home/index.html", context)
