#usr/bin/env python3

import json # needed?
import os
import requests
from xml.etree import ElementTree


# TODO
# keep it simple and flexible
# methods series, geoset, relation, category, series/categories, updates, search
# check 200 needed?
# TODO consitent use of '' ""
# NOTE allow just list to be returned?
# TODO getitem and len
# TODO info
# TODO session suport?

API_KEY = os.environ['EIA_KEY']

class APIError(Exception): #TODO better name and description
    pass


class Series(object):
    """docstring for Series."""
    def __init__(self, series_id):
        super(Series, self).__init__()
        self.series_id = series_id #test for list? xml option id


    def _url(self, path):
        url = 'http://api.eia.gov/series/?api_key={}&series_id={}'.format(API_KEY, self.series_id)
        return url + path


    def _fetch(self, url):
        req = requests.get(url)
        json_data = req.json()
        return json_data


    # def _fetch_xml(self, url):
    #     req = requests.get(url+'out=xml')
    #     #xml_data = ElementTree.fromstring(req.content)
    #     xml_data = req.content
    #     return xml_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url("&num={}".format(n))
        data = self._fetch(url)
        return data

    # num and start cannot coexist
    # num & end are fine
    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #naming
    def data(self, start=None, end=None, all_data=False):
        if start and end:
            limits = '&start={}&end={}'.format(start, end)
        elif start:
            limits = '&start={}'.format(start)
        elif end:
            limits = '&end={}'.format(end)
        elif all_data:
            # This will return every datapoint in the series!
            limits = ''
        else:
            raise APIError('No time limits given, pass all_data=True to get every datapoint in the series.')

        url = self._url(limits)
        # if xml:
        #     data = self._fetch_xml(url)
        # else:
        data = self._fetch(url)

        return data


    def categories(self):
        # risky hardcode sep method _url_categories
        url = 'http://api.eia.gov/series/categories/?series_id={}&api_key={}'.format(self.series_id, API_KEY)
        data = self._fetch(url)
        return data


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.series_id)


# IDEA should it inherit? maybe be part of series as list option
class MultiSeries(Series):
    """docstring for MultiSeries."""
    def __init__(self, multiseries):
        super(MultiSeries, self).__init__(';'.join(multiseries))
        self.multiseries = multiseries

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.multiseries)

# TODO finish
class Geoset(object):
    """docstring for Geoset."""
    def __init__(self, arg):
        super(Geoset, self).__init__()
        self.arg = arg
        #http://api.eia.gov/geoset/?geoset_id=sssssss&regions=region1,region2,region3,...&api_key=YOUR_API_KEY_HERE[&start=|&num=][&end=][&out=xml|json]

# TODO finish
class Relation(object):
    """docstring for Relation."""
    def __init__(self, geoset_id, regions):
        super(Relation, self).__init__()
        self.geoset_id = geoset_id
        self.regions = regions
        #http://api.eia.gov/relation/?relation_id=rrrrrrr&region=region1&api_key=YOUR_API_KEY_HERE[&start=|&num=][&end=][&out=xml|json]


class Category(object):
    """docstring for Category."""
    def __init__(self, category_id):
        super(Category, self).__init__()
        self.category_id = category_id


    def get_info(self):
        if self.category_id:
            url = 'http://api.eia.gov/category/?api_key={}&category_id={}'.format(API_KEY, self.category_id)
        else:
            url = 'http://api.eia.gov/category/?api_key={}'.format(API_KEY)

        req = requests.get(url)
        json_data = req.json()
        return json_data


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pass #is this ok or needed

    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.category_id)


# IDEA could just be a method in series
class Categories(object):
    """docstring for Categories."""
    def __init__(self, series_id):
        super(Categories, self).__init__()
        self.series_id = series_id
        #http://api.eia.gov/series/categories/?series_id=&api_key=YOUR_API_KEY_HERE


    def _url_categories(self, path):
        url = 'http://api.eia.gov/series/categories/?series_id={}&api_key={}'.format(self.series_id, API_KEY)
        return url + path


    def _fetch(self, url):
        req = requests.get(url)
        json_data = req.json()
        return json_data


class Updates(object):
    """docstring for Updates."""
    def __init__(self, category_id=None, deep=False, rows=None, firstrow=None):
        super(Updates, self).__init__()
        self.category_id = category_id
        self.deep = deep
        self.rows = rows
        self.firstrow = firstrow


    def _url(self, path):
        url = 'http://api.eia.gov/updates/?api_key={}'.format(API_KEY)#[&category_id=X][&deep=true|false][&firstrow=nnnnn][&rows=nn][&out=xml
        return url + path


    def _fetch(self, url):
        req = requests.get(url)
        json_data = req.json()
        return json_data

    # naming
    def get(self):
        params = []
        keys = self.__dict__

        for k,v in keys.items():
            if v:
                param = '&{}={}'.format(k,v)
                params.append(param)

        options=''.join(params)
        url = self._url(options)
        data= self._fetch(url)

        return data


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__)


class Search(object):
    """docstring for Search."""
    def __init__(self, search_term, search_value):
        super(Search, self).__init__()
        self.search_term = search_term
        self.search_value = search_value


    def _url(self):#, path):
        url = 'http://api.eia.gov/search/?search_term={}&search_value={}'.format(self.search_term, self.search_value)
        return url# + path


    def _fetch(self, url):
        req = requests.get(url)
        json_data = req.json()
        return json_data

    # naming
    # TODO implement page_num and rows_per_page
    def find(self, page_num=None, rows_per_page=None):
        url = self._url()
        data = self._fetch(url)
        return data


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pass #should anything be cleaned up here?


    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.search_term, self.search_value)
