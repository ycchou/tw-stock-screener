from PIL import Image
import os
import io

source_path = r"d:\Antigravity\tw-stock-screener\frontend\icons\icon-512.png"
output_dir = os.path.dirname(source_path)
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

def remove_background_simple(img):
    print("Applying simple threshold algorithm...")
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    
    # 計算並列印一些統計，以幫助除錯
    white_pixels = 0
    total_pixels = 0
    
    for item in datas:
        total_pixels += 1
        # 閾值判定：如果非常接近白色 (250+)，則變透明
        # 同時也處理接近白色的灰色邊緣
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
             new_data.append((255, 255, 255, 0))
             white_pixels += 1
        else:
             new_data.append(item)
    
    img.putdata(new_data)
    print(f"Processed {total_pixels} pixels, removed {white_pixels} white pixels.")
    return img

img_transparent = None

try:
    from rembg import remove
    print("Using rembg for high-quality background removal...")
    with open(source_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)
        img_transparent = Image.open(io.BytesIO(output_data))
except ImportError:
    print("rembg module not found, falling back to simple method.")
    img = Image.open(source_path)
    img_transparent = remove_background_simple(img)
except Exception as e:
    print(f"Error using rembg: {e}. Falling back to simple method.")
    img = Image.open(source_path)
    img_transparent = remove_background_simple(img)

if img_transparent:
    # 確保是 RGBA
    img_transparent = img_transparent.convert("RGBA")
    
    # 存檔備份
    # img_transparent.save(os.path.join(output_dir, "icon-512-transparent-source.png"))
    
    # 因為去背後原本的圖案可能也是紫色，我們不需要改變顏色，只需要 resize
    
    # 1. 生成所有 PWA icons (透明背景)
    for size in sizes:
        resized_img = img_transparent.resize((size, size), Image.Resampling.LANCZOS)
        filename = f"icon-{size}.png"
        resized_img.save(os.path.join(output_dir, filename))
        print(f"Generated {filename}")

    # 2. 生成 iOS 專用 icon (深色背景)
    # 使用 App 主題色 #1a1a2e 作為背景
    ios_size = 180
    bg_color = (26, 26, 46) # #1a1a2e
    ios_icon = Image.new("RGB", (ios_size, ios_size), bg_color)

    # 為了美觀，將圖示縮小一點置中 (80%)
    padding = int(ios_size * 0.15)
    inner_size = ios_size - (padding * 2)
    
    resized_inner = img_transparent.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    
    # 貼上圖示 (使用 alpha channel 作為 mask)
    ios_icon.paste(resized_inner, (padding, padding), resized_inner)
    
    ios_icon.save(os.path.join(output_dir, "apple-touch-icon.png"))
    print("Generated apple-touch-icon.png with theme background")

print("Icon set updated successfully.")
