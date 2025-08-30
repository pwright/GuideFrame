#!/usr/bin/env python3
"""
Test script to test GuideFrame assembly functions with test files
"""

import os
import sys
sys.path.append('.')

from guideframe.assembly import assemble_audio_video, combine_all_videos, assemble

def test_audio_video_combination():
    """Test combining audio and video files"""
    print("Testing audio/video combination...")
    
    # Create a simple test audio file
    os.system("ffmpeg -f lavfi -i sine=frequency=1000:duration=2 -y test_audio.mp3")
    
    # Test the function
    result = assemble_audio_video("test_video1.mp4", "test_audio.mp3", "test_output1.mp4")
    print(f"Audio/video combination result: {result}")
    
    if result and os.path.exists("test_output1.mp4"):
        print("✓ Audio/video combination successful")
        return True
    else:
        print("✗ Audio/video combination failed")
        return False

def test_video_concatenation():
    """Test concatenating multiple videos"""
    print("\nTesting video concatenation...")
    
    # Test with our test videos
    test_files = ["test_video1.mp4", "test_video2.mp4"]
    
    # Check if files exist
    for f in test_files:
        if not os.path.exists(f):
            print(f"✗ Test file {f} not found")
            return False
    
    result = combine_all_videos(test_files, "test_concatenated.mp4")
    print(f"Video concatenation result: {result}")
    
    if result and os.path.exists("test_concatenated.mp4"):
        print("✓ Video concatenation successful")
        return True
    else:
        print("✗ Video concatenation failed")
        return False

def test_full_assembly():
    """Test the full assembly process"""
    print("\nTesting full assembly process...")
    
    # Create step files for testing
    os.system("cp test_video1.mp4 step1.mp4")
    os.system("cp test_video2.mp4 step2.mp4")
    os.system("cp test_audio.mp3 step1.mp3")
    os.system("cp test_audio.mp3 step2.mp3")
    
    # Test assembly with 2 steps
    result = assemble(2)
    print(f"Full assembly result: {result}")
    
    if result:
        print("✓ Full assembly successful")
        return True
    else:
        print("✗ Full assembly failed")
        return False

def cleanup():
    """Clean up test files"""
    print("\nCleaning up test files...")
    test_files = [
        "test_video1.mp4", "test_video2.mp4", "test_audio.mp3",
        "test_output1.mp4", "test_concatenated.mp4",
        "step1.mp4", "step2.mp4", "step1.mp3", "step2.mp3"
    ]
    
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed {f}")

def main():
    """Main test function"""
    print("GuideFrame Assembly Functions Test")
    print("=" * 40)
    
    try:
        # Test 1: Audio/video combination
        test1 = test_audio_video_combination()
        
        # Test 2: Video concatenation
        test2 = test_video_concatenation()
        
        # Test 3: Full assembly
        test3 = test_full_assembly()
        
        # Summary
        print("\n" + "=" * 40)
        print("TEST SUMMARY:")
        print(f"Audio/Video Combination: {'✓ PASS' if test1 else '✗ FAIL'}")
        print(f"Video Concatenation:     {'✓ PASS' if test2 else '✗ FAIL'}")
        print(f"Full Assembly:           {'✓ PASS' if test3 else '✗ FAIL'}")
        
        if all([test1, test2, test3]):
            print("\n🎉 All tests passed! Assembly functions are working correctly.")
        else:
            print("\n❌ Some tests failed. Check the output above for details.")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup()

if __name__ == "__main__":
    main() 