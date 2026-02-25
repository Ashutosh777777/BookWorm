#!/usr/bin/env python3
"""
PDF Text-to-Speech Reader
A tool to read PDF books aloud with pause/resume controls and bookmarking
"""

import pyttsx3
import PyPDF2
import json
import os
import re
from threading import Thread, Event
import time

class PDFReader:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.paused = Event()
        self.stopped = Event()
        self.current_pdf = None
        self.current_page = 0
        self.bookmark_file = "bookmarks.json"
        
        # Configure TTS engine
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
    def extract_text_from_pdf(self, pdf_path, start_page=0, end_page=None):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                if end_page is None:
                    end_page = total_pages
                
                text = ""
                for page_num in range(start_page, min(end_page, total_pages)):
                    page = pdf_reader.pages[page_num]
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
                
                return text, total_pages
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None, 0
    
    def find_introduction(self, pdf_path):
        """Search for the introduction page in the PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # Common introduction keywords
                intro_keywords = [
                    'introduction', 'preface', 'foreword', 
                    'prologue', 'about this book'
                ]
                
                print(f"\nSearching for introduction in {total_pages} pages...")
                
                for page_num in range(min(50, total_pages)):  # Search first 50 pages
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text().lower()
                    
                    for keyword in intro_keywords:
                        if keyword in text:
                            print(f"Found '{keyword}' on page {page_num + 1}")
                            return page_num
                
                print("Introduction not found. Starting from page 1.")
                return 0
        except Exception as e:
            print(f"Error searching for introduction: {e}")
            return 0
    
    def search_chapter(self, pdf_path, chapter_name):
        """Search for a specific chapter in the PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                print(f"\nSearching for '{chapter_name}'...")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text().lower()
                    
                    if chapter_name.lower() in text:
                        print(f"Found on page {page_num + 1}")
                        return page_num
                
                print(f"Chapter '{chapter_name}' not found.")
                return None
        except Exception as e:
            print(f"Error searching for chapter: {e}")
            return None
    
    def save_bookmark(self, pdf_path, page_num):
        """Save current reading position"""
        bookmarks = self.load_bookmarks()
        bookmarks[pdf_path] = page_num
        
        try:
            with open(self.bookmark_file, 'w') as f:
                json.dump(bookmarks, f, indent=2)
            print(f"\nBookmark saved at page {page_num + 1}")
        except Exception as e:
            print(f"Error saving bookmark: {e}")
    
    def load_bookmarks(self):
        """Load saved bookmarks"""
        if os.path.exists(self.bookmark_file):
            try:
                with open(self.bookmark_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def get_bookmark(self, pdf_path):
        """Get bookmark for specific PDF"""
        bookmarks = self.load_bookmarks()
        return bookmarks.get(pdf_path, 0)
    
    def speak_text(self, text):
        """Speak the given text with pause/resume capability"""
        sentences = re.split(r'[.!?]+', text)
        
        for i, sentence in enumerate(sentences):
            if self.stopped.is_set():
                break
            
            # Wait if paused
            while self.paused.is_set():
                if self.stopped.is_set():
                    break
                time.sleep(0.1)
            
            if self.stopped.is_set():
                break
            
            if sentence.strip():
                self.engine.say(sentence.strip())
                self.engine.runAndWait()
    
    def read_pdf(self, pdf_path, start_page=0):
        """Read PDF from specified page"""
        self.current_pdf = pdf_path
        self.current_page = start_page
        self.stopped.clear()
        self.paused.clear()
        
        print(f"\nReading from page {start_page + 1}...")
        print("\nControls:")
        print("  'p' - Pause/Resume")
        print("  's' - Stop")
        print("  'b' - Bookmark current page")
        print("  'n' - Next 5 pages")
        print("  'j' - Jump to page")
        
        text, total_pages = self.extract_text_from_pdf(pdf_path, start_page)
        
        if text:
            # Start reading in a separate thread
            read_thread = Thread(target=self.speak_text, args=(text,))
            read_thread.start()
            
            # Handle user input for controls
            self.handle_controls(read_thread, pdf_path, start_page, total_pages)
    
    def handle_controls(self, read_thread, pdf_path, start_page, total_pages):
        """Handle user input for playback controls"""
        while read_thread.is_alive():
            try:
                command = input().strip().lower()
                
                if command == 'p':
                    if self.paused.is_set():
                        self.paused.clear()
                        print("Resumed")
                    else:
                        self.paused.set()
                        print("Paused")
                
                elif command == 's':
                    self.stopped.set()
                    print("Stopped")
                    break
                
                elif command == 'b':
                    self.save_bookmark(pdf_path, self.current_page)
                
                elif command == 'n':
                    self.stopped.set()
                    read_thread.join()
                    new_page = min(start_page + 5, total_pages - 1)
                    self.read_pdf(pdf_path, new_page)
                    break
                
                elif command == 'j':
                    page_input = input("Enter page number: ").strip()
                    try:
                        jump_page = int(page_input) - 1
                        if 0 <= jump_page < total_pages:
                            self.stopped.set()
                            read_thread.join()
                            self.read_pdf(pdf_path, jump_page)
                            break
                        else:
                            print(f"Invalid page. Must be between 1 and {total_pages}")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            
            except EOFError:
                time.sleep(0.1)
        
        read_thread.join()


def main():
    reader = PDFReader()
    
    print("=" * 60)
    print("PDF Text-to-Speech Reader")
    print("=" * 60)
    
    # Get PDF file path
    pdf_path = input("\nEnter the path to your PDF file: ").strip()
    
    if not os.path.exists(pdf_path):
        print("Error: File not found!")
        return
    
    # Check for existing bookmark
    bookmark_page = reader.get_bookmark(pdf_path)
    if bookmark_page > 0:
        resume = input(f"\nFound bookmark at page {bookmark_page + 1}. Resume? (y/n): ").strip().lower()
        if resume == 'y':
            reader.read_pdf(pdf_path, bookmark_page)
            return
    
    # Ask where to start reading
    print("\nWhere would you like to start reading?")
    print("1. From the introduction (auto-detect)")
    print("2. From the beginning")
    print("3. Search for a chapter")
    print("4. Specific page number")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        start_page = reader.find_introduction(pdf_path)
        reader.read_pdf(pdf_path, start_page)
    
    elif choice == '2':
        reader.read_pdf(pdf_path, 0)
    
    elif choice == '3':
        chapter_name = input("Enter chapter name: ").strip()
        start_page = reader.search_chapter(pdf_path, chapter_name)
        if start_page is not None:
            reader.read_pdf(pdf_path, start_page)
        else:
            print("Chapter not found. Starting from beginning.")
            reader.read_pdf(pdf_path, 0)
    
    elif choice == '4':
        page_num = input("Enter page number: ").strip()
        try:
            start_page = int(page_num) - 1
            reader.read_pdf(pdf_path, max(0, start_page))
        except ValueError:
            print("Invalid page number. Starting from beginning.")
            reader.read_pdf(pdf_path, 0)
    
    else:
        print("Invalid choice. Starting from beginning.")
        reader.read_pdf(pdf_path, 0)


if __name__ == "__main__":
    main()