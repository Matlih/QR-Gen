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
    logo_padding: int = 6,
    logo_bg_color: Optional[str] = None,
) -> Path:
    """
    Generate a QR code image from a URL or text and save it as PNG.
    Optionally, embed a logo in the center with a dedicated clean space and customize colors.

    Args:
        url_or_text: The string to encode in the QR code.
        output_path: Where to save the generated image.
        box_size: Size of each box in the QR grid.
        border: Border thickness in boxes.
        fill_color: Color of the QR code data modules.
        back_color: Background color of the QR code.
        logo_path: Optional path to an image to embed in the center.
        logo_padding: Padding in pixels around the logo's dedicated space.
        logo_bg_color: Background color for the logo space (matches QR background by default).

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

    is_transparent = back_color.strip().lower() == "transparent"
    effective_back_color = "white" if is_transparent else back_color

    img = qr.make_image(fill_color=fill_color, back_color=effective_back_color).convert("RGBA")

    if is_transparent:
        from PIL import ImageColor
        try:
            bg_rgb = ImageColor.getrgb(effective_back_color)
            if len(bg_rgb) == 4:
                bg_rgb = bg_rgb[:3]
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    if pixels[x, y][:3] == bg_rgb:
                        pixels[x, y] = (bg_rgb[0], bg_rgb[1], bg_rgb[2], 0)
        except Exception as e:
            logger.warning(f"Could not make background transparent: {e}")

    if logo_path:
        logo_path = Path(logo_path)
        if not logo_path.is_file():
            raise FileNotFoundError(f"Logo file not found: {logo_path}")
        
        try:
            from PIL import ImageColor, ImageDraw
            logo = Image.open(logo_path).convert("RGBA")
            
            # Proportionally scale logo to fit comfortably in the center (max ~1/3.8 of QR code size)
            max_logo_dim = max(10, int(img.size[0] / 3.8))
            logo.thumbnail((max_logo_dim, max_logo_dim), Image.Resampling.LANCZOS)
            
            lw, lh = logo.size
            pos = ((img.size[0] - lw) // 2, (img.size[1] - lh) // 2)
            
            # Create reserved space (quiet zone / badge) for the logo in the middle
            pad = max(0, int(logo_padding))
            radius = min(6, pad) if pad > 0 else 0
            bg_box = (pos[0] - pad, pos[1] - pad, pos[0] + lw + pad, pos[1] + lh + pad)
            
            target_bg = (
                logo_bg_color.strip()
                if logo_bg_color and logo_bg_color.strip()
                else ("transparent" if is_transparent else effective_back_color)
            )
            
            if target_bg.lower() == "transparent":
                # Clear all pixels in the reserved logo space (removes QR modules in the center)
                mask = Image.new("L", img.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                if radius > 0:
                    mask_draw.rounded_rectangle(bg_box, radius=radius, fill=255)
                else:
                    mask_draw.rectangle(bg_box, fill=255)
                trans = Image.new("RGBA", img.size, (0, 0, 0, 0))
                img.paste(trans, (0, 0), mask=mask)
            else:
                # Fill the reserved logo space with the specified or matching background color
                bg_rgb = ImageColor.getrgb(target_bg)
                bg_rgba = (bg_rgb[0], bg_rgb[1], bg_rgb[2], 255) if len(bg_rgb) == 3 else bg_rgb
                badge = Image.new("RGBA", img.size, (0, 0, 0, 0))
                badge_draw = ImageDraw.Draw(badge)
                if radius > 0:
                    badge_draw.rounded_rectangle(bg_box, radius=radius, fill=bg_rgba)
                else:
                    badge_draw.rectangle(bg_box, fill=bg_rgba)
                img.paste(badge, (0, 0), mask=badge)
            
            # Paste the logo in the center of its reserved space
            img.paste(logo, pos, mask=logo)
        except Exception as e:
            logger.error(f"Failed to apply logo: {e}")
            raise

    out = Path(output_path)
    img.save(str(out))
    return out.resolve()
