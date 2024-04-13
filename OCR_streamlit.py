import streamlit as st
import easyocr
import pandas as pd
import numpy as np
import mysql.connector

def fetch_data_and_transfer_to_mysql():
        # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="india123#",
        database="business_card"
    )

    cursor = conn.cursor()


    reader= easyocr.Reader(['en'])
    list1=[]
    list=['1.png','2.png', '3.png','4.png','5.png']


    def extract_info(entry):
        phone_number = ''
        email = ''

        lst2 = []
        
        for item in entry:
            bbox, text, confidence = item

            lst2.append(text)

            if any(char.isalpha() for char in text):  # Check if text contains alphabetic characters
                # print(text)
                if '@' in text:
                    email = text

            elif any(char.isdigit() for char in text) and ('+' in text or '-' in text):
                phone_number = text

        name = lst2[0]
        job_title = lst2[1]

        return name, job_title, phone_number, email


    for i in list:
        results = reader.readtext(i)
        name, job_title, phone_number, email = extract_info(results)

        print(name,job_title,phone_number,email)

        cursor.execute(f"INSERT INTO contacts (name, job_title, phone_number, email) VALUES ('{str(name)}', '{str(job_title)}', '{str(phone_number)}', '{str(email)}');")
        conn.commit()

    # Closing the cursor & connection
    cursor.close()
    conn.close()

def main():
    st.title("Data Extraction from Image using OCR")

    if st.button("Fetch Data and Transfer to MySQL"):
        fetch_data_and_transfer_to_mysql()
        st.success("Done!!!!")

if __name__ == "__main__":
    main()