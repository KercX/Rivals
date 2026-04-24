#!/usr/bin/env python3
"""
Instagram Public Bio Scanner
Extracts ONLY text from public profile bio.
No phone number retrieval unless user posted it publicly.
Author: KercX (for educational/legal use only)
"""

import requests
import re
import sys
from bs4 import BeautifulSoup

def get_public_bio(username):
    """
    Scrape PUBLIC Instagram bio (legal, like viewing a web page)
    Returns: bio text and any phone numbers/emails found there
    """
    url = f"https://www.instagram.com/{username}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": "Profile not found or private"}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Instagram loads data in JSON script tags
        # Find meta description (contains bio)
        meta_desc = soup.find("meta", attrs={"name": "description"})
        bio_text = ""
        if meta_desc:
            content = meta_desc.get("content", "")
            # Bio is usually the first part before follower counts
            bio_text = content.split(".")[0] if "." in content else content
        
        # Also search for script tags with JSON
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and '"biography"' in script.string:
                import json
                try:
                    # Very crude extraction - real would need proper JSON parsing
                    match = re.search(r'"biography":"(.*?)"', script.string)
                    if match:
                        bio_text = match.group(1).replace('\\n', '\n')
                except:
                    pass
        
        # Extract phone numbers from bio
        phone_pattern = r'[\+\(]?[0-9]{1,4}[\)\-\s]?[0-9]{6,12}'
        phones = re.findall(phone_pattern, bio_text)
        
        # Extract emails from bio
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, bio_text)
        
        return {
            "username": username,
            "bio_text": bio_text.strip(),
            "phones_found_in_bio": phones if phones else None,
            "emails_found_in_bio": emails if emails else None,
            "note": "These numbers/emails appear ONLY if user publicly typed them in bio"
        }
        
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python instagram_bio_scanner.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    result = get_public_bio(username)
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"\n📸 Instagram Profile: @{username}")
        print("=" * 50)
        print(f"📝 Bio text:\n{result['bio_text']}\n")
        
        if result['phones_found_in_bio']:
            print(f"📞 Phone numbers found in bio: {result['phones_found_in_bio']}")
        else:
            print("📞 No phone number found in public bio")
        
        if result['emails_found_in_bio']:
            print(f"📧 Emails found in bio: {result['emails_found_in_bio']}")
        
        print("\n" + "=" * 50)
        print("⚠️  This only shows what the user publicly typed.")
        print("    Instagram does NOT reveal private phone numbers.")

if __name__ == "__main__":
    main()
