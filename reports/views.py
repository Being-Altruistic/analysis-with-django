from django.shortcuts import render, get_object_or_404, redirect
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image, remove_record
from .models import Report, assign_peers
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

import uuid, random
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from analysis_with_django.settings import EMAIL_HOST_USER




@login_required
def ReportDetailViewSecured(request, pk, token):

    rep = Report.objects.get(pk=pk)


    if request.method == 'POST':
        print(request.POST)
        instance = assign_peers.objects.get(token = token, assigned_to = request.user, report = rep)
        instance.comments = request.POST.get('floatingTextarea2')
        instance.save()

        
    if assign_peers.objects.filter(token = token, assigned_to = request.user, report = rep).exists() or assign_peers.objects.filter(assigned_by = request.user).exists():

        qs = assign_peers.objects.filter(token = token, report = rep, assigned_by=request.user)


        for i in qs:
            i.notification="VIEWED"

        assign_peers.objects.bulk_update(qs, ['notification'])
        
        context ={
            'allow_view':True,
            'report_detail_obj':rep,
            'token':token,
            'all_comments':assign_peers.objects.filter(token = token, report = rep, comments__isnull= False),
            'request': request
        }

    else:
        context ={
                'allow_view':False
            }
    

    return render(request, 'reports/pvt_detail.html',context)





def assign_report(request,pk):
    if request.method == 'POST':

        print('request::>>', request.POST)

        
        if request.POST.get('operation',False):
            return remove_record(pk,request)


        if request.POST.getlist('emails') != []:
            
            print('request::>>', request.POST.getlist('emails'))


            if assign_peers.objects.filter(report_id=pk).exists():
                assign_peers.objects.filter(report_id=pk).delete()



            token_access = str(uuid.uuid4()).replace('-','').lower()[:12]+str(random.randint(0,9))

            # Objects for Bulk Create
            qs_objects = []

            for i in request.POST.getlist('emails'):
                print(i)
                qs_objects.append(
                    
                                assign_peers(
                                                assigned_by = request.user,
                                                assigned_to = User.objects.get(username = i),
                                                token = token_access,
                                                report = Report.objects.get(id=pk)
                                            )

                                )

            print(qs_objects)


            # Bulk Create
            assign_peers.objects.bulk_create(
                qs_objects
            )


            # Get reports obj

            report_obj = Report.objects.get(id=pk)
            access_lnk_peer_obj = assign_peers.objects.filter(token = token_access, report = report_obj).first()





            template_data = {
                'repno':report_obj.id,
                'name':report_obj.name,
                'remark':report_obj.remarks,
                'created':report_obj.created,

                # build_absolute_uri
                'access_link':request.build_absolute_uri(access_lnk_peer_obj.get_absolute_url()),
            }

            print('IMP TESTEST @@##$$', template_data)


            html_body= render_to_string('reports/assign_peer_emailtemp.html', template_data)

            msg = EmailMultiAlternatives(
                subject="Important! |  Invite to Peer Review the attached Sales Report.",

                body=html_body,

                # From Asigned by | Reply to Assigned By | to Assigned to

                from_email=EMAIL_HOST_USER,

                to=request.POST.getlist('emails'),

                reply_to=[EMAIL_HOST_USER],
            )

            msg.mixed_subtype = 'related'
            msg.attach_alternative(html_body, "text/html")

            msg.send()
        
        else:
            print('No Data')


    return JsonResponse({'msg':request.POST})




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

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)

        all_report_ids = Report.objects.all().values_list('id')


        context.update({
            'assign_peers_qs': assign_peers.objects.filter(assigned_by=self.request.user,report_id__in=all_report_ids),
            'users': User.objects.all(),
            'notifications':assign_peers.objects.filter(assigned_by=self.request.user, report_id__in=all_report_ids, notification='NOTIFIED'),
        })

        print('MMYY KWARGS::>>', assign_peers.objects.filter(assigned_by=self.request.user, report_id__in=all_report_ids, notification='NOTIFIED'))
        return context

    
''' For above Class
def get_queryset(self):
        return CharacterSeries.objects.order_by('name')


        <<< ABOVE OP as of NOW >>> SAMPLE P TO LEARN >>>
        MMYY KWARGS::>> {'paginator': None, 'page_obj': None, 'is_paginated': False, 'object_list': <QuerySet [<Report: aknasbcjna>, <Report: This Report for Quaterly Months>, <Report: eewaawd>, 
        <Report: YOYYOYOYOOY>, <Report: dadad>, <Report: dadad>, <Report: dadad>, <Report: dadad>, <Report: adasas>, <Report: Test Report>]>, 'report_list_obj': <QuerySet [<Report: aknasbcjna>, 
        <Report: This Report for Quaterly Months>, <Report: eewaawd>, <Report: YOYYOYOYOOY>, 
        <Report: dadad>, <Report: dadad>, <Report: dadad>, <Report: dadad>, <Report: adasas>, <Report: Test Report>]>, 
        'view': <reports.views.ReportListView object at 0x0000020F8004D430>, 
        'assign_peers_qs': <QuerySet [<assign_peers: 04a2c62236e91:  admin[ > ]edumats100@gmail.com>, <assign_peers: 2facdbcb41a62:  admin[ > ]edumats100@gmail.com>, 
        <assign_peers: 4e49d644f40b6:  admin[ > ]edumats100@gmail.com>]>}
        
'''
        
    

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



