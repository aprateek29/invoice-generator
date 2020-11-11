from django.shortcuts import render, redirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .models import Product
from .forms import addForm


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


data = {
    "company": "The Prateek's Company",
    "address": "123 Street name",
    "city": "John Cenapur",
    "state": "Delhi",
    "zipcode": "110101",


    "phone": "555-555-2345",
    "email": "company@gmail.com",
    "website": "johncena.com",
	# "invoice_total": '5165.00',
	# "product_list": [{'name':'Concepts of Physics Vol I & II ', 'price': 999.00, 'quantity': 2, 'product_total': 1998.00} ,{'name':'Predictive Astrology of the Hindus', 'price': 535.00, 'quantity': 1, 'product_total': 535.00},{'name':'Astro Sutra', 'price': 175.00, 'quantity': 5, 'product_total': 875.00},{'name':'Foundation PCMB (Science + Maths) for IIT-JEE/NEET/Olympiad for Class 9', 'price': 767.00, 'quantity': 2, 'product_total': 1534.00},{'name':'Foundation Mathematics for IIT-JEE/Olympiad for Class 10 ', 'price': 223.00, 'quantity': 1, 'product_total': 223.00}]
}

# Opens up page as PDF


class ViewPDF(View):


	def get(self, request, *args, **kwargs):

		product_list = Product.objects.all()
		invoice_total = 0
		for product in product_list:
			invoice_total += product.price

		data['product_list'] = product_list
		data['invoice_total'] = invoice_total
		pdf = render_to_pdf('billing/pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('billing/pdf_template.html', data)
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" % ("12341231")
		content = "attachment; filename='%s'" % (filename)
		response['Content-Disposition'] = content
		return response


def index(request):
    context = {}
    return render(request, 'billing/index.html', context)

def add_product(request):
	if request.method == 'POST':
		form = addForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	form = addForm()
	return render(request, 'billing/add.html', {'form':form})

def remove_all(request):
	ok = Product.objects.all()
	if len(ok) > 5:
		product = Product.objects.all()[5:]
		l = []
		for i in product:
			l.append(i.id)
		print(l)
		Product.objects.filter(id__in=l).delete()
	return redirect('/')