#!/usr/bin/env python3
"""
Test script for Osiris.AI Mobile
Tests individual components before full deployment
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image
import tempfile

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5")
    except ImportError as e:
        print(f"❌ PyQt5: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI")
    except ImportError as e:
        print(f"❌ Google Generative AI: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✅ Speech Recognition")
    except ImportError as e:
        print(f"❌ Speech Recognition: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3")
    except ImportError as e:
        print(f"❌ pyttsx3: {e}")
        return False
    
    return True

def test_camera():
    """Test camera functionality"""
    print("\nTesting camera...")
    
    try:
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("⚠️ Camera not available (this is OK if no camera is connected)")
            return True
        
        ret, frame = camera.read()
        if ret:
            print("✅ Camera capture successful")
            print(f"   Frame shape: {frame.shape}")
        else:
            print("❌ Camera capture failed")
            return False
        
        camera.release()
        return True
        
    except Exception as e:
        print(f"❌ Camera test error: {e}")
        return False

def test_voice_system():
    """Test voice system initialization"""
    print("\nTesting voice system...")
    
    try:
        import speech_recognition as sr
        import pyttsx3
        
        # Test speech recognition
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print("✅ Speech recognition initialized")
        
        # Test TTS
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)
        tts_engine.setProperty('volume', 0.9)
        print("✅ Text-to-speech initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice system test error: {e}")
        return False

def test_gemini_api():
    """Test Gemini API configuration"""
    print("\nTesting Gemini API...")
    
    try:
        from config import config
        import google.generativeai as genai
        
        if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠️ Gemini API key not configured")
            print("   Edit config.py to set your API key")
            return True  # Not a failure, just not configured
        
        # Try to configure (but don't make actual API calls in test)
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        print("✅ Gemini API configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test error: {e}")
        return False

def test_image_processing():
    """Test image processing functionality"""
    print("\nTesting image processing...")
    
    try:
        # Create a test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        test_image[:, :] = [0, 128, 0]  # Green background
        
        # Add some shapes to simulate a crop
        cv2.rectangle(test_image, (100, 100), (200, 200), (0, 255, 0), -1)
        cv2.circle(test_image, (400, 300), 50, (0, 255, 255), -1)
        
        # Test OpenCV operations
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        print("✅ OpenCV color conversion")
        
        # Test PIL operations
        pil_image = Image.fromarray(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        print("✅ PIL image conversion")
        
        # Test saving/loading
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            cv2.imwrite(tmp.name, test_image)
            loaded_image = cv2.imread(tmp.name)
            
            if loaded_image is not None:
                print("✅ Image save/load")
            else:
                print("❌ Image save/load failed")
                return False
            
            os.unlink(tmp.name)
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing test error: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    
    try:
        from config import config
        
        # Test config attributes
        assert hasattr(config, 'GEMINI_API_KEY')
        assert hasattr(config, 'APP_NAME')
        assert hasattr(config, 'GEMINI_MODEL')
        print("✅ Configuration attributes")
        
        # Test validation
        issues = config.validate_config()
        if issues:
            print(f"⚠️ Configuration issues: {len(issues)}")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("✅ Configuration validation")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def test_gui_creation():
    """Test GUI creation without showing it"""
    print("\nTesting GUI creation...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test basic widget creation
        from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
        
        window = QMainWindow()
        label = QLabel("Test")
        button = QPushButton("Test Button")
        
        print("✅ Basic GUI components")
        
        # Don't show the window, just test creation
        return True
        
    except Exception as e:
        print(f"❌ GUI creation test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Osiris.AI Mobile - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Camera", test_camera),
        ("Voice System", test_voice_system),
        ("Gemini API", test_gemini_api),
        ("Image Processing", test_image_processing),
        ("Configuration", test_config),
        ("GUI Creation", test_gui_creation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed! Ready to launch Osiris.AI Mobile")
        return True
    else:
        print("Some tests failed. Check the issues above before launching.")
        return False

def main():
    """Main test function"""
    success = run_all_tests()
    
    if success:
        print("\nRun 'py run_osiris_ai_mobile.py' to launch the application")
    else:
        print("\nFix the issues above and run tests again")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()