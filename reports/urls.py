from django.urls import path
from .views import (create_report_view,ReportListView,
                    render_pdf_view, ReportDetailView,UploadTemplateView,ReportDetailViewSecured,
                    csv_upload_view,assign_report)

app_name = 'reports'

urlpatterns = [
    path('',ReportListView.as_view(),name='main'),
    path('save/',create_report_view,name='create-report'),


    # To Upload EXcel File & Extract Excel Data
    path('upload/',csv_upload_view,name='upload'),

    # To Display DropZone JS
    path('from_file/',UploadTemplateView.as_view() ,name='from-file'),
    
    path('<pk>/',ReportDetailView.as_view(),name='detail'),
    path('<pk>/pdf/',render_pdf_view ,name='pdf-page'),

    path('assign_report/<int:pk>',assign_report ,name='assign'),
    path('assign_report/<int:pk>/<str:token>',ReportDetailViewSecured,name='secured_detail'),

]

