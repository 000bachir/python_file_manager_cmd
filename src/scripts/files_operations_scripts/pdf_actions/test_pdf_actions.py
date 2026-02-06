from __future__ import annotations
from unittest import mock
import pytest
import pymupdf
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os
from pdf_actions import pdfActions
from typing import Any, Tuple


class TestCreateBlankPage:
    def test_create_blank_pdf_page_success(self, tmp_path):
        pdf_actions = pdfActions()
        output_file = tmp_path / "test_blank.pdf"

        pdf_actions.create_blank_pdf_page(str(output_file))

        assert output_file.exists()
        doc = pymupdf.open(str(output_file))
        assert len(doc) == 1
        page = doc[0]
        assert abs(page.rect.width - 595) < 1
        assert abs(page.rect.height - 842) < 1
        doc.close()

    def test_create_blank_pdf_page_invalid_path(self):
        """Test creation with invalid file path"""
        pdf_actions = pdfActions()
        invalid_path = "/invalid/directory/that/does/not/exist/test.pdf"

        with pytest.raises(Exception):
            pdf_actions.create_blank_pdf_page(invalid_path)

    @patch("pymupdf.open")
    def test_create_blank_pdf_page_logs_error_on_exception(self, mock_open):
        pdf_actions = pdfActions()
        pdf_actions_logger = Mock()

        mock_open.side_effect = Exception("test error")
        with pytest.raises(Exception):
            pdf_actions.create_blank_pdf_page("test.pdf")
            pdf_actions.logger.error.assert_called_once()
            assert (
                "create_blank_pdf_page has crashed"
                in pdf_actions.logger.error.call_args[0][0]
            )

    def test_create_multi_blank_page(self, tmp_path):
        pdf_actions = pdfActions()
        for i in range(3):
            output_file = tmp_path / f"test_blank{i}.pdf"
            pdf_actions.create_blank_pdf_page(str(output_file))
            assert output_file.exists()
            doc = pymupdf.open(str(output_file))
            assert len(doc) == 1
            doc.close()


class TestSplitingSinglePages:
    @pytest.fixture
    def sample_pdf(self, tmp_path):
        doc = pymupdf.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((100, 100), "text content")
        filename = "./testing.pdf"
        doc.save(filename)
        doc.close()
        yield filename

        if os.path.exists(filename):
            os.remove(filename)

    def test_splitting_single_page_not_found(self):
        pdf_actions = pdfActions()
        if os.path.exists("./testing.pdf"):
            os.remove("./testing.pdf")
        result = pdf_actions.spliting_single_pages("dumb_filename.pdf")
        assert result is False

    def test_spliting_ignores_input_filename_parameter(self, sample_pdf):
        pdf_actions = pdfActions()
        # The method should ignore this parameter and use "./testing.pdf"
        result = pdf_actions.spliting_single_pages("completely_different_file.pdf")
        # Should not return False (which would indicate file not found)
        assert result != False or result is None
