
from django.shortcuts import get_object_or_404, render, redirect
from .models import  Prestamo
from .forms import PrestamoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


@login_required
def listar_prestamo(request):
    query = request.GET.get('q', '')
    mes = request.GET.get('mes', '')
    monto_min = request.GET.get('monto_min', '')

    # Using Prestamo model instead of list.objects
    prestamos = Prestamo.objects.select_related('empleado').all()

    if query:
        prestamos = prestamos.filter(empleado__nombre__icontains=query)

    if mes:
        try:
            mes_int = int(mes)
            prestamos = prestamos.filter(fecha_prestamo__month=mes_int)
        except ValueError:
            print("⚠️ Mes inválido: no se aplicó filtro por mes")

    if monto_min:
        try:
            monto_val = float(monto_min)
            prestamos = prestamos.filter(monto__gte=monto_val)
        except ValueError:
            print("Monto mínimo inválido: no se aplicó filtro")

    paginator = Paginator(prestamos, 5)
    page = request.GET.get('page', 1)

    try:
        prestamos_paginados = paginator.page(page)
    except PageNotAnInteger:
        prestamos_paginados = paginator.page(1)
    except EmptyPage:
        prestamos_paginados = paginator.page(paginator.num_pages)

    contexto = {
        'prestamos': prestamos_paginados,
        'title': 'Listado de Préstamos',
        'q': query,
        'mes': mes,
        'monto_min': monto_min,
    }

    return render(request, 'prestamo/list.html', contexto)

@login_required
def crear_prestamo(request):
    contexto = {'title': 'Crear Préstamo'}
    if request.method == 'GET':
        form = PrestamoForm()
        contexto['form'] = form
        return render(request, 'prestamo/create.html', contexto)
    else:
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Nomina:listar_prestamo')
        else:
            contexto['form'] = form
            return render(request, 'prestamo/create.html', contexto)

@login_required
def actualizar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, pk=id)
    contexto = {'title': 'Actualizar Préstamo'}
    if request.method == 'GET':
        form = PrestamoForm(instance=prestamo)
        contexto['form'] = form
        return render(request, 'prestamo/create.html', contexto)
    else:
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('Nomina:listar_prestamo')
        else:
            contexto['form'] = form
            return render(request, 'prestamo/create.html', contexto)

@login_required
def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, pk=id)
    if request.method == 'POST':
        prestamo.delete()
        return redirect('Nomina:listar_prestamo')
    return render(request, 'prestamo/delete.html', {
        'prestamo': prestamo, 
        'title': 'Eliminar Préstamo'
    })