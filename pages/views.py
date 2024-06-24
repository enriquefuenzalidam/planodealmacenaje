from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.urls import reverse
from . import models




class cumuloeliminacion(LoginRequiredMixin, View):
	def get(self, request, entry_id):
		cumulo = get_object_or_404(models.Entry, pk=entry_id)
		etiquetas = cumulo.tags.split(',') if cumulo.tags else []
		etiquetas = list(set(etiquetas))
		return render(request, 'pages/borradoconfirmacion.html', {'modelTipoFila': 'Entry', 'entry_id': entry_id, 'titulo': cumulo.title, 'etiquetas': etiquetas, 'rowHasTitle': True, 'entry': cumulo})

	def post(self, request, entry_id):
		cumulo = get_object_or_404(models.Entry, pk=entry_id)
		cumulo.delete()
		return redirect('inicio')


class especificacioneliminacion(LoginRequiredMixin, View):
	def get(self, request, entry_id, element_kind, element_id):
		entry = get_object_or_404(models.Entry, pk=entry_id)
		especificacion = None
		if element_kind == 'texto':
			especificacion = get_object_or_404(models.Description, pk=element_id)
			especificacionContenido = especificacion.content[:200] + '...' if len(especificacion.content) > 200 else especificacion.content
			if especificacion.title:
				rowHasTitle = True
				especificacionTitulo = especificacion.title
			else:
				rowHasTitle = False
				especificacionTitulo = None
		elif element_kind == 'cantidad':
			especificacion = get_object_or_404(models.Number, pk=element_id)
			especificacionContenido = especificacion.number
			rowHasTitle = True
			especificacionTitulo = especificacion.number_title
		elif element_kind == 'fecha':
			especificacion = get_object_or_404(models.Date, pk=element_id)
			especificacionContenido = especificacion.date
			rowHasTitle = True
			especificacionTitulo = especificacion.date_title
		elif element_kind == 'imagen':
			especificacion = get_object_or_404(models.Image, pk=element_id)
			especificacionContenido = especificacion.image
			if especificacion.image_title:
				rowHasTitle = True
				especificacionTitulo = especificacion.image_title
			else:
				rowHasTitle = False
				especificacionTitulo = None
		elif element_kind == 'documento':
			especificacion = get_object_or_404(models.File, pk=element_id)
			especificacionContenido = especificacion.file
			if especificacion.file_title:
				rowHasTitle = True
				especificacionTitulo = especificacion.file_title
			else:
				rowHasTitle = False
				especificacionTitulo = None
		else:
			raise Http404("Especificación no encontrada")
		return render(request, 'pages/borradoconfirmacion.html', {'modelTipoFila': element_kind, 'entry_id': entry_id, 'element_id': element_id, 'titulo': especificacionTitulo, 'especificacionContenido': especificacionContenido, 'rowHasTitle': rowHasTitle})

	def post(self, request, entry_id, element_kind, element_id):
		entry = get_object_or_404(models.Entry, pk=entry_id)
		element = None
		if element_kind == 'texto':
			element = get_object_or_404(models.Description, pk=element_id)
		elif element_kind == 'cantidad':
			element = get_object_or_404(models.Number, pk=element_id)
		elif element_kind == 'fecha':
			element = get_object_or_404(models.Date, pk=element_id)
		elif element_kind == 'imagen':
			element = get_object_or_404(models.Image, pk=element_id)
		elif element_kind == 'documento':
			element = get_object_or_404(models.File, pk=element_id)
		else:
			raise Http404("Especificación no encontrada")
		element.delete()
		return redirect('cumulo', entry_id=entry_id)



class cumulo(LoginRequiredMixin, TemplateView):

	def get(self, request, entry_id):
		entry = get_object_or_404(models.Entry, pk=entry_id)
		entry_tags = entry.tags.split(',') if entry.tags else []
		entry_tags = list(set(entry_tags))
		return render(request, 'pages/cumulo.html', {'entry': entry, 'entry_tags': entry_tags})




class cumuloedicion(LoginRequiredMixin, TemplateView):
	template_name = 'pages/cumuloedicion.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		entry_id = kwargs['entry_id']
		entrada = get_object_or_404(models.Entry, pk=entry_id)
		entrada_titulo = entrada.title
		entrada_etiquetas = entrada.tags
		context['entrada'] = entrada
		context['entrada_titulo'] = entrada_titulo
		context['entrada_etiquetas'] = entrada_etiquetas
		return context

	def post(self, request, entry_id):
		nuevo_entrada = get_object_or_404(models.Entry, pk=entry_id)
		nuevo_entrada_titulo = request.POST.get('cumuloEdicionTitulo').strip()
		nuevo_entrada_etiquetas = request.POST.get('cumuloEdicionTags')
		nuevo_entrada_etiquetas_lista = [etiqueta.strip() for etiqueta in nuevo_entrada_etiquetas.strip().lower().split(',') if etiqueta.strip()]
		nuevo_entrada_etiquetas_lista = list(set(nuevo_entrada_etiquetas_lista))
		nuevo_entrada_etiquetas = ','.join(nuevo_entrada_etiquetas_lista)
		data = request.POST

		faltaCampoUno = False
		faltaCampoDos = False
		if not nuevo_entrada_titulo:
			faltaCampoUno = True
		if not nuevo_entrada_etiquetas.split():
			faltaCampoDos = True
		if faltaCampoUno or faltaCampoDos:
			return render(request, self.template_name, { 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'entry_id': entry_id, 'entrada_titulo': nuevo_entrada.title, 'data': data})
		else:
			nuevo_entrada.title = nuevo_entrada_titulo
			tagsLista = [etiqueta.strip() for etiqueta in nuevo_entrada_etiquetas.strip().lower().split(',') if etiqueta.strip()]
			tagsLista = list(set(tagsLista))
			nuevo_entrada_etiquetas = ','.join(tagsLista)
			nuevo_entrada.tags = nuevo_entrada_etiquetas
			nuevo_entrada.save()
			return redirect('cumulo', entry_id=entry_id)



class nuevocumulo(LoginRequiredMixin, TemplateView):
	template_name = 'pages/nuevocumulo.html'
	def post(self, request, *args, **kwargs):
		title = request.POST.get('nuevoCumuloTitulo').strip()
		tags = request.POST.get('nuevoCumuloTags')
		data = request.POST
		faltaCampoUno = False
		faltaCampoDos = False
		if not title or not tags:
			if not title:
				faltaCampoUno = True
			if not tags:
				faltaCampoDos = True
			return render(request, self.template_name, { 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'data': data})
		tagsLista = [etiqueta.strip() for etiqueta in tags.strip().lower().split(',') if etiqueta.strip()]
		tagsLista = list(set(tagsLista))
		tags = ','.join(tagsLista)
		entry = models.Entry.objects.create(title=title, tags=tags)
		return redirect('cumulo', entry_id=entry.pk)

class especificacion(LoginRequiredMixin, TemplateView):
	template_name = 'pages/especificacion.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		entry_id = kwargs['entry_id']
		entry = get_object_or_404(models.Entry, pk=entry_id)
		context['entry'] = entry
		return context

	def post(self, request, entry_id, element_kind):
		entry = get_object_or_404(models.Entry, pk=entry_id)
		data = request.POST
		if element_kind == 'Description':
			title = request.POST.get('nuevaEspecificacionTitulo').strip()
			content = request.POST.get('nuevaEspecificacionContent')
			if not title:
				title = None
			if not content:
				faltaCampoUno = False
				faltaCampoDos = True
				return render(request, self.template_name, {'entry': entry, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'element_kind': element_kind, 'data': data})
			models.Description.objects.create(entry=entry, title=title, content=content)
		elif element_kind == 'Number':
			number_title = request.POST.get('nuevaEspecificacionTitulo').strip()
			number = request.POST.get('nuevaEspecificacionNumber')
			faltaCampoUno = False
			faltaCampoDos = False
			noNumeroCampoDos = False
			if not number_title or not number or not number.isdigit():
				if not number_title:
					faltaCampoUno = True
				if not number:
					faltaCampoDos = True
				elif not number.isdigit():
					faltaCampoDos = True
					noNumeroCampoDos = True
				return render(request, self.template_name, {'entry': entry, 'noNumeroCampoDos': noNumeroCampoDos, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'element_kind': element_kind, 'data': data})
			models.Number.objects.create(entry=entry, number_title=number_title, number=number)
		elif element_kind == 'Date':
			date_title = request.POST.get('nuevaEspecificacionTitulo').strip()
			date = request.POST.get('nuevaEspecificacionDate')
			faltaCampoUno = False
			faltaCampoDos = False
			if not date_title or not date:
				if not date_title:
					faltaCampoUno = True
				if not date:
					faltaCampoDos = True
				return render(request, self.template_name, {'entry': entry, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'element_kind': element_kind, 'data': data})
			models.Date.objects.create(entry=entry, date_title=date_title, date=date)
		elif element_kind == 'Image':
			image_title = request.POST.get('nuevaEspecificacionTitulo').strip()
			image = request.FILES.get('nuevaEspecificacionImage')
			faltaCampoUno = False
			faltaCampoDos = False
			fleSuperLimit = False
			if not image_title:
				image_title = None
			if not image:
				faltaCampoDos = True
			if image.size > 104857600:
				fleSuperLimit = True
			if faltaCampoDos or fleSuperLimit:
				return render(request, self.template_name, {'entry': entry, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'fleSuperLimit': fleSuperLimit, 'element_kind': element_kind, 'data': data})
			models.Image.objects.create(entry=entry, image_title=image_title, image=image)
		elif element_kind == 'File':
			file_title = request.POST.get('nuevaEspecificacionTitulo').strip()
			file = request.FILES.get('nuevaEspecificacionFile')
			faltaCampoUno = False
			faltaCampoDos = False
			fleSuperLimit = False
			if not file_title:
				image_title = None
			if not file:
				faltaCampoDos = True
			if file.size > 104857600:
				fleSuperLimit = True
			if faltaCampoDos or fleSuperLimit:
				return render(request, self.template_name, {'entry': entry, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'fleSuperLimit': fleSuperLimit, 'element_kind': element_kind, 'data': data})
			models.File.objects.create(entry=entry, file_title=file_title, file=file)
		return redirect('cumulo', entry_id=entry.pk)


class especificacionedicion(LoginRequiredMixin, TemplateView):
	template_name = 'pages/especificacionedicion.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		entry_id = kwargs['entry_id']
		element_id = kwargs['element_id']
		element_kind = kwargs['element_kind']
		entry = get_object_or_404(models.Entry, pk=entry_id)
		if element_kind == 'texto':
			element = get_object_or_404(models.Description, pk=element_id)
			element_title = element.title
			element_content = element.content
		elif element_kind == 'cantidad':
			element = get_object_or_404(models.Number, pk=element_id)
			element_title = element.number_title
			element_content = element.number
		elif element_kind == 'fecha':
			element = get_object_or_404(models.Date, pk=element_id)
			element_title = element.date_title
			element_content = element.date.strftime('%Y-%m-%d')
		elif element_kind == 'imagen':
			element = get_object_or_404(models.Image, pk=element_id)
			element_title = element.image_title
			element_content = element.image
		elif element_kind == 'documento':
			element = get_object_or_404(models.File, pk=element_id)
			element_title = element.file_title
			element_content = element.file
		else:
			raise Http404("Especificación no encontrada")
		context['entry'] = entry
		context['element'] = element
		context['element_kind'] = element_kind
		context['element_title'] = element_title
		context['element_content'] = element_content
		return context

	def post(self, request, entry_id, element_kind, element_id):
		entry = get_object_or_404(models.Entry, pk=entry_id)
		if element_kind == 'texto':
			element = get_object_or_404(models.Description, pk=element_id)
		elif element_kind == 'cantidad':
			element = get_object_or_404(models.Number, pk=element_id)
		elif element_kind == 'fecha':
			element = get_object_or_404(models.Date, pk=element_id)
		elif element_kind == 'imagen':
			element = get_object_or_404(models.Image, pk=element_id)
		elif element_kind == 'documento':
			element = get_object_or_404(models.File, pk=element_id)
		else:
			raise Http404("Especificación no encontrada")
		data = request.POST

		if element_kind == 'texto':
			element.title = data.get('especificacionEdicionTitulo').strip()
			element.content = data.get('especificacionEdicionContent').strip()
			if not element.title:
				element.title = None
			if not element.content:
				faltaCampoDos = True
				return render(request, self.template_name, { 'faltaCampoDos': faltaCampoDos, 'entry_id': entry.pk, 'element_kind': element_kind, 'element_id': element.pk, 'entry': entry, 'data': data})
		elif element_kind == 'cantidad':
			element.number_title = data.get('especificacionEdicionTitulo').strip()
			cantidad = data.get('especificacionEdicionNumber')
			faltaCampoUno = False
			faltaCampoDos = False
			noNumeroCampoDos = False
			if not element.number_title or not cantidad or not cantidad.isdigit():
				if not element.number_title:
					faltaCampoUno = True
				if not cantidad:
					faltaCampoDos = True
				elif not cantidad.isdigit():
					faltaCampoDos = True
					noNumeroCampoDos = True
				return render(request, self.template_name, { 'noNumeroCampoDos': noNumeroCampoDos, 'faltaCampoUno': faltaCampoUno, 'faltaCampoDos': faltaCampoDos, 'entry_id': entry.pk, 'element_kind': element_kind, 'element_id': element.pk, 'entry': entry, 'data': data})
			else:
				element.number = cantidad
		elif element_kind == 'fecha':
			element.date_title = data.get('especificacionEdicionTitulo').strip()
			element.date = data.get('especificacionEdicionDate')
			faltaCampoUno = False
			if not element.date_title:
				faltaCampoUno = True
				return render(request, self.template_name, { 'faltaCampoUno': faltaCampoUno, 'entry_id': entry.pk, 'element_kind': element_kind, 'element_id': element.pk, 'entry': entry, 'data': data})
		elif element_kind == 'imagen':
			element.image_title = data.get('especificacionEdicionTitulo').strip()
			image = request.FILES.get('especificacionEdicionImage')
			if not element.image_title:
				element.image_title = None
			if image:
				element.image = image
		elif element_kind == 'documento':
			element.file_title = data.get('especificacionEdicionTitulo').strip()
			file = request.FILES.get('especificacionEdicionFile')
			if not element.file_title:
				element.file_title = None
			if file:
				element.file = file
		element.save()
		return redirect('cumulo', entry_id=entry.pk)


class inicio(LoginRequiredMixin, TemplateView):
	template_name = 'pages/inicio.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_template'] = self.template_name
		return context

	def post(self, request, *args, **kwargs):
		buscadosEtiquetas = [etiqueta.strip() for etiqueta in request.POST.get('porEtiquetaBusqueda', '').strip().lower().split(',') if etiqueta.strip()]
		cumulos = models.Entry.objects.all()
		encontradosCumulos = []
		for cumulo in cumulos:
			cumuloEtiquetas = [etq.strip() for etq in cumulo.tags.strip().lower().split(',')]
			if any(bEtq == etq for bEtq in buscadosEtiquetas for etq in cumuloEtiquetas):
				encontradosCumulos.append(cumulo)
		encontradosCumulos = list(set(encontradosCumulos))
		return render(request, 'pages/busquedaresultados.html', {'encontradosCumulos': encontradosCumulos, 'buscadosEtiquetas': buscadosEtiquetas})


class busquedaresultados(LoginRequiredMixin, TemplateView):
	template_name = 'pages/busquedaresultados.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		encontradosCumulos = []
		buscadosEtiquetas = []
		if 'buscadosEtiquetas' in kwargs:
			encontradosCumulos = kwargs.get('encontradosCumulos', [])
			buscadosEtiquetas = kwargs.get('buscadosEtiquetas', [])
		else:
			cumulos = models.Entry.objects.all()
			tag = self.kwargs.get('tag', []).strip().lower()
			for cumulo in cumulos:
				cumuloEtiquetas = [etq.strip() for etq in cumulo.tags.strip().lower().split(',')]
				if any(tag == etq for etq in cumuloEtiquetas):
					encontradosCumulos.append(cumulo)
			encontradosCumulos = list(set(encontradosCumulos))
			buscadosEtiquetas.append(tag)

		context['encontradosCumulos'] = encontradosCumulos
		context['buscadosEtiquetas'] = buscadosEtiquetas
		return context

class identificacion(LoginRequiredMixin, TemplateView):
	template_name = 'pages/identificacion.html'
