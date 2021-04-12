import os.path
import json

template = """
<!doctype html>
<html>
<head>
<title>Cut Proof - {scale}</title>
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
.p {
position: absolute;
transition: opacity linear 0.5s;
}
.p:hover,
.p:active {
opacity: 0;
}

.p-img {
display: block;
}
"""


def generate_cut_proof_html(pieces_json_file, output_dir, scale):
    """Create a cut proof showing how the image was cut. Should look like
    original."""

    with open(pieces_json_file, "r") as pieces_json:
        piece_bboxes = json.load(pieces_json)

    pieces_html = []
    for (i, v) in piece_bboxes.items():
        i = int(i)
        x = v[0]
        y = v[1]
        width = v[2] - v[0]
        height = v[3] - v[1]
        el = "".join([
            f"<div id='p-{i}' class='p pc-{i}' style='left:{x}px;top:{y}px;'>",
            f"<img class='p-img' src='raster/{i}.png' width='{width}' height='{height}'>",
            "</div>"
        ])
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

    f = open(os.path.join(output_dir, "cut_proof.html"), "w")
    f.write(html)
    f.close()
