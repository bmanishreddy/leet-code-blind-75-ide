#!/usr/bin/env python3
"""
Extract questions from PDF file
"""

import sys
import os

pdf_path = "/Users/manishb/Desktop/Print.pdf"

# Try different PDF libraries
try:
    import PyPDF2
    print("Using PyPDF2...")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        print("=" * 80)
        print("EXTRACTED TEXT FROM PDF:")
        print("=" * 80)
        print(text)
        print("=" * 80)
        
except ImportError:
    try:
        import pdfplumber
        print("Using pdfplumber...")
        
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            
            print("=" * 80)
            print("EXTRACTED TEXT FROM PDF:")
            print("=" * 80)
            print(text)
            print("=" * 80)
            
    except ImportError:
        print("Neither PyPDF2 nor pdfplumber available. Installing pdfplumber...")
        os.system("pip3 install pdfplumber --quiet")
        
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                
                print("=" * 80)
                print("EXTRACTED TEXT FROM PDF:")
                print("=" * 80)
                print(text[:5000])  # Print first 5000 chars
                print("...")
                print("=" * 80)
        except Exception as e:
            print(f"Error: {e}")

