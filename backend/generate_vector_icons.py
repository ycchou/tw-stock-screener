from PIL import Image, ImageDraw

def create_icon():
    # 建立 1024x1024 的高解析度畫布
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 定義紫色系顏色 (參照 CSS 變數)
    # Primary Accent: #6366f1 (Indigo)
    # Secondary Accent: #8b5cf6 (Violet)
    
    # 我們使用漸層色的概念，給予不同的 K 線不同深淺
    color_wicks = (139, 92, 246, 255) # 燭芯統用紫色
    
    # Candle 1 (左，陰線/回檔感 -> 深一點)
    color_body_1 = (124, 58, 237, 255) 
    
    # Candle 2 (中，主升段 -> 亮紫色)
    color_body_2 = (139, 92, 246, 255)
    
    # Candle 3 (右，高檔整理 -> 另一種紫)
    color_body_3 = (167, 139, 250, 255) # 較亮
    
    # 畫燭芯 (寬度 32px)
    wick_width = 30
    
    # Candle 1 (左)
    # Wick: 200 -> 800
    draw.line([(256, 250), (256, 850)], fill=color_wicks, width=wick_width)
    # Body: 400 -> 700 (實體)
    draw.rounded_rectangle([(180, 450), (332, 700)], radius=30, fill=color_body_1)
    
    # Candle 2 (中，最高)
    # Wick: 100 -> 800
    draw.line([(512, 100), (512, 850)], fill=color_wicks, width=wick_width)
    # Body: 250 -> 650
    draw.rounded_rectangle([(436, 250), (588, 650)], radius=30, fill=color_body_2)
    
    # Candle 3 (右)
    # Wick: 300 -> 700
    draw.line([(768, 300), (768, 750)], fill=color_wicks, width=wick_width)
    # Body: 350 -> 550
    draw.rounded_rectangle([(692, 350), (844, 550)], radius=30, fill=color_body_3)
    
    return img

if __name__ == '__main__':
    import os
    
    base_dir = r"d:\Antigravity\tw-stock-screener\frontend\icons"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    print("Generating new vector icons...")
    img = create_icon()
    
    # 生成各尺寸 PWA Icons (透明背景)
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(base_dir, f"icon-{s}.png"))
        print(f"Generated icon-{s}.png")
        
    # 生成 iOS Icon (深色背景)
    ios_size = 180
    bg_color = (26, 26, 46) # #1a1a2e 背景
    ios_img = Image.new('RGB', (ios_size, ios_size), bg_color)
    
    # 內縮 15% padding 讓圖示居中
    padding = int(ios_size * 0.15)
    inner_size = ios_size - (padding * 2)
    resized_inner = img.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    
    ios_img.paste(resized_inner, (padding, padding), resized_inner)
    ios_img.save(os.path.join(base_dir, "apple-touch-icon.png"))
    print("Generated apple-touch-icon.png")
