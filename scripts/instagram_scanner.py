#!/usr/bin/env python3
"""
Advanced Instagram Public OSINT
Extracts all PUBLIC data (no private phone/email).
Uses official Instagram Graph API via RapidAPI (free tier) or public scraping.
For reliability, use RapidAPI (no login required).
"""

import requests
import json
import sys
from datetime import datetime

class InstagramOSINT:
    def __init__(self, rapidapi_key=None):
        """
        Optional: Provide RapidAPI key for higher reliability.
        Get free key from https://rapidapi.com/rockethearts/api/instagram48/
        """
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://instagram48.p.rapidapi.com/"
    
    def get_profile_public(self, username):
        """Fetch public profile info via RapidAPI (if key provided)"""
        if not self.rapidapi_key:
            return self._scrape_profile(username)  # fallback to scraping
        
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "instagram48.p.rapidapi.com"
        }
        url = f"{self.base_url}get_user_info?username={username}"
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            return self._parse_api_data(data)
        except Exception as e:
            return {"error": f"API error: {e}"}
    
    def _parse_api_data(self, data):
        user = data.get("data", {}).get("user", {})
        edge = user.get("edge_followed_by", {})
        return {
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "bio": user.get("biography"),
            "external_url": user.get("external_url"),
            "followers": edge.get("count", 0),
            "following": user.get("edge_follow", {}).get("count", 0),
            "posts": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "is_private": user.get("is_private", False),
            "is_verified": user.get("is_verified", False),
            "business_category": user.get("business_category_name"),
            "profile_pic": user.get("profile_pic_url_hd"),
            "recent_hashtags": self._extract_hashtags(user.get("biography", "")),
            "emails_in_bio": self._extract_emails(user.get("biography", "")),
            "phones_in_bio": self._extract_phones(user.get("biography", "")),
            "profile_url": f"https://instagram.com/{user.get('username')}"
        }
    
    def _scrape_profile(self, username):
        """Fallback: scrape public page (no API) – limited data"""
        try:
            from bs4 import BeautifulSoup
            url = f"https://www.instagram.com/{username}/"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                return {"error": "Profile not found or private"}
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            meta_desc = soup.find("meta", attrs={"name": "description"})
            bio = meta_desc.get("content", "") if meta_desc else ""
            return {
                "username": username,
                "bio": bio.split(".")[0],
                "followers": self._extract_number(bio, "Followers"),
                "following": self._extract_number(bio, "Following"),
                "posts": self._extract_number(bio, "Posts"),
                "profile_url": url,
                "note": "Limited data – use RapidAPI for full info"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_number(self, text, keyword):
        import re
        pattern = rf'(\d+[.,]?\d*[KMB]?)\s*{keyword}'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return "N/A"
    
    def _extract_hashtags(self, text):
        import re
        return re.findall(r'#\w+', text)
    
    def _extract_emails(self, text):
        import re
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)
    
    def _extract_phones(self, text):
        import re
        pattern = r'[\+\(]?[0-9]{1,4}[\)\-\s]?[0-9]{6,12}'
        return re.findall(pattern, text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python instagram_advanced.py <username> [rapidapi_key]")
        sys.exit(1)
    
    username = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    scanner = InstagramOSINT(rapidapi_key=api_key)
    data = scanner.get_profile_public(username)
    
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
