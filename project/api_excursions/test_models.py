from django.test import TestCase
from django.contrib.auth import get_user_model
from api_agency.models import Wilaya
from .models import ExcursionOrganizer, Location, Excursion, ExcursionLocation

# Get the custom user model
User = get_user_model()

class ModelTests(TestCase):
    
    def setUp(self):
        """
        Set up the initial data for the tests. This method is called before every test.
        """
        # Create a user for testing
        self.user = User.objects.create_user(email='testuser', password='12345')
        # Create a Wilaya for testing
        self.wilaya = Wilaya.objects.create(name='Test Wilaya', code=34)

    def test_create_excursion_organizer(self):
        """
        Test the creation of an ExcursionOrganizer instance.
        """
        # Create an ExcursionOrganizer instance
        organizer = ExcursionOrganizer.objects.create(owner=self.user, name='Test Organizer')
        
        # Check that the organizer's owner is the user created in setUp
        self.assertEqual(organizer.owner, self.user)
        # Check that the organizer's name is correct
        self.assertEqual(organizer.name, 'Test Organizer')
        # Check that the logo_url is None by default
        self.assertIsNone(organizer.logo_url)

    def test_create_location(self):
        """
        Test the creation of a Location instance.
        """
        # Create a Location instance
        location = Location.objects.create(
            wilaya=self.wilaya,
            latitude=36.752887,
            longitude=3.042048,
            address='Test Address'
        )
        
        # Check that the location's wilaya is correct
        self.assertEqual(location.wilaya, self.wilaya)
        # Check that the latitude is correct
        self.assertEqual(location.latitude, 36.752887)
        # Check that the longitude is correct
        self.assertEqual(location.longitude, 3.042048)
        # Check that the address is correct
        self.assertEqual(location.address, 'Test Address')

    def test_create_excursion(self):
        """
        Test the creation of an Excursion instance.
        """
        # Create an ExcursionOrganizer instance
        organizer = ExcursionOrganizer.objects.create(owner=self.user, name='Test Organizer')
        # Create an Excursion instance
        excursion = Excursion.objects.create(
            organizer=organizer,
            title='Test Excursion',
            description='This is a test excursion.',
            price=100.00
        )
        
        # Check that the excursion's organizer is correct
        self.assertEqual(excursion.organizer, organizer)
        # Check that the title is correct
        self.assertEqual(excursion.title, 'Test Excursion')
        # Check that the description is correct
        self.assertEqual(excursion.description, 'This is a test excursion.')
        # Check that the price is correct
        self.assertEqual(excursion.price, 100.00)

    def test_create_excursion_location(self):
        """
        Test the creation of an ExcursionLocation instance.
        """
        # Create an ExcursionOrganizer instance
        organizer = ExcursionOrganizer.objects.create(owner=self.user, name='Test Organizer')
        # Create an Excursion instance
        excursion = Excursion.objects.create(
            organizer=organizer,
            title='Test Excursion',
            description='This is a test excursion.',
            price=100.00
        )
        # Create a Location instance
        location = Location.objects.create(
            wilaya=self.wilaya,
            latitude=36.752887,
            longitude=3.042048,
            address='Test Address'
        )
        # Create an ExcursionLocation instance
        excursion_location = ExcursionLocation.objects.create(
            excursion=excursion,
            location=location,
            point_type=ExcursionLocation.MEETING_POINT,
            order=1,
            time='2024-07-27 10:00:00'
        )
        
        # Check that the ExcursionLocation's excursion is correct
        self.assertEqual(excursion_location.excursion, excursion)
        # Check that the location is correct
        self.assertEqual(excursion_location.location, location)
        # Check that the point type is correct
        self.assertEqual(excursion_location.point_type, ExcursionLocation.MEETING_POINT)
        # Check that the order is correct
        self.assertEqual(excursion_location.order, 1)
        # Check that the time is correct
        self.assertEqual(excursion_location.time, '2024-07-27 10:00:00')

if __name__ == '__main__':
    unittest.main()
