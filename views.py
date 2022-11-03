
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .pushdata import push2dB
from .customer_login import Login
from .token_validation import token_authentication
from .devices import Device
from .SourceData import ViewData
from .dashboard import Dash

def health(request):
    return JsonResponse({"status":"Success","Message":"API Running"})

@csrf_exempt
# @token_authentication
def data2dB(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)
            result = push2dB(json_data)
            return JsonResponse({"Message":result["message"]})
    except Exception as e:
        return JsonResponse({"status":"Fail","error":str(e)})

@csrf_exempt
#@api_view(['POST'])
def login(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)        
            login_class = Login(json_data)
            result = login_class.user_authentication()
            return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({"status":"Fail","error":str(e)})
    
@csrf_exempt
@token_authentication
def device_list(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            token = request.headers['Authorization'].split()[1]
            json_data= {"token":token}
            device_class = Device(json_data)
            result = device_class.device_details()
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse({"status":"Fail","error":str(e)})
        
@csrf_exempt
@token_authentication
def update_device(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body) 
            device_class = Device(json_data)
            result = device_class.modify_device_details()
            return JsonResponse(result,safe=False)
    except Exception as e:
        return JsonResponse({"status":"Fail","error":str(e)})

@csrf_exempt
@token_authentication
def activity_details(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            token = request.headers['Authorization'].split()[1]
            json_data= {"token":token}
            device_class = Device(json_data)
            result = device_class.activity_list()
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse({"status":"Fail","error":str(e)})

@csrf_exempt
@token_authentication
def view_sourcedata(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body) 
            source_data_class = ViewData(json_data)
            result = source_data_class.view_data()
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse({"status":"Fail","error":str(e)})
        
@csrf_exempt
@token_authentication
def edit_sourcedata(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body) 
            source_data_class = ViewData(json_data)
            result = source_data_class.update_data()
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse({"status":"Fail","error":str(e)})

@csrf_exempt
@token_authentication
def get_analytics_data(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body) 
            analytics_data_class = Dash(json_data)
            result = analytics_data_class.GetData()
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse({"status":"Fail","error":str(e)})