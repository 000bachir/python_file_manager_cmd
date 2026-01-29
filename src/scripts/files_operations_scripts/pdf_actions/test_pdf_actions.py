from __future__ import annotations
import pytest
import logging
import pymupdf
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from pdf_actions import pdfActions


class testPdfActions:
    def test_init_with_logging_enabled(self):
        actions_pdf = pdfActions(enable_loggin=False)
        assert not hasattr(actions_pdf, "logger")
