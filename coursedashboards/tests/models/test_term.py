from unittest import TestCase

from coursedashboards.models import Term


class TestTerm(TestCase):

    def setUp(self):
        # create terms
        self.winter2016 = Term()
        self.winter2016.quarter = 'winter'
        self.winter2016.year = 2016
        self.spring2016 = Term()
        self.spring2016.quarter = 'spring'
        self.spring2016.year = 2016
        self.summer2016 = Term()
        self.summer2016.quarter = 'summer'
        self.summer2016.year = 2016
        self.autumn2016 = Term()
        self.autumn2016.quarter = 'autumn'
        self.autumn2016.year = 2016
        self.winter2017 = Term()
        self.winter2017.quarter = 'winter'
        self.winter2017.year = 2017
        self.spring2017 = Term()
        self.spring2017.quarter = 'spring'
        self.spring2017.year = 2017
        self.summer2017 = Term()
        self.summer2017.quarter = 'summer'
        self.summer2017.year = 2017
        self.autumn2017 = Term()
        self.autumn2017.quarter = 'autumn'
        self.autumn2017.year = 2017

        self.terms = [self.winter2017, self.autumn2016, self.summer2016,
                      self.autumn2017, self.spring2016, self.summer2017,
                      self.spring2017, self.winter2016]

    def test_term_sort(self):
        sorted_terms = sorted(self.terms, cmp=Term.compare_terms)

        self.assertEqual(sorted_terms, [self.winter2016, self.spring2016,
                                        self.summer2016, self.autumn2016,
                                        self.winter2017, self.spring2017,
                                        self.summer2017, self.autumn2017])

    def test_term_key(self):
        self.assertEquals(self.spring2016.term_key, 20162)
        self.assertEquals(self.autumn2017.term_key, 20173)
