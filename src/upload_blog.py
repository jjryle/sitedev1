#!/usr/bin/env python3
import ftplib
import sys

def upload_md(filename):
    try:
        ftp = ftplib.FTP()
        ftp.connect("6.tcp.ngrok.io", 13008)
        ftp.login("jryle", "alskdjf^%&$2930u42prj")
        
        with open(filename, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
        
        ftp.quit()
        print(f"✅ Uploaded: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_blog.py filename.md")
    else:
        upload_md(sys.argv[1])