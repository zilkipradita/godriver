from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from datetime import date
from datetime import time
from datetime import datetime
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from driver.models import Users_roles
from driver.models import Users
from driver.models import Trips
from driver.models import Order_trips
from driver.serializers import Users_rolesSerializer
from driver.serializers import Users_Serializer
from driver.serializers import Trips_Serializer
from driver.serializers import Order_tripsSerializer
from driver.serializers import User_loginSerializer
from driver.serializers import Create_userSerializer
from driver.serializers import Create_tripsSerializer
from driver.serializers import Takes_orderSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import jwt
from datetime import timedelta
from random import randrange
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def index(request):
    return HttpResponse("Hello, world. You're at the Driver index.")

@csrf_exempt
@swagger_auto_schema(methods=['POST'], request_body=Create_userSerializer)
@api_view(['POST'])
def create_user(request):
    dt = datetime.now() 
    response_data = {} 
    
    if request.method == 'POST':
        users_data = JSONParser().parse(request)
        users_serializer = Users_Serializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()

            response_data['code'] = '201'
            response_data['message'] = 'CREATED'
            response_data['result'] = users_serializer.data
            response_data['date'] = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            users = Users.objects.get(id=users_serializer.data['id']) 
            users_data['password'] = make_password(users_data['password'])
            users_serializer = Users_Serializer(users, data=users_data) 
            if users_serializer.is_valid(): 
                users_serializer.save() 

            return JsonResponse(response_data, status=status.HTTP_201_CREATED) 
        
        response_data['code'] = '412'
        response_data['message'] = 'PRECONDITION FAILED'
        response_data['result'] = users_serializer.errors
        response_data['date'] = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

        return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED)

@csrf_exempt
@swagger_auto_schema(methods=['POST'], request_body=User_loginSerializer)
@api_view(['POST']) 
def login(request):
    dt = datetime.now() 
    response_data = {} 

    if request.method == 'POST':
        users_data = JSONParser().parse(request)
        username = users_data['username']
        password = users_data['password']

        users = Users.objects.filter(username=username)
        if users.count() > 0 :
            users_data = Users.objects.get(username=username)
            users_serializer = Users_Serializer(users_data) 
            decoded = check_password(password,users_serializer.data['password'])
            if decoded == True :

                users = {}
                users['id']       = users_serializer.data['id']
                users['username'] = users_serializer.data['username']
                users['name']     = users_serializer.data['name']
                users['telp']     = users_serializer.data['telp']
                users['email']    = users_serializer.data['email']

                users_rolesdata = Users_roles.objects.get(id=users_serializer.data['users_roles'])
                users_rolesserializer = Users_rolesSerializer(users_rolesdata)                 

                roles = {}
                roles['id']   = users_rolesserializer.data['id']
                roles['name'] = users_rolesserializer.data['name']
                    
                result = {}
                result['users'] = users
                result['roles'] = roles
                    
                response_data['code']    = '200'
                response_data['message'] = 'Username and Password is match, Successfully login, Welcome '+ users_serializer.data['name']  
                response_data['token']   = generate_token(username)  
                response_data['result']  = result
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                return JsonResponse(response_data,  status=status.HTTP_200_OK, safe=False) 
            else :
                response_data['code']    = '412'
                response_data['message'] = 'Username and Password is not match, Failed to login'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)
               
                return JsonResponse(response_data,  status=status.HTTP_412_PRECONDITION_FAILED, safe=False) 
        else :
            response_data['code']    = '404'
            response_data['message'] = 'Username is not found'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND, safe=False) 

def generate_token(username):
    dt=datetime.utcnow()+timedelta(minutes=60)

    payload = {}
    payload["username"] = username
    payload["exp"]      = dt
        
    encoded_jwt = jwt.encode(payload, "5b9799a5860f950804d839736c300d99", algorithm="HS256")

    return encoded_jwt

@csrf_exempt
@swagger_auto_schema(methods=['POST'], request_body=Create_tripsSerializer, manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['POST'])
def create_trips(request):
  dt = datetime.now() 
  response_data = {}
    
  if request.method == 'POST':
        trips_data = JSONParser().parse(request)    
        trips_data['cost'] = randrange(1000, 100000, 1000)
        trips_serializer = Trips_Serializer(data=trips_data)

        if trips_serializer.is_valid():
            users = Users.objects.get(id=trips_data['users'])
            if users.users_roles_id ==1:

                trips = Trips.objects.filter(status='available', users_id=trips_data['users'])
                if trips.count() > 0 :

                    response_data['code']    = '412'
                    response_data['message'] = 'This users ('+ trips_data['users'] +') has created trip before, and the trip is still available, delete it first if you want to make a new trip'
                    response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                    return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED)
                else :
                    trips_serializer.save()

                    response_data['code']    = '201'
                    response_data['message'] = 'CREATED'
                    response_data['result']  = trips_serializer.data
                    response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                    return JsonResponse(response_data, status=status.HTTP_201_CREATED) 
            else:
                response_data['code']    = '412'
                response_data['message'] = 'Only User level can create a trip, your level is Driver'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED)
        else :
            response_data['code']    = '412'
            response_data['message'] = 'PRECONDITION FAILED'
            response_data['result']  = trips_serializer.errors
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED)

@swagger_auto_schema(methods=['GET'], manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['GET'])
def show_trips(request):
    dt = datetime.now() 
    response_data = {}
    result = {}
    data = {}
        
    if request.method == 'GET': 
        trips = Trips.objects.select_related('users').filter(status="available").order_by('id')
        
        count = 0
        while count <= trips.count()-1:
            data[count] = {
                "id": trips[count].id,
                "destination": trips[count].destination,
                "location": trips[count].location,
                "cost": trips[count].cost,
                "status": trips[count].status,
                "users_id": trips[count].users.id,
                "name": trips[count].users.name,
                "telp": trips[count].users.telp,
                "email": trips[count].users.email,
                "created_at": trips[count].created_at,
                "updated_at": trips[count].updated_at,
                }
            count+=1

        result['count'] = trips.count()
        result['data'] = data
        
        response_data['code']    = '200'
        response_data['message'] = 'OK'  
        response_data['result']  = result
        response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

        return JsonResponse(response_data,  status=status.HTTP_200_OK, safe=False)    

@swagger_auto_schema(methods=['DELETE'], manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['DELETE'])
def delete_trips(request, id, user):
    dt = datetime.now() 
    response_data = {}
        
    if request.method == 'DELETE': 
        try: 
            trips = Trips.objects.get(id=id, status='available', users_id=user) 
            trips.delete() 

            response_data['code']    = '200'
            response_data['message'] = 'Trips was deleted successfully!'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Trips.DoesNotExist: 
            response_data['code']    = '404'
            response_data['message'] = 'Trip does not exist'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
        
@csrf_exempt
@swagger_auto_schema(methods=['POST'], request_body=Takes_orderSerializer, manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['POST'])
def takes_order(request):
    dt = datetime.now() 
    response_data = {}
    result = {}
        
    if request.method == 'POST': 
        order_tripsdata = JSONParser().parse(request)
        order_tripsserializer = Order_tripsSerializer(data=order_tripsdata)

        if order_tripsserializer.is_valid():
            trips = Trips.objects.get(id=order_tripsdata['trips'])
            if trips.status == 'available' :

                driver = Users.objects.get(id=order_tripsdata['driver'])
                if driver.users_roles_id ==2:

                    order_trips = Order_trips.objects.filter(trips__status='taken', driver_id=order_tripsdata['driver'])
                    if order_trips.count() > 0:
                        response_data['code']    = '412'
                        response_data['message'] = 'You can not take this trip because you already takes another trip, finish it first then you can take another trip'
                        response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                        return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED, safe=False)      
                    else:
                        order_tripsserializer.save()

                        trips.status = 'taken'
                        trips.save()

                        trips_serializer = Trips_Serializer(trips) 

                        result['order']  = order_tripsserializer.data
                        result['trip']   = trips_serializer.data
                               
                        response_data['code']    = '201'
                        response_data['message'] = 'CREATED'
                        response_data['result']  = result
                        response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                        return JsonResponse(response_data, status=status.HTTP_201_CREATED)         
                else :
                    response_data['code']    = '412'
                    response_data['message'] = 'Only Driver level can take this trip, your level is User'
                    response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                    return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED, safe=False)  
            else :
                response_data['code']    = '412'
                response_data['message'] = 'The selected trip is already taken'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED, safe=False)        
        else :
            response_data['code']    = '412'
            response_data['message'] = 'PRECONDITION FAILED'
            response_data['result']  = order_tripsserializer.errors
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED)

@swagger_auto_schema(methods=['GET'], manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['GET'])   
def trips_status(request, id):
    dt = datetime.now() 
    response_data = {}
    driver = {}
    result = {}

    if request.method == 'GET': 
        try: 
            trips = Trips.objects.get(id=id)
            trips_serializer = Trips_Serializer(trips) 

            try:        
                order_trips = Order_trips.objects.select_related('driver').get(trips_id=id)

                driver['id']       = order_trips.driver.id
                driver['username'] = order_trips.driver.username
                driver['name']     = order_trips.driver.name
            except Order_trips.DoesNotExist: 
                driver['id']       = ''
                driver['username'] = ''
                driver['name']     = ''
                
            result['trip']   = trips_serializer.data
            result['driver'] = driver

            response_data['code']    = '200'
            response_data['message'] = 'OK'
            response_data['result']  = result
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Trips.DoesNotExist: 
            response_data['code']    = '404'
            response_data['message'] = 'Trip does not exist'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
            


@swagger_auto_schema(methods=['PUT'], manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['PUT'])  
def order_done(request, id, driver):
    dt = datetime.now() 
    response_data = {}

    if request.method == 'PUT': 
        try: 
            order_trips = Order_trips.objects.get(trips_id=id, driver_id=driver)

            trips = Trips.objects.get(id=id)
            trips_serializer = Trips_Serializer(trips) 
            trips.status = 'done'
            trips.save()

            response_data['code']    = '200'
            response_data['message'] = 'OK'
            response_data['result']  = trips_serializer.data
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Order_trips.DoesNotExist: 
            response_data['code']    = '404'
            response_data['message'] = 'Order Trip does not exist'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
        
@swagger_auto_schema(methods=['PUT'], manual_parameters=[openapi.Parameter('token',openapi.IN_HEADER,description="token", type=openapi.IN_HEADER),openapi.Parameter('username',openapi.IN_HEADER,description="username", type=openapi.IN_HEADER)])
@api_view(['PUT'])  
def order_canceled(request, id, driver):
    dt = datetime.now() 
    response_data = {}

    if request.method == 'PUT': 
        try: 
            order_trips = Order_trips.objects.get(trips_id=id, driver_id=driver)

            try:
                trips = Trips.objects.get(id=id, status='taken') 
                trips_serializer = Trips_Serializer(trips) 
                trips.status = 'available'
                trips.save()
                    
                order_trips.delete()
                    
                response_data['code']    = '200'
                response_data['message'] = 'OK'
                response_data['result']  = trips_serializer.data
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                return JsonResponse(response_data, status=status.HTTP_200_OK)
            except Trips.DoesNotExist: 
                response_data['code']    = '404'
                response_data['message'] = 'Only trip in taken status that can be canceled'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
        except Order_trips.DoesNotExist: 
            response_data['code']    = '404'
            response_data['message'] = 'Order Trip does not exist'
            response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

            return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)