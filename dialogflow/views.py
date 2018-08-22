from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import actions
import json


def index(request):
    return render(request, 'dialogflow/index.html', {
        'WEB_DEMO_URL': settings.DIALOGFLOW['WEB_DEMO_URL'],
    })


@require_POST
@csrf_exempt
def fulfillment(request):
  
    action_name = request.JSON['result']['action'].replace('-', '_')
    params = request.JSON['result']['parameters']

    # action_name = json.loads(request.body)['result']['action']
    # params      = json.loads(request.body)['result']['parameters']
    action = getattr(actions, action_name, None)

    print("action name -> %s" % action_name)
    print("param -> %s" % params)
    print("action -> %s" % action)
    # return {'speech': '제가 처리할 수 없는 부분입니다.',}

    if callable(action):
        response = action(**params)
    else:
        response = {
            'speech': '제가 처리할 수 없는 부분입니다.',
        }

    return response

"""
def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

return data

@require_http_methods(['POST'])
def fulfillment(request):
    #dialogflow_ = dialogflow(**settings.DIALOGFLOW)
    input_dict = convert(request.body)
    input_text = json.loads(input_dict)['text']
    print ("input text",input_text)
    #responses = dialogflow_.text_request(str(input_text))
    access_token = 'cab0e92861494ed2bddff46324771fe4'
    client = apiai.ApiAI(access_token)
    request_1 = client.text_request()
    request_1.query =input_text
    #print(request.query)
    #request_1.query = "Today is 13th December, 2018" # or whatever other input the user puts
    byte_response = request_1.getresponse().read()
    json_response = byte_response.decode('utf8')#.replace("'", '"') # replaces all quotes with double quotes
    json_obj = json.loads(json_response)
    print (json_obj['result']['fulfillment']['speech'])
    if request.method == "GET":
        # Return a method not allowed response
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)
    elif request.method == "POST":
        data = {
            'text': str(json_obj['result']['fulfillment']['speech']),
        }
        return JsonResponse(data, status=200)
        #return HttpResponse(json_obj['result']['fulfillment'])
    elif request.method == "PATCH":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    elif request.method == "DELETE":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
return JsonResponse(data, status=405)

"""