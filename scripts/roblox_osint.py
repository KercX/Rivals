#!/usr/bin/env python3
"""
Roblox Public OSINT – extracts ONLY public profile data.
No private info (phone/email) can be retrieved.
Author: KercX
"""

import requests
import sys
import json

def get_roblox_info(username):
    """Get public Roblox user information"""
    
    # First, get user ID from username
    user_api = f"https://api.roblox.com/users/get-by-username?username={username}"
    
    try:
        user_resp = requests.get(user_api, timeout=10)
        if user_resp.status_code != 200:
            return {"error": "User not found"}
        
        user_data = user_resp.json()
        user_id = user_data.get("Id")
        
        if not user_id:
            return {"error": "User ID not found"}
        
        # Now get profile details
        profile_api = f"https://users.roblox.com/v1/users/{user_id}"
        profile_resp = requests.get(profile_api, timeout=10)
        profile_data = profile_resp.json()
        
        # Get friends count
        friends_api = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
        friends_resp = requests.get(friends_api, timeout=10)
        friends_count = friends_resp.json().get("count", 0)
        
        # Get user's groups (first 5)
        groups_api = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
        groups_resp = requests.get(groups_api, timeout=10)
        groups_data = groups_resp.json()
        groups = [(g["group"]["name"], g["role"]["name"]) for g in groups_data.get("data", [])[:5]]
        
        result = {
            "username": profile_data.get("name"),
            "display_name": profile_data.get("displayName"),
            "description": profile_data.get("description"),
            "created": profile_data.get("created"),
            "is_banned": profile_data.get("isBanned", False),
            "friends_count": friends_count,
            "groups": groups,
            "profile_url": f"https://www.roblox.com/user.aspx?username={username}",
            "note": "Phone numbers and emails are NOT publicly accessible on Roblox"
        }
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python roblox_osint.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    data = get_roblox_info(username)
    
    if "error" in data:
        print(f"❌ {data['error']}")
    else:
        print(f"\n🎮 Roblox Profile: {data['username']}")
        print("=" * 50)
        print(f"Display name: {data['display_name']}")
        print(f"Bio: {data['description'] or '(empty)'}")
        print(f"Joined: {data['created']}")
        print(f"Friends: {data['friends_count']}")
        if data['groups']:
            print("Groups:")
            for name, role in data['groups']:
                print(f"  - {name} ({role})")
        print(f"\n🔗 {data['profile_url']}")
        print("\n⚠️  Phone number not available – Roblox keeps this private.")

if __name__ == "__main__":
    main()
