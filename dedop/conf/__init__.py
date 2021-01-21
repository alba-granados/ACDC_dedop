"""
Processor configuration management.
"""
from .characterization import CharacterisationFile
from .configuration import ConfigurationFile
from .constants import ConstantsFile
from .auxiliary_file_reader import AuxiliaryFileReader
from .auxiliary_parameter import AuxiliaryParameter
from .acdc_configuration import ACDCConfiguration

__author__ = 'DeDop Development Team'

__all__ = [
    'CharacterisationFile',
    'ConstantsFile',
    'ConfigurationFile',
    'AuxiliaryFileReader',
    'AuxiliaryParameter',
    'ACDCConfiguration'
]

