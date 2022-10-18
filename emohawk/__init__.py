# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


import numpy as np

__name__ = "emohawk"
__version__ = "0.0.1"
__author__ = "European Centre for Medium-Range Weather Forecasts (ECMWF)"
__author_email__ = "james.varndell@ecmwf.int"
__license__ = "Apache License Version 2.0"
__description__ = ""


class Data:
    """
    High-level abstract class represnting arbitrary geospatial data.

    Offers polymorphism to well-know geospatial file formats and Python
    libraries, plus convenience methods for quickly extracting useful
    information from complex data structures.
    NOTE: Do not call this class directly outside of the emohawk source code.
    """

    def __init__(self, source, **kwargs):
        self.source = source
        self._extents = None

    def mutate(self):
        return self

    def to_numpy(self, *args, **kwargs):
        self._not_implemented()

    def to_pandas(self, *args, **kwargs):
        self._not_implemented()

    def to_xarray(self, *args, **kwargs):
        self._not_implemented()

    def to_netcdf(self, *args, **kwargs):
        self._not_implemented()

    def to_grib(self, *args, **kwargs):
        self._not_implemented()

    def to_json(self, *args, **kwargs):
        self._not_implemented()

    def to_geojson(self, *args, **kwargs):
        try:
            return self.to_json(*args, **kwargs)
        except NotImplementedError:
            self._not_implemented()

    def to_dict(self, *args, **kwargs):
        self._not_implemented()

    def to_shapefile(self, *args, **kwargs):
        self._not_implemented()

    def to_csv(self, *args, **kwargs):
        self._not_implemented()

    def save(self, *args, **kwargs):
        self._not_implemented()

    def axis(self, *args, **kwargs):
        self._not_implemented()

    def component(self, *args, **kwargs):
        self._not_implemented()

    @property
    def extents(self):
        if self._extents is None:
            try:
                self._extents = self._get_extents()
            except NotImplementedError:
                self._not_implemented()
        return self._extents

    def _get_extents(self):
        x0 = np.amax(self.axis("x").values)
        x1 = np.amin(self.axis("x").values)
        y0 = np.amin(self.axis("y").values)
        y1 = np.amax(self.axis("y").values)
        return (x0, x1, y0, y1)

    @property
    def crs(self):
        self._not_implemented()

    def _not_implemented(self):
        import inspect

        func = inspect.stack()[1][3]
        module = self.__class__.__module__
        name = self.__class__.__name__

        raise NotImplementedError(f"{module}.{name}.{func}")


def open(source, *args, **kwargs):
    """
    Open a file, directory, or Python object as a emohawk `Data` class.

    Offers flexible polymorphism to get your geospatial data into a format
    that suits your needs.

    Parameters
    ----------
    source : (str or object)
        The source of your data. This can be a string respresenting the path
        to your data file, or an object that is understood by emohawk (for example
        an xarray, numpy or pandas object).

    Returns
    -------
    emohawk.Data
        Polymorphic data object with methods for transforming data into a wide
        range of geospatial data formats and Python objects.
    """
    from . import readers, wrappers

    if isinstance(source, str):
        opener = readers.get_reader
    else:
        opener = wrappers.get_wrapper
    result = opener(source, *args, **kwargs)

    return result
