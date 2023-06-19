import shutil
from pathlib import Path

import pytest

from lamindb import File

# how do we properly abstract out the default storage variable?
# currently, we're only mocking it through `default_storage` as
# set in conftest.py


@pytest.fixture(
    scope="module", params=[(True, "./default_storage/"), (False, "./outside_storage/")]
)
def get_test_filepaths(request):
    isin_default_storage: bool = request.param[0]
    root_dir: Path = Path(request.param[1])
    test_folder = root_dir / "my_folder/"
    test_folder.mkdir(parents=True)
    test_filepath = test_folder / "my_file.csv"
    test_filepath.write_text("a")
    # return a boolean indicating whether test filepath is in default storage
    # and the test filepath
    yield (isin_default_storage, test_filepath)
    shutil.rmtree(test_folder)


# this tests the basic (non-provenance-related) metadata
@pytest.mark.parametrize("key", [None, "my_new_folder/my_file.csv"])
@pytest.mark.parametrize("name", [None, "my name"])
def test_init_from_filepath_basic_fields(get_test_filepaths, key, name):
    isin_default_storage = get_test_filepaths[0]
    test_filepath = get_test_filepaths[1]
    if name is None and key is None and not isin_default_storage:
        with pytest.raises(ValueError):
            file = File(test_filepath, key=key, name=name)
    else:
        file = File(test_filepath, key=key, name=name)
        assert file.name is None if name is None else file.name == name
        assert file.suffix == ".csv"
        if key is None:
            assert (
                file.key == "my_folder/my_file.csv"
                if isin_default_storage
                else file.key is None
            )
        else:
            assert file.key == key
        assert file.storage.root == Path("./default_storage").resolve().as_posix()
        assert file.hash == "DMF1ucDxtqgxw5niaXcmYQ"
        if isin_default_storage and key is None:
            assert str(test_filepath.resolve()) == str(file.path())
