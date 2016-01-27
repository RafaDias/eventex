from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
                name="Rafael Dias",
                slug='rafael-dias',
                photo='http://hbn.link/hb-pic'
        )

    def test_create(self):

        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                                         value='rafaeldiasmello@gmail.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                                         value='21986669847')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """ Contact kind should be limited to E or P """
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='rafaeldiasmello@gmail.com')
        self.assertEqual('rafaeldiasmello@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Rafael Dias',
            slug='rafael-dias',
            photo='http://hbn.link/rd-pic'
        )
        s.contact_set.create(kind=Contact.EMAIL, value='rafaeldiasmello@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='21986669847')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['rafaeldiasmello@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['21986669847']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)