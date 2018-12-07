#usr/bin/env python3

__version__ = "0.1.3"

import os
import requests
from xml.etree import ElementTree


# TODO how does the api handle errors
# check 200 needed?
# NOTE allow just list to be returned?
# IDEA kwargs for future proofing

API_KEY = os.environ['EIA_KEY']

class EIAError(Exception):
    pass


class Series(object):
    """
    Create an object representing a single EIA data series.

    :param series_id: string
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, series_id, xml=False, session=None):
        super(Series, self).__init__()
        self.series_id = series_id
        self.xml = xml
        self.session = session


    def _url(self, path):
        url = 'http://api.eia.gov/series/?api_key={}&series_id={}'.format(API_KEY, self.series_id)
        return url + path


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = s.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data


    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    #error handling
    def get_data(self, start=None, end=None, all_data=False):
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
        """Find the categories the series is a member of."""
        url = self._url_categories()
        data = self._fetch(url)
        return data


    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.series_id)


class MultiSeries(Series):
    """
    Create an object representing multiple EIA data series.

    :param multiseries: list of strings, each refering to a series.
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, multiseries, **kwargs):
        super(MultiSeries, self).__init__(';'.join(multiseries), **kwargs)
        self.multiseries = multiseries
        if not isinstance(self.multiseries, list):
            raise EIAError('MultiSeries requires a list of series ids to be passed')
        if len(self.multiseries) > 100:
            raise EIAError('The maximum number of series that can be requested is 100.')

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.multiseries)


class Geoset(object):
    """
    Gets a set of the series belonging to the geoset_id and matching the list of regions.

    :param geoset_id: integer >= 0.
    :param regions: list of strings, each representing a region code.
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, geoset_id, regions, xml=False, session=None):
        super(Geoset, self).__init__()
        if not isinstance(regions, list):
            raise EIAError('Geoset requires a list of regions to be passed')
        self.geoset_id = geoset_id
        self.regions = ';'.join(regions)
        self.xml = xml
        self.session = session


    def _url(self, path):
        url = 'http://api.eia.gov/geoset/?geoset_id={}&regions={}&api_key={}'.format(self.geoset_id, self.regions, API_KEY)
        return url + path


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = s.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data


    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    def get_data(self, start=None, end=None, all_data=False):
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


    def __repr__(self):
        return '{}({!r}, {})'.format(self.__class__.__name__, self.geoset_id, self.regions)


# list option
# TODO finish
# NOTE currently broken
class Relation(object):
    """docstring for Relation."""
    def __init__(self, relation_id, regions, xml=False, session=None):
        super(Relation, self).__init__()
        self.relation_id = relation_id
        self.regions =  regions
        self.xml = xml
        self.session = session
        #http://api.eia.gov/relation/?relation_id=rrrrrrr&region=region1&api_key=YOUR_API_KEY_HERE[&start=|&num=][&end=][&out=xml|json]

#https://www.eia.gov/opendata/embed.cfm?type=relation&relation_id=SEDS.FFTCB.A&regions=USA&geoset_id=SEDS.FFTCB.A
    def _url(self, path):
        url = 'http://api.eia.gov/relation/?relation_id={}&regions={}&api_key={}'.format(self.relation_id, self.regions, API_KEY)
        return url + path


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            print(url)
            req = s.get(url)
            json_data = req.json()
            return json_data


    def last(self, n):
        """Returns the last n datapoints."""
        url = self._url('&num={}'.format(n))
        data = self._fetch(url)
        return data


    def last_from(self, n, end):
        """Returns the last n datapoints before a given date."""
        url = self._url("&num={}&end={}".format(n, end))
        data = self._fetch(url)
        return data

    #raise on no data?
    #error handling
    def get_data(self, start=None, end=None, all_data=False):
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
    """
    Gets name and category id for a single category, also lists child categories.

    :param category_id: integer >= 0.
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, category_id=None, xml=False, session=None):
        super(Category, self).__init__()
        self.category_id = category_id
        self.xml = xml
        self.session = session


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = s.get(url)
            json_data = req.json()
            return json_data


    def get_info(self):
        if self.category_id is not None:
            url = 'http://api.eia.gov/category/?api_key={}&category_id={}'.format(API_KEY, self.category_id)
        else:
            url = 'http://api.eia.gov/category/?api_key={}'.format(API_KEY)

        data = self._fetch(url)
        return data


    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.category_id)


class Updates(object):
    """
    Finds out which series in a Category are recently updated.

    :param category_id: integer >= 0.
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, category_id=None, xml=False, session=None):
        super(Updates, self).__init__()
        self.category_id = category_id
        self.xml = xml
        self.session = session


    def _url(self, path):
        url = 'http://api.eia.gov/updates/?api_key={}'.format(API_KEY)
        return url + path


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = s.get(url)
            json_data = req.json()
            return json_data


    def get_updates(self, deep=False, rows=None, firstrow=None):
        params = []

        if self.category_id is not None:
            params.append('&category_id={}'.format(self.category_id))
        if deep:
            params.append('&deep=true')
        if rows:
            if rows > 10000:
                raise EIAError('The maximum number of rows allowed is 10000.')
            else:
                params.append('&rows={}'.format(rows))
        if firstrow:
            params.append('&firstrow={}'.format(firstrow))

        options=''.join(params)
        url = self._url(options)
        data= self._fetch(url)

        return data


    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.category_id)


class Search(object):
    """
    Allows searching by series_id, keyword or a date range.

    :param search_value: string that should be a series_id, ISO8601 time range or query term.
    :param xml: boolean specifying whether to output xml or json, defaults to json.
    :param session: object allowing an existing session to be passed, defaults to None.
    """
    def __init__(self, search_value, xml=False, session=None):
        super(Search, self).__init__()
        self.search_value = search_value
        self.xml = xml
        self.session = session


    def _url(self, path):
        url = 'http://api.eia.gov/search/?search_value={}'.format(self.search_value)
        return url + path


    def _fetch(self, url):
        s = self.session or requests.Session()
        if self.xml:
            req = s.get(url+'&out=xml')
            xml_data = ElementTree.fromstring(req.content)
            return xml_data
        else:
            req = s.get(url)
            json_data = req.json()
            return json_data


    def _find(self, search_term, page_num=None, rows_per_page=None):
        path = '&search_term={}'.format(search_term)
        if page_num:
            path += '&page_num={}'.format(page_num)
        if rows_per_page:
            path += '&rows_per_page={}'.format(rows_per_page)

        url = self._url(path)
        data = self._fetch(url)

        return data


    def by_last_updated(self, page_num=None, rows_per_page=None):
        """
        search_value format must be between 2 ISO8601 timestamps enclosed in square brackets.
        e.g. '[2017-01-01T00:00:00Z TO 2018-01-01T23:59:59Z]'
        """
        data = self._find('last_updated', page_num, rows_per_page)
        return data


    def by_name(self, page_num=None, rows_per_page=None):
        data = self._find('name', page_num, rows_per_page)
        return data


    def by_series_id(self, page_num=None, rows_per_page=None):
        data = self._find('series_id', page_num, rows_per_page)
        return data


    def __repr__(self):
        return '{}({!r},{!r})'.format(self.__class__.__name__, self.search_term, self.search_value)
