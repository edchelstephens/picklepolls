# class CeleryPingViewTest(DjangoViewTestCase, CeleryTaskTestMixin):
#     """CeleryPingView test."""

#     def setUp(self) -> None:
#         """Run this setUp before each test."""
#         super().setUp()
#         self.url = "/celery/ping/"
#         self.view = views.CeleryPingView.as_view()
#         self.request_factory = self.get_request_factory()
#         self.update_celery_always_eager()

#     def test_get_request_returns_OK(self) -> None:
#         """Get request to url returns OK, which means, settings are configured properly."""

#         expected = {"message": "Celery is working", "status": "OK", "title": "Success"}

#         request = self.request_factory.get(self.url)
#         response = self.view(request)
#         response_data = self.get_dict_response_data(response)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_data, expected)
