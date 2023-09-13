import tkinter as tk
import re
import os
import pyperclip
import time
from reserved_word_list import get_reserved_words

class FilePreviewQualityEnum:
    
    NOTDEFINED = 0
    
    # It will allow example 500 charters per line, and then ignore the following characters
    # It will allow 150 lines, and ignore the rest of the lines
    # We get kind of a text bounding box, everything in the box is visible, and everything outside is simply ignored
    # It is used when user is scrolling superfast through files and we just need to see the first 150 lines in a file and example 250 characters per line
    # We dont need to load the full file, just a preview of the first part of the file
    SUPERFAST = 1
    
    # In Small files everything is loaded.
    # For big files we will load some of the file, so the scrollbars are visible
    MEDIUMQUALITY = 2

    # Load the full file in the preview
    # It will be activated AFTER the scrollbar is scrolled more than 60% to the end of the file
    FULLQUALITY = 3
    
        
    DISABLECOLOR = 4    

class TextDisplayFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # LINENUMBERS ---------------------------------
        # Create the Text_Linenumber widget
        self.text_linenum = tk.Text(self, width=4, wrap="none", bg="#1e1e1e", fg="#818181", padx=4, pady=16,
                                    font=("Consolas", 11))
        self.text_linenum.grid(row=0, column=0, sticky="nsw")
        self.text_linenum.config(relief="flat")
        self.text_linenum.tag_configure("right_align", justify="right")
        self.text_linenum.config(highlightthickness=0)
        # self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure(0, minsize=1) 
        
        # Create a container frame to hold the text widget and scrollbars
        container = tk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Text Editor ---------------------------------
        self.text = tk.Text(container, wrap="none", bg="#1e1e1e", fg="#D4D4D4", padx=16, pady=16,
                            font=("Consolas", 11))
        self.text.configure(selectbackground="#264F78")
        self.text.grid(row=0, column=1, sticky="nsew")
        self.text.bind("<Button-3>", self.on_text_show_context_menu)
        self.text.config(highlightthickness=0)
        self.text.config(highlightbackground="#1e1e1e")  # border color
        self.text.config(highlightcolor="#1e1e1e")  # border color

        # Scrollbars
        self.scrollbar_y = tk.Scrollbar(container, width=14, borderwidth=0, highlightthickness=2,
                                        troughcolor='#ededed', activebackground='#3daee9', bg='#c4c4c4',
                                        highlightcolor='blue')
        self.scrollbar_y.grid(row=0, column=1, sticky="nes")
        self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, width=14, borderwidth=0, highlightthickness=0,
                                        troughcolor='#ededed', activebackground='#3daee9', bg='#c4c4c4',
                                        highlightcolor='blue')
        self.scrollbar_x.grid(row=1, column=1,  sticky="ew")

        # Configure scrollbars
        self.text.config(yscrollcommand=self.controller.handle_scroll_code_view, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.config(command=self.text.yview)
        self.scrollbar_x.config(command=self.text.xview)

        self.content = ""
        self.set_code_to("")
    
    def set_code_to(self, content,  file_ext = "", quality = FilePreviewQualityEnum.NOTDEFINED):
        self.content = content

        # TODO: Implement timer:  root.after(500, update_timer).
        # TODO: https://chat.openai.com/share/1915b0b5-a07a-458b-a020-aa3c5ab3a4aa
        # TODO: use: Listbox KeyRelease and ListBox MouseUp to commit a file selection
        
        if quality == FilePreviewQualityEnum.SUPERFAST:
            self.content = self.quality_superfast( content)
        if quality == FilePreviewQualityEnum.MEDIUMQUALITY:
            print(">>> LOAD MEDIUM QUALITY")
            self.content = self.quality_medium( content)
        if quality == FilePreviewQualityEnum.FULLQUALITY:
            # self.content = self.quality_full( content)
            pass
        
        try:
            # Convert Windows-style newline characters to Unix-style at line ends
            # content = re.sub(r'\r\n$', '\n', content, flags=re.MULTILINE)
            # content = content.replace('\r\n', '\n')
            
            # Fixes bug with rectangles at the end of the lines in CRLF files
            # Carriage Return (CR): ASCII code 13 (0x0D)
            content = self.content.replace('\x0D', '')
            
            self.text.delete(1.0, tk.END)  # Clear the current text
            self.text.insert(tk.END, self.content)  # Insert the new text
            if quality != FilePreviewQualityEnum.DISABLECOLOR:
                self.highlight_text(file_ext)
            self.show()
            
        except Exception as e:
            print(f"Error displaying text: {str(e)}")
        
        self.insert_linenumbers()

    def scroll_to_top(self):
        # self.text.yview_moveto(0.0)  # Scroll to the top
        pass
    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(padx=(0,0), pady=(0,0), side='left', fill=tk.BOTH, expand=True)

    # Performance: For fast preview it will:
    # It will crop the text to have a maximum of 500 characters on each line. It will cut off any characters, longer than that.
    # It will crop the text to have maximum 150 lines
    def quality_superfast(self, text):
        # Split the multiline string into individual lines
        lines = text.splitlines()

        # Initialize an empty list to store the modified lines
        cut_lines = []

        # Loop through each line and cut after 20 characters
        for line in lines:
            # Append the first 500 characters of the line to the list
            cut_lines.append(line[:500])
            
            # If the list already contains 150 lines, break the loop
            if len(cut_lines) >= 150:
                break
        
        # Important line/code for the scrollbar to work, when switching from preview to full quality. Do not delete.
        self.controller.line_count = len(cut_lines)
        
        # Join the modified lines back into a multiline string
        result = '\n'.join(cut_lines)

        return result

    # Performance: For fast preview it will:
    # It will crop the text to have a maximum of 500 characters on each line. It will cut off any characters, longer than that.
    # It will crop the text to have maximum 150 lines
    def quality_medium(self, text):
        # Split the multiline string into individual lines
        lines = text.splitlines()
        # self.controller.line_count = len(lines)

        # Initialize an empty list to store the modified lines
        cut_lines = []

        # Loop through each line and cut after 20 characters
        for line in lines:
            # Append the first 2000 characters of the line to the list
            cut_lines.append(line[:2000])
            
            # If the list already contains 1000 lines, break the loop
            if len(cut_lines) >= 150:
                break

        # Join the modified lines back into a multiline string
        result = '\n'.join(cut_lines)

        return result


    # Linenumbers
    
    def show_linenumbers(self):
        self.text_linenum.grid()
        # # Configure the tag to align the text to the right
        # self.text_linenum.config(relief="flat")
        # self.text_linenum.tag_configure("right_align", justify="right")
        # self.text_linenum.config(highlightthickness=0)

    def hide_linenumbers(self):
        self.text_linenum.grid_remove() 
        self.grid_columnconfigure(0, weight=0)  # Resize the second column to zero
    
    def toggle_linenumbers_visibility(self, int_value):
        if int_value == 0:
            self.hide_linenumbers()
        else:
            self.show_linenumbers()        
            
    
    def insert_linenumbers(self):
        # Clear the current line numbers
        self.text_linenum.delete('1.0', 'end')

        num_lines = self.text.get('1.0', 'end').count('\n')

        # Insert line numbers in TextA
        line_numbers = '\n'.join(str(i) for i in range(1, num_lines + 1))
        self.text_linenum.insert('1.0', line_numbers)
        self.text_linenum.tag_add("right_align", "1.0", "end")
        
    def on_text_show_context_menu(self, event):
        context_menu = tk.Menu(self.text, tearoff=0)
        context_menu.add_command(label="Copy               ", command=self.on_copy_text_to_clipboard)
        context_menu.tk_popup(event.x_root, event.y_root)

    def on_copy_text_to_clipboard(self, event=None):
        result = ""
        if self.text.tag_ranges("sel"):
            result = self.text.get("sel.first", "sel.last")
            self.controller.set_statusbar("Selected Text Copied To The Clipboard")
        else:
            result =  self.content
            self.controller.set_statusbar("All Text Copied To The Clipboard")
            

        pyperclip.copy(result)
        


    def highlight_text(self, file_ext = ""):
        
        file_ext = file_ext.lower()
        
        self.text.tag_configure("yellow", foreground="#e1a50f")
        self.text.tag_configure("keyword", foreground="#569CD6")
        self.text.tag_configure("numbers", foreground="#B8D7A3")
        self.text.tag_configure("redish", foreground="red")
        self.text.tag_configure("comment", foreground="#6A9955")
        self.text.tag_configure("quotation", foreground="#CE9178")
        self.text.tag_configure("xml-bracket", foreground="#7d7a76")
        self.text.tag_configure("xml-attribute-left-side", foreground="#6ec5fa")
        self.text.tag_configure("json-quoted-value", foreground="#CE9178")
        # Samme som baggrundsfarven
        # self.text.tag_configure("newline", foreground="#1e1e1e")  # Transparent color for newline characters
        
        if file_ext == "txt":
            return    
        
        if file_ext == "css" or file_ext == "sass" or file_ext == "scss":
            self.highlight_css_comments()
            self.highlight_open_close_brackets()
            self.css_highlight_text()
            return
        
        if file_ext == "html" or file_ext == "xml" or file_ext == "xaml":
            self.highlight_reserved_words(file_ext)
            self.highlight_quotation()
            self.highlight_xml_attribute_left_side()
            self.highlight_xml_brackets()
            self.highlight_comment_html()
            return 
        
        if file_ext == "md":
            self.markdown_highlight_text(file_ext)
            return 

        if file_ext == "json":
            self.highlight_numbers()
            self.highlight_open_close_brackets()
            self.highlight_json_quoted_strings()
            self.highlight_quotation()
            self.json_highlight_text()
            # reserved words: true, false
            self.highlight_reserved_words(file_ext)
            return
        
        if file_ext == "sql":
            self.highlight_reserved_words(file_ext)
            self.highlight_comment_doubledash()
            self.highlight_comment_hashtag()
            self.highlight_comment_slash_star()
            return             

        self.highlight_comment_doubledash()
        self.highlight_comment_doubleslash()
        self.highlight_comment_slash_star()
        self.highlight_comment_hashtag()
        self.highlight_comment_html()

        self.highlight_reserved_words(file_ext)
        self.highlight_numbers()
        self.highlight_quotation()
        self.highlight_open_close_brackets()
        # self.highlight_special_characers()

    # Mathces: # comments
    def highlight_comment_hashtag(self):
        # Comments starting with "//", "#" and "--" in greenish
        if "#" in self.content:
            comments = r"(?m)(?<!\w)(#).*"
            self.highlight_matches(comments, "comment")
    
    # Mathces: // comment
    def highlight_comment_doubleslash(self):
        if "//" in self.content:
            comments = r"(?m)(?<!\w)(\/\/).*"
            self.highlight_matches(comments, "comment")
    
    # Matches: /** comments **/
    def highlight_comment_slash_star(self):
        if "/**" in self.content:
            comments = r"/\*.*?\*/"
            self.highlight_matches(comments, "comment")
    
    # Mathces: -- comment
    def highlight_comment_doubledash(self):
        if "--" in self.content:
            comments = r"(?m)(?<!\w)(--).*"
            self.highlight_matches(comments, "comment")
    
    # Matches: <!-- comments -->
    def highlight_comment_html(self):
        if "<!--" in self.content:
            comments = r"<!--.*?-->"
            self.highlight_matches(comments, "comment")

    def highlight_css_comments(self):
        # Matches: /* ... */ (single-line) and /** ... */ (multi-line) CSS comments
        css_comments = r"/\*[\s\S]*?\*/"
        self.highlight_matches(css_comments, "comment")
    
    # Matches: numbers 0-9
    def highlight_numbers(self):
        numbers = r"\b\d+\b"
        self.highlight_matches(numbers, "numbers")
    
    # Matches: quotation
    def highlight_quotation(self):
        quotation = r'"([^"\\]|\\.)*"'
        self.highlight_matches(quotation, "quotation")
    
    # Matches: Special characters
    def highlight_open_close_brackets(self):
        special_chars = r"[()\[\]{}]"
        self.highlight_matches(special_chars, "yellow")
    
    # Matches: Special characters
    def highlight_special_characers(self):
        special_chars = r"[!@#$%^*]"
        self.highlight_matches(special_chars, "yellow")
        
    def highlight_xml_brackets(self):
        # Matches: <, </, >, /> outside of <!-- --> comments
        brackets_slashes = r"(?<!<!--)(?<!-->)[<>/](?!.*?-->)"
        self.highlight_matches(brackets_slashes, "xml-bracket")
    
    def highlight_xml_attribute_left_side(self):
        # Matches the left side of XML attributes
        attribute_left_side = r"(?<=\s)(\w+)(?=\s*=\s*['\"])"
        self.highlight_matches(attribute_left_side, "xml-attribute-left-side")    
    
    def highlight_quoted_json_values(self):
        # Matches: "value"
        quoted_values = r'(?<=": ")[^"]*(?=")'
        self.highlight_matches(quoted_values, "json-quoted-value")    
    
    # Reserved words in blue
    def highlight_reserved_words(self, file_ext):
        reserved_words = []
        reserved_words = get_reserved_words(file_ext)
        # Add your reserved words here as an array
        reserved_words_pattern = r"\b(" + "|".join(reserved_words) + r")\b"
        self.highlight_matches(reserved_words_pattern, "keyword")
    

    def highlight_(self):
        pass
    
        
    # General highlighter for all file types
    def highlight_matches(self, pattern, tag, exclude=[]):
        for line in range(1, int(self.text.index('end').split('.')[0])+1):
            line_start = f"{line}.0"
            line_end = f"{line}.end"

            for match in re.finditer(pattern, self.text.get(line_start, line_end)):
                start = f"{line}.{match.start()}"
                end = f"{line}.{match.end()}"
                exclude_ranges = any(self.text.tag_ranges(exclude_tag) for exclude_tag in exclude)
                if not exclude_ranges:
                    self.text.tag_add(tag, start, end)

    # --------------------------------------------------------------------------------------------------

    # CSS
    def css_highlight_text(self):
        
        # # Define CSS syntax patterns
        # property_pattern = r"(?<![-\w])[\w-]+(?=\s*:)"
        # value_pattern = r"(?<=:)\s*([^;]+)"
        # selector_pattern = r"([^\{\}]+)(?=\{)"

        # Precompile regex patterns for faster matching
        property_pattern = re.compile(r"(?<![-\w])[\w-]+(?=\s*:)")  # Matches CSS properties
        value_pattern = re.compile(r"(?<=:)\s*([^;]+)")  # Matches CSS property values
        selector_pattern = re.compile(r"([^\{\}]+)(?=\{)")  # Matches CSS selectors


        # Define CSS syntax tags
        css_property_tag = "css_property"
        css_value_tag = "css_value"
        css_selector_tag = "css_selector"
        # Configure text widget

        self.text.tag_configure("css_value", foreground="#CE9178")
        self.text.tag_configure("css_property", foreground="#9CDCFE")
        # self.text.tag_configure("css_selector", foreground="#d7ba7d")
        
        print('-----------------------------')
                
        start_time1 = time.time()
        self.css_highlight_matches(value_pattern, "css_value")
        end_time1 = time.time()

        
        start_time2 = time.time()
        self.css_highlight_matches(property_pattern, "css_property")
        end_time2 = time.time()
        
        
        start_time3 = time.time()
        self.css_highlight_matches(selector_pattern, "css_selector")
        end_time3 = time.time()
        # self.css_wordlist()


        # Calculate the time taken to execute the function
        execution_time1 = end_time1 - start_time1
        execution_time2 = end_time2 - start_time2
        execution_time3 = end_time3 - start_time3
        print(f'css1: {execution_time1}')
        print(f'css2: {execution_time2}')
        print(f'css3: {execution_time3}')

    def css_highlight_matches(self, pattern, tag):
        content = self.text.get("1.0", "end")

        for match in re.finditer(pattern, content):
            start = self.text.index(f"1.0 + {match.start()} chars")
            end = self.text.index(f"1.0 + {match.end()} chars")
            self.text.tag_add(tag, start, end)

    # def css_wordlist(self):
    #     # Define the list of words to highlight
    #     self.css_words = [
    #         "!important",
    #         'px', 
    #         'em', 
    #         'vh', 
    #         'vw', 
    #         'vmin', 
    #         'vmax', 
    #         '%', 
    #         # 'pt', 
    #         # 'pc', 
    #         # 'cm', 
    #         # 'mm', 
    #         # 'in',
    #         # 'ex', 
    #         # 'ch', 
    #         'rem', 
    #         'fr', 
    #         # 'deg', 
    #         # 'rad', 
    #         # 'turn' ,
    #     ]

        # # Configure the tag for highlighting
        # self.css_highlight_word_tag = "css_word_highlight"

        # # Configure text widget
        # self.text.tag_configure(self.css_highlight_word_tag, background="yellow")
        
        # content = self.text.get("1.0", "end")
        # for word in self.css_words:
        #     start = "1.0"
        #     while True:
        #         start = self.text.search(word, start, stopindex=tk.END)
        #         if not start:
        #             break
        #         end = self.text.index(f"{start}+{len(word)}c")
        #         self.text.tag_add(self.css_highlight_word_tag, start, end)
        #         start = end

    # Markdown
    def markdown_highlight_text(self, file_ext=""):
        # Heading tags
        #  I had to set the fontsize to 11, else it does not match with the linenumbers on the left
        self.text.tag_configure("heading1", foreground="white", font=("Arial", 11, "bold"))
        self.text.tag_configure("heading2", foreground="white", font=("Arial", 11, "bold"))
        self.text.tag_configure("heading3", foreground="white", font=("Arial", 11, "bold"))
        self.text.tag_configure("heading4", foreground="white", font=("Arial", 11, "bold"))
        self.text.tag_configure("heading5", foreground="white", font=("Arial", 11, "bold"))
        self.text.tag_configure("heading6", foreground="white", font=("Arial", 11, "bold"))

        # ... (existing tag configurations)

        # Apply heading styles
        self.markdown_highlight_headings()

    def markdown_highlight_headings(self):
        # Heading patterns
        heading1_pattern = r"^(#\s+.+)$"
        heading2_pattern = r"^(##\s+.+)$"
        heading3_pattern = r"^(###\s+.+)$"
        heading4_pattern = r"^(####\s+.+)$"
        heading5_pattern = r"^(#####\s+.+)$"
        heading6_pattern = r"^(######\s+.+)$"

        # Highlight heading patterns
        self.markdown_highlight_matches(heading1_pattern, "heading1")
        self.markdown_highlight_matches(heading2_pattern, "heading2")
        self.markdown_highlight_matches(heading3_pattern, "heading3")
        self.markdown_highlight_matches(heading4_pattern, "heading4")
        self.markdown_highlight_matches(heading5_pattern, "heading5")
        self.markdown_highlight_matches(heading6_pattern, "heading6")

    def markdown_highlight_matches(self, pattern, tag, exclude=[]):
        for line in range(1, int(self.text.index("end").split(".")[0]) + 1):
            line_start = f"{line}.0"
            line_end = f"{line}.end"

            for match in re.finditer(pattern, self.text.get(line_start, line_end)):
                start = f"{line}.{match.start()}"
                end = f"{line}.{match.end()}"
                exclude_ranges = any(self.text.tag_ranges(exclude_tag) for exclude_tag in exclude)
                if not exclude_ranges:
                    self.text.tag_add(tag, start, end)
    
    # JSON
    
    def json_highlight_text(self):
        self.text.tag_configure("quoted_string", foreground="#9cdcfe")

        self.highlight_json_quoted_strings()

    def highlight_json_quoted_strings(self):
        for line in range(1, int(self.text.index("end").split(".")[0]) + 1):
            line_start = f"{line}.0"
            line_end = f"{line}.end"

            # Get the line text
            line_text = self.text.get(line_start, line_end)

            # Find the first quoted string in the line
            match = re.search(r'"([^"\\]|\\.)*"', line_text)

            if match:
                # Highlight the first quoted string
                start = f"{line}.{match.start()}"
                end = f"{line}.{match.end()}"
                self.text.tag_add("quoted_string", start, end)
