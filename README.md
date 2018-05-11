# eiapy

Python 3 wrapper for the U.S. Energy Information Administration API.  

`pip install eiapy`

Current PyPI version 0.1.0

For more details about the API go to the EIA's [Open Data](https://www.eia.gov/opendata/) page.

Go [here](https://www.eia.gov/opendata/register.cfm#terms_of_service) to see the
API terms of service and [here](https://www.eia.gov/about/copyrights_reuse.cfm)
for an explanation of copyright and reuse of their data.

## Quick example

Get the last 5 datapoints for the electricity interchange between California and Mexico.

```python3
>>> from eiapy import Series
>>> cal_to_mex = Series('EBA.CISO-CFE.ID.H')
>>> pprint(cal_to_mex.last(5))
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

## Notes on API behaviour
- When providing invalid time limits for a series data request data=[] is returned.
- For data requests num & start cannot be used together but num & end can.
- When an invalid series id is passed this is the response.
```
# {'request': {'series_id': 'eba.ciso-cfe.id.', 'command': 'series', 'num': '5'},
#  'data': {'error': 'invalid series_id. For key registration, documentation, and examples see https://www.eia.gov/developer/'}}
```

## TODO list

- Implement Relation query
- Docs on how to use code, examples
- Full section on getting an API key for Windows/Mac/Linux
- Better setup and build using https://github.com/kennethreitz/setup.py
- Notes on api behaviour (part done)
- Better naming of some functions
