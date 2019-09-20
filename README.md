# eiapy
[![PyPI](https://img.shields.io/pypi/v/eiapy.svg)](https://pypi.org/project/eiapy/) [![PyPI - License](https://img.shields.io/pypi/l/eiapy.svg)](https://pypi.org/project/eiapy/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eiapy.svg)](https://pypi.org/project/eiapy/)  

Python 3 wrapper for the U.S. Energy Information Administration API.  

### Quick start
```bash
pip install eiapy
```

Get the last 5 measurements of the electricity flow between California and Mexico.

```python3
>>> from eiapy import Series
>>> cal_to_mex = Series('EBA.CISO-CFE.ID.H')
>>> cal_to_mex.last(5)
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

Further examples can be found [in this gist](https://gist.github.com/systemcatch/019cf50302093b9b51838c62b99623df).

To find more details about the API go to the EIA's [Open Data](https://www.eia.gov/opendata/) page. To find interesting data (and identifiers) [browse the data sets](https://www.eia.gov/opendata/qb.php).

For specific information about the [real-time grid display](https://www.eia.gov/beta/electricity/gridmonitor/dashboard/electric_overview/US48/US48) please see [this guide](https://www.eia.gov/realtime_grid/docs/userguide-knownissues.pdf).

Go [here](https://www.eia.gov/opendata/register.cfm#terms_of_service) to see the
API terms of service and [here](https://www.eia.gov/about/copyrights_reuse.cfm)
for an explanation of copyright and reuse of their data.

### Setting up your API key
An API key is needed to access the EIA's data, you can get one [here](https://www.eia.gov/opendata/register.php). eiapy needs this key to be manually set in the operating system environmental variables.

**Mac & Linux**  
Open a terminal and enter the following;
```bash
export EIA_KEY=type_your_api_key_here
```
To set it permanently follow the instructions on this [stackexchange question](https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables).

**Windows**  
Open a Command Prompt and enter the following;
```bat
setx EIA_KEY "type_your_api_key_within_the_quotes"
```

### Notes on API behaviour
- When providing invalid time limits for a series data request an empty data list is returned.
- For data requests num & start cannot be used together but num & end can.
- When an invalid series id is passed this is the response.
```python3
{'request': {'series_id': 'eba.ciso-cfe.id.', 'command': 'series', 'num': '5'},
 'data': {'error': 'invalid series_id. For key registration, documentation, and
 examples see https://www.eia.gov/developer/'}}
```

### Changelog
**0.1.4**
- Fixed broken Search `repr`.
- Added Python 3.7 to supported versions.
- Mention real-time grid in readme.

**0.1.3**
- Simplify construction and use of the Search class.
- Explain how to set up the API key.
- Added gist of examples to readme.

**0.1.2**
- Rename several methods for extra clarity.
- data -> get_data
- get -> get_updates

**0.1.1**  
- Started using requests session functionality to improve performance.
- Fixed a mistake in the MultiSeries class that stopped it working entirely.
- Added a version attribute to the package.
- Overhaul of readme.
