import random
from pathlib import Path
import json

# 風格定義
STYLES = {
    '簡約風': {
        'description': '簡單俐落的設計，注重材質與剪裁',
        'colors': ['黑色', '白色', '灰色', '米色'],
        'keywords': ['極簡', '俐落', '質感'],
        'images': {
            '穿搭示範': 'style_images/2376ee5939108504fcd0447f77b69c78.jpg',
            '配色參考': 'style_images/24ca12d5930e029749a5feab88a67dd9.jpg',
            '單品推薦': 'style_images/3958c2d9505bd9d245173f87195fb9a3.jpg'
        }
    },
    '韓系風': {
        'description': '清新可愛的韓式穿搭，強調層次感',
        'colors': ['粉色', '淺藍', '奶油色', '淺卡其'],
        'keywords': ['甜美', '清新', '疊穿'],
        'images': {
            '穿搭示範': 'style_images/907d90300aeb7d5588537059d4b9fd91.jpg',
            '配色參考': 'style_images/ecdcb6503dc3523211ae7f53cbf9d566.jpg',
            '單品推薦': 'style_images/2376ee5939108504fcd0447f77b69c78.jpg'
        }
    },
    '文青風': {
        'description': '文藝復古的氣質搭配，強調個人特色',
        'colors': ['深藍', '咖啡色', '墨綠', '酒紅'],
        'keywords': ['復古', '文藝', '質感'],
        'images': {
            '穿搭示範': 'style_images/24ca12d5930e029749a5feab88a67dd9.jpg',
            '配色參考': 'style_images/3958c2d9505bd9d245173f87195fb9a3.jpg',
            '單品推薦': 'style_images/907d90300aeb7d5588537059d4b9fd91.jpg'
        }
    },
    '街頭風': {
        'description': '充滿活力的街頭風格，展現個性魅力',
        'colors': ['黑色', '白色', '紅色', '藍色'],
        'keywords': ['潮流', '運動', '個性'],
        'images': {
            '穿搭示範': 'style_images/ecdcb6503dc3523211ae7f53cbf9d566.jpg',
            '配色參考': 'style_images/2376ee5939108504fcd0447f77b69c78.jpg',
            '單品推薦': 'style_images/24ca12d5930e029749a5feab88a67dd9.jpg'
        }
    },
    '日系風': {
        'description': '溫柔細膩的日式搭配，注重細節與整體感',
        'colors': ['米白', '淺灰', '淺咖啡', '杏色'],
        'keywords': ['溫柔', '細膩', '自然'],
        'images': {
            '穿搭示範': 'style_images/3958c2d9505bd9d245173f87195fb9a3.jpg',
            '配色參考': 'style_images/907d90300aeb7d5588537059d4b9fd91.jpg',
            '單品推薦': 'style_images/ecdcb6503dc3523211ae7f53cbf9d566.jpg'
        }
    }
}

# 色系搭配建議
COLOR_COMBINATIONS = {
    '黑白灰': {
        'main_colors': ['黑色', '白色', '灰色'],
        'accent_colors': ['紅色', '藍色', '黃色'],
        'description': '經典永不過時的搭配',
        'images': {
            '搭配示範': 'color_images/2b318e6ee7e48fcf7b5dbd6e25f991fd.jpg',
            '色票參考': 'color_images/2b59887768e9bc758a61c64e3291894e.jpg'
        }
    },
    '溫暖系': {
        'main_colors': ['卡其色', '棕色', '米色'],
        'accent_colors': ['墨綠', '酒紅', '深藍'],
        'description': '溫暖柔和的大地色系',
        'images': {
            '搭配示範': 'color_images/5df0590115c7a6e909e8d3f18bdca977.jpg',
            '色票參考': 'color_images/728aa28ecfca6e4c9d33aa4bcfb8ac3b.jpg'
        }
    },
    '清新系': {
        'main_colors': ['白色', '淺藍', '粉色'],
        'accent_colors': ['淺灰', '淺紫', '薄荷綠'],
        'description': '清新淡雅的柔和色系',
        'images': {
            '搭配示範': 'color_images/d5280e5e748a5e4fef85278a53529364.jpg',
            '色票參考': 'color_images/2b318e6ee7e48fcf7b5dbd6e25f991fd.jpg'
        }
    },
    '活力系': {
        'main_colors': ['藍色', '紅色', '黃色'],
        'accent_colors': ['白色', '灰色', '黑色'],
        'description': '充滿活力的明亮色系',
        'images': {
            '搭配示範': 'color_images/2b59887768e9bc758a61c64e3291894e.jpg',
            '色票參考': 'color_images/5df0590115c7a6e909e8d3f18bdca977.jpg'
        }
    }
}

def load_labels(label_file='model/labels.txt'):
    try:
        with open(label_file, 'r', encoding='utf-8') as f:
            # 讀取每一行並處理，格式應該是 "索引 類別名稱"
            labels = {}
            for line in f:
                idx, label = line.strip().split(' ', 1)
                labels[int(idx)] = label
            return [labels[i] for i in range(len(labels))]
    except Exception as e:
        print(f"無法讀取標籤文件：{str(e)}")
        return ['Class 1', 'Class 2']  # 預設標籤

LABELS = load_labels()

class FashionModel:
    def __init__(self):
        self.labels = LABELS
        print("測試模式已啟動！")
        
    def predict(self, img_path):
        """
        預測圖片中的配件（測試模式）
        """
        try:
            # 檢查圖片是否存在
            if not Path(img_path).is_file(): 
                raise FileNotFoundError("找不到圖片檔案")
            
            # 測試模式：隨機返回結果
            predicted_class = random.randint(0, len(self.labels)-1)
            confidence = random.uniform(0.7, 0.9)
            return self.labels[predicted_class], confidence
        except Exception as e:
            print(f"預測時發生錯誤：{str(e)}")
            return "未知", 0.0

# 搭配建議規則
FASHION_ITEMS = {
    '帽子': {
        'high': '完美的帽子選擇！建議搭配：\n' + 
                '1. 棉質帽子搭配白襯衫與牛仔外套\n' + 
                '2. 草編帽配棉麻襯衫與淺色寬褲，營造夏日感\n' + 
                '3. 毛呢帽搭配長版風衣與靴子，展現時髦感',
        'medium': '不錯的帽子搭配！建議：\n' + 
                 '1. 棒球帽與運動風上衣結合，打造街頭風格\n' + 
                 '2. 毛帽搭配毛衣與靴子，適合文青風格穿搭\n' + 
                 '3. 牛仔帽搭配格紋襯衫，展現休閒風格',
        'low': '基本帽子搭配建議：\n' + 
               '1. 簡約素色帽搭配基本款T恤\n' + 
               '2. 選擇百搭色系增加實用性\n' + 
               '3. 注意帽子與整體造型的協調性'
    },
    '眼鏡': {
        'high': '絕佳的眼鏡款式！推薦搭配：\n' + 
                '1. 金屬鏡框配針織衫與深色牛仔褲\n' + 
                '2. 塑膠框眼鏡搭配寬鬆毛衣與格紋褲，展現學院風\n' + 
                '3. 透明鏡框配風衣與高領毛衣，時尚有型',
        'medium': '很棒的眼鏡選擇！建議：\n' + 
                 '1. 復古圓框鏡搭配高腰褲與格紋襯衫\n' + 
                 '2. 粗框眼鏡配針織外套，營造知性風格\n' + 
                 '3. 嘗試搭配簡約配件突出眼鏡特色',
        'low': '基本眼鏡搭配建議：\n' + 
               '1. 選擇適合臉型的鏡框款式\n' + 
               '2. 搭配簡約服飾不搶戲\n' + 
               '3. 注意整體色調的協調'
    },
    '手錶': {
        'high': '優質的手錶選擇！建議搭配：\n' + 
                '1. 皮錶帶適合西裝或襯衫等正式場合\n' + 
                '2. 矽膠錶帶搭配運動風連帽上衣與慢跑褲\n' + 
                '3. 金屬錶帶配襯衫與針織背心，展現日系簡約',
        'medium': '不錯的手錶款式！推薦：\n' + 
                 '1. 木質手錶搭配自然風麻紗與大地色系\n' + 
                 '2. 時尚錶款配西裝外套提升質感\n' + 
                 '3. 運動錶搭配休閒運動風格',
        'low': '基本手錶搭配建議：\n' + 
               '1. 選擇百搭款式增加實用性\n' + 
               '2. 注意錶帶材質與服裝質地搭配\n' + 
               '3. 考慮場合選擇合適款式'
    },
    '裙子': {
        'high': '完美的裙裝選擇！推薦搭配：\n' + 
                '1. 棉質裙搭配短版上衣展現腰身比例\n' + 
                '2. 牛仔裙配襯衫與簡約小白鞋\n' + 
                '3. 紗裙與針織罩衫一同穿著，柔和有層次',
        'medium': '很好的裙子款式！建議：\n' + 
                 '1. 格紋裙配針織毛衣營造學院風格\n' + 
                 '2. 百摺裙與簡約素T，打造極簡時尚\n' + 
                 '3. A字裙搭配貼身上衣突顯曲線',
        'low': '基本裙裝搭配建議：\n' + 
               '1. 選擇適合身形的裙長\n' + 
               '2. 注意上下身比例協調\n' + 
               '3. 配件搭配提升整體造型'
    },
    '上衣': {
        'high': '出色的上衣選擇！推薦搭配：\n' + 
                '1. 棉T搭配高腰褲能延伸腿部比例\n' + 
                '2. 雪紡材質搭配層次感馬甲背心\n' + 
                '3. 針織上衣混搭飾品提升質感',
        'medium': '不錯的上衣款式！建議：\n' + 
                 '1. 寬鬆襯衫與窄裙組合營造韓系簡約風\n' + 
                 '2. 格紋襯衫加吊帶褲打造可愛學院風\n' + 
                 '3. 素色上衣搭配特色長褲或裙子',
        'low': '基本上衣搭配建議：\n' + 
               '1. 選擇適合場合的材質款式\n' + 
               '2. 注意整體搭配的平衡\n' + 
               '3. 可搭配配件增添風格'
    },
    '外套': {
        'high': '完美的外套選擇！建議搭配：\n' + 
                '1. 西裝外套配素色高領內搭與修身褲款\n' + 
                '2. 牛仔外套搭配寬褲與靴子營造大人感\n' + 
                '3. 毛呢外套配帽子與絲巾創造層次感',
        'medium': '很棒的外套款式！推薦：\n' + 
                 '1. 皮衣外套與黑褲、老爹鞋適合街頭風\n' + 
                 '2. 針織外套搭配連身裙增添優雅感\n' + 
                 '3. 風衣搭配高領毛衣展現質感',
        'low': '基本外套搭配建議：\n' + 
               '1. 選擇百搭款式與顏色\n' + 
               '2. 注意整體搭配的溫度層次\n' + 
               '3. 配件搭配提升造型完整度'
    },
    '耳環': {
        'high': '優雅的耳環選擇！推薦搭配：\n' + 
                '1. 金屬耳環配綁髮造型讓耳環更突出\n' + 
                '2. 珍珠耳環搭配露肩上衣，增添柔美感\n' + 
                '3. 壓克力耳環配細鏈項鍊更顯精緻',
        'medium': '不錯的耳環款式！建議：\n' + 
                 '1. 圈型耳環搭配休閒牛仔展現俐落感\n' + 
                 '2. 垂墜耳環配合簡約髮型\n' + 
                 '3. 小巧耳釘搭配正式造型',
        'low': '基本耳環搭配建議：\n' + 
               '1. 選擇適合場合的款式\n' + 
               '2. 注意與其他飾品的搭配\n' + 
               '3. 考慮整體造型的平衡'
    },
    '項鍊': {
        'high': '完美的項鍊選擇！推薦搭配：\n' + 
                '1. 金屬項鍊配V領上衣拉長頸部線條\n' + 
                '2. 簡約T恤搭配天然石項鍊增添亮點\n' + 
                '3. 疊戴不同長度細鏈增加層次感',
        'medium': '很棒的項鍊款式！建議：\n' + 
                 '1. 鎖骨鍊搭配露肩毛衣展現法式氣質\n' + 
                 '2. 珍珠項鍊配襯衫增添優雅感\n' + 
                 '3. 短版項鍊搭配圓領上衣',
        'low': '基本項鍊搭配建議：\n' + 
               '1. 選擇適合衣領的長度\n' + 
               '2. 注意與其他飾品的協調\n' + 
               '3. 配合場合選擇合適款式'
    }
}

def get_style_recommendation():
    """
    隨機生成風格搭配建議
    """
    style = random.choice(list(STYLES.keys()))
    color_scheme = random.choice(list(COLOR_COMBINATIONS.keys()))
    
    style_info = STYLES[style]
    color_info = COLOR_COMBINATIONS[color_scheme]
    
    recommendation = {
        '風格': style,
        '風格描述': style_info['description'],
        '主要色系': color_scheme,
        '主色調': color_info['main_colors'],
        '點綴色': color_info['accent_colors'],
        '風格關鍵字': style_info['keywords'],
        '建議單品': [],  # 將根據不同風格添加具體單品
        '圖片參考': {
            **style_info['images'],
            **color_info['images']
        }
    }
    
    return recommendation

def get_recommendation(label, confidence):
    """
    根據預測結果和信心度返回搭配建議，並加入風格推薦
    """
    if confidence >= 0.7:
        level = 'high'
    elif confidence >= 0.4:
        level = 'medium'
    else:
        level = 'low'

    basic_recommendation = FASHION_ITEMS.get(label, {}).get(level, '無特定搭配建議')
    style_recommendation = get_style_recommendation()
    
    return {
        'basic': basic_recommendation,
        'style': style_recommendation
    }
