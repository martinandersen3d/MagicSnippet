import subprocess

def copy_html_to_clipboard_linux(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
            
            process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'text/html'], stdin=subprocess.PIPE)
            process.communicate(input=html_content.encode('utf-8'))
            
            print("HTML content from file copied to clipboard on Linux.")
    except Exception as e:
        print("Error:", e)