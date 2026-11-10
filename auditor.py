import os
import configparser
import json

def run_audit():
    config = configparser.ConfigParser()
    
    # Ensure the rules file exists
    if not os.path.exists('rules.ini'):
        print("❌ Error: rules.ini file not found in this folder!")
        return []
        
    config.read('rules.ini')
    audit_results = []

    for section in config.sections():
        check_type = config[section].get('check_type', '')
        remediation = config[section].get('remediation', 'No remediation provided.')
        status = "FAIL"  # Default to fail to show GRC gaps
        
        # Rule Type 1: Configuration Value Check
        if check_type == "configuration_value":
            target_file = config[section].get('target_file', '')
            expected = config[section].get('expected_value', '')
            
            # If the file exists, check it. If not, it fails the compliance audit.
            if os.path.exists(target_file):
                with open(target_file, 'r') as f:
                    content = f.read()
                    if expected in content:
                        status = "PASS"
            else:
                status = "FAIL"

        # Rule Type 2: Environment Variable Check
        elif check_type == "environment_variable":
            var_name = config[section].get('variable_name', '')
            expected = config[section].get('expected_value', '')
            actual_value = os.getenv(var_name, "NOT_SET")
            
            if actual_value.upper() == expected.upper():
                status = "PASS"
            else:
                status = "FAIL"
                
        # Rule Type 3: File Permission Check (Fallback simulation for Windows/Mac local testing)
        else:
            status = "FAIL"

        # Dynamically add the rule data into our results list
        audit_results.append({
            "control": section,
            "status": status,
            "remediation": remediation
        })


    return audit_results

if __name__ == "__main__":
    results = run_audit()
    with open('audit_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("\n✅ Audit complete. Found definitions for", len(results), "controls.")
    print("Results successfully saved to audit_results.json")
    
    input("\nPress Enter to close this window...")