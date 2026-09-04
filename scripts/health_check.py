#!/usr/bin/env python3
import sys
import platform
import subprocess
import importlib.util
import os
from pathlib import Path

def print_header(title):
    print(f"\n{'='*40}")
    print(f"{title}")
    print(f"{'='*40}")

def check_python():
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("✗ Warning: Python 3.9+ is recommended.")
        return False
    return True

def check_os():
    os_name = platform.system()
    arch = platform.machine()
    print(f"✓ Operating System: {os_name}")
    print(f"✓ CPU Architecture: {arch}")
    
    if os_name == "Darwin" and arch == "arm64":
        print("✓ Apple Silicon detected.")
    elif os_name == "Darwin":
        print("✗ Note: Running on Intel Mac. Some performance optimizations may differ.")
    return True

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg found: {version_line.split(' ')[2]}")
            return True
    except FileNotFoundError:
        pass
    print("✗ FFmpeg not found!")
    print("  Fix: Install FFmpeg using Homebrew:")
    print("  brew install ffmpeg")
    print("  Then run: ffmpeg -version")
    return False

def check_package(package_name, display_name=None):
    if display_name is None:
        display_name = package_name
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"✓ {display_name} installed")
        return True
    else:
        print(f"✗ {display_name} not found")
        print(f"  Fix: pip install {display_name}")
        return False

def check_env_vars():
    print_header("API Configuration")
    
    # Check .env file
    env_path = Path('.env')
    if env_path.exists():
        print("✓ .env file found")
    else:
        print("✗ .env file not found. Copy .env.example to .env")
    
    # Try to load if python-dotenv is installed
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
        
    hf = os.getenv('HUGGINGFACE_TOKEN')
    gemini = os.getenv('GEMINI_API_KEY')
    openai = os.getenv('OPENAI_API_KEY')
    
    if hf and len(hf) > 10:
        print("✓ Hugging Face token configured")
    else:
        print("✗ Hugging Face token NOT configured (Required for speaker diarization)")
        
    if gemini and len(gemini) > 10:
        print("✓ Gemini API configured")
    else:
        print("○ Gemini API NOT configured (Needed for AI Insights)")
        
    if openai and len(openai) > 10:
        print("✓ OpenAI API configured")
    else:
        print("○ OpenAI API NOT configured (Optional alternative to Gemini)")

def main():
    print_header("MeetIntel AI - System Health Check")
    
    status = True
    status &= check_python()
    status &= check_os()
    status &= check_ffmpeg()
    
    print("\nChecking Python Dependencies:")
    status &= check_package('streamlit')
    status &= check_package('faster_whisper', 'faster-whisper')
    status &= check_package('pyannote.audio', 'pyannote.audio')
    status &= check_package('torch', 'PyTorch')
    status &= check_package('jiwer')
    
    # Check libmagic specifically since it has OS dependencies
    try:
        import magic
        print("✓ libmagic installed and working")
    except ImportError as e:
        print(f"✗ libmagic error: {e}")
        print("  Fix: brew install libmagic")
        status = False
    
    check_env_vars()
    
    print_header("System Status")
    if status:
        print("System Status: READY - All critical dependencies met.")
    else:
        print("System Status: NEEDS ATTENTION - Please fix the issues marked with '✗' above.")

if __name__ == "__main__":
    main()
