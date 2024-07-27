from datetime import date, datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api_auth.models import User
from api_auth.serializers import UserDetailsSerializer
from api_agency.serializers import AgencyDetailSerializer,AgencySerializer,RateDetailsSerializer,BranchDetailsSerializer,VehicleDetailsSerializer,VehicleSerializer,AgencyReservationDetailsSerializer,FeedbackSerializer,ReportSerializer
from api_agency.models import Agency,Branch,Vehicle,Reservation,Rate,Feedback,Report,Subscription
from api_admin.permissions import IsAdmin
from api_admin.serializers import *
from api_destination.models import Destination,DestinationRate,DestinationFeedback
# from api_destination.serializers import DestinationSerializer,RateDetailsSerializer
import api_destination.serializers as api_destination_serializers
from api_activity.models import Activity,ActivityRate,ActivityFeedback
import api_activity.serializers as api_acticity_serializers
from rest_framework.decorators import api_view
from django.db.models import Sum,Count
from django.db.models.functions import TruncYear,TruncMonth
from rest_framework import filters
from api_admin.filters import ClientAgeFilter


# Create your views here.

#-----------------------------------USERS-------------------------------------#

class AdminUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAdmin]

class AdminUserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        else:
            return AdminUserUpdateSerializer
    
#-----------------------------------AGENCIES-------------------------------------#

class AdminAgencyList(generics.ListAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [IsAdmin]

class AdminValidateAgency(generics.UpdateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_validated != True:
            print(F"Agency not validated")
            instance.is_validated = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminAgencyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AgencyDetailSerializer
        else:
            return AgencySerializer


class AdminAgencyRatings(generics.ListAPIView):
    queryset = Rate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = RateDetailsSerializer


class AdminAgencyRatingsDetails(generics.RetrieveDestroyAPIView):
    queryset = Rate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = RateDetailsSerializer


class AdminAgencyFeedbacks(generics.ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = FeedbackSerializer


class AdminAgencyFeedbacksDetails(generics.RetrieveDestroyAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = FeedbackSerializer

#-----------------------------------BRANCHES-------------------------------------#

class AdminBranchList(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminBranchSerializer
        else:
            return BranchDetailsSerializer
        


class AdminBranchDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BranchDetailsSerializer
        else:
            return AdminBranchSerializer
        
#-----------------------------------VEHICLES-------------------------------------#


class AdminVehicleList(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = VehicleDetailsSerializer


class AdminVehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdmin]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VehicleDetailsSerializer
        else:
            return VehicleSerializer
    
#-----------------------------------RESERVATIONS-------------------------------------#

class AdminReservationList(generics.ListAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AgencyReservationDetailsSerializer




class AdminReservationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AgencyReservationDetailsSerializer
        else:
            return AdminReservationSerializer
#-----------------------------------DESTINATIONS-------------------------------------#
class AdminDestinationList(generics.ListAPIView):
    queryset = Destination.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminDestinationSerializer

class AdminDestinationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdminDestinationSerializer
        else:
            return api_destination_serializers.DestinationSerializer


class AdminDestinationRatings(generics.ListAPIView):
    queryset = DestinationRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.RateDetailsSerializer



class AdminDestinationRatingsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = DestinationRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.RateDetailsSerializer

class AdminDestinationFeedbacks(generics.ListAPIView):
    queryset = DestinationFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.FeedbackSerializer


class AdminDestinationFeedbacksDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = DestinationFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.FeedbackSerializer


#-----------------------------------ACTIVITIES-------------------------------------#

class AdminActivityList(generics.ListAPIView):
    queryset = Activity.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminActivitySerializer



class AdminActivityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdminActivitySerializer
        else:
            return api_acticity_serializers.ActivitySerializer
        

class AdminActivityRatings(generics.ListAPIView):
    queryset = ActivityRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.RateDetailsSerializer


class AdminActivityRatingsDetails(generics.RetrieveDestroyAPIView):
    queryset = ActivityRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.RateDetailsSerializer



class AdminActivityFeedbacks(generics.ListAPIView):
    queryset = ActivityFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.FeedbackSerializer



class AdminActivityFeedbacksDetails(generics.RetrieveDestroyAPIView):
    queryset = ActivityFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.FeedbackSerializer

#-----------------------------------REPORTS-------------------------------------#

class AdminReportsList(generics.ListAPIView):
    queryset = Report.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = ReportSerializer




class AdminReportsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = ReportSerializer





#-----------------------------------STATESTICS-------------------------------------#



@api_view(['GET'])
def users_stats(request):
    if request.method == 'GET':
        all_users = User.objects.exclude(role = 'admin').exclude(role = 'branch_admin')
        agencies = all_users.filter(role = 'agency_admin').count()
        clients = all_users.filter(role = 'default').count()
        all_users = all_users.count()
        # all_users_serializer = UserDetailsSerializer(all_users,many = True)
        # agencies_serializer = UserDetailsSerializer(agencies,many = True)
        # clients_serializer = UserDetailsSerializer(clients,many = True)
        perc_all_users = 100
        perc_agencies = agencies*perc_all_users / all_users
        perc_clients = clients*perc_all_users / all_users
        result = {
            "all_users":all_users,
            "agencies":agencies,
            "clients":clients,
            "perc_all_users":perc_all_users,
            "perc_agencies":perc_agencies,
            "perc_clientsr":perc_clients,
        }
        return Response(result, status = status.HTTP_200_OK)      

# @api_view(['GET'])
# def reservations_status_stats(request):
#     if request.method == 'GET':
#         wilaya_pk = request.GET.get('wilaya')
#         all_reservations = total_reservations = Reservation.objects.all()
#         total_accepted_reservations = total_reservations.filter(status = 'accepted').count()
#         total_refused_reservations = total_reservations.filter(status = 'refused').count()
#         total_postponed_reservations = total_reservations.filter(status = 'postponed').count()
#         #calculate percentage
#         perc_total_reservations = 100
#         total_reservations = total_reservations.count()
#         perc_total_accepted_reservations = total_accepted_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0
#         perc_total_refused_reservations = total_refused_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0
#         perc_total_postponed_reservations = total_postponed_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0
#         result = {
#             "total_reservations":total_reservations,
#             "total_accepted_reservations":total_accepted_reservations,
#             "total_refused_reservations":total_refused_reservations,
#             "total_postponed_reservations":total_postponed_reservations,
#             "perc_total_reservations":perc_total_reservations,
#             "perc_total_accepted_reservations":perc_total_accepted_reservations,
#             "perc_total_refused_reservations":perc_total_refused_reservations,
#             "perc_total_postponed_reservations":perc_total_postponed_reservations,
#         }
#         if wilaya_pk:
#             wilaya_reservations = all_reservations.filter(branch__wilaya = wilaya_pk)
#             wilaya_aceepted_reservations = wilaya_reservations.filter(status = 'accepted').count()
#             wilaya_refused_reservations = wilaya_reservations.filter(status = 'refused').count()  
#             wilaya_postponed_reservations = wilaya_reservations.filter(status = 'postponed').count()  
#             perc_all_wilaya_reservations = 100
#             wilaya_reservations = wilaya_reservations.count()
#             #calculate percentage
#             perc_wilaya_accepted_reservations = wilaya_aceepted_reservations * perc_all_wilaya_reservations / wilaya_reservations if wilaya_reservations > 0 else 0
#             perc_wilaya_refused_reservations = wilaya_refused_reservations * perc_all_wilaya_reservations / wilaya_reservations if wilaya_reservations > 0 else 0
#             perc_wilaya_postponed_reservations = wilaya_postponed_reservations * perc_all_wilaya_reservations / wilaya_reservations if wilaya_reservations > 0 else 0
#             #calculate the percentage of the given wilaya reservations from all the reservations.
#             perc_contrib_wilaya_reservations = wilaya_reservations * 100 / total_reservations if total_reservations > 0 else 0
#             #add data to the json 
#             result['wilaya_reservations'] = wilaya_reservations
#             result['wilaya_aceepted_reservations'] = wilaya_aceepted_reservations
#             result['wilaya_refused_reservations'] = wilaya_refused_reservations
#             result['wilaya_postponed_reservations'] = wilaya_postponed_reservations
#             result['perc_contrib_wilaya_reservations'] = perc_contrib_wilaya_reservations
#             result['perc_all_wilaya_reservations'] = perc_all_wilaya_reservations
#             result['perc_wilaya_accepted_reservations'] = perc_wilaya_accepted_reservations
#             result['perc_wilaya_refused_reservations'] = perc_wilaya_refused_reservations
#             result['perc_wilaya_postponed_reservations'] = perc_wilaya_postponed_reservations


#         return Response(result, status = status.HTTP_200_OK)
from datetime import date, timedelta
@api_view(['GET'])
def reservations_stats(request):
    if request.method == 'GET':
        reservations = total_reservations = Reservation.objects.all()
        wilaya = request.GET.get('wilaya') 
        if wilaya:
            reservations = reservations.filter(branch__wilaya = wilaya)
        # reservation_status = request.GET.get('status')
        # if reservation_status:
        #     reservations = reservations.filter(status = reservation_status)
        gender = request.GET.get('gender')
        if gender :
            reservations = reservations.filter(client__gender = gender)
        min_age = request.GET.get('min_age')
        if min_age:
            today = date.today()
            print(f"today = {today}")
            min_birth_date = today - timedelta(days=int(min_age)*365)
            print(f"min_birth_date = {min_birth_date}")
            reservations = reservations.filter(client__date_of_birth__gte=min_birth_date)
        max_age = request.GET.get('max_age')
        if max_age:
            today = date.today()
            print(f"today = {today}")   
            max_birth_date = today - timedelta(days=(int(max_age))*365)
            print(f"max_birth_date = {max_birth_date}")
            reservations = reservations.filter(client__date_of_birth__lte=max_birth_date)

        total_accepted_reservations = reservations.filter(status = 'accepted').count()
        total_refused_reservations = reservations.filter(status = 'refused').count()
        total_postponed_reservations = reservations.filter(status = 'postponed').count()
        #calculate percentage
        perc_total_reservations = 100
        total_reservations = total_reservations.count()
        perc_total_accepted_reservations = total_accepted_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0
        perc_total_refused_reservations = total_refused_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0
        perc_total_postponed_reservations = total_postponed_reservations * perc_total_reservations / total_reservations if total_reservations > 0 else 0

        
        result = {
            "total_reservations":total_reservations,
            "total_accepted_reservations":total_accepted_reservations,
            "total_refused_reservations":total_refused_reservations,
            "total_postponed_reservations":total_postponed_reservations,
            "perc_total_accepted_reservations":perc_total_accepted_reservations,
            "perc_total_refused_reservations":perc_total_refused_reservations,
            "perc_total_postponed_reservations":perc_total_postponed_reservations,
        }
        if wilaya:
            perc_contrib_wilaya_reservations = reservations.count() * 100 / total_reservations if total_reservations > 0 else 0
            result['perc_contrib_wilaya_reservations'] = perc_contrib_wilaya_reservations
        return Response(result, status = status.HTTP_200_OK)
@api_view(['GET'])
def all_subscriptions_income_stats(request):

    if request.method == 'GET':
        subscriptions = Subscription.objects.all()
        #calculate income from subscriptions
        subscriptions_revenue = subscriptions.aggregate(revenue = Sum('plan__price'))
        print(f"subscription revenue = {subscriptions_revenue}")
        result = {
            "subscriptions_revenue":subscriptions_revenue,
            
        }
        #calculate income from subscriptions per year
        per_year_subscription_revenue = subscriptions.annotate(
            year=TruncYear('created_at'),).values('year').annotate(
                subscriptions_count = Count('id')).annotate(
                    subscriptions_revenue_per_year = Sum('plan__price'))
        result['per_year_subscription_revenue'] = per_year_subscription_revenue
        return Response(result, status = status.HTTP_200_OK)
@api_view(['GET'])
def yearly_subscriptions_income_stats(request):

    if request.method == 'GET':
        subscriptions = Subscription.objects.all()
        given_year = request.GET.get('year')
        current_month = 0
        if not given_year:
            #set given year to the current year
            given_year = date.today().year
            current_month = datetime.now().date().month
              
        given_year_subscriptions_revenue = subscriptions.filter(
            #get  subscriptions created in the given year
            created_at__year__range = [int(given_year) - 1,given_year] ).annotate(
                #group subscriptions by month and create a new column month
                month=TruncMonth('created_at')).values('month').annotate(
                    #create two  new columns that contain subscriptions count and revenue each month 
                    subscriptions_count = Count('id'),
                    subscriptions_revenue_per_month = Sum('plan__price'),
                    ).order_by('month')
        #creating data to display
        data_to_display = {}
        for i in range( current_month + 11 ,current_month -1, -1):
            month = i % 12  +1
            data_to_display[month] = {
                "month":month,
                "subscriptions_count":0,
                "subscriptions_revenue_per_month":0
            }

        #update data to display from the data fetched from the database
        for subscription in given_year_subscriptions_revenue:
            data_to_display[subscription['month'].month].update(
                {
                    "subscriptions_count":subscription['subscriptions_count'],
                    "subscriptions_revenue_per_month":subscription['subscriptions_revenue_per_month'],
                }
            )
            print(f"subscription : {subscription['month'].month}")
        result = {
            "data_to_display":data_to_display
        }
        return Response(result,status = status.HTTP_200_OK)
    
