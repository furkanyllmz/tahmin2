from django.urls import path
from .import views
from .views import newsletter_signup,newsletter_success
from .views import ads_txt

urlpatterns =[
    path("",views.home),
    path("home",views.home),
    path("matches",views.match_predictions_view),
    path("matches/<str:id>",views.match_details_view,name="details"),
    path('newsletter/', newsletter_signup, name='newsletter'),
    path('newsletter-success/', newsletter_success, name='newsletter_success'),
    path("google67322d1adb8aa749.html",views.googlesearchconsole),
    path("ads.txt", ads_txt, name="ads_txt"),

    


]