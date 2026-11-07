import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_master_icon(size=1024):
    # Master image with deep emerald gradient background
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Base Rounded Squircle / Shield for App Icon
    corner_radius = int(size * 0.22)
    
    # Draw gradient background on a separate surface
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    
    # Elegant Emerald Gradient: top-left (#047857) to bottom-right (#022c22)
    for y in range(size):
        ratio = y / size
        r = int(6 * (1 - ratio) + 2 * ratio)
        g = int(120 * (1 - ratio) + 44 * ratio)
        b = int(87 * (1 - ratio) + 34 * ratio)
        bg_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Mask with rounded rectangle
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=corner_radius, fill=255)
    
    # Apply mask to background
    rounded_bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded_bg.paste(bg, (0, 0), mask)
    img = Image.alpha_composite(img, rounded_bg)
    draw = ImageDraw.Draw(img)

    # 2. Outer Golden Ornamental Border
    border_inset = int(size * 0.04)
    border_width = int(size * 0.018)
    gold_color = (245, 158, 11, 230)      # Amber-500
    gold_highlight = (252, 211, 77, 255)  # Amber-300
    
    draw.rounded_rectangle(
        [(border_inset, border_inset), (size - border_inset, size - border_inset)],
        radius=corner_radius - int(border_inset * 0.6),
        outline=gold_color,
        width=border_width
    )

    # 3. Inner Decorative Mihrab / Arch Architechture
    center_x = size // 2
    mihrab_top = int(size * 0.18)
    mihrab_bottom = int(size * 0.82)
    mihrab_left = int(size * 0.22)
    mihrab_right = int(size * 0.78)

    # Islamic Arch Points (Ogee arch)
    arch_points = []
    # Base pillars
    arch_points.append((mihrab_left, mihrab_bottom))
    arch_points.append((mihrab_left, int(size * 0.45)))
    
    # Curve upward to pointed peak
    steps = 40
    for i in range(steps + 1):
        t = i / steps
        # Ogee curve left side
        x = mihrab_left + (center_x - mihrab_left) * t
        # Shape formula for Islamic ogee arch
        y = int(size * 0.45) - int(math.sin(t * math.pi / 2) ** 1.3 * (int(size * 0.45) - mihrab_top))
        arch_points.append((int(x), int(y)))
    
    for i in range(steps, -1, -1):
        t = i / steps
        x = size - (mihrab_left + (center_x - mihrab_left) * t)
        y = int(size * 0.45) - int(math.sin(t * math.pi / 2) ** 1.3 * (int(size * 0.45) - mihrab_top))
        arch_points.append((int(x), int(y)))

    arch_points.append((mihrab_right, mihrab_bottom))

    # Fill Mihrab with darker emerald glow
    draw.polygon(arch_points, fill=(2, 44, 34, 210), outline=gold_highlight)
    
    # Thicker Mihrab Frame
    for offset in range(1, int(size * 0.015)):
        offset_points = [(p[0], p[1]) for p in arch_points]
        draw.polygon(offset_points, outline=gold_color)

    # 4. Central Radiant Islamic Kaaba & Crescent
    # Kaaba cube silhouette inside the mihrab
    kaaba_w = int(size * 0.26)
    kaaba_h = int(size * 0.26)
    kaaba_x1 = center_x - kaaba_w // 2
    kaaba_y1 = int(size * 0.46)
    kaaba_x2 = kaaba_x1 + kaaba_w
    kaaba_y2 = kaaba_y1 + kaaba_h

    # Shadow under Kaaba
    draw.ellipse([(kaaba_x1 - 10, kaaba_y2 - 8), (kaaba_x2 + 10, kaaba_y2 + 25)], fill=(0, 20, 15, 180))

    # Kaaba body (rich charcoal black)
    draw.rounded_rectangle([(kaaba_x1, kaaba_y1), (kaaba_x2, kaaba_y2)], radius=int(size * 0.02), fill=(20, 25, 30, 255), outline=(60, 65, 75, 255), width=2)
    
    # Golden Kiswah Belt (Hizam)
    belt_y1 = kaaba_y1 + int(kaaba_h * 0.22)
    belt_y2 = belt_y1 + int(kaaba_h * 0.14)
    draw.rectangle([(kaaba_x1, belt_y1), (kaaba_x2, belt_y2)], fill=(251, 191, 36, 255)) # Amber gold
    # Golden Bab al-Kaaba (Door)
    door_w = int(kaaba_w * 0.28)
    door_h = int(kaaba_h * 0.52)
    door_x1 = center_x + int(kaaba_w * 0.08)
    door_y1 = kaaba_y2 - door_h
    draw.rounded_rectangle([(door_x1, door_y1), (door_x1 + door_w, kaaba_y2)], radius=int(size * 0.01), fill=(245, 158, 11, 255))

    # 5. Radiant Golden Crescent above Kaaba
    crescent_cx = center_x
    crescent_cy = int(size * 0.33)
    crescent_r = int(size * 0.085)
    
    # Outer circle for crescent
    cres_outer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cres_draw = ImageDraw.Draw(cres_outer)
    cres_draw.ellipse(
        [(crescent_cx - crescent_r, crescent_cy - crescent_r),
         (crescent_cx + crescent_r, crescent_cy + crescent_r)],
        fill=gold_highlight
    )
    
    # Inner subtract circle to form the sickle shape
    inner_r = int(crescent_r * 0.85)
    inner_cx = crescent_cx + int(crescent_r * 0.38)
    inner_cy = crescent_cy - int(crescent_r * 0.22)
    
    cres_cut = Image.new("L", (size, size), 255)
    cut_draw = ImageDraw.Draw(cres_cut)
    cut_draw.ellipse([(inner_cx - inner_r, inner_cy - inner_r), (inner_cx + inner_r, inner_cy + inner_r)], fill=0)
    
    cres_final = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cres_final.paste(cres_outer, (0, 0), cres_cut)
    
    img = Image.alpha_composite(img, cres_final)
    draw = ImageDraw.Draw(img)

    # 6. Star of Dawn inside the crescent
    star_cx = crescent_cx + int(crescent_r * 0.32)
    star_cy = crescent_cy - int(crescent_r * 0.18)
    star_r = int(size * 0.025)
    
    def draw_star(center, radius, points=5):
        cx, cy = center
        pts = []
        for i in range(points * 2):
            r = radius if i % 2 == 0 else radius * 0.45
            angle = i * math.pi / points - math.pi / 2
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        return pts

    draw.polygon(draw_star((star_cx, star_cy), star_r, 5), fill=gold_highlight)

    # 7. Elegant Arabic Typography badge at the bottom: "المُصَلِّي"
    # Ribbon at base
    ribbon_w = int(size * 0.6)
    ribbon_h = int(size * 0.1)
    ribbon_x1 = center_x - ribbon_w // 2
    ribbon_y1 = int(size * 0.84)
    draw.rounded_rectangle([(ribbon_x1, ribbon_y1), (ribbon_x1 + ribbon_w, ribbon_y1 + ribbon_h)], radius=int(ribbon_h * 0.4), fill=(4, 120, 87, 240), outline=gold_color, width=3)

    # Little golden beads on ribbon ends
    draw.ellipse([(ribbon_x1 + 10, ribbon_y1 + ribbon_h//2 - 6), (ribbon_x1 + 22, ribbon_y1 + ribbon_h//2 + 6)], fill=gold_highlight)
    draw.ellipse([(ribbon_x1 + ribbon_w - 22, ribbon_y1 + ribbon_h//2 - 6), (ribbon_x1 + ribbon_w - 10, ribbon_y1 + ribbon_h//2 + 6)], fill=gold_highlight)

    return img

def export_all_sizes():
    out_dir = r"C:\Users\melwa\OneDrive\Documents\GitHub\Alsalah"
    icons_dir = os.path.join(out_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    master = create_master_icon(1024)
    master_path = os.path.join(icons_dir, "master-1024.png")
    master.save(master_path, "PNG")
    print(f"Master icon saved to {master_path}")

    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
        "icon-maskable-192.png": 192,
        "icon-maskable-512.png": 512,
    }

    # Generate resized pngs in both /icons/ and root
    for filename, sz in sizes.items():
        resized = master.resize((sz, sz), Image.Resampling.LANCZOS)
        # In /icons/
        p1 = os.path.join(icons_dir, filename)
        resized.save(p1, "PNG")
        # In root
        p2 = os.path.join(out_dir, filename)
        resized.save(p2, "PNG")
        print(f"Generated: {filename} ({sz}x{sz})")

    # Generate multi-size favicon.ico (16, 32, 48)
    ico_img = master.resize((48, 48), Image.Resampling.LANCZOS)
    ico_path1 = os.path.join(out_dir, "favicon.ico")
    ico_path2 = os.path.join(icons_dir, "favicon.ico")
    ico_img.save(ico_path1, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    ico_img.save(ico_path2, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("Multi-size favicon.ico generated successfully.")

if __name__ == "__main__":
    export_all_sizes()
