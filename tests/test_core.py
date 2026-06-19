import os
from pathlib import Path

import pytest
from qr_gen.core import generate_qr

def test_generate_qr_basic(tmp_path):
    output_file = tmp_path / "test_qr.png"
    result = generate_qr("https://example.com", output_path=output_file)
    
    assert result.exists()
    assert result == output_file
    assert result.stat().st_size > 0

def test_generate_qr_empty_url(tmp_path):
    with pytest.raises(ValueError, match="cannot be empty"):
        generate_qr("", output_path=tmp_path / "fail.png")

def test_generate_qr_custom_colors(tmp_path):
    output_file = tmp_path / "colored_qr.png"
    result = generate_qr(
        "Hello", 
        output_path=output_file, 
        fill_color="blue", 
        back_color="yellow"
    )
    assert result.exists()

def test_generate_qr_with_logo_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        generate_qr(
            "Hello",
            output_path=tmp_path / "logo_qr.png",
            logo_path="non_existent_logo.png"
        )
