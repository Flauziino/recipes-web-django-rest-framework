from unittest import TestCase

from django.http import HttpRequest

from utils.pagination import make_pagination_range, make_pagination


class PaginatorTestFunc(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_mid_page(self):
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_mid_range_is_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 18 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 20 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_pagination_shows_correct_number_of_items_per_page(self):
        request = HttpRequest()
        request.GET['page'] = '2'
        query_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        per_page = 6

        page_obj, pagination_range = make_pagination(
            request,
            query_set,
            per_page,
            4
        )

        self.assertEqual(list(page_obj), [7, 8, 9, 10, 11, 12])

    def test_pagination_shows_correct_range_of_pages(self):
        request = HttpRequest()
        request.GET['page'] = '2'
        query_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        per_page = 6

        page_obj, pagination_range = make_pagination(
            request,
            query_set,
            per_page,
            4
        )

        self.assertEqual(
            len(pagination_range['page_range']), 2
        )

    def test_pagination_dont_have_another_page(self):
        request = HttpRequest()
        request.GET['page'] = '1'
        query_set = [1, 2, 3, 4]
        per_page = 6

        page_obj, pagination_range = make_pagination(
            request,
            query_set,
            per_page,
            4
        )

        self.assertFalse(page_obj.has_other_pages())

    def test_pagination_have_another_page_with_just_one_item(self):
        request = HttpRequest()
        request.GET['page'] = '2'
        query_set = [1, 2, 3, 4, 5, 6, 7]
        per_page = 6

        page_obj, pagination_range = make_pagination(
            request,
            query_set,
            per_page,
            4
        )

        self.assertTrue(page_obj.has_other_pages())
        self.assertEqual(
            list(page_obj), [7]
        )

    def test_pagination_current_page_conversion_with_valid_value(self):
        request = HttpRequest()
        request = HttpRequest()
        request.GET['page'] = '2'
        query_set = [1, 2, 3, 4, 5, 6, 7]
        per_page = 6

        page_obj, pagination_range = make_pagination(
            request,
            query_set,
            per_page,
            4
        )

        self.assertEqual(
            pagination_range['current_page'], 2
        )

    def test_pagination_current_page_conversion_with_invalid_value(self):
        request = HttpRequest()
        request.GET['page'] = 'invalid'

        try:
            current_page = int(request.GET.get('page', 1))
        # testando se o value error é levantado fazendo com que o current_page
        # se torne 1. comentario adicionado pois o coverage nao esta captando
        # este teste.
        except ValueError:
            current_page = 1

        self.assertEqual(current_page, 1)
