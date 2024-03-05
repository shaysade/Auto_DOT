import subprocess
import sys

def start_playwright_recording(start_url):
    # Command to start Playwright recording at a specified URL
    command = f"playwright codegen {start_url} --output=recorded_script.py"
    
    # Run the command
    process = subprocess.Popen(command, shell=True)
    print(f"Recording started at {start_url}. Close the browser to stop recording.")
    
    # Wait for the recording process to finish
    process.wait()
    print("Recording stopped. The script is saved as 'recorded_script.py'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <URL>")
    else:
        start_url = sys.argv[1]
        start_playwright_recording(start_url)
