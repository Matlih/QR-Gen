import logging
from pathlib import Path
from typing import Optional, Tuple, Union

import qrcode
from PIL import Image

logger = logging.getLogger(__name__)

def generate_qr(
    url_or_text: str,
    output_path: Union[str, Path] = "qrcode.png",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    logo_path: Optional[Union[str, Path]] = None,
) -> Path:
    """
    Generate a QR code image from a URL or text and save it as PNG.
    Optionally, embed a logo in the center and customize colors.

    Args:
        url_or_text: The string to encode in the QR code.
        output_path: Where to save the generated image.
        box_size: Size of each box in the QR grid.
        border: Border thickness in boxes.
        fill_color: Color of the QR code data modules.
        back_color: Background color of the QR code.
        logo_path: Optional path to an image to embed in the center.

    Returns:
        Path to the saved image.

    Raises:
        ValueError: If url_or_text is empty.
        FileNotFoundError: If logo_path is provided but file does not exist.
    """
    if not url_or_text:
        raise ValueError("The input text or URL cannot be empty.")

    # High error correction is needed if we are placing a logo in the center
    error_correction = qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_L

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url_or_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    if logo_path:
        logo_path = Path(logo_path)
        if not logo_path.is_file():
            raise FileNotFoundError(f"Logo file not found: {logo_path}")
        
        try:
            logo = Image.open(logo_path).convert("RGBA")
            
            # Calculate the logo size (usually around 1/4th to 1/3rd of the QR code size)
            basewidth = int(img.size[0] / 3.5)
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            
            # Calculate the position to center the logo
            pos = (
                (img.size[0] - logo.size[0]) // 2,
                (img.size[1] - logo.size[1]) // 2
            )
            
            # Paste the logo on the QR code
            img.paste(logo, pos, mask=logo)
        except Exception as e:
            logger.error(f"Failed to apply logo: {e}")
            raise

    out = Path(output_path)
    img.save(str(out))
    return out.resolve()
