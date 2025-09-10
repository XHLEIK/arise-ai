"""
Test script for the Application Scanner module.

This script demonstrates how to use the ApplicationScanner class
to find installed applications on the system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.app_scanner import ApplicationScanner


def test_application_scanner():
    """
    Test the ApplicationScanner functionality.
    """
    print("🔍 A.R.I.S.E. Application Scanner Test")
    print("=" * 50)
    
    # Create scanner instance
    scanner = ApplicationScanner("data/applications.json")
    
    print(f"Operating System: {scanner.system}")
    print("Starting application scan...")
    print()
    
    try:
        # Run the scan
        applications = scanner.run_scan()
        
        print(f"✅ Scan completed successfully!")
        print(f"📱 Found {len(applications)} applications")
        print(f"💾 Results saved to: {scanner.output_file}")
        print()
        
        # Display popular applications found
        popular_apps = ['Google Chrome', 'Mozilla Firefox', 'WhatsApp', 'Discord', 
                       'Spotify', 'Visual Studio Code', 'Microsoft Edge']
        
        print("🔥 Popular Applications Found:")
        print("-" * 30)
        found_popular = 0
        for app in popular_apps:
            path = scanner.get_application_path(app)
            if path:
                print(f"✅ {app}: {path}")
                found_popular += 1
            else:
                print(f"❌ {app}: Not found")
        
        print(f"\nFound {found_popular}/{len(popular_apps)} popular applications")
        print()
        
        # Display all found applications (limited to first 20)
        print("📋 All Found Applications (first 20):")
        print("-" * 40)
        for i, (name, path) in enumerate(applications.items()):
            if i >= 20:
                print(f"... and {len(applications) - 20} more applications")
                break
            print(f"{i+1:2d}. {name}")
            print(f"    Path: {path}")
            print()
        
        # Test application lookup
        print("🔍 Testing Application Lookup:")
        print("-" * 30)
        test_apps = ['chrome', 'firefox', 'notepad']
        for app in test_apps:
            path = scanner.get_application_path(app)
            if path:
                print(f"✅ Found '{app}': {path}")
            else:
                print(f"❌ '{app}' not found")
        
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = test_application_scanner()
    
    if success:
        print("\n🎉 Application scanner test completed successfully!")
    else:
        print("\n💥 Application scanner test failed!")
        sys.exit(1)
