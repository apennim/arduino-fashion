from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import logging
import json
from model_utils import FashionModel, get_recommendation

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 設定上傳資料夾
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
STYLE_IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'style_images')
COLOR_IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'color_images')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 確保必要的目錄存在
for folder in [UPLOAD_FOLDER, STYLE_IMAGES_FOLDER, COLOR_IMAGES_FOLDER]:
    try:
        os.makedirs(folder, exist_ok=True)
        logger.info(f"目錄已確認：{folder}")
    except Exception as e:
        logger.error(f"創建目錄時發生錯誤：{str(e)}")

# 初始化模型
try:
    model = FashionModel()
    logger.info("模型初始化成功")
except Exception as e:
    logger.error(f"模型初始化失敗：{str(e)}")
    model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            logger.warning("沒有檔案被上傳")
            return render_template('index.html', error='請選擇一個檔案')
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("檔案名稱為空")
            return render_template('index.html', error='請選擇一個檔案')
            
        if file and allowed_file(file.filename):
            try:
                # 安全地保存檔案
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                logger.info(f"檔案已保存：{filepath}")
                
                # 檢查檔案是否確實被保存
                if not os.path.exists(filepath):
                    raise Exception("檔案未能成功保存")
                
                # 使用模型進行預測
                if model is not None:
                    label, confidence = model.predict(filepath)
                    logger.info(f"預測結果：{label}，信心度：{confidence}")
                    
                    # 獲取推薦
                    recommendations = get_recommendation(label, confidence)
                    
                    return render_template('index.html', 
                                        label=label,
                                        confidence=f"{confidence:.2%}",
                                        basic_recommendation=recommendations['basic'],
                                        style_recommendation=recommendations['style'],
                                        image=filename)
                else:
                    raise Exception("模型未正確初始化")
                    
            except Exception as e:
                logger.error(f"處理上傳檔案時發生錯誤：{str(e)}")
                return render_template('index.html', error=f'處理圖片時發生錯誤：{str(e)}')
        else:
            logger.warning(f"不支援的檔案類型：{file.filename}")
            return render_template('index.html', error='只支援 PNG、JPG、JPEG 和 GIF 格式的圖片')
    
    return render_template('index.html')

@app.after_request
def add_header(response):
    """
    防止瀏覽器快取靜態文件
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    # 顯示應用信息
    print('=== 時尚配件辨識系統 ===')
    print(f'上傳目錄: {UPLOAD_FOLDER}')
    print(f'風格圖片目錄: {STYLE_IMAGES_FOLDER}')
    print(f'配色圖片目錄: {COLOR_IMAGES_FOLDER}')
    print('支援的檔案類型:', ', '.join(ALLOWED_EXTENSIONS))
    print('正在啟動伺服器...')
    print('請訪問: http://localhost:5000')
    print('按 Ctrl+C 可以停止伺服器')
    print('========================')
    
    app.run(debug=True)
