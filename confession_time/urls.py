
#import the necessary items
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import Settings
from django.conf.urls.static import static
from confessions import urls as confessions_urls
from ctime_api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(confessions_urls)),
    path('api/', include(api_urls))
]
