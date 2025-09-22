import os
import requests
import ctypes
from datetime import datetime
from pathlib import Path

def get_bing_wallpaper_url():
    response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    response.raise_for_status()
    data = response.json()
    image_url = "https://www.bing.com" + data["images"][0]["url"]
    return image_url

def download_image(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)

def set_wallpaper(image_path):
    # SPI_SETDESKWALLPAPER = 20
    # Update INI file = 3
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 3)

def main():
    image_url = get_bing_wallpaper_url()
    today = datetime.now().strftime("%Y-%m-%d")
    save_dir = Path.home() / "Pictures" / "BingWallpapers"
    save_dir.mkdir(parents=True, exist_ok=True)
    image_path = save_dir / f"bing_{today}.jpg"

    if not image_path.exists():
        download_image(image_url, image_path)
        print(f"Downloaded wallpaper to {image_path}")
    else:
        print(f"Wallpaper for today already downloaded: {image_path}")

    set_wallpaper(image_path)
    print("Wallpaper set!")

if __name__ == "__main__":
    main()
