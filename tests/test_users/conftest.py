import pytest
from django.urls import reverse


class BaseTestUser:

    view_name = None

    def get_url(self, *args, **kwargs):
        return reverse(viewname=self.view_name, args=args, kwargs=kwargs)

    @pytest.fixture
    def client_get(self, client):
        def inner(**kwargs):
            return client.get(self.get_url(kwargs.pop('pk')), **kwargs)

        return inner

    @pytest.fixture
    def client_post(self, client):
        def inner(**kwargs):
            return client.post(self.get_url(kwargs.pop('pk')), **kwargs)

        return inner
