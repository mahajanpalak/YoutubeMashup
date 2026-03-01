import streamlit as st
import os
import zipfile
import smtplib
from email.message import EmailMessage
from mashup import download_videos, process_audios, merge_audios
st.title("🎵 Mashup Generator Web App")

singer = st.text_input("Enter Singer Name")
num_videos = st.number_input("Number of Videos (>10)", min_value=11)
duration = st.number_input("Duration in seconds (>20)", min_value=21)
email = st.text_input("Enter Email ID")

if st.button("Generate Mashup"):

    if not singer or not email:
        st.error("Please fill all fields.")
    else:
        try:
            download_videos(singer, num_videos)
            clips = process_audios(duration, num_videos)
            output_file = "web_output.mp3"
            merge_audios(clips, output_file)

            # Create ZIP
            zip_filename = "mashup.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                zipf.write(os.path.join("output", output_file))

            # Send Email
            msg = EmailMessage()
            msg['Subject'] = 'Your Mashup File'
            msg['From'] = "your_email@gmail.com"
            msg['To'] = email
            msg.set_content("Attached is your mashup file.")

            with open(zip_filename, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application',
                                   subtype='zip', filename=zip_filename)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("your_email@gmail.com", "your_app_password")
                smtp.send_message(msg)

            st.success("Mashup sent successfully!")

        except Exception as e:
            st.error(f"Error: {e}")