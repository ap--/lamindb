"""Storage API.

Valid suffixes.

.. autosummary::
   :toctree: .

   VALID_SUFFIXES

Array accessors.

.. autosummary::
   :toctree: .

   AnnDataAccessor
   BackedAccessor
"""

from lamindb_setup.core.upath import LocalPathClasses, UPath, infer_filesystem

from ._backed_access import AnnDataAccessor, BackedAccessor
from ._tiledbsoma import register_for_tiledbsoma_store, write_tiledbsoma_store
from ._valid_suffixes import VALID_SUFFIXES
from .objects import infer_suffix, write_to_disk
from .paths import delete_storage, load_to_memory
