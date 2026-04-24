#!/usr/bin/env python3
"""
Minecraft Public OSINT
Retrieves UUID, skin, name history, and optional servers.
No private data (phone/email) – all from Mojang API.
"""

import requests
import sys
import json
from datetime import datetime

class MinecraftOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "MinecraftOSINT/1.0"})
    
    def get_uuid(self, username):
        """Convert username to UUID (Java edition)"""
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("id"), data.get("name")
        return None, None
    
    def get_name_history(self, uuid):
        """Get all previous usernames"""
        url = f"https://api.mojang.com/user/profiles/{uuid}/names"
        resp = self.session.get(url)
        if resp.status_code == 200:
            names = resp.json()
            return [{"name": n["name"], "changed_at": n.get("changedToAt")} for n in names]
        return []
    
    def get_skin(self, uuid):
        """Get skin URL and model type"""
        url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            data = resp.json()
            properties = data.get("properties", [])
            for prop in properties:
                if prop.get("name") == "textures":
                    import base64
                    decoded = base64.b64decode(prop.get("value")).decode('utf-8')
                    import json as json_lib
                    texture_data = json_lib.loads(decoded)
                    skin_url = texture_data.get("textures", {}).get("SKIN", {}).get("url")
                    return skin_url
        return None
    
    def get_bedrock_gamertag(self, xuid):
        """Convert Xbox User ID (XUID) to gamertag (requires Xbox API – limited)"""
        # This is complex; fallback to manual input
        return None
    
    def get_server_status(self, server_ip, port=25565):
        """Ping a Minecraft server (Java) to see if it's online (optional)"""
        # Not implemented fully – requires socket
        pass
    
    def full_scan(self, username):
        uuid, current_name = self.get_uuid(username)
        if not uuid:
            return {"error": f"Username '{username}' not found (Java edition)"}
        
        name_history = self.get_name_history(uuid)
        skin_url = self.get_skin(uuid)
        
        return {
            "current_username": current_name,
            "uuid": uuid,
            "name_history": name_history,
            "skin_url": skin_url,
            "profile_url_java": f"https://namemc.com/profile/{current_name}",
            "profile_url_bedrock": f"https://xboxgamertag.com/search/{current_name}",
            "note": "Phone numbers and emails are NEVER public on Minecraft."
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python minecraft_osint.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    scanner = MinecraftOSINT()
    data = scanner.full_scan(username)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
