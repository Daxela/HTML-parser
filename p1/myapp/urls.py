from django.urls import path
from . import views
from . import frontviews


urlpatterns = [
    path('main/request/work/<int:request_id>/', views.Basic.as_view()),
    path('main/request/work/<int:request_id>/deleted/', views.Del.as_view()),
    path('main/request/work/<int:request_id>/ignored/', views.Ign.as_view()),
    path('main/request/work/', views.Main.as_view()),
    path('main/', frontviews.main),
    path('main/request/', frontviews.req),
    path('main/history/', frontviews.history)
]

