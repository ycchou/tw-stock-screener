from PIL import Image
import os

source_path = r"d:\Antigravity\tw-stock-screener\frontend\icons\icon-512.png"
output_dir = os.path.dirname(source_path)

# 定義要生成的尺寸
sizes = [72, 96, 128, 144, 152, 192, 384]

try:
    img = Image.open(source_path)
    print(f"Loaded source image: {source_path}, Mode: {img.mode}")

    # 1. 生成一般 PWA icons (保留透明度)
    for size in sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        filename = f"icon-{size}.png"
        resized_img.save(os.path.join(output_dir, filename))
        print(f"Generated {filename}")

    # 2. 生成 iOS 專用 icon (180x180, 不透明背景)
    # iOS icon 不支援透明背景，會變成黑色。我們手動加上背景色。
    ios_size = 180
    bg_color = (26, 26, 46) # #1a1a2e
    
    ios_bg = Image.new("RGB", (ios_size, ios_size), bg_color)
    resized_for_ios = img.resize((ios_size, ios_size), Image.Resampling.LANCZOS)
    
    if img.mode == 'RGBA':
        ios_bg.paste(resized_for_ios, (0, 0), resized_for_ios)
    else:
        ios_bg.paste(resized_for_ios, (0, 0))
        
    ios_bg.save(os.path.join(output_dir, "apple-touch-icon.png"))
    print("Generated apple-touch-icon.png (with background)")

except Exception as e:
    print(f"Error: {e}")
