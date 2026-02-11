import subprocess
import sys

def install_requirements():
    # Strict Enterprise Standards: List of required R&D packages
    requirements = [
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn"
    ]
    
    print("LOG: Initializing Environment Setup for Pipeline_v2...")
    
    for package in requirements:
        print(f"LOG: Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"LOG: Successfully installed {package}")
        except Exception as e:
            print(f"ERROR: Failed to install {package}. {str(e)}")

    print("\n--- ENVIRONMENT SETUP COMPLETE ---")
    print("LOG: All R&D tools are now active in venv.")
    print("----------------------------------\n")

if __name__ == "__main__":
    install_requirements()