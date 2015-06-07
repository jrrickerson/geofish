import sys
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from ..data import models


def geolocate_region_api(request):
    lat = request.GET('lat', None)
    lon = request.GET('lon', None)
    zipcode = request.GET('zip', None)

    # Pretend we did a GIS point to shape lookup here *wink*
    region = models.Region.objects.get(name='Lake Lanier')
    return region_detail_api(request, region.pk)


def region_detail_api(request, region_id):
    region = get_object_or_404(models.Region, pk=region_id)

    # THIS region specific info
    orgs = [region.regulatory_body]
    limits = list(region.limits.all())
    regulations = list(region.regulations.all())
    unlawful_actions = list(region.unlawful_actions.all())

    # Bubble up through all containing regions
    current_region = region
    while current_region.parent_region:
        prev_region = current_region
        current_region = current_region.parent_region
        if not current_region.regulatory_body in orgs:
            orgs.append(current_region.regulatory_body)
        limits += [lim for lim in current_region.limits.all() if lim not in limits]
        regulations += [reg for reg in current_region.regulations.all() if reg not in regulations]
        unlawful_actions += [action for action in
            current_region.unlawful_actions.exclude(exclusions=prev_region)
            if action not in unlawful_actions]
        
    species_list = [{
        'common_name': rs.species.common_name,
        'scientific_name': rs.species.scientific_name,
        'catch_limit': rs.catch_limit,
        'catch_limit_qualifier': rs.catch_limit_qualifier,
        'size_limit': rs.size_limit,
        'size_limit_qualifier': rs.size_limit_qualifier,
        'best_bet': rs.best_bet,
        'record_size': rs.record_size,
    } for rs in models.RegionSpecies.objects.filter(region=region)]

    parent_name = region.parent_region.name if region.parent_region else ''
    parent_url = reverse('region-detail', args=(region.parent_region.pk,)) if region.parent_region else ''

    return JsonResponse({
        'region': {
            'id': region.pk,
            'name': region.name,
            'parent_name': parent_name,
            'parent': parent_url,
            'orgs': [model_to_dict(org) for org in orgs],
            'limits': [model_to_dict(lim) for lim in limits],
            'regulations': [model_to_dict(reg) for reg in regulations],
            'unlawful_actions': [model_to_dict(ua) for ua in unlawful_actions],
            'species_list': species_list,
        }
    })


@csrf_exempt
def report_event_api(request):
    if not request.method == 'POST':
        return HttpResponse('{} Not Allowed'.format(request.method), status=405)
    
    print('Started view.')
    device = request.POST.get('device', '')
    event_type = request.POST.get('type', '')
    region_id = request.POST.get('region', None)
    event = models.FishingEvent(device=device, event_type=event_type, region_id=region_id, timestamp=now())
    # Optional stuff
    event.latitude = request.POST.get('latitude', None)
    event.longitude = request.POST.get('longitude', None)
    event.species = request.POST.get('species', None)
    event.size = request.POST.get('size', '')
    event.weight = request.POST.get('weight', '')
    event.notes = request.POST.get('notes', '')
    print('Built Event.')

    try:
        event.save()
    except Exception as ex:
        print(sys.exec_info())
        return HttpResponse('Data was missing or improperly formatted.', status=400)

    print('Saved Event.')

    return event_detail_api(request, event.pk)


def event_detail_api(request, event_id):
    event = get_object_or_404(models.FishingEvent, pk=event_id)

    return JsonResponse({
        'id': event.pk,
        'device': event.device,
        'type': event.event_type,
        'region': reverse('region-detail', args=(event.region.pk,),),
        'species': model_to_dict(event.species) if event.species else None,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'size': event.size,
        'weight': event.weight,
        'notes': event.notes,
    })

