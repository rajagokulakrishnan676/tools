import streamlit as st
import requests
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

class lookup:
    minute_requests = 0
    last_request_time = datetime.min

    @staticmethod
    def run():
        st.header("IP Address Query")

        query_type = st.radio("Select query type:", ["Single IP", "Multiple IP", "Upload File"])

        if query_type == "Single IP":
            lookup.handle_single_ip_query()
        elif query_type == "Multiple IP":
            lookup.handle_multiple_ip_query()
        elif query_type == "Upload File":
            lookup.handle_file_upload()

    @staticmethod
    def handle_single_ip_query():
        st.subheader("Single IP Query")
        ip_address = st.text_input("Enter IP Address or Domain", "")
        if st.button("Query"):
            if ip_address:
                result = lookup.perform_request(ip_address)
                if result:
                    lookup.display_ip_details(result)
                    lookup.display_ip_on_map([result])
            else:
                st.warning("Please enter an IP Address or Domain.")

    @staticmethod
    def handle_multiple_ip_query():
        st.subheader("Multiple IP Query")
        ip_addresses = st.text_area("Enter IP Addresses or Domains (one per line)", "")
        if st.button("Query"):
            results = []
            for line in ip_addresses.splitlines():
                result = lookup.perform_request(line.strip())
                if result:
                    results.append(result)
            lookup.display_multiple_ip_details(results)
            lookup.display_ip_on_map(results)
            

    @staticmethod
    def handle_file_upload():
        st.subheader("Upload File")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'IP Address' in df.columns:
                    ip_list = df['IP Address'].tolist()
                elif 'Domain' in df.columns:
                    ip_list = df['Domain'].tolist()
                else:
                    st.error("Column name 'IP Address' or 'Domain' not found in the uploaded file.")
                    return

                if st.button("Start Query"):
                    results = []
                    progress_bar = st.progress(0)
                    for i, ip in enumerate(ip_list):
                        result = lookup.perform_request(ip.strip())
                        if result:
                            results.append(result)
                        progress_bar.progress((i + 1) / len(ip_list))

                    progress_bar.empty()
                    lookup.display_multiple_ip_details(results)
                    lookup.display_ip_on_map(results)
                    lookup.enable_download_button(results)

            except Exception as e:
                st.error(f"Error: {e}")

    @staticmethod
    def perform_request(ip_address):
        if lookup.rate_limit_exceeded():
            st.warning("Rate limit exceeded. Please wait and try again later.")
            return None

        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            lookup.update_request_count()

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return data
                else:
                    st.error(f"Error fetching data for {ip_address}. Status message: {data['message']}")
                    return None
            else:
                st.error(f"Error fetching data for {ip_address}. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            return None

    @staticmethod
    def rate_limit_exceeded():
        now = datetime.now()
        if (now - lookup.last_request_time) < timedelta(seconds=60):
            if lookup.minute_requests >= 150:
                return True
        return False

    @staticmethod
    def update_request_count():
        now = datetime.now()
        if (now - lookup.last_request_time) >= timedelta(minutes=1):
            lookup.minute_requests = 0
        lookup.minute_requests += 1
        lookup.last_request_time = now

    @staticmethod
    def display_ip_details(data):
        st.subheader("Query Result:")
        details = {
            "IP Address": data.get('query', ''),
            "Country": data.get('country', ''),
            "Region": data.get('regionName', ''),
            "City": data.get('city', ''),
            "Latitude": data.get('lat', ''),
            "Longitude": data.get('lon', ''),
            "ISP": data.get('isp', ''),
            "Organization": data.get('org', '')
        }
        st.json(details)

    @staticmethod
    def display_multiple_ip_details(results):
        st.subheader("Query Results:")
        if not results:
            st.write("No results to display.")
            return

        data = []
        for result in results:
            if "Error" in result:
                data.append(result)
            else:
                details = {
                    "IP Address": result.get('query', ''),
                    "Country": result.get('country', ''),
                    "Region": result.get('regionName', ''),
                    "City": result.get('city', ''),
                    "Latitude": result.get('lat', ''),
                    "Longitude": result.get('lon', ''),
                    "ISP": result.get('isp', ''),
                    "Organization": result.get('org', '')
                }
                data.append(details)
        
        df = pd.DataFrame(data)
        st.dataframe(df)

    @staticmethod
    def enable_download_button(results):
        st.subheader("Download Results")
        download_data_txt = lookup.format_results_for_download(results, format='txt')
        download_data_csv = lookup.format_results_for_download(results, format='csv')

        st.download_button(
            label="Download results as TXT",
            data=download_data_txt,
            file_name="ip_query_results.txt",
            mime="text/plain"
        )

        st.download_button(
            label="Download results as CSV",
            data=download_data_csv,
            file_name="ip_query_results.csv",
            mime="text/csv"
        )

    @staticmethod
    def format_results_for_download(results, format='txt'):
        lines = []
        if format == 'txt':
            for result in results:
                if "Error" in result:
                    lines.append(f"{result['IP Address']}: {result['Error']}\n")
                else:
                    lines.append(
                        f"IP Address: {result.get('query', '')}\n"
                        f"Country: {result.get('country', '')}\n"
                        f"Region: {result.get('regionName', '')}\n"
                        f"City: {result.get('city', '')}\n"
                        f"Latitude: {result.get('lat', '')}\n"
                        f"Longitude: {result.get('lon', '')}\n"
                        f"ISP: {result.get('isp', '')}\n"
                        f"Organization: {result.get('org', '')}\n"
                        "----------------------------------------\n"
                    )
            return ''.join(lines)
        elif format == 'csv':
            columns = ["IP Address", "Country", "Region", "City", "Latitude", "Longitude", "ISP", "Organization"]
            csv_data = []
            for result in results:
                if "Error" not in result:
                    row = [result.get('query', ''),
                        result.get('country', ''),
                        result.get('regionName', ''),
                        result.get('city', ''),
                        result.get('lat', ''),
                        result.get('lon', ''),
                        result.get('isp', ''),
                        result.get('org', '')]
                    csv_data.append(row)

            df = pd.DataFrame(csv_data, columns=columns)
            return df.to_csv(index=False)

    @staticmethod
    def display_ip_on_map(ip_data):
        st.subheader("IP Address Locations on Map")
        map = folium.Map()

        for ip in ip_data:
            if "Error" not in ip:
                lat = ip.get('lat')
                lon = ip.get('lon')
                if lat and lon:
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"{ip['query']} - {ip['city']}, {ip['country']}"
                    ).add_to(map)

        html = map._repr_html_()

        st.components.v1.html(html, height=600, width=800)



