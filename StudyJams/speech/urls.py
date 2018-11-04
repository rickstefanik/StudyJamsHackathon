from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'speech'


urlpatterns = [
    #url(r'^$', ListView.as_view(queryset=FacultyMember.objects.all().order_by("name"), template_name="faculty/faculty.html"))
    url(r'^$', views.index, name="index"),
]
