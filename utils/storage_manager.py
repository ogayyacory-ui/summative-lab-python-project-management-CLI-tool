"""Compatibility wrapper for the CLI storage layer."""

from utils.storage_handler import get_data_file, load_data, save_data

__all__ = ["get_data_file", "load_data", "save_data"]
