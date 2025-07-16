import qrcode

app_url = "https://arise-service.streamlit.app/"
img = qrcode.make(app_url)
img.save("streamlit_app_qr.png")
print("QR code saved")