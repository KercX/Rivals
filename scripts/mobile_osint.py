#!/usr/bin/env python3
"""
Rivals - Mobile Device OSINT Intelligence
iOS & Android device fingerprinting and analysis
Author: KercX
"""

import json
import requests
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import argparse
import hashlib
from urllib.parse import quote_plus

class MobileOSINT:
    """Mobile device intelligence gathering"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "ios": {},
            "android": {},
            "device_links": []
        }
    
    # iOS/iTunes API endpoints
    ITUNES_API = "https://itunes.apple.com/lookup"
    APP_STORE_API = "https://itunes.apple.com/search"
    
    # Android/Google Play endpoints
    GOOGLE_PLAY_API = "https://play.google.com/store/apps/details"
    
    def lookup_apple_id(self, email: str) -> Dict:
        """Look up Apple ID / iCloud account"""
        try:
            # Using haveibeenpwned-like approach for Apple services
            # Note: This is for educational purposes
            
            # iTunes account lookup
            params = {"term": email, "entity": "all"}
            response = requests.get(self.ITUNES_API, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("resultCount", 0) > 0:
                    return {
                        "found": True,
                        "results": data.get("results", [])[:5],
                        "service": "iTunes/App Store"
                    }
            return {"found": False, "reason": "No associated account found"}
        except Exception as e:
            return {"found": False, "error": str(e)}
    
    def lookup_android_devices(self, gmail: str) -> Dict:
        """Look up Android/Google account information"""
        try:
            # Google account check via public endpoints
            results = []
            
            # Check Google+ (deprecated but may have archive)
            gplus_url = f"https://plus.google.com/+{quote_plus(gmail.split('@')[0])}"
            
            # Check Google Play Developer account
            dev_url = f"https://play.google.com/store/apps/dev?id={hashlib.md5(gmail.encode()).hexdigest()}"
            
            results.append({
                "type": "Google+ Legacy",
                "url": gplus_url,
                "note": "May be deprecated but can contain historical data"
            })
            
            return {
                "found": True,
                "devices": results,
                "associated_email": gmail
            }
        except Exception as e:
            return {"found": False, "error": str(e)}
    
    def check_imessage(self, phone_number: str) -> Dict:
        """Check if phone number supports iMessage"""
        # This would require Apple's internal APIs
        # For educational purposes - demonstrates concept
        return {
            "service": "iMessage",
            "phone": phone_number,
            "status": "unknown",
            "note": "Requires Apple Private API or MDM solution"
        }
    
    def find_sim_swap_risk(self, phone_number: str) -> Dict:
        """Check SIM swap vulnerability indicators"""
        # Check public breach databases
        # This is a placeholder for actual implementation
        return {
            "phone": phone_number,
            "risk_level": "unknown",
            "carrier": "detect_carrier(phone_number)",
            "recommendation": "Use carrier-specific protection"
        }
    
    def analyze_mobile_metadata(self, image_path: str) -> Dict:
        """Extract mobile device metadata from images"""
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
        
        metadata = {
            "device_make": None,
            "device_model": None,
            "software": None,
            "gps": None,
            "timestamp": None
        }
        
        try:
            img = Image.open(image_path)
            exif = img._getexif()
            
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    if tag == "Make":
                        metadata["device_make"] = value
                    elif tag == "Model":
                        metadata["device_model"] = value
                    elif tag == "Software":
                        metadata["software"] = value
                    elif tag == "DateTime":
                        metadata["timestamp"] = value
                    elif tag == "GPSInfo":
                        # Convert GPS coordinates
                        gps = {}
                        for gps_tag in value:
                            gps_name = GPSTAGS.get(gps_tag, gps_tag)
                            gps[gps_name] = value[gps_tag]
                        metadata["gps"] = self._convert_gps(gps)
                        
        except Exception as e:
            metadata["error"] = str(e)
        
        return metadata
    
    def _convert_gps(self, gps_data: Dict) -> Optional[Dict]:
        """Convert GPS coordinates to decimal degrees"""
        try:
            def to_degrees(value):
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)
            
            lat = to_degrees(gps_data.get("GPSLatitude", [0, 0, 0]))
            lon = to_degrees(gps_data.get("GPSLongitude", [0, 0, 0]))
            
            if gps_data.get("GPSLatitudeRef") == "S":
                lat = -lat
            if gps_data.get("GPSLongitudeRef") == "W":
                lon = -lon
                
            return {"latitude": lat, "longitude": lon}
        except:
            return None
    
    def search_public_bans(self, username: str) -> Dict:
        """Search for user in public mobile game bans"""
        # Game ban databases
        platforms = {
            "cod_mobile": f"https://codm.bans/{username}",
            "pubg_mobile": f"https://pubgm.bans/{username}",
            "free_fire": f"https://ff.bans/{username}"
        }
        
        results = {}
        for platform, url in platforms.items():
            try:
                # Placeholder - would need actual API
                results[platform] = {"checked": True, "url": url}
            except:
                results[platform] = {"checked": False, "error": "API unavailable"}
        
        return results
    
    def generate_mobile_report(self) -> str:
        """Generate comprehensive mobile OSINT report"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              MOBILE OSINT REPORT - RIVALS                     ║
║                     Generated by KercX                        ║
╚══════════════════════════════════════════════════════════════╝

📱 DEVICE INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Report Time: {self.results.get('timestamp', 'N/A')}

🍎 iOS/iCloud Findings:
"""
        ios = self.results.get("ios", {})
        for key, value in ios.items():
            report += f"  • {key}: {value}\n"
        
        report += """
🤖 Android/Google Findings:
"""
        android = self.results.get("android", {})
        for key, value in android.items():
            report += f"  • {key}: {value}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Generated by: Rivals Mobile OSINT Module
  Author: KercX | GitHub: @KercX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report

def main():
    parser = argparse.ArgumentParser(description='Rivals Mobile OSINT')
    parser.add_argument('--apple-id', help='Apple ID/email to lookup')
    parser.add_argument('--google', help='Gmail/Google account')
    parser.add_argument('--phone', help='Phone number to analyze')
    parser.add_argument('--image', help='Image file for metadata extraction')
    parser.add_argument('--username', help='Gaming username')
    
    args = parser.parse_args()
    
    mobile = MobileOSINT()
    
    if args.apple_id:
        result = mobile.lookup_apple_id(args.apple_id)
        mobile.results["ios"]["apple_id"] = result
        print(f"\n🍎 Apple ID Lookup for: {args.apple_id}")
        print(json.dumps(result, indent=2))
    
    if args.google:
        result = mobile.lookup_android_devices(args.google)
        mobile.results["android"]["google"] = result
        print(f"\n🤖 Google Account: {args.google}")
        print(json.dumps(result, indent=2))
    
    if args.phone:
        imessage = mobile.check_imessage(args.phone)
        sim_risk = mobile.find_sim_swap_risk(args.phone)
        mobile.results["ios"]["imessage"] = imessage
        mobile.results["android"]["sim_risk"] = sim_risk
        print(f"\n📞 Phone Analysis: {args.phone}")
        print(f"  iMessage: {imessage}")
        print(f"  SIM Swap Risk: {sim_risk}")
    
    if args.image:
        metadata = mobile.analyze_mobile_metadata(args.image)
        print(f"\n📸 Image Metadata:")
        print(json.dumps(metadata, indent=2))
    
    if args.username:
        bans = mobile.search_public_bans(args.username)
        print(f"\n🎮 Gaming Ban Check for: {args.username}")
        print(json.dumps(bans, indent=2))
    
    # Generate full report
    if any([args.apple_id, args.google, args.phone, args.image, args.username]):
        print(mobile.generate_mobile_report())

if __name__ == "__main__":
    main()
