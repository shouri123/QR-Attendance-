import qrcode

# Create QR code for stopping and sending the sheet
stop_url = "http://192.168.0.107:5000/scan?code=STOP_SCAN"  # Replace IP with your computer's IP address

# Generate QR code
img = qrcode.make(stop_url)

# Save the QR code
img.save("stop_qr.png")
print("Stop QR code generated successfully!")

