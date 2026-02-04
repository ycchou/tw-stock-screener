from PIL import Image
import os

# 使用者上傳圖片的絕對路徑
source_path = r"C:/Users/Chou Yu-Cheng/.gemini/antigravity/brain/02d5b2c2-c99e-4a31-9d3b-56bc900c6fc3/uploaded_media_1770223481532.png"
output_dir = r"d:\Antigravity\tw-stock-screener\frontend\icons"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Reading source image from: {source_path}")

try:
    img = Image.open(source_path)
    print(f"Image loaded. Size: {img.size}, Mode: {img.mode}")

    sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]

    for size in sizes:
        # 高品質縮放
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        if size == 180:
            # 處理 iOS Icon (apple-touch-icon)
            filename = "apple-touch-icon.png"
            
            # iOS 不支援透明背景，如果是 RGBA，合成到深色背景上
            if resized.mode == 'RGBA':
                # 使用 App 主題色背景 #1a1a2e (26, 26, 46) 
                # 或者如果原圖是滿版且角落透明，這會填滿角落
                bg = Image.new("RGB", (size, size), (26, 26, 46))
                bg.paste(resized, (0, 0), resized)
                bg.save(os.path.join(output_dir, filename))
            else:
                resized.convert("RGB").save(os.path.join(output_dir, filename))
                
        else:
            # 處理 Android/PWA Icon
            filename = f"icon-{size}.png"
            resized.save(os.path.join(output_dir, filename))
            
        print(f"Generated {filename}")

    print("All icons updated successfully based on the uploaded image.")

except Exception as e:
    print(f"An error occurred: {e}")
