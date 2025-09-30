#!/usr/bin/env python3
"""
Simple test script for Osiris.AI Mobile (Windows compatible)
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("OK: PyQt5")
    except ImportError as e:
        print(f"FAIL: PyQt5 - {e}")
        return False
    
    try:
        import cv2
        print("OK: OpenCV")
    except ImportError as e:
        print(f"FAIL: OpenCV - {e}")
        return False
    
    try:
        from PIL import Image
        print("OK: Pillow")
    except ImportError as e:
        print(f"FAIL: Pillow - {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("OK: Google Generative AI")
    except ImportError as e:
        print(f"FAIL: Google Generative AI - {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("OK: Speech Recognition")
    except ImportError as e:
        print(f"FAIL: Speech Recognition - {e}")
        return False
    
    try:
        import pyttsx3
        print("OK: pyttsx3")
    except ImportError as e:
        print(f"FAIL: pyttsx3 - {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import config
        print("OK: Configuration imported")
        
        if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("WARNING: Gemini API key not configured")
        else:
            print("OK: Gemini API key configured")
        
        return True
        
    except ImportError as e:
        print(f"FAIL: Configuration - {e}")
        return False

def test_camera():
    """Test camera"""
    print("\nTesting camera...")
    
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        
        if camera.isOpened():
            print("OK: Camera available")
            camera.release()
        else:
            print("WARNING: Camera not available (optional)")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Camera - {e}")
        return False

def main():
    """Main test function"""
    print("Osiris.AI Mobile - Simple Component Test")
    print("=" * 45)
    
    tests = [
        test_imports,
        test_config,
        test_camera,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"ERROR: Test crashed - {e}")
            failed += 1
    
    print("\n" + "=" * 45)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("SUCCESS: All tests passed!")
        print("Run: py run_osiris_ai_mobile.py")
    else:
        print("ISSUES: Some tests failed")
        print("Check dependencies and configuration")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()