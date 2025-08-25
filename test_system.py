#!/usr/bin/env python3
"""
Test script for Face Recognition Attendance System
Run this to verify all components are working correctly
"""

import os
import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from utils.face_utils import FaceRecognitionSystem
        print("✅ FaceRecognitionSystem imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FaceRecognitionSystem: {e}")
        return False
    
    try:
        from utils.db_utils import AttendanceManager
        print("✅ AttendanceManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AttendanceManager: {e}")
        return False
    
    try:
        from utils.report_utils import ReportGenerator
        print("✅ ReportGenerator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ReportGenerator: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test if all required directories exist or can be created"""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        'dataset',
        'models', 
        'attendance',
        'uploads',
        'templates',
        'static/css',
        'static/js',
        'utils'
    ]
    
    for directory in required_dirs:
        try:
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(directory):
                print(f"✅ Directory '{directory}' exists/created")
            else:
                print(f"❌ Failed to create directory '{directory}'")
                return False
        except Exception as e:
            print(f"❌ Error with directory '{directory}': {e}")
            return False
    
    return True

def test_face_recognition_system():
    """Test the face recognition system initialization"""
    print("\n🤖 Testing Face Recognition System...")
    
    try:
        from utils.face_utils import FaceRecognitionSystem
        
        # Initialize system
        face_system = FaceRecognitionSystem()
        print("✅ FaceRecognitionSystem instance created")
        
        # Test system status
        status = face_system.get_system_status()
        print(f"✅ System status: {status}")
        
        # Test known students
        students = face_system.get_known_students()
        print(f"✅ Known students: {len(students)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Face recognition system test failed: {e}")
        traceback.print_exc()
        return False

def test_attendance_manager():
    """Test the attendance management system"""
    print("\n📊 Testing Attendance Manager...")
    
    try:
        from utils.db_utils import AttendanceManager
        
        # Initialize manager
        attendance_manager = AttendanceManager()
        print("✅ AttendanceManager instance created")
        
        # Test system stats
        stats = attendance_manager.get_system_stats()
        print(f"✅ System stats: {stats}")
        
        # Test getting all dates
        dates = attendance_manager.get_all_dates()
        print(f"✅ Attendance dates: {len(dates)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Attendance manager test failed: {e}")
        traceback.print_exc()
        return False

def test_report_generator():
    """Test the report generation system"""
    print("\n📈 Testing Report Generator...")
    
    try:
        from utils.report_utils import ReportGenerator
        
        # Initialize generator
        report_generator = ReportGenerator()
        print("✅ ReportGenerator instance created")
        
        # Test with sample data
        sample_data = [
            {'name': 'Test Student', 'status': 'Present', 'confidence': 'High'},
            {'name': 'Another Student', 'status': 'Absent', 'confidence': 'N/A'}
        ]
        
        # Test CSV generation
        csv_content = report_generator.generate_csv(sample_data, '2024-01-01')
        if csv_content:
            print("✅ CSV generation successful")
        else:
            print("❌ CSV generation failed")
            return False
        
        # Test summary report
        summary = report_generator.generate_summary_report(sample_data, '2024-01-01')
        if summary:
            print("✅ Summary report generation successful")
        else:
            print("❌ Summary report generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Report generator test failed: {e}")
        traceback.print_exc()
        return False

def test_flask_app():
    """Test if Flask app can be imported and configured"""
    print("\n🌐 Testing Flask Application...")
    
    try:
        # Test Flask import
        import flask
        print("✅ Flask imported successfully")
        
        # Test if app.py can be imported
        try:
            import app
            print("✅ Flask app imported successfully")
        except ImportError:
            print("⚠️  Flask app not yet runnable (expected for first run)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        print("💡 Install Flask: pip install flask")
        return False

def main():
    """Run all tests"""
    print("🚀 Face Recognition Attendance System - System Test")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Directory Structure", test_directory_structure),
        ("Face Recognition System", test_face_recognition_system),
        ("Attendance Manager", test_attendance_manager),
        ("Report Generator", test_report_generator),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Check Python version (3.8+ required)")
        print("   - Ensure all files are in correct locations")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
