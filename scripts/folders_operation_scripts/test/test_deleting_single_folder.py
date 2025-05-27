import os
import pytest
from unittest.mock import patch
from scripts.folders_operation_scripts.Delete_Single_Folder import DeletingSingleFolderClass


@pytest.fixture
def deleter():
    return DeletingSingleFolderClass()


@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree")
def test_deletion_success(mock_rmtree, mock_exists, deleter):
    result = deleter.DeletingSingleFolder("/fake/path", "folder")
    full_path = os.path.join("/fake/path", "folder")
    mock_rmtree.assert_called_once_with(full_path)
    assert result is True


@patch("os.path.exists", return_value=False)
def test_folder_not_found(mock_exists, deleter):
    result = deleter.DeletingSingleFolder("/fake/path", "missing")
    assert result is False


@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree", side_effect=PermissionError("Access denied"))
def test_permission_error(mock_rmtree, mock_exists, deleter):
    result = deleter.DeletingSingleFolder("/fake/path", "no_access")
    assert result is False


@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree", side_effect=Exception("Unexpected error"))
def test_generic_exception(mock_rmtree, mock_exists, deleter):
    result = deleter.DeletingSingleFolder("/fake/path", "bad_folder")
    assert result is False
