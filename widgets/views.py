from django.shortcuts import render

from .models import Widget


def index(request):
    return render(request, "index.html")


def widgets(request):
    if request.method == "POST":
        query = Widget.objects.filter(key=request.POST["key"])
        if query.count():
            for obj in query.all():
                obj.value = request.POST["value"]
                obj.save()
        else:
            obj = Widget(key=request.POST["key"], value=request.POST["value"])
            obj.save()
    widgets = Widget.objects.all()
    return render(request, "widgets.html", {"widgets": widgets})
