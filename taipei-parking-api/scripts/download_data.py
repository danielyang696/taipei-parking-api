from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json"
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "parking_lots.json"

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as response:
        data = response.read()
    OUTPUT.write_bytes(data)
    print(f"Downloaded {len(data):,} bytes -> {OUTPUT}")

if __name__ == "__main__":
    main()
