import os
import sys

def main():
    python_exe = sys.executable

    print("Starting full review analysis pipeline...\n")

    print("Step 1: Running scraper.py")
    os.system(f'"{python_exe}" scraper.py')

    print("\nStep 2: Running preprocess.py")
    os.system(f'"{python_exe}" preprocess.py')

    print("\nStep 3: Running llm_analyzer.py")
    os.system(f'"{python_exe}" llm_analyzer.py')

    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()