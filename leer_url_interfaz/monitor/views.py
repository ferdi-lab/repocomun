from django.shortcuts import render, redirect
from .models import UrlMonitor
from .utils import check_url_for_changes

def check_urls(request):
    urls = UrlMonitor.objects.all()
    for url_obj in urls:
        changed, new_hash, _ = check_url_for_changes(url_obj.url, url_obj.last_hash)
        if changed:
            url_obj.last_hash = new_hash
            url_obj.has_changes = True
            url_obj.marked_done = False
        url_obj.save()
    return redirect('dashboard')

def mark_done(request, pk):
    url_obj = UrlMonitor.objects.get(pk=pk)
    url_obj.marked_done = True
    url_obj.save()
    return redirect('dashboard')

def dashboard(request):
    urls = UrlMonitor.objects.all()
    return render(request, 'dashboard.html', {'urls': urls})
