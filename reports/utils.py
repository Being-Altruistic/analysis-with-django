import base64, uuid
from django.core.files.base import ContentFile
from django.http import JsonResponse
from reports.models import assign_peers
from django.contrib.auth.models import User


def remove_record(pk, request):
    try:
        if assign_peers.objects.filter(report_id=pk, assigned_to = User.objects.get(username = request.POST.get('username'))).exists():
            user_obj = User.objects.get(username = request.POST.get('username'))
            assign_peers.objects.filter(report_id=pk, assigned_to = user_obj).delete()
        else:
            return JsonResponse({'message':'OK','status':200})
    except:
        print('&&&&&^^ Error &&&&&&&&&^^^^^')



def get_report_image(data):
    print('utils>>>>>><<>>>', data)

    # The data has key as image & 2 values.
    # Split will return splitting 2 values into 2 variables.
    
    split_data_1st_part, str_image_2nd_part = data.split()
    print('utils>>>>>><<>>>', split_data_1st_part)
    print('utils>>>>>><<>>>', str_image_2nd_part)
    
    '''
    Also can be written as
    _ is used if the first split part is not required or no use.
    _, str_image_2nd_part = data.split()
    split_data_1st_part, str_image_2nd_part = data.split()
    '''
    decoded_img = base64.b64decode(str_image_2nd_part)
    img_name = str(uuid.uuid4())[:10] + '.png'
    data = ContentFile(decoded_img, name=img_name)
    return data