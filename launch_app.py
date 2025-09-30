#!/usr/bin/env python3
"""
Quick launcher for Osiris.AI Mobile with Traditional Chinese UI
"""

import sys
import os

def main():
    """Launch the application"""
    print("啟動 Osiris.AI 智慧農業助手...")
    print("Starting Osiris.AI Smart Agriculture Assistant...")
    
    try:
        # Import and run the application
        from OsirisAI_Mobile import main as app_main
        app_main()
        
    except ImportError as e:
        print(f"導入錯誤 Import Error: {e}")
        print("請確保所有依賴項已安裝 Please ensure all dependencies are installed")
        input("按 Enter 退出 Press Enter to exit...")
        
    except Exception as e:
        print(f"應用程式錯誤 Application Error: {e}")
        input("按 Enter 退出 Press Enter to exit...")

if __name__ == "__main__":
    main()