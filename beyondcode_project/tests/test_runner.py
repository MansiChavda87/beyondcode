"""
TDD Test Runner for Django CMS
Provides comprehensive test execution and reporting
"""

import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings
from django.core.management import call_command
import time
import json
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()


class TestRunner:
    """Custom test runner for TDD workflow"""
    
    def __init__(self):
        self.test_results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'duration': 0,
            'tests': []
        }
    
    def run_all_tests(self):
        """Run all tests with comprehensive reporting"""
        print("=" * 80)
        print("BEYONDCODE AI CMS - TDD TEST SUITE")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run different test categories
        test_suites = [
            ('Models', 'tests.test_models'),
            ('Views', 'tests.test_views'),
            ('Integration', 'tests.test_integration'),
            ('Performance', 'tests.test_performance'),
            ('Security', 'tests.test_security'),
            ('URLs', 'tests.test_urls'),
            ('End-to-End', 'tests.test_e2e'),
        ]
        
        overall_start_time = time.time()
        
        for suite_name, suite_module in test_suites:
            print(f"Running {suite_name} Tests...")
            print("-" * 40)
            
            suite_start_time = time.time()
            result = self.run_test_suite(suite_module)
            suite_duration = time.time() - suite_start_time
            
            print(f"{suite_name} Results:")
            print(f"  Total: {result['total']}")
            print(f"  Passed: {result['passed']}")
            print(f"  Failed: {result['failed']}")
            print(f"  Errors: {result['errors']}")
            print(f"  Skipped: {result['skipped']}")
            print(f"  Duration: {suite_duration:.2f}s")
            print()
        
        overall_duration = time.time() - overall_start_time
        
        print("=" * 80)
        print("OVERALL TEST RESULTS")
        print("=" * 80)
        print(f"Total Tests: {self.test_results['total']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Errors: {self.test_results['errors']}")
        print(f"Skipped: {self.test_results['skipped']}")
        print(f"Total Duration: {overall_duration:.2f}s")
        print()
        
        # Calculate success rate
        if self.test_results['total'] > 0:
            success_rate = (self.test_results['passed'] / self.test_results['total']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print("=" * 80)
        
        # Save results
        self.save_test_results()
        
        return self.test_results['failed'] == 0 and self.test_results['errors'] == 0
    
    def run_test_suite(self, test_module):
        """Run a specific test suite"""
        TestRunnerClass = get_runner(settings)
        test_runner = TestRunnerClass(verbosity=2, interactive=False, keepdb=False)
        
        suite_start_time = time.time()
        failures = test_runner.run_tests([test_module])
        suite_duration = time.time() - suite_start_time
        
        # Calculate results
        suite_results = {
            'total': 0,
            'passed': 0,
            'failed': len(failures) if failures else 0,
            'errors': 0,
            'skipped': 0,
            'duration': suite_duration
        }
        
        # Update overall results
        self.test_results['total'] += suite_results['total']
        self.test_results['failed'] += suite_results['failed']
        self.test_results['errors'] += suite_results['errors']
        self.test_results['skipped'] += suite_results['skipped']
        self.test_results['duration'] += suite_duration
        
        return suite_results
    
    def run_specific_tests(self, test_patterns):
        """Run specific tests based on patterns"""
        print("=" * 80)
        print("RUNNING SPECIFIC TESTS")
        print("=" * 80)
        
        TestRunnerClass = get_runner(settings)
        test_runner = TestRunnerClass(verbosity=2, interactive=False, keepdb=False)
        
        start_time = time.time()
        failures = test_runner.run_tests(test_patterns)
        duration = time.time() - start_time
        
        print(f"Test Duration: {duration:.2f}s")
        print(f"Failures: {len(failures) if failures else 0}")
        
        return len(failures) == 0
    
    def run_performance_tests(self):
        """Run only performance tests"""
        return self.run_specific_tests(['tests.test_performance'])
    
    def run_security_tests(self):
        """Run only security tests"""
        return self.run_specific_tests(['tests.test_security'])
    
    def run_integration_tests(self):
        """Run only integration tests"""
        return self.run_specific_tests(['tests.test_integration'])
    
    def run_tdd_cycle(self):
        """Run a complete TDD cycle"""
        print("=" * 80)
        print("TDD CYCLE EXECUTION")
        print("=" * 80)
        
        # Step 1: Run existing tests (should pass)
        print("Step 1: Running existing tests...")
        existing_tests_pass = self.run_specific_tests(['tests.test_models', 'tests.test_views'])
        
        if not existing_tests_pass:
            print("❌ Existing tests are failing. Fix them first!")
            return False
        
        print("✅ Existing tests pass. Proceeding with TDD cycle.")
        print()
        
        # Step 2: Write new test (RED)
        print("Step 2: Write new test (RED phase)")
        print("   - Write a failing test for new functionality")
        print("   - Verify it fails as expected")
        print()
        
        # Step 3: Implement minimal code (GREEN)
        print("Step 3: Implement minimal code (GREEN phase)")
        print("   - Write minimal code to make test pass")
        print("   - Run test to verify it passes")
        print()
        
        # Step 4: Refactor (REFACTOR)
        print("Step 4: Refactor (REFACTOR phase)")
        print("   - Improve code quality without changing behavior")
        print("   - Ensure all tests still pass")
        print()
        
        # Step 5: Run full test suite
        print("Step 5: Running full test suite...")
        full_suite_pass = self.run_all_tests()
        
        if full_suite_pass:
            print("✅ TDD cycle completed successfully!")
        else:
            print("❌ TDD cycle failed. Review and fix issues.")
        
        return full_suite_pass
    
    def save_test_results(self):
        """Save test results to JSON file"""
        results_file = os.path.join(
            os.path.dirname(__file__),
            'test_results',
            f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        # Add timestamp
        self.test_results['timestamp'] = datetime.now().isoformat()
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"Test results saved to: {results_file}")
    
    def generate_test_report(self):
        """Generate a detailed test report"""
        report_file = os.path.join(
            os.path.dirname(__file__),
            'test_results',
            f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        )
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .summary {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 20px; margin: 20px 0; }}
                .metric {{ background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric h3 {{ margin: 0 0 10px 0; }}
                .metric .value {{ font-size: 2em; font-weight: bold; }}
                .success {{ color: #28a745; }}
                .danger {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
                .info {{ color: #17a2b8; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>BEYONDCODE AI CMS - Test Report</h1>
                <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>Total Tests</h3>
                    <div class="value">{self.test_results['total']}</div>
                </div>
                <div class="metric">
                    <h3>Passed</h3>
                    <div class="value success">{self.test_results['passed']}</div>
                </div>
                <div class="metric">
                    <h3>Failed</h3>
                    <div class="value danger">{self.test_results['failed']}</div>
                </div>
                <div class="metric">
                    <h3>Errors</h3>
                    <div class="value warning">{self.test_results['errors']}</div>
                </div>
                <div class="metric">
                    <h3>Duration</h3>
                    <div class="value info">{self.test_results['duration']:.2f}s</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        print(f"Test report generated: {report_file}")


def main():
    """Main entry point for test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run TDD tests for BeyondCode AI CMS')
    parser.add_argument('--suite', choices=['all', 'models', 'views', 'integration', 'performance', 'security', 'urls', 'e2e'],
                       default='all', help='Test suite to run')
    parser.add_argument('--tdd-cycle', action='store_true', help='Run complete TDD cycle')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--security', action='store_true', help='Run security tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.tdd_cycle:
        success = runner.run_tdd_cycle()
    elif args.performance:
        success = runner.run_performance_tests()
    elif args.security:
        success = runner.run_security_tests()
    elif args.integration:
        success = runner.run_integration_tests()
    elif args.suite == 'all':
        success = runner.run_all_tests()
    else:
        # Run specific suite
        test_modules = {
            'models': 'tests.test_models',
            'views': 'tests.test_views',
            'integration': 'tests.test_integration',
            'performance': 'tests.test_performance',
            'security': 'tests.test_security',
            'urls': 'tests.test_urls',
            'e2e': 'tests.test_e2e',
        }
        success = runner.run_specific_tests([test_modules[args.suite]])
    
    if success:
        print("\n🎉 All tests passed! The CMS is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please review and fix the issues.")
        sys.exit(1)


if __name__ == '__main__':
    main()