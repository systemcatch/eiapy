#usr/bin/env python3

import os
import requests
from xml.etree import ElementTree


# TODO how does the api handle errors
# keep it simple and flexible
# methods series, geoset, relation, category, series/categories, updates, search
# check 200 needed?
# NOTE allow just list to be returned?
# TODO session suport?

API_KEY = os.environ['EIA_KEY']

class EIAError(Exception):
    pass


class Series(object):
    """docstring for Series."""
    def __init__(self, series_id, xml=False):
        super(Series, self).__init__()
        self.series_id = series_id
        self.xml = xml

    def _url(self, path):
        url = 'http://api.eia.gov/series/?api_key={}&series_id={}'.format(API_KEY, self.series_id)
        return url + path


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = requests.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data

    # num and start cannot coexist
    # num & end are fine
    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    #naming error handling
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
            raise EIAError('No time limits given for data request, pass all_data=True to get every datapoint in the series.')

        url = self._url(limits)
        data = self._fetch(url)

        return data


    def _url_categories(self):
        url = 'http://api.eia.gov/series/categories/?series_id={}&api_key={}'.format(self.series_id, API_KEY)
        return url


    def categories(self):
        url = self._url_categories()
        data = self._fetch(url)
        return data


    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.series_id)


# IDEA should it inherit? maybe be part of series as list option
class MultiSeries(Series):
    """docstring for MultiSeries."""
    def __init__(self, multiseries):
        super(MultiSeries, self).__init__(';'.join(multiseries))
        self.multiseries = multiseries
        if not isinstance(self.multiseries, list): # expects but got for clarity
            raise EIAError('MultiSeries requires a list of series ids to be passed')

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.multiseries)

# list option
class Geoset(object):
    """docstring for Geoset."""
    def __init__(self, geoset_id, regions, xml=False):
        super(Geoset, self).__init__()
        self.geoset_id = geoset_id
        self.regions = regions
        self.xml = xml


    def _url(self, path):
        url = 'http://api.eia.gov/geoset/?geoset_id={}&regions={}&api_key={}'.format(self.geoset_id, self.regions, API_KEY)
        return url + path


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = requests.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data

    # num and start cannot coexist
    # num & end are fine
    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    #naming
    def data(self, start=None, end=None, all_data=False):
        if start and end:
            limits = '&start={}&end={}'.format(start, end)
        elif start:
            limits = '&start={}'.format(start)
        elif end:
            limits = '&end={}'.format(end)
        elif all_data:
            # This will return every datapoint in the geoset!
            limits = ''
        else:
            raise EIAError('No time limits given for data request, pass all_data=True to get every datapoint in the series.')

        url = self._url(limits)
        data = self._fetch(url)

        return data

# list option
# TODO finish
class Relation(object):
    """docstring for Relation."""
    def __init__(self, relation_id, regions, xml=False):
        super(Relation, self).__init__()
        self.relation_id = relation_id
        self.regions =  regions
        self.xml = xml
        #http://api.eia.gov/relation/?relation_id=rrrrrrr&region=region1&api_key=YOUR_API_KEY_HERE[&start=|&num=][&end=][&out=xml|json]

    def _url(self, path):
        url = 'http://api.eia.gov/relation/?relation_id={}&regions={}&api_key={}'.format(self.relation_id, self.regions, API_KEY)
        return url + path


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            print(url)
            req = requests.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data

    # num and start cannot coexist
    # num & end are fine
    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    #naming error handling
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
            raise EIAError('No time limits given for data request, pass all_data=True to get every datapoint in the series.')

        url = self._url(limits)
        data = self._fetch(url)

        return data


class Category(object):
    """docstring for Category."""
    def __init__(self, category_id=None, xml=False):
        super(Category, self).__init__()
        self.category_id = category_id
        self.xml = xml


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = requests.get(url)
            json_data = req.json()
            return json_data


    def get_info(self):
        if self.category_id is not None:
            url = 'http://api.eia.gov/category/?api_key={}&category_id={}'.format(API_KEY, self.category_id)
        else:
            url = 'http://api.eia.gov/category/?api_key={}'.format(API_KEY)

        data = self._fetch(url)
        return data


    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.category_id)


# should specify params in get? flexibility
class Updates(object):
    """docstring for Updates."""
    def __init__(self, category_id=None, deep=False, rows=None, firstrow=None, xml=False):
        super(Updates, self).__init__()
        self.category_id = category_id
        self.deep = deep
        self.rows = rows
        self.firstrow = firstrow
        self.xml = xml


    def _url(self, path):
        url = 'http://api.eia.gov/updates/?api_key={}'.format(API_KEY)
        return url + path


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = requests.get(url)
            json_data = req.json()
            return json_data

    # max rows is 10000, should there be a max_rows flag?
    # naming
    def get(self):
        params = []
        keys = self.__dict__

        # BUG this fails for category 0
        for k,v in keys.items():
            if v:
                param = '&{}={}'.format(k,v)
                params.append(param)

        options=''.join(params)
        url = self._url(options)
        data= self._fetch(url)

        return data


    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__)


class Search(object):
    """docstring for Search."""
    def __init__(self, search_term, search_value, xml=False):
        super(Search, self).__init__()
        self.search_term = search_term
        self.search_value = search_value
        self.xml = xml


    def _url(self, path):
        url = 'http://api.eia.gov/search/?search_term={}&search_value={}'.format(self.search_term, self.search_value)
        return url + path


    def _fetch(self, url):
        if self.xml:
            req = requests.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = requests.get(url)
            json_data = req.json()
            return json_data

    # naming
    def find(self, page_num=None, rows_per_page=None):
        path = ''
        if page_num:
            path += '&page_num={}'.format(page_num)
        if rows_per_page:
            path += '&rows_per_page={}'.format(rows_per_page)
        url = self._url(path)
        print(url)
        data = self._fetch(url)
        return data


    # TODO make sure this is properly done
    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.search_term, self.search_value)
