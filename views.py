
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .db import push2dB

def health(request):
    return JsonResponse({"status":200,"API":"Finally Running"})

@csrf_exempt
def data2dB(request):
    print("Arjun")
    try:
        if 'application/json' in request.META['CONTENT_TYPE']:
            json_data= json.loads(request.body)
            result = push2dB(json_data)
            return JsonResponse({"status":200,"Message":result["message"]})
    except Exception as e:
            return JsonResponse ({"status_code":500,"message":str(e)})
