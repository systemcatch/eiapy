# eiapy

Python 3 wrapper for the U.S. Energy Information Administration API.  

Work in progress, many parts don't work. Everything likely to change.  

For more details about the API go to the EIA's [Open Data](https://www.eia.gov/opendata/) page.

Quick example

Get the last 5 datapoints for the electricity interchange between CAISO and Comision Federal de Electricidad.

```python3
>>> from eiapy import Series
>>> from pprint import pprint
>>> caiso_to_cfe = Series('EBA.CISO-CFE.ID.H')
>>> pprint(caiso_to_cfe.last(5))
{'request': {'command': 'series', 'series_id': 'EBA.CISO-CFE.ID.H'},
 'series': [{'data': [['20180401T07Z', -11],
                      ['20180401T06Z', -16],
                      ['20180401T05Z', -11],
                      ['20180401T04Z', -7],
                      ['20180401T03Z', -5]],
             'description': 'Timestamps follow the ISO8601 standard '
                            '(https://en.wikipedia.org/wiki/ISO_8601). Hourly '
                            'representations are provided in Universal Time.',
             'end': '20180401T07Z',
             'f': 'H',
             'name': 'Actual Net Interchange for California Independent System '
                     'Operator (CISO) to Comision Federal de Electricidad '
                     '(CFE), Hourly',
             'series_id': 'EBA.CISO-CFE.ID.H',
             'start': '20150701T00Z',
             'units': 'megawatthours',
             'updated': '2018-04-02T08:43:16-0400'}]}

```

## TODO list

- Implement Geoset & Relation
- Finish other methods
- Clean up main
- Docstrings
- Add a license
- Link to EIA's terms and conditions
- Docs on how to use code, api key, examples
- Notes on api behaviour
- Make a pip package, maybe use pipenv
- Define python versions supported. 3.5/3.6+?
- Add xml option
- Version numbering system
