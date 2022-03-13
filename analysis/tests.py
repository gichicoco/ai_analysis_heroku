from django.test import TestCase
from django.urls import resolve
from django.test import TestCase
from .views import analysis_new, analysis_detail


class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "AI分析", status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "analysis/top.html")


class CreateAnalysisTest(TestCase):
    def test_should_resolve_analysis_new(self):
        found = resolve("/analysis/new/")
        self.assertEqual(analysis_new, found.func)


class AnalysisDetailTest(TestCase):
    def test_should_resolve_analysis_detail(self):
        found = resolve("/analysis/1/")
        self.assertEqual(analysis_detail, found.func)
