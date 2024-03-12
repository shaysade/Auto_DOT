import subprocess
import sys

def start_playwright_recording(start_url):
    # Command to start Playwright recording at a specified URL, avoiding shell=True for security reasons
    command = ["playwright", "codegen", start_url, "--output=recorded_script.py"]
    
    try:
        # Run the command without shell=True
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Recording started at {start_url}. Close the browser to stop recording.")
        
        # Wait for the recording process to finish
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print("Recording stopped. The script is saved as 'recorded_script.py'.")
            with open('recorded_script.py', 'r') as file:
                return file.read()
        else:
            print(f"Recording failed with error: {stderr.decode('utf-8')}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <URL>")
    else:
        start_url = sys.argv[1]
        start_playwright_recording(start_url)
