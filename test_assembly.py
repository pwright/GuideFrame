#!/usr/bin/env python3
"""
Test script to debug GuideFrame assembly issues
"""

import os
import sys
import subprocess

def check_ffmpeg():
    """Check if FFmpeg is available and working"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ FFmpeg is available")
            # Print first line of version info
            version_line = result.stdout.split('\n')[0]
            print(f"  {version_line}")
            return True
        else:
            print("✗ FFmpeg returned error code")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg command timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        return False

def check_current_directory():
    """Check current directory and list relevant files"""
    print(f"\nCurrent working directory: {os.getcwd()}")
    
    # List all files
    print("\nAll files in current directory:")
    for item in sorted(os.listdir('.')):
        if os.path.isfile(item):
            size = os.path.getsize(item)
            print(f"  {item} ({size} bytes)")
        else:
            print(f"  {item}/ (directory)")
    
    # Check for expected step files
    print("\nChecking for expected step files:")
    step_files = []
    for i in range(1, 10):
        video_file = f"step{i}.mp4"
        audio_file = f"step{i}.mp3"
        if os.path.exists(video_file):
            size = os.path.getsize(video_file)
            print(f"  ✓ {video_file} ({size} bytes)")
            step_files.append(video_file)
        else:
            print(f"  ✗ {video_file} (not found)")
        
        if os.path.exists(audio_file):
            size = os.path.getsize(audio_file)
            print(f"  ✓ {audio_file} ({size} bytes)")
        else:
            print(f"  ✗ {audio_file} (not found)")
    
    return step_files

def test_ffmpeg_concat():
    """Test FFmpeg concat functionality with a simple test"""
    print("\nTesting FFmpeg concat functionality...")
    
    # Create a simple test file list
    test_list = "test_file_list.txt"
    test_output = "test_output.mp4"
    
    # Find any existing MP4 files to test with
    mp4_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    
    if len(mp4_files) < 2:
        print("  Need at least 2 MP4 files to test concat")
        return False
    
    # Use first two MP4 files for testing
    test_files = mp4_files[:2]
    print(f"  Testing with files: {test_files}")
    
    # Create test file list
    with open(test_list, 'w', encoding='utf-8') as f:
        for video_file in test_files:
            abs_path = os.path.abspath(video_file)
            f.write(f"file '{abs_path}'\n")
    
    # Show test file list contents
    print(f"  Test file list contents:")
    with open(test_list, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"    {line.strip()}")
    
    # Test FFmpeg concat
    try:
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', test_list, 
               '-c', 'copy', test_output, '-y']
        print(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("  ✓ FFmpeg concat test successful")
            if os.path.exists(test_output):
                size = os.path.getsize(test_output)
                print(f"  ✓ Test output created: {test_output} ({size} bytes)")
            return True
        else:
            print(f"  ✗ FFmpeg concat test failed")
            print(f"    Return code: {result.returncode}")
            if result.stderr:
                print(f"    Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error testing FFmpeg concat: {e}")
        return False
    finally:
        # Cleanup test files
        if os.path.exists(test_list):
            os.remove(test_list)
        if os.path.exists(test_output):
            os.remove(test_output)

def main():
    """Main test function"""
    print("GuideFrame Assembly Debug Test")
    print("=" * 40)
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("\nCannot proceed without FFmpeg")
        return
    
    # Check current directory
    step_files = check_current_directory()
    
    # Test FFmpeg concat
    test_ffmpeg_concat()
    
    print("\nDebug test complete!")
    print("\nRecommendations:")
    if not step_files:
        print("- No step video files found. Ensure you're in the correct directory.")
    else:
        print(f"- Found {len(step_files)} step video files.")
        print("- Try running the assembly process again with the improved error handling.")

if __name__ == "__main__":
    main() 