import datetime

from django.contrib.admin import AdminSite
from django.test import TestCase
from django.urls import reverse

from employees.admin import EmployeeAdmin
from employees.models import Employee


class EmployeeTestCase(TestCase):
    def setUp(self) -> None:
        self.employee = Employee.objects.create(
            firstname='John',
            surname='Smith',
            birthdate=datetime.datetime.now()
        )

    def test_admin_get_view_on_site_url(self):
        employee_admin = EmployeeAdmin(model=Employee, admin_site=AdminSite)
        url = employee_admin.get_view_on_site_url(self.employee)
        self.assertEqual(url, reverse('employee-detail', kwargs={'pk': self.employee.id}))

    def test_employee_model_fullname(self):
        self.assertEqual(
            self.employee.full_name(),
            'John Smith'
        )

    def test_employee_model_str(self):
        self.assertEqual(
            self.employee.__str__(),
            f'{self.employee.id}: {self.employee.firstname} {self.employee.surname}'
        )
