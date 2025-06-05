from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image(filename, text, bg_color, text_color=(255, 255, 255)):
    # 創建一個 400x400 的圖片
    img = Image.new('RGB', (400, 400), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 添加文字
    text_position = (200, 200)
    draw.text(text_position, text, fill=text_color, anchor="mm")
    
    # 保存圖片
    img.save(filename)

def main():
    # 確保目錄存在
    style_dir = 'static/style_images'
    color_dir = 'static/color_images'
    os.makedirs(style_dir, exist_ok=True)
    os.makedirs(color_dir, exist_ok=True)
    
    # 風格示意圖
    style_images = {
        'minimal': ((200, 200, 200), '簡約風格'),
        'korean': ((255, 182, 193), '韓系風格'),
        'vintage': ((139, 69, 19), '文青風格'),
        'street': ((0, 0, 0), '街頭風格'),
        'japanese': ((255, 240, 220), '日系風格')
    }
    
    # 配色示意圖
    color_images = {
        'bw': ((0, 0, 0), '黑白灰系'),
        'warm': ((210, 180, 140), '溫暖系'),
        'fresh': ((173, 216, 230), '清新系'),
        'vibrant': ((255, 0, 0), '活力系')
    }
    
    # 生成風格圖片
    for style, (color, text) in style_images.items():
        for img_type in ['style', 'colors', 'items']:
            filename = os.path.join(style_dir, f'{style}_{img_type}.jpg')
            create_sample_image(filename, f'{text}\n{img_type}', color)
    
    # 生成配色圖片
    for scheme, (color, text) in color_images.items():
        for img_type in ['style', 'palette']:
            filename = os.path.join(color_dir, f'{scheme}_{img_type}.jpg')
            create_sample_image(filename, f'{text}\n{img_type}', color)

if __name__ == '__main__':
    main()
    print("示例圖片已生成完成！")
