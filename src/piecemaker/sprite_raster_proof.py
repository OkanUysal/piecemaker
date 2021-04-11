import os.path
import json
from uuid import uuid4

from PIL import Image

template = """
<!doctype html>
<html>
<head>
<title>Sprite Raster Proof - {scale}</title>
<link rel="stylesheet" media="all" href="sprite_raster.css">
<style>
{style}
</style>
</head>
<body>
<p>
Piece count: {piece_count}
</p>

<!-- All the piece div elements -->
<div class="container">
{pieces}
</div>
</body>
</html>"""

style = """
body {
background: black;
color: white;
}
.container {
position: relative;
}
.pc {
position: absolute;
transition: opacity linear 0.5s;
}
.pc:hover,
.pc:active {
opacity: 0;
}

.pc > img {
display: block;
}
"""


def generate_sprite_raster_proof_html(pieces_json_file, output_dir, sprite_layout, scale):
    """Create a sprite proof showing how the image was cut. Should look like
    original."""

    with open(pieces_json_file, "r") as pieces_json:
        piece_bboxes = json.load(pieces_json)

    im = Image.open(os.path.join(output_dir, "sprite_without_padding.png"))
    (bg_image_width, bg_image_height) = im.size
    im.close()

    cachebust = str(uuid4())
    pieces_style = [
        f".pc.pc--{scale}"
        + "{"
        + f"""background-image: url('sprite_without_padding.png?{cachebust}');
background-size: {bg_image_width}px {bg_image_height}px;
"""
        + "}"
    ]
    for (i, v) in sprite_layout.items():
        x = v[0]
        y = v[1]
        width = v[2]
        height = v[3]
        pieces_style.append(
            f"[data-pc='{i}'].pc.pc--{scale}"
            + "{"
            + f"background-position:{x * -1}px {y * -1}px;"
            + f"width:{width}px;height:{height}px;"
            + "}"
        )

    with open(os.path.join(output_dir, "sprite_raster.css"), "w") as css:
        css.write("".join(pieces_style))

    pieces_html = []
    for (i, v) in piece_bboxes.items():
        i = int(i)
        x = v[0]
        y = v[1]
        width = v[2] - v[0]
        height = v[3] - v[1]
        el = f"""
<div class='pc pc--{scale}' data-pc='{i}' style='left:{x}px;top:{y}px;'></div>"""
        pieces_html.append(el)

    pieces = "".join(pieces_html)
    html = template.format(
        **{
            "scale": scale,
            "pieces": pieces,
            "piece_count": len(piece_bboxes.items()),
            "style": style,
        }
    )

    f = open(os.path.join(output_dir, "sprite_raster_proof.html"), "w")
    f.write(html)
    f.close()