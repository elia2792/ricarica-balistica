import os
from PIL import Image, ImageDraw, ImageFont

def create_og_image():
    width = 1200
    height = 630
    img = Image.new('RGB', (width, height), color='#0f1115')
    draw = ImageDraw.Draw(img)

    # Tactical grid background lines
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill='#181c24', width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill='#181c24', width=1)

    # Tactical corner brackets and border
    margin = 30
    draw.rectangle([margin, margin, width - margin, height - margin], outline='#232834', width=2)
    bracket_len = 40
    # Top-left
    draw.line([(margin, margin), (margin + bracket_len, margin)], fill='#f59e0b', width=4)
    draw.line([(margin, margin), (margin, margin + bracket_len)], fill='#f59e0b', width=4)
    # Top-right
    draw.line([(width - margin, margin), (width - margin - bracket_len, margin)], fill='#f59e0b', width=4)
    draw.line([(width - margin, margin), (width - margin, margin + bracket_len)], fill='#f59e0b', width=4)
    # Bottom-left
    draw.line([(margin, height - margin), (margin + bracket_len, height - margin)], fill='#f59e0b', width=4)
    draw.line([(margin, height - margin), (margin, height - margin - bracket_len)], fill='#f59e0b', width=4)
    # Bottom-right
    draw.line([(width - margin, height - margin), (width - margin - bracket_len, height - margin)], fill='#f59e0b', width=4)
    draw.line([(width - margin, height - margin), (width - margin, height - margin - bracket_len)], fill='#f59e0b', width=4)

    # Crosshair in background
    cx, cy = 980, 315
    for r in [50, 90, 140]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline='#1e293b', width=2)
    draw.line([(cx - 160, cy), (cx + 160, cy)], fill='#334155', width=2)
    draw.line([(cx, cy - 160), (cx, cy + 160)], fill='#334155', width=2)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill='#f59e0b')

    # Fonts
    font_paths = [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/Library/Fonts/Arial.ttf'
    ]
    font_large = None
    font_med = None
    font_small = None

    for p in font_paths:
        if os.path.exists(p):
            try:
                font_large = ImageFont.truetype(p, 54)
                font_med = ImageFont.truetype(p, 28)
                font_small = ImageFont.truetype(p, 20)
                break
            except Exception:
                continue

    if not font_large:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Badge: MIL-SPEC // CIP CERTIFIED
    draw.rectangle([70, 80, 340, 120], fill='#1e293b', outline='#f59e0b', width=1)
    draw.text((85, 90), 'TACTICAL RELOAD HUB', fill='#f59e0b', font=font_small)

    # Title
    draw.text((70, 150), 'BALLISTIC OPS', fill='#ffffff', font=font_large)
    draw.text((490, 150), '//', fill='#f59e0b', font=font_large)
    draw.text((70, 225), 'RICARICA MUNIZIONI', fill='#ffffff', font=font_large)

    # Subtitle / Description
    draw.text((70, 315), 'Tabelle CIP • Calcolo Costo Colpo • Quaderno di Tiro', fill='#94a3b8', font=font_med)

    # Bullet pills
    features = [
        ('TABELLE CIP & DOSI', '#2563eb'),
        ('COSTO AL SINGOLO COLPO', '#16a34a'),
        ('AMMORTAMENTO PRESSA', '#f59e0b'),
        ('ETICHETTE MUNIZIONI PDF', '#8b5cf6')
    ]
    
    start_x = 70
    start_y = 400
    for label, color in features:
        draw.rectangle([start_x, start_y, start_x + 240, start_y + 45], fill='#161920', outline=color, width=2)
        draw.text((start_x + 15, start_y + 12), label, fill='#e2e8f0', font=font_small)
        start_x += 255

    # Footer domain
    draw.line([(70, 520), (width - 70, 520)], fill='#232834', width=1)
    draw.text((70, 545), 'https://ricarica-balistica.onrender.com', fill='#10b981', font=font_med)
    draw.text((820, 548), 'Free & Open Ballistics Tool', fill='#64748b', font=font_small)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img', 'og-preview.png')
    img.save(output_path, 'PNG', quality=95)
    print(f'[+] OG Preview salvato con successo in {output_path}')

if __name__ == '__main__':
    create_og_image()
