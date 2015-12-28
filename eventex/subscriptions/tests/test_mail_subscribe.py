from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Rafael Dias', cpf='12345678910',
                    email='rafaeldiasmello@gmail.com', phone='21-9888888')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'rafaeldiasmello@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Rafael Dias',
            '12345678910',
            'rafaeldiasmello@gmail.com',
            '21-9888888'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)