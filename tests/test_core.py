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

def test_generate_qr_with_logo_space(tmp_path):
    from PIL import Image
    logo_file = tmp_path / "dummy_logo.png"
    Image.new("RGBA", (50, 50), (255, 0, 0, 255)).save(logo_file)

    output_file = tmp_path / "qr_with_logo.png"
    result = generate_qr(
        "https://example.com",
        output_path=output_file,
        logo_path=logo_file,
        logo_padding=8,
    )
    assert result.exists()
    assert result.stat().st_size > 0

def test_generate_qr_with_logo_and_custom_bg(tmp_path):
    from PIL import Image
    logo_file = tmp_path / "dummy_logo.png"
    Image.new("RGBA", (40, 40), (0, 128, 255, 255)).save(logo_file)

    output_file = tmp_path / "qr_with_custom_logo_bg.png"
    result = generate_qr(
        "https://example.com",
        output_path=output_file,
        logo_path=logo_file,
        logo_bg_color="#FFFFFF",
        back_color="transparent",
        logo_padding=10,
    )
    assert result.exists()
    assert result.stat().st_size > 0
