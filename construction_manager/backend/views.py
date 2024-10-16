from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import ConstructionSite, Material
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import datetime


def get_material_quantity(request, site_id, material_id):
    try:
        material = Material.objects.get(id=material_id, site_id=site_id)
        return JsonResponse({'quantity': material.quantity})
    except Material.DoesNotExist:
        return JsonResponse({'quantity': 0})


def get_materials_for_site(request, site_id):
    materials = Material.objects.filter(site_id=site_id)
    materials_list = list(materials.values('id', 'description', 'quantity'))
    return JsonResponse(materials_list, safe=False)

@require_POST
def move_material(request):
    data = json.loads(request.body)
    departure_site_id = data['departure_site']
    material_id = data['material_description']
    quantity = int(data['quantity'])
    destination_site_id = data['destination_site']

    try:
        material = Material.objects.get(id=material_id, site_id=departure_site_id)
        if material.quantity < quantity:
            return HttpResponseBadRequest('Insufficient quantity at departure site')

        # Update the quantity at the departure site
        material.quantity -= quantity
        material.save()

        # Check if the material exists at the destination site
        destination_material, created = Material.objects.get_or_create(
            description=material.description,
            unit=material.unit,
            unit_price=material.unit_price,
            n_bc=material.n_bc,
            n_bl=material.n_bl,
            supplier=material.supplier,
            site_id=destination_site_id,
            defaults={
                'quantity': quantity,
                'total_price': material.total_price,
                'notes': material.notes,
                'entry_date': datetime.now(),
            }
        )
        if not created:
            # If the material already exists, just update the quantity and entry date
            destination_material.quantity += quantity
            destination_material.entry_date = datetime.now()
            destination_material.save()

        return JsonResponse({'message': 'Material moved successfully'})
    except Material.DoesNotExist:
        return HttpResponseBadRequest('Material not found at departure site')

def home(request):
    sites = ConstructionSite.objects.all()
    return render(request, 'home.html', {'sites': sites})

def materials(request):
    materials = Material.objects.all()
    sites = ConstructionSite.objects.all()
    return render(request, 'materials.html', {'materials': materials, 'sites': sites})

def inventory(request):
    materials = Material.objects.all()
    return render(request, 'inventory.html', {'materials': materials})
def movement(request):
    sites = ConstructionSite.objects.all()
    return render(request, 'movement.html', {'sites': sites})

@csrf_exempt
def add_construction_site(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        site = ConstructionSite.objects.create(name=data['name'])
        return JsonResponse({'id': site.id, 'name': site.name, 'last_modified': site.last_modified})

@csrf_exempt
def delete_construction_site(request, site_id):
    site = get_object_or_404(ConstructionSite, id=site_id)
    site.delete()
    return HttpResponse(status=204)

@csrf_exempt
def add_material(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        site = get_object_or_404(ConstructionSite, id=data['site_id'])
        material = Material.objects.create(
            description=data['description'],
            quantity=data['quantity'],
            unit=data['unit'],
            unit_price=data['unit_price'],
            total_price=data['total_price'],
            n_bc=data['n_bc'],
            n_bl=data['n_bl'],
            supplier=data['supplier'],
            site=site,
            notes=data['notes']
        )
        return JsonResponse({'id': material.id, 'description': material.description, 'quantity': material.quantity, 'unit': material.unit, 'unit_price': material.unit_price, 'total_price': material.total_price, 'n_bc': material.n_bc, 'n_bl': material.n_bl, 'entry_date': material.entry_date, 'supplier': material.supplier, 'site': material.site.name, 'notes': material.notes})

@csrf_exempt
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return HttpResponse(status=204)
