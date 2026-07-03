import os
import sys

def verify_environment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_dirs = [
        "data/raw",
        "data/processed",
        "data/chroma_db",
        "src"
    ]
    
    all_passed = True
    
    print("--- Environment Verification ---")
    for d in required_dirs:
        dir_path = os.path.join(base_dir, *d.split('/'))
        
        # Ensure it exists
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"[CREATED] {d}")
            except Exception as e:
                print(f"[ERROR] Could not create {d}: {e}")
                all_passed = False
                continue
                
        # Check permissions
        has_read = os.access(dir_path, os.R_OK)
        has_write = os.access(dir_path, os.W_OK)
        
        if has_read and has_write:
            print(f"[OK] {d} (Read/Write OK)")
        else:
            print(f"[ERROR] {d} - Missing permissions (Read: {has_read}, Write: {has_write})")
            all_passed = False
            
    if all_passed:
        print("\nSUCCESS: Environment satisfies eval.md criteria.")
        sys.exit(0)
    else:
        print("\nFAILURE: Environment does not satisfy eval.md criteria.")
        sys.exit(1)

if __name__ == "__main__":
    verify_environment()
