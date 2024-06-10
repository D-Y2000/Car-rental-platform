import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.serializers import NewSubscriptionSerializer, ListNewSubscriptionSerializer
from api_agency.permissions import IsAgency
from api_agency.models import Agency, NewSubscription
# Create your views here.

# this subscription remains pending until the checkout is done and the webhook from the e-payment provider is received
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAgency])
def create_subscription(request):
    # Retrieve the authenticated user's agency
    user = request.user
    agency = Agency.objects.get(user=user)
    request.data['agency'] = agency.id

    serializer = NewSubscriptionSerializer(data=request.data)    
    
    if serializer.is_valid():
        print("serializer is valid \n > Create pending subscription")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Your Chargily Pay Secret key, will be used to calculate the Signature
api_secret_key = settings.CHARGILY_SECRET_KEY

@csrf_exempt
@require_POST
def webhook(request):
    # Extracting the 'signature' header from the HTTP request
    signature = request.headers.get('signature')
    print("webhook> signature: ", signature)

    # Getting the raw payload from the request body
    payload = request.body.decode('utf-8')
    print("webhook> payload: ", payload)

    # If there is no signature, ignore the request
    if not signature:
        print("webhook> no signature")
        return HttpResponse(status=400)

    # Calculate the signature
    computed_signature = hmac.new(api_secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()

    # If the calculated signature doesn't match the received signature, ignore the request
    if not hmac.compare_digest(signature, computed_signature):
        print("webhook> signature mismatch")
        return HttpResponse(status=403)

    # If the signatures match, proceed to decode the JSON payload
    event = json.loads(payload)

    # Switch based on the event type
    if event['type'] == 'checkout.paid':
        print("webhook> checkout.paid")

        checkout = event['data']
        # Handle the successful payment.
        # Find the subscription associated with the checkout
        subscription = NewSubscription.objects.get(checkout_id=checkout['id'])
        # Update the status of the subscription to 'success'
        subscription.status = 'paid'
        subscription.save()

        print("webhook> subscription updated", subscription)

    elif event['type'] == 'checkout.failed':
        print("webhook> checkout.failed")
        checkout = event['data']
        # Handle the failed payment.
        # Find the subscription associated with the checkout
        subscription = NewSubscription.objects.get(checkout_id=checkout['id'])
        # Update the status of the subscription to 'success'
        subscription.status = 'failed'
        subscription.save()

    # Respond with a 200 OK status code to let us know that you've received the webhook
    return JsonResponse({}, status=200)


@api_view(['GET'])
def list_subscriptions(request):
    subscriptions = NewSubscription.objects.all()
    serializer = ListNewSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)