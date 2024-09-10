import requests
import json
import time
import streamlit as st
import cv2
import numpy as np
import re

API_KEY = '0382d237-4582-4a5b-9652-624c5e5066a2'

class phishing:
    @staticmethod
    def submit_url_for_scan(url):
        headers = {
            'API-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        data = {
            "url": url,
            "visibility": "public"
        }

        try:
            response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                uuid = result.get("uuid")
                return uuid
            else:
                st.error(f"Failed to submit URL for scanning. Status Code: {response.status_code}")
                st.error(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    @staticmethod
    def retrieve_scan_result(uuid, max_wait_time=120):
        result_url = f"https://urlscan.io/api/v1/result/{uuid}/"
        
        start_time = time.time()
        with st.spinner('Waiting for scan result...'):
            while True:
                response = requests.get(result_url)
                
                if response.status_code == 200:
                    scan_result = response.json()
                    verdict = scan_result.get('verdicts', {}).get('overall', {}).get('score', 0)
                    tags = scan_result.get('tags', [])
                    if verdict < 0 or 'phishing' in tags or 'malware' in tags:
                        return 'malicious'
                    else:
                        return 'safe'
                elif response.status_code == 404:
                    time.sleep(5)
                    if time.time() - start_time > max_wait_time:
                        return None
                else:
                    return None

    @staticmethod
    def analyze_qr_code(qr_image):
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(qr_image)
        if data:
            if phishing.contains_payment_identifier(data):
                if phishing.is_malicious_link(data):
                    return None, "The QR code contains a potentially harmful download link."
                else:
                    return data, "The QR code is safe and contains payment-related information."
            else:
                return None, "The QR code does not contain a recognized payment identifier."
        else:
            return None, "QR code not detected or is unreadable."

    @staticmethod
    def contains_payment_identifier(data):
        payment_keywords = ["@upi", "pay", "bank", "wallet", "payment"]
        return any(keyword in data.lower() for keyword in payment_keywords)

    @staticmethod
    def is_malicious_link(data):
        apk_pattern = r"(https?://[^\s]+\.apk)"
        if re.search(apk_pattern, data.lower()):
            return True
        return False

    def run(self):
        st.title("ADVANCED LINK CHECKER")

        option = st.radio("Select Check Type", ["URL Checker", "QR Code Checker"])

        if option == "URL Checker":
            url_to_scan = st.text_input("Enter the URL you want to scan for phishing")
            
            if st.button("Scan URL"):
                if url_to_scan:
                    if ".trycloudflare.com" in url_to_scan:
                        st.warning("The URL appears to be potentially malicious. Please report it to 1930.")
                    else:
                        uuid = self.submit_url_for_scan(url_to_scan)
                        
                        if uuid:
                            st.write("URL submission successful. UUID:", uuid)
                            with st.spinner('Retrieving scan result...'):
                                verdict = self.retrieve_scan_result(uuid)
                                
                            if verdict:
                                if verdict == 'malicious':
                                    st.error("The URL is likely malicious.")
                                else:
                                    st.success("The URL appears to be safe.")
                            else:
                                st.error("Failed to retrieve scan result.")
                        else:
                            st.error("Failed to submit URL for scanning.")
                else:
                    st.warning("Please enter a valid URL.")

        elif option == "QR Code Checker":
            st.write("Upload QR code image for scanning")
            uploaded_file = st.file_uploader("Choose a QR code image", type=["png", "jpg", "jpeg"])

            if uploaded_file is not None:
                img_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                qr_image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
                
                st.image(qr_image, caption='Uploaded QR Code', use_column_width=True)
                
                data, message = self.analyze_qr_code(qr_image)
                
                if data:
                    st.success(message)
                else:
                    st.error(f"Failed to process QR code: {message}")

def main():
    phish_instance = phishing()
    phish_instance.run()

if __name__ == '__main__':
    main()
