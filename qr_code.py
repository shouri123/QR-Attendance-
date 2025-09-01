import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Load Excel file
df = pd.read_excel("Claas 6 Attendance.xlsx")  # Make sure your file is named correctly

# Create output folder
os.makedirs("qr_codes", exist_ok=True)

# Load a font
try:
    font = ImageFont.truetype("arial.ttf", size=18)
except:
    font = ImageFont.load_default()

for index, row in df.iterrows():
    name = str(row["name"])
    roll = str(row["roll"])
    section = str(row["section"])

    # Data encoded in QR
    data = f"http://localhost:5000/checkin?name={name}&id={roll}&section={section}"

    # Generate QR
    qr = qrcode.make(data)
    qr = qr.resize((300, 300))

    # Create image with space for text
    img_with_text = Image.new("RGB", (300, 360), "white")
    img_with_text.paste(qr, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(img_with_text)
    text = f"{name}\nRoll: {roll} | Section: {section}"
    draw.text((10, 310), text, font=font, fill="black")

    # Save QR code
    filename = f"qr_codes/{name.replace(' ', '_')}_{roll}.png"
    img_with_text.save(filename)

    print(f"✅ Saved: {filename}")
