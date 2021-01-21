import netCDF4 as nc
from typing import Iterator

from ..output.l1bs_writer import L1BSVariables


class NetCDFReaderL1BS:
    """
    retrieves data from a netCDF document in blocks
    """

    @property
    def variables(self) -> Iterator[L1BSVariables]:
        return iter(L1BSVariables)

    @property
    def dimensions(self):
        return self._doc.dimensions

    def __init__(self, filename, chunk_size=40):
        """
        open document and set block size
        """

        self._doc = nc.Dataset(filename, 'r')
        self.cache = {}
        self.chunk_index = None
        self.chunk_size = chunk_size

        for varname in self.variables:
            name = varname.value

            var = self._doc.variables[name]
            var.set_auto_mask(False)

    def get_variable(self, varname: L1BSVariables) -> nc.Variable:
        return self._doc.variables[varname.value]

    def get_value(self, varname: L1BSVariables, index: int):
        """
        get the value of a variable at a specific index
        """
        chunk_index = index % self.chunk_size
        chunk_start = index - chunk_index

        if chunk_start != self.chunk_index:
            self._load_chunk(chunk_start)

        return self.cache[varname][chunk_index]

    def _load_chunk(self, chunk_start: int):
        """
        read a new chunk & replace the existing one
        """
        chunk_end = chunk_start + self.chunk_size

        for varname in self.variables:
            name = varname.value
            var = self._doc.variables[name]
            varlen = var.shape[0]

            if chunk_start >= varlen:
                continue

            end = min(varlen, chunk_end)

            self.cache[varname] = var[chunk_start:end].copy()

        self.chunk_index = chunk_start

    def close(self):
        self._doc.close()

    def read_globals(self):
        attrs = {}
        for attr_name in self._doc.ncattrs():
            attrs[attr_name] = self._doc.getncattr(attr_name)
        return attrs
