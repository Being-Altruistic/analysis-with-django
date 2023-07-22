from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from sales.models import Sale, Position, CSV
import csv
from django.utils.dateparse import parse_date
from products.models import Product
from customers.models import Customer

#  Protecting Function based Views using Decorators 
from django.contrib.auth.decorators import login_required
#  Protecting Class based Views using Mixins 
from django.contrib.auth.mixins import LoginRequiredMixin





def ReportDelete(request, pk):
    print('DELETEDELETE >><<<$$@@@', pk)
    Report.objects.get(pk=pk).delete()
    return JsonResponse({'msg': 'deleted'})




# For Dropzone
class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'reports/from_file.html'

# For Dropzone
@login_required
def csv_upload_view(request):
    print('@@@@@@@@@ File being sent')

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')

        # Create CSV entries.
        obj, created = CSV.objects.get_or_create(file_name = csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)

                # To avoid the header row
                reader.__next__() 
                for row in reader:

                    transaction_id  = row[0]
                    product         = row[1]
                    quantity_no     = int(row[2])
                    customer        = row[3]

                    # DATE TO PARSE MUST BE YYYY-MM-DD Format
                    date            = parse_date(row[4])


                    '''
                    TASK 1

                    1. Create Products in DB from Excel Data, if not exist else continue
                    2. Create Customer bought Product Exist
                    3. Create Salesman
                    4. Create Position
                    5. Create Sales Instance
                    '''
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    
                    # If Product instance for get() is None
                    except Product.DoesNotExist:
                        product_obj = None
                    
                    if product_obj is not None:
                        print('CUSTOMER', customer)
                        # _ = created. If doesn't exist & new created, then created = True
                        # Create the customer who's product exists.
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)

                        # Current Logged-in User
                        salesman_obj = Profile.objects.get(user=request.user)

                        position_obj = Position.objects.create(
                            product = product_obj,
                            quantity = quantity_no,
                            created = date
                        )

                        # Due to Get or Create, the records are not repeated here.
                        sale_obj, _ = Sale.objects.get_or_create(
                            transaction_id = transaction_id,
                            customer = customer_obj,
                            salesman = salesman_obj,
                            created = date
                        )

                        # Updating Sale M2M Field
                        # Sale.Position field
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()

                return JsonResponse({'ex':False})
        else:
            return JsonResponse({'ex':True})


# Listing The Reports Created
class ReportListView(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/main.html'
    context_object_name = "report_list_obj"
    

class ReportDetailView(LoginRequiredMixin,DetailView):
    model = Report
    template_name = 'reports/detail.html'
    context_object_name = "report_detail_obj"
    

@login_required
def create_report_view(request):
    # if request.is_ajax():
    if request.method=='POST':
        print('POST CHECK ******',request.POST)
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        author= Profile.objects.get(user  = request.user)

        Report.objects.create(
            name = name,
            remarks = remarks,
            image = img,
            author = author
        )
    
        
    return JsonResponse({'msg':'Send Successfully'})


'''
AIM : View taken directly from xhtml2pdf package usage site

TO : Generate PRINTABLE / PDF VIEW for each REPORT
TO : Download PRINTABLE / PDF VIEW for each REPORT

Else, we can to the same using JS

This is much dynamic. No JS.
'''

def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # To Download PDF
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    # To Display the PDF
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response



