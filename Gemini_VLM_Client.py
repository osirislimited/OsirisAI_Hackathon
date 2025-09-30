import os
import base64
import google.generativeai as genai
from PIL import Image

class GeminiVLMClient:
    """Gemini VLM client for agricultural analysis"""
    
    def __init__(self):
        # *** CHANGE GEMINI API KEY HERE ***
        genai.configure(api_key=os.environ.get("AIzaSyDA-xVqq5eZ9u8kIkbaXDnFuXC6JxtBIhQ", ""))
        # *** CHANGE GEMINI MODEL HERE ***
        self.model = genai.GenerativeModel('gemini-1.5-pro-vision-latest')
        
    def analyze_crop_image(self, image_path, query, language="zh"):
        """Analyze crop image using Gemini VLM"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Create agricultural prompt (always in Cantonese)
            system_prompt = """你是專業農業顧問。分析農作物圖片並提供：
1. 作物健康診斷
2. 病蟲害識別  
3. 具體建議
4. 信心度評估
用繁體中文回答。"""
            
            full_prompt = f"{system_prompt}\n\n用戶問題: {query}"
            
            # Generate response
            response = self.model.generate_content([full_prompt, image])
            
            result = self._parse_response(response.text, query, language)
            
            return result, "分析成功"
            
        except Exception as e:
            return None, f"Gemini分析失敗: {str(e)}"
    
    def _parse_response(self, response, query, language):
        """Parse Gemini response"""
        # Extract diagnosis in Cantonese
        diagnosis = "分析完成"
        if any(word in response for word in ["健康", "正常", "良好"]):
            diagnosis = "作物健康狀況良好"
        elif any(word in response for word in ["病", "蟲害", "問題"]):
            diagnosis = "發現問題 - 請查看建議"
        
        # Extract recommendations
        recommendations = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if any(line.startswith(p) for p in ['1.', '2.', '3.', '-', '•']):
                clean_rec = line.lstrip('123456789.-• ').strip()
                if len(clean_rec) > 5:
                    recommendations.append(clean_rec)
        
        if not recommendations:
            recommendations = [
                "定期監察植物健康狀況",
                "確保適當的澆水時間表", 
                "檢查害蟲活動"
            ]
        
        return {
            'diagnosis': diagnosis,
            'confidence': 0.85,
            'recommendations': recommendations[:5],
            'raw_response': response,
            'query': query,
            'language': 'zh',
            'model': 'gemini-1.5-pro-vision'
        }

# Global client instance
gemini_vlm_client = GeminiVLMClient()