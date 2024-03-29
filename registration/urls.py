from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('results',views.results,name='results'),
    path('details', views.details, name='details'),
    path('questions', views.ques, name='ques'),
    path('social/signup',views.signup_redirect,name='signup_redirect'),
    path('login',views.handleLogin,name='handleLogin'),
    path('sign-up',views.handleSignUp,name='handleSignUp'),
    path('club-members',views.club_members,name='club_members'),
    path('club-members/search/<str:category>/<str:search_term>',views.search,name='search'),
    path('club-members/filter/<int:type>',views.filter,name='filter'),
    path('club-members/inductees/<int:id>',views.student_profile,name='student_profile'),
    path('like/<int:id>',views.like,name='like_student'),
    path('mark/<int:id>/<int:type>',views.mark,name="mark"),
    path('StudentsCSV', views.StudentsCSV, name="StudentsCSV"),
    path('WebCSV', views.WEBCSV, name="WEBCSV"),
    path('EventCSV', views.eventCSV, name="EventCSV"),
    path('ContentCSV', views.contentCSV, name="ContentCSV"),
    path('TechCSV', views.videoCSV, name="TechCSV"),
    path('GraphicCSV', views.GdCSV, name="GraphicCSV"),
    path('MaleCSV', views.MaleCSV, name="MaleCSV"),
    path('FemaleCSV', views.FemaleCSV, name="FemaleCSV"),
    path('RecentCSV', views.getPosts, name="RecentCSV"),
]