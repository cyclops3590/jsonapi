from django.test import TestCase, Client
from jsonapi.api import API
from jsonapi.resource import Resource

from ..resources import api


class TestApi(TestCase):
    def setUp(self):
        #self.api = api
        self.api = API()

    def test_resource_registration(self):
        class TestResource(Resource):
            class Meta:
                name = 'test'

        self.api.register(TestResource)
        self.assertEqual(self.api.resource_map['test'], TestResource)

    def test_resource_registration_decorator(self):
        @self.api.register
        class TestResource(Resource):
            class Meta:
                name = 'test'

        self.assertEqual(self.api.resource_map['test'], TestResource)

    def test_resource_registration_decorator_params(self):
        @self.api.register()
        class TestResource(Resource):
            class Meta:
                name = 'test'

        self.assertEqual(self.api.resource_map['test'], TestResource)

    def test_recource_api_reference(self):
        class TestResource(Resource):
            class Meta:
                name = 'test'

        self.assertFalse(hasattr(TestResource.Meta, 'api'))
        self.api.register(TestResource)
        self.assertTrue(TestResource.Meta.api is self.api)

    def test_resource_name_collapse_same_name(self):
        class NewsResource(Resource):
            class Meta:
                name = 'news'

        class NewsOtherResource(Resource):
            class Meta:
                name = 'news'

        self.api.register(NewsResource)
        with self.assertRaises(ValueError):
            # The same resource name
            self.api.register(NewsOtherResource)

    def test_resource_name_collapse_with_plural(self):
        class NewsResource(Resource):
            class Meta:
                name = 'news'

        class NewResource(Resource):
            class Meta:
                name = 'new'

        self.api.register(NewsResource)
        with self.assertRaises(ValueError):
            # NewResource.name_plural = NewsResource.name
            self.api.register(NewResource)

    def test_resource_name_collapse_with_singular(self):
        class NewsResource(Resource):
            class Meta:
                name = 'news'

        class NewssResource(Resource):
            class Meta:
                name = 'newss'

        self.api.register(NewsResource)
        with self.assertRaises(ValueError):
            # NewsResource.name_plural = NewssResource.name
            self.api.register(NewssResource)

    def test_base_url(self):
        self.assertTrue(self.api.base_url is None)
        c = Client()
        c.get(
            '/api/author',
            content_type='application/vnd.api+json'
        )
        self.assertEqual(self.api.base_url, "http://testserver")

    def test_api_url(self):
        self.assertTrue(self.api.api_url is None)
        c = Client()
        c.get(
            '/api/author',
            content_type='application/vnd.api+json'
        )
        self.assertEqual(self.api.api_url, "http://testserver/api")
