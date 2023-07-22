from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id,get_salesman_from_id, get_graph, get_chart
# Create your views here.
#  Protecting Function based Views using Decorators 
from django.contrib.auth.decorators import login_required
#  Protecting Class based Views using Mixins 
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def home_view(request):
    sales_df = None
    position_df = None
    df = None
    merged_df = None
    chart = None
    no_data = None
    
    # telling the form that action is on POST
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        sale_qs = Sale.objects.filter(created__date__lte=request.POST.get('date_to'),
                                created__date__gte=request.POST.get('date_from'))
        
        print(request.POST.get('chart_type'))
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        
        if len(sale_qs) > 0:
            position_data = []

            for sale in sale_qs:
                for pos in sale.get_positions():
                    position_data.append({
                    'position_id': pos.id,
                    'position': pos.product.name,
                    'quantity': pos.quantity,
                    'price': pos.price,
                    'sales_id': sale.id,
                    })

            # print('############1::>>',sale_qs)
            # print('############2::>>',position_data)
            # Passing Dictionary format.
            sales_df = pd.DataFrame(sale_qs.values())


            # Re-Defining Values | From ID values > Name values using APPLY()
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%d-%m-%Y'))

            sales_df.rename({'customer_id': 'Customer', 'salesman_id': 'Salesman','id':'sales_id'}, axis=1, inplace=True)

            # sales_df['sales_id'] = sales_df['id']

            position_df = pd.DataFrame(position_data)

            merged_df = pd.merge(sales_df, position_df, on='sales_id')

                                # perform on column                  # Apply agg on
            # df = merged_df.groupby('transaction_id', as_index = False)['price'].agg('sum')

            '''
            if as_index = T
            transaction_id 0FE074D4A956 10000.0 26C569DA8BA6 1010000.0 9D21F7FDF4F6 1000000.0 F68434AE7EF6 2560000.0 Name: price, dtype: float64
            '''
            
            # Plotting Charts
            # Here, work is done only on Sales_df data & not on MErged Data
            # For Result By
            chart = get_chart(chart_type, merged_df, results_by)

            # DFs cant be directly rendered in to HTML
            # Need to specially format it.
            sales_df = sales_df.to_html()
            position_df = position_df.to_html()
            merged_df = merged_df.to_html()
            # df = df.to_html()


            # print('$$$$$$>>>>',sales_df)
        else:
            no_data = 'No Data Available in inputted Timeline'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'position_df':position_df,
        'merged_df':merged_df,
        'df':df,
        'chart':chart,
        'no_data':no_data,
    }


    return render(request, 'sales/home.html',context)

# Using generics for Sale Listing
class SaleListView(LoginRequiredMixin,ListView):
    '''
    Display list with absolute URL
    This URL wil match to the DetailURL View
    '''
    model = Sale
    template_name = 'sales/main.html'
    context_object_name = "orm_obj_lists"


class SaleDetailView(LoginRequiredMixin,DetailView):
    model = Sale
    template_name = 'sales/detail.html'
    context_object_name = "orm_obj_detail"


