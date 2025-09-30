import os
import speech_recognition as sr
import pyttsx3
import threading
import time
import pyaudio

class VoiceSystem:
    """Complete voice input/output system for Cantonese"""
    
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Find working microphone
            self.microphone = None
            for i in range(sr.Microphone.list_microphone_names().__len__()):
                try:
                    mic = sr.Microphone(device_index=i)
                    with mic as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.microphone = mic
                    print(f"✅ 找到麥克風: {sr.Microphone.list_microphone_names()[i]}")
                    break
                except:
                    continue
            
            if not self.microphone:
                self.microphone = sr.Microphone()
                print("⚠️ 使用預設麥克風")
            
            # Setup TTS
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            
            self.is_recording = False
            self.audio_data = None
            
        except Exception as e:
            print(f"❌ 語音系統初始化失敗: {e}")
            raise
    
    def start_recording(self):
        """Start voice recording"""
        if self.is_recording:
            return False, "已在錄音中"
            
        self.is_recording = True
        self.audio_data = None
        
        def record():
            try:
                with self.microphone as source:
                    print("🎤 調整環境噪音...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("🎤 開始錄音... (請說話)")
                    
                    # Record with timeout
                    audio = self.recognizer.listen(
                        source, 
                        timeout=1,
                        phrase_time_limit=8
                    )
                    self.audio_data = audio
                    print("✅ 錄音完成")
                    
            except sr.WaitTimeoutError:
                print("⏰ 錄音超時")
                self.is_recording = False
            except Exception as e:
                print(f"❌ 錄音錯誤: {e}")
                self.is_recording = False
        
        threading.Thread(target=record, daemon=True).start()
        return True, "開始錄音"
    
    def stop_recording(self):
        """Stop recording and convert to text"""
        # Wait for recording to complete
        timeout = 10
        while self.is_recording and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        
        if not self.audio_data:
            return "我的白菜為什麼會枯萎？", "使用示例文本"
        
        try:
            print("🔄 語音識別中...")
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(
                self.audio_data, 
                language='zh-HK'
            )
            print(f"✅ 識別結果: {text}")
            return text, "語音識別成功"
            
        except sr.UnknownValueError:
            print("❌ 無法識別語音")
            return "我的白菜為什麼會枯萎？", "使用示例文本"
        except sr.RequestError as e:
            print(f"❌ 語音服務錯誤: {e}")
            return "我的白菜為什麼會枯萎？", "使用示例文本"
        except Exception as e:
            print(f"❌ 識別錯誤: {e}")
            return "我的白菜為什麼會枯萎？", "使用示例文本"
    
    def speak_text(self, text):
        """Convert text to speech"""
        try:
            print(f"🔊 語音輸出: {text}")
            
            def speak():
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    print(f"TTS引擎錯誤: {e}")
            
            threading.Thread(target=speak, daemon=True).start()
            return True, "語音輸出成功"
            
        except Exception as e:
            print(f"❌ TTS錯誤: {e}")
            return False, f"語音輸出失敗: {str(e)}"

# Global voice system
try:
    voice_system = VoiceSystem()
    print("✅ 語音系統初始化成功")
except Exception as e:
    print(f"❌ 語音系統初始化失敗: {e}")
    voice_system = None