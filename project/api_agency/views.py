from django.shortcuts import render
from rest_framework.decorators import api_view
from api_agency.serializers import *
from api_agency.models import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.




@api_view(['GET','POST'])
def agencies(request):
    if request.method=='GET':
        agencies=Agency.objects.all()
        serializer=AgencySerializer(agencies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        data=request.data
        serializer=AgencySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
def agency_details(request,pk):
    try:
        agency=Agency.objects.get(pk=pk)
    except Agency.DoesNotExist:
        return Response("Agency doesn't exist",status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer=AgencyDetailSerializer(agency)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        data=request.data
        serializer=AgencyDetailSerializer(data=data,instance=agency)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        agency.delete()
        return Response("Agency deleted",status=status.HTTP_202_ACCEPTED)


@api_view(['GET','POST'])
def branches(request):
    if request.method=='GET':
        branches=Branch.objects.all()
        serializer=BranchSerializer(branches,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        data=request.data
        serializer=BranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def branch_details(request,pk):
    try:
        branch=Branch.objects.get(pk=pk)
    except branch.DoesNotExist:
        return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer=BranchSerializer(branch)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        data=request.data
        serializer=BranchSerializer(data=data,instance=branch)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        branch.delete()
        return Response("Branch deleted",status=status.HTTP_202_ACCEPTED)
    
@api_view(['GET'])
def agency_branches(request,pk):
    agency=agency_details(request,pk)
    branches=Branch.objects.filter(agency=pk)
    
    serializer=BranchSerializer(branches,many=True)
    return Response(serializer.data,status= status.HTTP_200_OK)




@api_view(['GET'])
def vehicles_makes(request):
    makes=Make.objects.all()
    serializer=MakeSerializer(makes,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def vehicles_models(request,pk):
    models=Model.objects.filter(make_id=pk)
    serializer=ModelSerializer(models,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)



