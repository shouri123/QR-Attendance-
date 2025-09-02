# 📌 Smart Attendance System with QR Code

A Flask-based smart attendance system that uses **QR codes** to mark student attendance in real time and integrates with **Google Sheets** to automatically update records.  

👉 The unique part? Once attendance is done, scanning the **STOP QR** will stop the process and trigger an email with the **latest updated Google Sheet** attached.  

---

## ✨ Features  

- 📱 **QR-based Attendance** – Each student has a unique QR code.  
- 🌐 **Flask Web App** – Simple and lightweight backend.  
- 📊 **Google Sheets Integration** – Attendance data is stored directly in Google Sheets.  
- 📧 **Email Notifications** – Automatically sends the updated Google Sheet after attendance.  
- 🛑 **STOP QR Feature** – End attendance session by scanning a special STOP QR code.  
- 🎯 **User-Friendly Workflow** – Easy scanning, browser confirmation, and instant updates.  

---

## 🛠 Tech Stack  

- **Backend**: Flask (Python)  
- **Frontend**: HTML Templates (Jinja2, Bootstrap/Tailwind optional)  
- **Database**: Google Sheets (via Google API)  
- **Email Service**: SMTP (Gmail / custom config)  
- **Hosting (Planned)**: Render  

---

## 🚀 How it Works  

1. **Scan Student QR Code**  
   - Each student’s QR code contains their unique link.  
   - Open the link in a browser → attendance is marked in Google Sheet.  

2. **Attendance Confirmation**  
   - After scanning, you’ll see a web page confirming that attendance has been recorded.  

3. **Repeat for All Students**  
   - Continue scanning each student’s QR code until all are marked.  

4. **Scan STOP QR** 🛑  
   - Once all students are marked, scan the special **STOP QR code**.  
   - This will stop the attendance process.  

5. **Email Sent Automatically**  
   - The system sends an email with the **updated Google Sheet** attached.  
   - You can download and view the attendance directly from your inbox.  

---

## ⚙️ Setup & Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/shouri123/QR-Attendance-.git
   cd QR-Attendance-
