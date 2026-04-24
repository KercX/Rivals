#!/usr/bin/env python3
"""
Discord Public OSINT – requires User ID.
No private info (phone/email) can be retrieved.
Author: KercX
"""

import requests
import sys
import json

def get_discord_info(user_id):
    """
    Get public Discord user information.
    Note: Discord API requires authentication for most endpoints.
    This uses public-facing embed/cdn data only.
    """
    
    # Discord CDN avatar URL (public if user has avatar)
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/" + "{avatar_hash}.png"
    
    # Discord's user profile widget (if user has enabled)
    widget_api = f"https://api.discordstatus.com/users/{user_id}"
    
    # Alternative: use Discord's embed endpoint (no auth required for basic info)
    embed_preview = f"https://discord.com/users/{user_id}"
    
    try:
        # Fetch the user's profile page (this only gives what's public in embed)
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(embed_preview, headers=headers, timeout=10)
        
        # Parse for basic info (username, discriminator, banner)
        # This is limited because Discord requires OAuth for detailed data
        import re
        
        # Search for username in page source (very hacky, but only way without bot token)
        content = resp.text
        
        # Modern Discord usernames (without discriminator)
        username_match = re.search(r'<title>(.+?)</title>', content)
        username = username_match.group(1).replace(" - Discord", "") if username_match else user_id
        
        # Check if profile exists (non-404)
        if resp.status_code == 404:
            return {"error": "User not found or invalid ID"}
        
        result = {
            "user_id": user_id,
            "username": username,
            "profile_url": embed_preview,
            "avatar_url": f"https://cdn.discordapp.com/avatars/{user_id}/1.png" + "?size=256",
            "note": "Phone numbers and emails are NEVER public on Discord.",
            "limitations": "Full data requires Discord Bot token or OAuth2 authorization."
        }
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

def get_discord_by_username(username_with_discriminator):
    """
    Convert username#discriminator to user ID via Discord API.
    Requires bot token (not included for legal reasons).
    """
    return {"error": "Username to ID conversion requires Discord Bot token. Use User ID directly."}

def main():
    if len(sys.argv) < 2:
        print("Usage: python discord_osint.py <user_id>")
        print("Example: python discord_osint.py 123456789012345678")
        print("\nNote: You need the USER ID (right-click user -> Copy ID) with Developer Mode enabled.")
        sys.exit(1)
    
    user_id = sys.argv[1]
    data = get_discord_info(user_id)
    
    if "error" in data:
        print(f"❌ {data['error']}")
    else:
        print(f"\n💬 Discord Profile (ID: {data['user_id']})")
        print("=" * 50)
        print(f"Username: {data['username']}")
        print(f"Profile URL: {data['profile_url']}")
        print(f"Avatar URL: {data['avatar_url']}")
        print(f"\n⚠️  {data['note']}")
        print(f"📌 {data['limitations']}")

if __name__ == "__main__":
    main()
