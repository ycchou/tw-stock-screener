from PIL import Image
import os

# 使用者指定的新圖片路徑
source_path = r"d:\Antigravity\tw-stock-screener\frontend\icons\圖片2.png"
output_dir = r"d:\Antigravity\tw-stock-screener\frontend\icons"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Reading source image from: {source_path}")

try:
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at {source_path}")
        exit(1)

    img = Image.open(source_path)
    print(f"Image loaded. Size: {img.size}, Mode: {img.mode}")

    # 定義 PWA 和 iOS 需要的所有尺寸
    sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]

    for size in sizes:
        # 使用高品質重採樣進行縮放
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        if size == 180:
            # iOS (apple-touch-icon)
            filename = "apple-touch-icon.png"
            
            # iOS 不支援透明背景，如果是透明圖，合成到深色背景
            if resized.mode == 'RGBA':
                # 使用 App 主題色背景 #1a1a2e
                bg = Image.new("RGB", (size, size), (26, 26, 46))
                # 將圖示置中貼上 (如果是滿版圖示，座標 0,0 即可)
                bg.paste(resized, (0, 0), resized)
                bg.save(os.path.join(output_dir, filename))
            else:
                resized.convert("RGB").save(os.path.join(output_dir, filename))
                
        else:
            # Android/PWA (保留透明度)
            filename = f"icon-{size}.png"
            resized.save(os.path.join(output_dir, filename))
            
        print(f"Generated {filename}")

    print("All icons updated successfully using 圖片1.png.")

except Exception as e:
    print(f"An error occurred: {e}")
