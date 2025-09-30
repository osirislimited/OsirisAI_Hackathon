# Osiris.AI Mobile - Smart Agriculture Assistant

A mobile-style PyQt5 application powered by Google Gemini Vision-Language Model for agricultural analysis and recommendations.

## 🌱 What It Does

Osiris.AI delivers Best Management Practices (BMP) to farmers through:
- **Image Analysis**: Capture or upload crop photos for AI-powered health assessment
- **Voice Queries**: Ask questions in Cantonese or English using voice input
- **AI Diagnosis**: Get research-backed solutions for plant health and soil issues
- **Voice Guidance**: Hear recommendations spoken back to you
- **Data Logging**: Save analysis results for future reference

## 🚀 Features

### Core Capabilities
- **📸 Image Capture**: Use camera or load images from files
- **🎤 Voice Recognition**: Cantonese and English voice input
- **🤖 AI Analysis**: Powered by Google Gemini 1.5 Pro Vision
- **🔊 Text-to-Speech**: Hear analysis results spoken aloud
- **💾 Data Export**: Save analysis results as JSON files
- **📱 Mobile UI**: Clean, mobile-app-style interface

### Technical Features
- Real-time camera integration with OpenCV
- Google Speech Recognition for voice input
- Gemini VLM for crop health analysis
- PyQt5 modern GUI with responsive design
- Comprehensive error handling and validation

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10/11, macOS, or Linux
- **Camera**: Optional (for image capture)
- **Microphone**: Optional (for voice input)
- **Internet**: Required for AI analysis and voice recognition

### API Keys Required
- **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Installation

### Step 1: Clone/Download Project
```bash
git clone <repository-url>
cd Project_Osiris
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys
1. Edit `config.py` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key
2. Or create a `.env` file with:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Step 4: Test Installation
```bash
python test_osiris_mobile.py
```

### Step 5: Launch Application
```bash
python run_osiris_ai_mobile.py
```

## 🎯 Usage Guide

### Getting Started
1. **Launch**: Run `python run_osiris_ai_mobile.py`
2. **Configure**: Set your Gemini API key in `config.py`
3. **Test**: Use the test script to verify everything works

### Using the Application

#### Image Analysis
1. **Capture Photo**: Click "📷 Capture" to take a photo with your camera
2. **Load Image**: Click "📁 Load Image" to select an existing photo
3. **Analyze**: Click "🔬 Analyze Crop" to get AI analysis

#### Voice Queries
1. **Record**: Click "🎤 Record" to start voice recording
2. **Speak**: Ask your question in Cantonese or English
3. **Stop**: Click "⏹️ Stop" when finished speaking
4. **Listen**: Click "🔊 Speak Result" to hear the analysis

#### Example Queries
- **Cantonese**: "我的白菜為什麼會枯萎？" (Why is my bok choy wilting?)
- **English**: "What's wrong with my tomato plants?"
- **English**: "How can I improve my crop yield?"

### Saving Results
- Click "💾 Save Analysis" to export results as JSON
- Files are saved in the `results/` directory
- Each analysis includes timestamp, query, and AI response

## 🔧 Configuration

### API Keys (config.py)
```python
# Required: Gemini API Key
GEMINI_API_KEY = "your_gemini_api_key_here"

# Optional: Google Speech API Key (uses free tier by default)
GOOGLE_SPEECH_API_KEY = "your_google_speech_api_key_here"
```

### Application Settings
```python
# Voice settings
VOICE_LANGUAGE_CANTONESE = "zh-HK"
VOICE_LANGUAGE_ENGLISH = "en-US"
TTS_RATE = 150
TTS_VOLUME = 0.9

# Camera settings
CAMERA_INDEX = 0

# Gemini model
GEMINI_MODEL = "gemini-1.5-pro-vision-latest"
```

## 🧪 Testing & Debugging

### Run Component Tests
```bash
python test_osiris_mobile.py
```

This tests:
- ✅ All required imports
- 📷 Camera functionality
- 🎤 Voice system
- 🤖 Gemini API configuration
- 🖼️ Image processing
- ⚙️ Configuration validation
- 🖥️ GUI creation

### Common Issues & Solutions

#### "Gemini API key not configured"
- Edit `config.py` and set your actual API key
- Get key from: https://makersuite.google.com/app/apikey

#### "Camera not available"
- Check camera connection and drivers
- Try different camera index in config (0, 1, 2...)
- Camera is optional - you can still load images from files

#### "Voice system initialization failed"
- Install PyAudio: `pip install pyaudio`
- On Windows, you might need: `pip install pipwin && pipwin install pyaudio`
- Voice is optional - you can type queries manually

#### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.7+)

## 📁 Project Structure

```
Project_Osiris/
├── OsirisAI_Mobile.py          # Main mobile application
├── config.py                   # Configuration and API keys
├── run_osiris_ai_mobile.py     # Launcher with dependency checking
├── test_osiris_mobile.py       # Component testing script
├── requirements.txt            # Python dependencies
├── README_Mobile.md           # This documentation
├── .env.example               # Environment variables template
├── results/                   # Saved analysis results
└── logs/                     # Application logs
```

## 🔄 Development Workflow

### For Developers
1. **Setup**: Install dependencies and configure API keys
2. **Test**: Run `python test_osiris_mobile.py` before changes
3. **Debug**: Check console output for detailed error messages
4. **Deploy**: Use `python run_osiris_ai_mobile.py` for production

### Adding Features
- **New AI Models**: Update `config.py` GEMINI_MODEL setting
- **UI Changes**: Modify `OsirisAI_Mobile.py` UI sections
- **Voice Languages**: Add language codes to config
- **Export Formats**: Extend `save_analysis()` method

## 🌍 Supported Languages

### Voice Recognition
- **Cantonese**: zh-HK
- **English**: en-US

### AI Analysis
- **Input**: Cantonese and English queries
- **Output**: Responds in the same language as the query

## 📊 Performance & Optimization

### Recommended Usage
- **Image Size**: Up to 10MB per image
- **Voice Recording**: 10 seconds maximum per query
- **Analysis Time**: 3-10 seconds depending on internet speed
- **Concurrent Users**: Single user per instance

### Resource Usage
- **RAM**: ~200MB base + image processing
- **CPU**: Low usage except during analysis
- **Network**: Required for AI analysis and voice recognition
- **Storage**: Minimal (analysis results only)

## 🔒 Privacy & Security

### Data Handling
- **Images**: Processed locally, sent to Gemini API for analysis
- **Voice**: Processed by Google Speech Recognition
- **Results**: Saved locally only
- **API Keys**: Stored in local config files

### Security Best Practices
- Keep API keys secure and don't share them
- Regularly update dependencies
- Use environment variables for sensitive data
- Review saved analysis files before sharing

## 🆘 Support & Troubleshooting

### Getting Help
1. **Run Tests**: `python test_osiris_mobile.py`
2. **Check Logs**: Look at console output for error details
3. **Verify Config**: Ensure API keys are correctly set
4. **Update Dependencies**: `pip install -r requirements.txt --upgrade`

### Known Limitations
- Requires internet connection for AI analysis
- Voice recognition accuracy varies with accent/pronunciation
- Camera support depends on system drivers
- Gemini API has usage limits (check Google's pricing)

## 📝 License

This project is developed for educational and research purposes in smart agriculture and machine learning applications.

## 🙏 Acknowledgments

- **Google Gemini**: AI vision and language model
- **PyQt5**: Cross-platform GUI framework
- **OpenCV**: Computer vision library
- **SpeechRecognition**: Voice input processing
- **pyttsx3**: Text-to-speech synthesis

---

**Ready to help farmers make data-driven decisions! 🌱🤖**