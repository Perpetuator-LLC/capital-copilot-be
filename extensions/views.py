from django.shortcuts import render


def task_detail(request):
    return render(request, "landing/home.html")
