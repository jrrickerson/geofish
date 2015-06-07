from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'region/geo$', views.geolocate_region_api, name='geolocate-region'),
    url(r'region/([0-9]+)$', views.region_detail_api, name='region-detail'),
    #url(r'org/$', views.org_list_api, name='org-list'),
    #url(r'org/([0-9]+)/$', views.org_detail_api, name='org-detail'),
    #url(r'reg/$', views.reg_list_api, name='reg-list'),
    #url(r'reg/([0-9]+)/$', views.reg_detail_api, name='reg-detail'),
    #url(r'limit/$', views.limit_list_api, name='limit-list'),
    #url(r'limit/([0-9]+)/$', views.limit_detail_api, name='limit-detail'),
    #url(r'unlawful/$', views.unlawful_list_api, name='unlawful-list'),
    #url(r'unlawful/([0-9]+)/$', views.unlawful_detail_api, name='unlawful-detail'),
    #url(r'species/$', views.species_list_api, name='species-list'),
    #url(r'species/([0-9]+)/$', views.species_detail_api, name='species-detail'),
    url(r'event$', views.report_event_api, name='report-event'),
    url(r'event/([0-9]+)$', views.event_detail_api, name='event-detail'),
]

