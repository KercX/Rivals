#!/usr/bin/env python3
"""
Advanced Roblox Public OSINT
Extracts public inventory, badges, groups, friends, and more.
No private data (phone/email) – all from Roblox public APIs.
"""

import requests
import sys
import json
from datetime import datetime

class RobloxOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RobloxOSINT/1.0"})
    
    def get_user_id(self, username):
        url = f"https://api.roblox.com/users/get-by-username?username={username}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("Id")
        return None
    
    def get_profile_info(self, user_id):
        url = f"https://users.roblox.com/v1/users/{user_id}"
        resp = self.session.get(url)
        return resp.json() if resp.status_code == 200 else {}
    
    def get_friends_count(self, user_id):
        url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
        resp = self.session.get(url)
        return resp.json().get("count", 0) if resp.status_code == 200 else 0
    
    def get_friends_list(self, user_id, limit=20):
        """Public friends list (only those who have it public)"""
        url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
        params = {"limit": limit, "userSort": "1"}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return [{"name": f["name"], "id": f["id"]} for f in data.get("data", [])]
        return []
    
    def get_followers(self, user_id, limit=10):
        url = f"https://friends.roblox.com/v1/users/{user_id}/followers"
        params = {"limit": limit}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            return resp.json().get("data", [])
        return []
    
    def get_following(self, user_id, limit=10):
        url = f"https://friends.roblox.com/v1/users/{user_id}/followings"
        params = {"limit": limit}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            return resp.json().get("data", [])
        return []
    
    def get_groups(self, user_id):
        url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return [{"name": g["group"]["name"], "role": g["role"]["name"], "id": g["group"]["id"]} for g in data.get("data", [])]
        return []
    
    def get_inventory(self, user_id, asset_type="Asset", limit=10):
        """Public inventory (limited to certain asset types)"""
        # Roblox has public catalog API for users' items
        url = f"https://catalog.roblox.com/v1/search/items"
        params = {"category": "All", "creatorName": f"userid-{user_id}", "limit": limit, "sortType": "3"}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            items = resp.json().get("data", [])
            return [{"name": i["name"], "id": i["id"], "type": i.get("itemType")} for i in items]
        return []
    
    def get_badges(self, user_id, limit=20):
        """Public badges earned by user"""
        url = f"https://badges.roblox.com/v1/users/{user_id}/badges"
        params = {"limit": limit, "sortOrder": "Asc"}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return [{"name": b["name"], "id": b["id"]} for b in data.get("data", [])]
        return []
    
    def get_favorite_games(self, user_id, limit=10):
        """Public favorites (games)"""
        url = f"https://games.roblox.com/v1/users/{user_id}/favorites/games"
        params = {"limit": limit}
        resp = self.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return [{"name": g["name"], "id": g["id"], "placeVisits": g.get("placeVisits", 0)} for g in data.get("data", [])]
        return []
    
    def get_trade_status(self, user_id):
        """Public trade summary (if user has open trades)"""
        url = f"https://trades.roblox.com/v1/trades/summary/{user_id}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            return resp.json()
        return None
    
    def full_scan(self, username):
        user_id = self.get_user_id(username)
        if not user_id:
            return {"error": f"User {username} not found"}
        
        profile = self.get_profile_info(user_id)
        return {
            "username": username,
            "user_id": user_id,
            "display_name": profile.get("displayName"),
            "description": profile.get("description"),
            "created": profile.get("created"),
            "is_banned": profile.get("isBanned", False),
            "external_apps": profile.get("externalAppDisplayName"),
            "friends_count": self.get_friends_count(user_id),
            "friends_sample": self.get_friends_list(user_id, limit=10),
            "followers_count": len(self.get_followers(user_id, 1)) or "?",
            "groups": self.get_groups(user_id),
            "inventory_sample": self.get_inventory(user_id, limit=10),
            "badges_sample": self.get_badges(user_id, limit=10),
            "favorite_games": self.get_favorite_games(user_id, limit=5),
            "profile_url": f"https://www.roblox.com/user.aspx?username={username}",
            "note": "Phone numbers and emails are never public on Roblox."
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python roblox_advanced.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    scanner = RobloxOSINT()
    data = scanner.full_scan(username)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
