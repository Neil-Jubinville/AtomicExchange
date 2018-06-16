
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from views import Home, ResetDB


urlpatterns = [

    url(r'^$', Home.as_view() ),
    url(r'^resetdb', ResetDB.as_view() ),
    url(r'^admin/', admin.site.urls),
    url(r'^bitcoin/', include('bitcoin.urls')  ),
    url(r'^ethereum/', include('ethereum.urls')  ),

]
