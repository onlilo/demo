
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .pushdata import push2dB
from .customer_login import Login
from .token_validation import token_authentication
from .devices import Device


def health(request):
    return JsonResponse({"status":200,"Message":"API Running"})

@csrf_exempt
@token_authentication
def data2dB(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)
            result = push2dB(json_data)
            return JsonResponse({"Message":result["message"]})
    except:
            return JsonResponse ({"status":"Fail","status_code":500})

@csrf_exempt
#@api_view(['POST'])
def login(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)        
            login_class = Login(json_data)
            result = login_class.user_authentication()
            return JsonResponse(result, safe=False)
    except:
        return JsonResponse({"status_code":500,"status":"Fail"})
    
@csrf_exempt
@token_authentication
def device_list(request):
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)
            device_class = Device(json_data)
            result = device_class.device_details(json_data)
            return JsonResponse(result,safe=False)
    except Exception as e:
            return JsonResponse ({"status":"Fail","status_code":500,"error":str(e)})
