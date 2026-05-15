# trace_to_svg.py

from PIL import Image
import numpy as np
from skimage import measure
from pathlib import Path

INPUT = "favicon 9.png"
OUTPUT = "echosearch_exact_trace.svg"

img = Image.open(INPUT).convert("RGBA")
imgq = img.convert("P", palette=Image.ADAPTIVE, colors=4).convert("RGBA")
arr = np.array(imgq)

colors = np.unique(arr.reshape(-1, 4), axis=0)

svg_parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="120" height="120" viewBox="0 0 120 120" '
    'shape-rendering="geometricPrecision">'
]

for col in colors:
    if col[3] < 10:
        continue

    mask = np.all(arr == col, axis=-1).astype(np.uint8)
    contours = measure.find_contours(mask, 0.5)

    hex_color = "#%02x%02x%02x" % tuple(col[:3])
    opacity = round(col[3] / 255, 3)

    path_data = []

    for contour in contours:
        contour = np.fliplr(contour)

        if len(contour) < 3:
            continue

        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in contour)
        path_data.append(f"M {pts} Z")

    if path_data:
        svg_parts.append(
            f'<path d="{" ".join(path_data)}" '
            f'fill="{hex_color}" '
            f'fill-opacity="{opacity}"/>'
        )

svg_parts.append("</svg>")

svg_content = "\n".join(svg_parts)

Path(OUTPUT).write_text(svg_content, encoding="utf-8")

print(f"Saved SVG to: {OUTPUT}")
