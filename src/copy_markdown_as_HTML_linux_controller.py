import subprocess
import markdown

def copy_markdown_as_HTML_clipboard_linux(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as markdown_content:
            markdown_content = markdown_content.read()
            html = markdown.markdown(markdown_content, extensions=['tables', 'sane_lists'])
            process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'text/html'], stdin=subprocess.PIPE)
            process.communicate(input=html.encode('utf-8'))
    except Exception as e:
        print("Error:", e)