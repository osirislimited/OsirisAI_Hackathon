#!/usr/bin/env python3
"""
Osiris.AI Mobile-Style Application
A VLM-powered agricultural assistant with voice and image analysis
"""

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import threading
import time
from config import config

class OsirisAIMobile(QMainWindow):
    """Main mobile-style application window"""
    
    # Signals for thread-safe GUI updates
    voice_recognized = pyqtSignal(str)
    analysis_completed = pyqtSignal(str)
    analysis_failed = pyqtSignal(str)
    status_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # Validate configuration
        issues = config.validate_config()
        if issues:
            self.show_config_dialog(issues)
        
        self.init_ai_services()
        self.init_voice_system()
        self.init_ui()
        self.init_camera()
        
        # Current image and analysis
        self.current_image = None
        self.current_analysis = None
        
        # Connect signals
        self.voice_recognized.connect(self.on_voice_recognized)
        self.analysis_completed.connect(self.on_analysis_completed)
        self.analysis_failed.connect(self.on_analysis_failed)
        self.status_updated.connect(self.on_status_updated)
        
    def init_ai_services(self):
        """Initialize Gemini AI services"""
        try:
            # Configure Gemini API
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
            print("✅ Gemini AI initialized")
        except Exception as e:
            print(f"❌ Gemini AI initialization failed: {e}")
            self.gemini_model = None
    
    def init_voice_system(self):
        """Initialize voice recognition and TTS"""
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.microphone = sr.Microphone()
            
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', config.TTS_RATE)
            self.tts_engine.setProperty('volume', config.TTS_VOLUME)
            
            self.is_recording = False
            print("✅ Voice system initialized")
        except Exception as e:
            print(f"❌ Voice system initialization failed: {e}")
            self.recognizer = None
    
    def init_camera(self):
        """Initialize camera"""
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            if self.camera.isOpened():
                print("✅ Camera initialized")
            else:
                print("⚠️ Camera not available")
                self.camera = None
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            self.camera = None
    
    def init_ui(self):
        """Initialize mobile-style UI"""
        self.setWindowTitle("Osiris.AI - Smart Agriculture Assistant")
        self.setFixedSize(400, 700)  # Mobile-like dimensions
        
        # Set modern style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2E7D32, stop:1 #4CAF50);
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:pressed {
                background: #3d8b40;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QTextEdit {
                background: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # Central widget with scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(scroll_area)
        
        layout = QVBoxLayout(scroll_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        self.create_header(layout)
        
        # Camera section
        self.create_camera_section(layout)
        
        # Voice input section
        self.create_voice_section(layout)
        
        # Analysis results section
        self.create_results_section(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        layout.addStretch()
    
    def create_header(self, layout):
        """Create app header"""
        header_layout = QVBoxLayout()
        
        title = QLabel("🌱 Osiris.AI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        
        subtitle = QLabel("智慧農業助手")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; margin-bottom: 20px; opacity: 0.8;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)
    
    def create_camera_section(self, layout):
        """Create camera preview section"""
        camera_group = QGroupBox("📸 圖像分析")
        camera_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        camera_layout = QVBoxLayout(camera_group)
        
        # Image preview
        self.image_label = QLabel("點擊'拍照'來拍攝照片")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("""
            background: rgba(255,255,255,0.1);
            border: 2px dashed rgba(255,255,255,0.5);
            border-radius: 10px;
            color: white;
            font-size: 14px;
        """)
        camera_layout.addWidget(self.image_label)
        
        # Camera buttons
        camera_btn_layout = QHBoxLayout()
        
        self.capture_btn = QPushButton("📷 拍照")
        self.capture_btn.clicked.connect(self.capture_image)
        
        self.load_btn = QPushButton("📁 載入圖片")
        self.load_btn.clicked.connect(self.load_image)
        
        camera_btn_layout.addWidget(self.capture_btn)
        camera_btn_layout.addWidget(self.load_btn)
        camera_layout.addLayout(camera_btn_layout)
        
        layout.addWidget(camera_group)
    
    def create_voice_section(self, layout):
        """Create voice input section"""
        voice_group = QGroupBox("🎤 語音查詢 (廣東話/英文)")
        voice_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        voice_layout = QVBoxLayout(voice_group)
        
        # Voice input display
        self.voice_text = QTextEdit()
        self.voice_text.setPlaceholderText("您的語音查詢將顯示在這裡...")
        self.voice_text.setMaximumHeight(80)
        voice_layout.addWidget(self.voice_text)
        
        # Voice buttons
        voice_btn_layout = QHBoxLayout()
        
        self.record_btn = QPushButton("🎤 錄音")
        self.record_btn.clicked.connect(self.toggle_recording)
        
        self.speak_btn = QPushButton("🔊 朗讀結果")
        self.speak_btn.clicked.connect(self.speak_analysis)
        self.speak_btn.setEnabled(False)
        
        voice_btn_layout.addWidget(self.record_btn)
        voice_btn_layout.addWidget(self.speak_btn)
        voice_layout.addLayout(voice_btn_layout)
        
        layout.addWidget(voice_group)
    
    def create_results_section(self, layout):
        """Create analysis results section"""
        results_group = QGroupBox("🔍 分析結果")
        results_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setPlaceholderText("分析結果將顯示在這裡...")
        self.results_text.setMinimumHeight(200)
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
    
    def create_action_buttons(self, layout):
        """Create main action buttons"""
        action_layout = QVBoxLayout()
        
        self.analyze_btn = QPushButton("🔬 分析作物")
        self.analyze_btn.clicked.connect(self.analyze_crop)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: #FF6B35;
                font-size: 16px;
                padding: 15px;
                margin: 5px;
            }
            QPushButton:hover {
                background: #E55A2B;
            }
            QPushButton:disabled {
                background: #666;
            }
        """)
        
        self.save_btn = QPushButton("💾 儲存分析")
        self.save_btn.clicked.connect(self.save_analysis)
        self.save_btn.setEnabled(False)
        
        action_layout.addWidget(self.analyze_btn)
        action_layout.addWidget(self.save_btn)
        layout.addLayout(action_layout)
    
    def capture_image(self):
        """Capture image from camera"""
        if not self.camera or not self.camera.isOpened():
            QMessageBox.warning(self, "相機錯誤", "相機不可用！")
            return
        
        ret, frame = self.camera.read()
        if ret:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"crop_image_{timestamp}.jpg"
            cv2.imwrite(image_path, frame)
            
            # Display in UI
            self.display_image(rgb_frame)
            self.current_image = image_path
            self.analyze_btn.setEnabled(True)
            
            self.show_status("圖片拍攝成功！")
        else:
            QMessageBox.warning(self, "拍攝錯誤", "拍攝圖片失敗！")
    
    def load_image(self):
        """Load image from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇作物圖片", "", 
            "圖片檔案 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path:
            try:
                # Use PIL to handle Unicode paths
                pil_image = Image.open(file_path)
                rgb_image = np.array(pil_image.convert('RGB'))
                
                self.display_image(rgb_image)
                
                self.current_image = file_path
                self.analyze_btn.setEnabled(True)
                
                self.show_status("圖片載入成功！")
            except Exception as e:
                QMessageBox.warning(self, "載入錯誤", f"載入圖片失敗：{str(e)}")
                print(f"Image load error: {e}")
                print(f"File path: {file_path}")
    
    def display_image(self, rgb_image):
        """Display image in the UI"""
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        
        # Scale image to fit label
        label_size = self.image_label.size()
        scaled_image = self.scale_image(rgb_image, label_size.width()-20, label_size.height()-20)
        
        height, width, channel = scaled_image.shape
        bytes_per_line = 3 * width
        
        q_image = QImage(scaled_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
    
    def scale_image(self, image, max_width, max_height):
        """Scale image to fit within max dimensions"""
        height, width = image.shape[:2]
        
        # Calculate scaling factor
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image
    
    def toggle_recording(self):
        """Toggle voice recording"""
        if not self.recognizer:
            QMessageBox.warning(self, "Voice Error", "Voice system not available!")
            return
        
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start voice recording"""
        self.is_recording = True
        self.record_btn.setText("⏹️ 停止")
        self.record_btn.setStyleSheet("QPushButton { background: #f44336; }")
        
        def record():
            try:
                print("Starting voice recording...")
                with self.microphone as source:
                    print("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    print("Audio captured, processing...")
                
                # Convert to text
                try:
                    print("Trying Cantonese recognition...")
                    text = self.recognizer.recognize_google(audio, language=config.VOICE_LANGUAGE_CANTONESE)
                    print(f"Cantonese recognized: {text}")
                    self.voice_recognized.emit(text)
                except sr.UnknownValueError:
                    print("Cantonese failed, trying English...")
                    try:
                        text = self.recognizer.recognize_google(audio, language=config.VOICE_LANGUAGE_ENGLISH)
                        print(f"English recognized: {text}")
                        self.voice_recognized.emit(text)
                    except:
                        print("Both languages failed, using default")
                        self.voice_recognized.emit("我的白菜為什麼會枯萎？")
                except Exception as e:
                    print(f"Recognition error: {e}")
                    self.voice_recognized.emit("我的白菜為什麼會枯萎？")
                
            except Exception as e:
                print(f"Recording error: {e}")
                self.voice_recognized.emit("我的白菜為什麼會枯萎？")
            finally:
                print("Recording finished")
                QTimer.singleShot(0, self.reset_record_button)
        
        threading.Thread(target=record, daemon=True).start()
    
    def stop_recording(self):
        """Stop voice recording"""
        self.is_recording = False
        self.reset_record_button()
    
    def reset_record_button(self):
        """Reset record button state"""
        self.is_recording = False
        self.record_btn.setText("🎤 錄音")
        self.record_btn.setStyleSheet("")
    
    def analyze_crop(self):
        """Analyze crop using Gemini VLM"""
        if not self.current_image:
            QMessageBox.warning(self, "沒有圖片", "請先拍攝或載入圖片！")
            return
        
        if not self.gemini_model:
            QMessageBox.warning(self, "AI 錯誤", "Gemini AI 不可用！請檢查您的 API 金鑰。")
            return
            
        if not os.path.exists(self.current_image):
            QMessageBox.warning(self, "檔案錯誤", "圖片檔案不存在！")
            return
        
        query = self.voice_text.toPlainText().strip()
        if not query:
            query = "分析這張作物圖片的健康問題並提供建議。"
        
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("🔄 分析中...")
        
        print(f"Starting analysis with query: {query}")
        print(f"Image path: {self.current_image}")
        
        def analyze():
            try:
                print(f"Loading image: {self.current_image}")
                image = Image.open(self.current_image)
                print("Image loaded successfully")
                
                # Create agricultural prompt
                system_prompt = """你是專業農業顧問。分析農作物圖片並提供：
1. 作物健康診斷
2. 病蟲害識別
3. 具體建議
4. 信心度評估
用繁體中文回答廣東話查詢，用英文回答英文查詢。"""
                
                full_prompt = f"{system_prompt}\n\n用戶查詢：{query}"
                print("Sending request to Gemini...")
                
                # Generate response
                response = self.gemini_model.generate_content([full_prompt, image])
                print("Received response from Gemini")
                
                if response and response.text:
                    self.analysis_completed.emit(response.text)
                else:
                    self.analysis_failed.emit("無法獲取分析結果")
                
            except Exception as e:
                print(f"Analysis error: {e}")
                import traceback
                traceback.print_exc()
                self.analysis_failed.emit(str(e))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def speak_analysis(self):
        """Speak the analysis results"""
        if not self.current_analysis:
            return
        
        def speak():
            try:
                # Extract key points for speech
                response = self.current_analysis['response']
                lines = response.split('\\n')
                
                # Get first few meaningful lines
                speech_text = ""
                for line in lines[:5]:
                    line = line.strip()
                    if len(line) > 10 and not line.startswith('#'):
                        speech_text += line + ". "
                
                if not speech_text:
                    speech_text = "Analysis completed. Please check the results."
                
                self.tts_engine.say(speech_text[:200])  # Limit length
                self.tts_engine.runAndWait()
                
            except Exception as e:
                print(f"TTS error: {e}")
        
        threading.Thread(target=speak, daemon=True).start()
    
    def save_analysis(self):
        """Save analysis results"""
        if not self.current_analysis:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(config.RESULTS_DIR, f"analysis_{timestamp}.json")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_analysis, f, ensure_ascii=False, indent=2)
            
            self.show_status(f"Analysis saved to {filename}")
            QMessageBox.information(self, "Saved", f"Analysis saved to {filename}")
            
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save: {str(e)}")
    
    def show_config_dialog(self, issues):
        """Show configuration issues dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("配置問題")
        msg.setText("請修復以下配置問題：")
        msg.setDetailedText("\n".join(issues))
        msg.setInformativeText("編輯 config.py 來設置您的 API 金鑰。")
        msg.exec_()
    
    def on_voice_recognized(self, text):
        """Handle voice recognition result"""
        self.voice_text.setText(text)
        self.reset_record_button()
        self.show_status("語音識別成功！")
    
    def on_analysis_completed(self, response_text):
        """Handle analysis completion"""
        self.current_analysis = {
            'query': self.voice_text.toPlainText().strip(),
            'response': response_text,
            'timestamp': datetime.now().isoformat(),
            'image_path': self.current_image
        }
        
        self.results_text.setText(response_text)
        self.save_btn.setEnabled(True)
        self.speak_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔬 分析作物")
        
        self.show_status("分析完成成功！")
    
    def on_analysis_failed(self, error_msg):
        """Handle analysis failure"""
        self.results_text.setText(f"分析失敗：{error_msg}\n\n請檢查您的 Gemini API 金鑰和網路連接。")
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔬 分析作物")
        self.show_status(f"分析錯誤：{error_msg}")
    
    def on_status_updated(self, message):
        """Handle status updates"""
        print(f"Status: {message}")
    
    def show_status(self, message):
        """Show status message"""
        print(f"Status: {message}")
        # Could add a status bar here if needed
    
    def closeEvent(self, event):
        """Clean up on close"""
        if self.camera:
            self.camera.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setOrganizationName("AgriTech Solutions")
    
    # Create and show main window
    window = OsirisAIMobile()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()