import cv2
import numpy as np

def make_ascii_art():
    img_bgr = cv2.imread("avatar.png")
    h, w = img_bgr.shape[:2]
    
    # GrabCut to isolate foreground
    mask = np.zeros((h, w), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # bounding box around person (center 75% width, 92% height)
    rect = (int(w * 0.10), int(h * 0.04), int(w * 0.80), int(h * 0.92))
    cv2.grabCut(img_bgr, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    fg_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Clean up mask with morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    # Grayscale image
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # Apply CLAHE for rich local contrast (eyes, hair, beard)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    contrast_gray = clahe.apply(gray)
    
    # Mask out background to pure white (255)
    processed = np.where(fg_mask == 1, contrast_gray, 255)
    
    # Target ASCII dimensions: 180 cols, 96 rows
    target_w, target_h = 180, 96
    resized = cv2.resize(processed, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Edge boost to emphasize outline of face, hair, and features
    edges = cv2.Canny(resized, 50, 140)
    
    ramp = " .:-=+*c#%@"
    lines = []
    for r in range(target_h):
        line_chars = []
        for c in range(target_w):
            val = int(resized[r, c])
            is_edge = edges[r, c] > 0
            if val > 225:
                line_chars.append(" ")
            else:
                if is_edge and val < 200:
                    val = max(0, val - 35)
                idx = int((225 - val) / 225 * (len(ramp) - 1))
                idx = max(0, min(len(ramp) - 1, idx))
                line_chars.append(ramp[idx])
        lines.append("".join(line_chars))
        
    return lines

def generate_svg(lines):
    svg_w, svg_h = 840.0, 880.0
    text_w = 800.0
    y_start = 43.2
    y_step = 8.333333333333334
    
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')
    out.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>')
    out.append(f'<rect width="{svg_w}" height="{svg_h}" rx="12" fill="url(#bg)"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{svg_w - 1}" height="{svg_h - 1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>')
    out.append(f'<line x1="0" y1="30" x2="{svg_w}" y2="30" stroke="#30363d"/>')
    out.append('<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>')
    out.append('<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>')
    out.append('<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>')
    out.append(f'<text x="{svg_w / 2}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">priyanshu@github: ~$ ./portrait.sh</text>')
    
    for i, line in enumerate(lines):
        y = y_start + i * y_step
        begin = i * 0.06
        out.append(f'<clipPath id="r{i}"><rect x="20" y="{y - 6.2:.1f}" height="{y_step:.3f}" width="0"><animate attributeName="width" from="0" to="{text_w}" begin="{begin:.3f}s" dur="0.06s" fill="freeze"/></rect></clipPath>')
        out.append(f'<g clip-path="url(#r{i})"><text xml:space="preserve" x="20" y="{y:.1f}" fill="#c9d1d9" font-size="7.2" textLength="{text_w}" lengthAdjust="spacing">{line}</text></g>')
        
    out.append(f'<line x1="0" y1="{svg_h - 43}" x2="{svg_w}" y2="{svg_h - 43}" stroke="#30363d"/>')
    out.append(f'<text x="20" y="{svg_h - 24}" fill="#7d8590" font-size="13">priyanshu@github:~$ whoami <tspan fill="#c9d1d9">Priyanshu Thakur</tspan></text>')
    out.append('</svg>')
    
    with open("priyanshu-ascii.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Generated priyanshu-ascii.svg ({len(lines)} lines)")

if __name__ == "__main__":
    lines = make_ascii_art()
    generate_svg(lines)
