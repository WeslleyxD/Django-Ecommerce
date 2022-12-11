from django.core.paginator import Paginator
from django.shortcuts import render


def pagination(request, objects: list, per_page: int):
    paginator = Paginator(objects, per_page) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
    #return render(request, 'list.html', {'page_obj': page_obj})