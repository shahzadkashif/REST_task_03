from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from .models import Flight, Booking


class FlightListTest(APITestCase):
	def setUp(self):
		self.flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		self.flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}
		Flight.objects.create(**self.flight1)
		Flight.objects.create(**self.flight2)

	def test_url_works(self):
		response = self.client.get(reverse('flights-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_list(self):
		response = self.client.get(reverse('flights-list'))
		flights = Flight.objects.all()
		self.assertEqual(len(response.data), flights.count())
		flight = flights[0]
		self.assertEqual(dict(response.data[0]), {"id" : flight.id, "destination" : flight.destination, "time": str(flight.time), "price": str(flight.price)})
		flight = flights[1]
		self.assertEqual(dict(response.data[1]), {"id" : flight.id, "destination" : flight.destination, "time": str(flight.time), "price": str(flight.price)})


class BookingListTest(APITestCase):
	def setUp(self):
		self.flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		self.flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}
		flight1 = Flight.objects.create(**self.flight1)
		flight2 = Flight.objects.create(**self.flight2)
		user = User.objects.create(username="laila", password="1234567890-=")

		Booking.objects.create(flight=flight1, date="2018-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2019-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight1, date="2021-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2021-01-01", user=user, passengers=2)


	def test_url_works(self):
		response = self.client.get(reverse('bookings-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_response(self):
		response = self.client.get(reverse('bookings-list'))
		bookings = Booking.objects.filter(date__gt=date.today())

		self.assertEqual(len(response.data), bookings.count())
		booking = bookings[0]
		self.assertEqual(dict(response.data[0]), {"id" : booking.id, "flight" : booking.flight.id, "date": str(booking.date)})
		booking = bookings[1]
		self.assertEqual(dict(response.data[1]), {"id" : booking.id, "flight" : booking.flight.id, "date": str(booking.date)})


class BookingDetails(APITestCase):
	def setUp(self):
		flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}

		flight1 = Flight.objects.create(**flight1)
		flight2 = Flight.objects.create(**flight2)
		user = User.objects.create(username="laila", password="1234567890-=")

		Booking.objects.create(flight=flight1, date="2018-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2019-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight1, date="2020-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2021-01-01", user=user, passengers=2)

	def test_url_works(self):
		response = self.client.get(reverse('booking-details', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_response(self):
		response = self.client.get(reverse('booking-details', args=[1]))
		booking = Booking.objects.get(id=1)
		self.assertEqual(dict(response.data), {"id" : booking.id, "flight" : booking.flight.id, "date": str(booking.date), "passengers":booking.passengers})

		response = self.client.get(reverse('booking-details', args=[2]))
		booking = Booking.objects.get(id=2)
		self.assertEqual(dict(response.data), {"id" : booking.id, "flight" : booking.flight.id, "date": str(booking.date), "passengers":booking.passengers})



class BookingUpdate(APITestCase):
	def setUp(self):
		flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}

		flight1 = Flight.objects.create(**flight1)
		flight2 = Flight.objects.create(**flight2)
		user = User.objects.create(username="laila", password="1234567890-=")

		Booking.objects.create(flight=flight1, date="2018-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2019-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight1, date="2020-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2021-01-01", user=user, passengers=2)

	def test_url_works(self):
		data = {"date": "2019-05-05", "passengers": 4}
		response = self.client.put(reverse('update-booking', args=[1]), data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_update(self):
		data = {"date": "2019-05-05", "passengers": 4}

		old_booking = Booking.objects.get(id=1)
		response = self.client.put(reverse('update-booking', args=[1]), data)
		new_booking = Booking.objects.get(id=1)
		self.assertEqual({"id":old_booking.id, "date":data["date"], "passengers":data["passengers"], "flight":old_booking.flight, "user":old_booking.user}, {"id":new_booking.id, "date":str(new_booking.date), "passengers":new_booking.passengers, "flight":new_booking.flight, "user":new_booking.user})


		old_booking = Booking.objects.get(id=2)
		response = self.client.put(reverse('update-booking', args=[2]), data)
		new_booking = Booking.objects.get(id=2)
		self.assertEqual({"id":old_booking.id, "date":data["date"], "passengers":data["passengers"], "flight":old_booking.flight, "user":old_booking.user}, {"id":new_booking.id, "date":str(new_booking.date), "passengers":new_booking.passengers, "flight":new_booking.flight, "user":new_booking.user})
		

class BookingDelete(APITestCase):
	def setUp(self):
		flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}

		flight1 = Flight.objects.create(**flight1)
		flight2 = Flight.objects.create(**flight2)
		user = User.objects.create(username="laila", password="1234567890-=")

		Booking.objects.create(flight=flight1, date="2018-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2019-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight1, date="2020-01-01", user=user, passengers=2)
		Booking.objects.create(flight=flight2, date="2021-01-01", user=user, passengers=2)

	def test_url_works(self):
		response = self.client.delete(reverse('cancel-booking', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


	def test_update(self):
		response = self.client.delete(reverse('cancel-booking', args=[1]))
		self.assertEqual(Booking.objects.all().count(), 3)
		self.assertEqual(Booking.objects.filter(id=1).count(), 0)


class Login(APITestCase):
	def setUp(self):
		flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}

		flight1 = Flight.objects.create(**flight1)
		flight2 = Flight.objects.create(**flight2)

		self.data = {"username":"laila", "password":"1234567890-="}
		user = User(username=self.data["username"])
		user.set_password(self.data["password"])
		user.save()

	def test_succeful_login(self):
		response = self.client.post(reverse('login'), self.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_unsucceful_login(self):
		response = self.client.post(reverse('login'), {"username" : "laila", "password": "1234567890-=1"})
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingCreate(APITestCase):
	def setUp(self):
		self.user_data = {"username":"laila", "password":"1234567890-="}
		self.data = {"date": "2019-05-05", "passengers": 4}
		user = User(username=self.user_data["username"])
		user.set_password(self.user_data["password"])
		user.save()

		user = User(username=self.user_data["username"]+"1")
		user.set_password(self.user_data["password"])
		user.save()

		flight1 = {'destination': 'Wakanda', 'time': '10:00', 'price': 230, 'miles': 4000}
		flight2 = {'destination': 'La la land', 'time': '00:00', 'price': 1010, 'miles': 1010}
		self.flight1 = Flight.objects.create(**flight1)
		self.flight2 = Flight.objects.create(**flight2)

		

	def test_url_works(self):
		response = self.client.post(reverse('login'), self.user_data)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

		response = self.client.post(reverse('book-flight', args=[1]), self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		

	def test_creation_works(self):
		response = self.client.post(reverse('login'), self.user_data)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

		user = User.objects.get(id=1)

		response = self.client.post(reverse('book-flight', args=[1]), self.data)
		bookings = Booking.objects.all()
		self.assertEqual(bookings.count(), 1)
		self.assertEqual(bookings[0].user, user)
		self.assertEqual(bookings[0].flight, self.flight1)
		self.assertEqual(bookings[0].passengers, self.data["passengers"])
		self.assertEqual(str(bookings[0].date), self.data["date"])

		user = User.objects.get(id=1)

		response = self.client.post(reverse('book-flight', args=[2]), self.data)
		bookings = Booking.objects.all()
		self.assertEqual(bookings.count(), 2)
		self.assertEqual(bookings[1].user, user)
		self.assertEqual(bookings[1].flight, self.flight2)
		self.assertEqual(bookings[1].passengers, self.data["passengers"])
		self.assertEqual(str(bookings[1].date), self.data["date"])





