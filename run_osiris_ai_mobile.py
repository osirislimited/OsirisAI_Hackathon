#!/usr/bin/env python3
"""
Osiris.AI Mobile Launcher
Checks dependencies and launches the mobile-style application
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'PyQt5': 'PyQt5',
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
        'google.generativeai': 'google-generativeai',
        'speech_recognition': 'SpeechRecognition',
        'pyttsx3': 'pyttsx3',
        'numpy': 'numpy',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            if module_name == 'cv2':
                import cv2
            elif module_name == 'PIL':
                from PIL import Image
            elif module_name == 'google.generativeai':
                import google.generativeai
            elif module_name == 'speech_recognition':
                import speech_recognition
            elif module_name == 'pyttsx3':
                import pyttsx3
            elif module_name == 'numpy':
                import numpy
            elif module_name == 'PyQt5':
                from PyQt5.QtWidgets import QApplication
            elif module_name == 'dotenv':
                from dotenv import load_dotenv
            
            print(f"✅ {package_name}")
            
        except ImportError:
            print(f"❌ {package_name} - Not installed")
            missing_packages.append(package_name)
        except Exception as e:
            print(f"⚠️ {package_name} - Error: {e}")
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    
    try:
        for package in packages:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print(f"Error: {result.stderr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def check_config():
    """Check configuration file"""
    try:
        from config import config
        issues = config.validate_config()
        
        if issues:
            print("\n⚠️ Configuration Issues:")
            for issue in issues:
                print(f"  {issue}")
            print("\n📝 Please edit config.py to set your API keys")
            print("   Get Gemini API key from: https://makersuite.google.com/app/apikey")
            return False
        
        print("✅ Configuration validated")
        return True
        
    except ImportError:
        print("❌ config.py not found")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def create_env_file():
    """Create .env file template if it doesn't exist"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        env_template = '''# Osiris.AI Environment Variables
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Google Speech API Key
GOOGLE_SPEECH_API_KEY=your_google_speech_api_key_here
'''
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_template)
            print(f"✅ Created {env_file} template")
        except Exception as e:
            print(f"❌ Failed to create {env_file}: {e}")

def main():
    """Main launcher function"""
    print("🌱 Osiris.AI Mobile Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"\n❌ Missing {len(missing_packages)} package(s)")
        
        response = input("\nInstall missing packages? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if not install_dependencies(missing_packages):
                print("❌ Failed to install dependencies")
                input("Press Enter to exit...")
                return
        else:
            print("❌ Cannot run without required dependencies")
            input("Press Enter to exit...")
            return
    
    # Create .env file template
    create_env_file()
    
    # Check configuration
    print("\n🔧 Checking configuration...")
    if not check_config():
        print("\n⚠️ Configuration issues found. The app will still launch,")
        print("   but you'll need to configure your API keys for full functionality.")
        input("Press Enter to continue...")
    
    # Launch application
    print("\n🚀 Launching Osiris.AI Mobile...")
    try:
        from OsirisAI_Mobile import main as app_main
        app_main()
        
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        print("Make sure OsirisAI_Mobile.py is in the same directory")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()