import requests
import sys
from datetime import datetime
import json

class SimpleAPITester:
    def __init__(self, base_url="https://sada-clone-7.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"Response: {json.dumps(response_data, indent=2)}")
                except:
                    print(f"Response: {response.text}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"Response: {response.text}")

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root Endpoint", "GET", "", 200)

    def test_create_status_check(self):
        """Test creating a status check"""
        test_data = {
            "client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"
        }
        return self.run_test("Create Status Check", "POST", "status", 200, test_data)

    def test_get_status_checks(self):
        """Test getting all status checks"""
        return self.run_test("Get Status Checks", "GET", "status", 200)

    def test_teachers_endpoints(self):
        """Test if teachers endpoints exist (expected from review request)"""
        print("\n🔍 Testing Teachers Endpoints (from review request)...")
        
        # Test teachers list endpoint
        teachers_success, _ = self.run_test("Get Teachers", "GET", "teachers", 200)
        
        # Test login endpoint
        login_data = {"username": "berdoz", "password": "berdoz@code"}
        login_success, _ = self.run_test("Login", "POST", "auth/login", 200, login_data)
        
        return teachers_success or login_success

def main():
    print("🚀 Starting Backend API Tests...")
    tester = SimpleAPITester()

    # Test existing endpoints
    print("\n" + "="*50)
    print("TESTING EXISTING API ENDPOINTS")
    print("="*50)
    
    tester.test_root_endpoint()
    tester.test_create_status_check()
    tester.test_get_status_checks()

    # Test expected teachers endpoints from review request
    print("\n" + "="*50)
    print("TESTING EXPECTED TEACHERS ENDPOINTS")
    print("="*50)
    
    teachers_exist = tester.test_teachers_endpoints()

    # Print results
    print(f"\n📊 Overall Results:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if not teachers_exist:
        print("\n⚠️  CRITICAL FINDING:")
        print("No teachers-related endpoints found!")
        print("The review request expects teachers functionality that doesn't exist in the backend.")
        
    return 0 if tester.tests_passed > 0 else 1

if __name__ == "__main__":
    sys.exit(main())