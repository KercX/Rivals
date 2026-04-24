#!/usr/bin/env python3
"""
Fortnite Public OSINT
Retrieves public stats (wins, kills, etc.) via official Epic Games API.
Requires free API key from https://fortnite-api.com (no auth needed for basic)
Also fetches current cosmetics/skins if available.
No phone numbers or emails – only public game data.
"""

import requests
import sys
import json

class FortniteOSINT:
    def __init__(self, api_key=None):
        # Free API from https://fortnite-api.com (no key needed for public endpoints)
        self.base_url = "https://fortnite-api.com/v2"
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": api_key})
    
    def get_player_stats(self, username, platform="epic"):
        """
        Get public stats for a Fortnite player.
        platform: 'epic' (default), 'psn', 'xbl'
        """
        # Step 1: Find player account ID
        lookup_url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}&accountType={platform}"
        resp = self.session.get(lookup_url)
        
        if resp.status_code == 404:
            return {"error": f"Player '{username}' not found on {platform}"}
        if resp.status_code != 200:
            return {"error": f"API error: {resp.status_code}"}
        
        data = resp.json()
        if data.get("status") != 200:
            return {"error": data.get("error", "Unknown error")}
        
        stats_data = data.get("data", {})
        account = stats_data.get("account", {})
        battle_pass = stats_data.get("battlePass", {})
        stats = stats_data.get("stats", {})
        
        # All-time stats (simplified)
        all_time = stats.get("all", {})
        overall = all_time.get("overall", {})
        
        result = {
            "username": username,
            "platform": platform,
            "account_id": account.get("id"),
            "name_history": account.get("nameHistory", [])[:5],
            "battle_pass": {
                "level": battle_pass.get("level"),
                "progress": battle_pass.get("progress")
            },
            "stats": {
                "wins": overall.get("wins", 0),
                "kills": overall.get("kills", 0),
                "matches_played": overall.get("matches", 0),
                "win_rate": round(overall.get("winRate", 0), 2),
                "kdr": round(overall.get("kd", 0), 2)
            },
            "profile_url": f"https://fortnite.gg/profile/{username}",
            "note": "Phone numbers are never public on Fortnite."
        }
        return result
    
    def get_current_shop(self):
        """Get current item shop (cosmetics) – not user-specific but useful context"""
        url = f"{self.base_url}/shop/br/combined"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("data", {}).get("featured", [])[:10]
            return [{"name": i.get("devName"), "price": i.get("price")} for i in items]
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python fortnite_osint.py <username> [platform]")
        print("Platforms: epic (default), psn, xbl")
        sys.exit(1)
    
    username = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else "epic"
    
    scanner = FortniteOSINT()
    data = scanner.get_player_stats(username, platform)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
