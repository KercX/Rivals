#!/usr/bin/env python3
"""
Rivals - Professional Image Metadata Analyzer
Extracts EXIF, GPS, and embedded data from profile images
"""

import sys
import json
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import hashlib
from datetime import datetime
import argparse

class ImageAnalyzer:
    def __init__(self, username, image_url, timeout=10):
        self.username = username
        self.image_url = image_url
        self.timeout = timeout
        self.results = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "image_hash": None,
            "dimensions": None,
            "format": None,
            "exif_data": {},
            "gps_coordinates": None,
            "error": None
        }
    
    def download_image(self):
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.image_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except Exception as e:
            self.results["error"] = f"Download failed: {str(e)}"
            return None
    
    def calculate_hash(self, image_data):
        """Calculate SHA256 hash of image"""
        return hashlib.sha256(image_data).hexdigest()
    
    def analyze_image(self):
        """Extract metadata from image"""
        image_data = self.download_image()
        if not image_data:
            return self.results
        
        self.results["image_hash"] = self.calculate_hash(image_data)
        
        try:
            img = Image.open(io.BytesIO(image_data))
            self.results["dimensions"] = f"{img.width}x{img.height}"
            self.results["format"] = img.format
            
            # Extract EXIF data
            exif_data = img._getexif() if hasattr(img, '_getexif') else None
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    
                    # Handle GPS data
                    if tag_name == "GPSInfo":
                        gps = {}
                        for gps_tag in value:
                            sub_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                            gps[sub_tag_name] = value[gps_tag]
                        
                        self.results["gps_coordinates"] = self.convert_gps(gps)
                        self.results["exif_data"]["GPSInfo"] = gps
                    else:
                        # Convert bytes to string if needed
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except:
                                value = str(value)
                        self.results["exif_data"][tag_name] = value
        
        except Exception as e:
            self.results["error"] = f"EXIF extraction failed: {str(e)}"
        
        return self.results
    
    def convert_gps(self, gps_data):
        """Convert GPS coordinates from EXIF format to decimal degrees"""
        try:
            def convert_to_degrees(value):
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)
            
            lat = convert_to_degrees(gps_data.get("GPSLatitude", [0, 0, 0]))
            lon = convert_to_degrees(gps_data.get("GPSLongitude", [0, 0, 0]))
            
            if gps_data.get("GPSLatitudeRef") == "S":
                lat = -lat
            if gps_data.get("GPSLongitudeRef") == "W":
                lon = -lon
            
            return {"latitude": lat, "longitude": lon}
        except:
            return None

def main():
    parser = argparse.ArgumentParser(description='Rivals Image Metadata Analyzer')
    parser.add_argument('username', help='Target username')
    parser.add_argument('image_url', help='URL of profile image')
    parser.add_argument('--output', '-o', default='image_analysis.json', help='Output file')
    
    args = parser.parse_args()
    
    analyzer = ImageAnalyzer(args.username, args.image_url)
    results = analyzer.analyze_image()
    
    # Output results
    if results.get('gps_coordinates'):
        print(f"\n📍 GPS Coordinates found for @{args.username}:")
        print(f"   Latitude: {results['gps_coordinates']['latitude']}")
        print(f"   Longitude: {results['gps_coordinates']['longitude']}")
    
    if results.get('exif_data'):
        print(f"\n📸 Metadata extracted: {len(results['exif_data'])} fields")
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Analysis saved to: {args.output}")

if __name__ == "__main__":
    main()
