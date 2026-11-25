from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')

def experience_view(request):
    return render(request, 'pages/experience.html')

def projects_view(request):
    return render(request, 'pages/projects.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

#nosotros hacemos el ccs, 