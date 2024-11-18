import streamlit as st
import pandas as pd
import bcrypt
from db import *

def main():
    st.title("Hospital Management System")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['user_id'] = None

    if not st.session_state['logged_in']:
       
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                user_info = verify_user(email, password)

                if user_info:
                    role, user_id = user_info
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = role
                    st.session_state['user_id'] = user_id
                    st.success(f"Successfully logged in as {role}")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['role'] = None
            st.session_state['user_id'] = None
            st.rerun()

        if st.session_state['role'] == 'admin':
            show_admin_interface()
        elif st.session_state['role'] == 'doctor':
            show_doctor_interface(st.session_state['user_id'])
        elif st.session_state['role'] == 'patient':
            show_patient_interface(st.session_state['user_id'])

def show_admin_interface():
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Doctors", "Patients", "Appointments", "Bills",
        "Medications", "Prescriptions", "Medical Records"
    ])

    with tab1:
        st.header("Doctors")
        option = st.selectbox("Select an option", ["Register Doctor", "Delete Doctor", "Doctors List"])
        if option == "Register Doctor":
            first_name = st.text_input("Doctor First Name")
            last_name = st.text_input("Doctor Last Name")
            phone_number = st.text_input("Doctor Phone Number")
            email = st.text_input("Doctor Email")
            dept_id = st.number_input("Department ID", min_value=1)
            password = st.text_input("Doctor Password", type="password")
            if st.button("Register as Doctor"):
                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'email': email,
                    'dept_id': dept_id,
                    'password': password
                }
                register_doctor(data)
                st.success("Doctor registered successfully.")
                first_name = ""
                last_name = ""
                phone_number = ""
                email = ""
                dept_id = 1
                password = ""
        elif option == "Delete Doctor":
            doctor_id = st.number_input("Doctor ID", min_value=0)
            if st.button("Delete Doctor"):
                delete_doctor(doctor_id)
                st.success("Doctor deleted successfully.")
                doctor_id = 0
        elif option == "Doctors List":
            doctors = get_all_doctors()
            if st.button("Get Doctors"):
                df = pd.DataFrame(doctors)
                st.dataframe(df)

    with tab2:
        st.header("Patients")
        option = st.selectbox("Select an option", ["Register Patient", "Delete Patient", "Patients List"])
        if option == "Register Patient":
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone_number = st.text_input("Phone Number")
            email = st.text_input("Email")
            address = st.text_input("Address")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'dob': dob,
                    'gender': gender,
                    'phone_number': phone_number,
                    'email': email,
                    'address': address,
                    'password': password
                }
                register_patient(data)
                st.success("Patient registered successfully.")
                first_name = ""
                last_name = ""
                dob = ""
                gender = ""
                phone_number = ""
                email = ""
                address = ""
                password = ""
        elif option == "Delete Patient":
            patient_id = st.number_input("Patient ID", min_value=0)
            if st.button("Delete"):
                delete_patient(patient_id)
                st.success("Patient deleted successfully.")
        elif option == "Patients List":
            patients = get_all_patients()
            if st.button("Get Patients"):
                df = pd.DataFrame(patients)
                st.dataframe(df)

    with tab3:
        st.header("Appointments")
        option = st.selectbox("Select an option", ["Create Appointment", "Update Appointment Date", "Update Appointment Time", "Update Appointment Status", "Delete Appointment", "Appointments List"])
        if option == "Create Appointment":
            patient_id = st.number_input("PatientID", min_value=0)
            doctor_id = st.number_input("DoctorID", min_value=0)
            date = st.date_input("Appointment Date")
            time = st.time_input("Appointment Time" )
            if st.button("Create Appointment"):
                data = {
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'date': date,
                    'time': time
                }
                create_apt(data)
                st.success("Appointment created successfully.")
                patient_id = 0
                doctor_id = 0
                date = None
                time = None
        elif option == "Update Appointment Date":
            apt_id = st.number_input("Appointment ID", min_value=0)
            date = st.date_input("New Appointment Date")
            if st.button("Update Appointment Date"):
                update_aptdate(date, apt_id)
                st.success("Appointment updated successfully.")
                apt_id = 0
                date = None
        elif option == "Update Appointment Time":
            apt_id = st.number_input("Appointment ID", min_value=0)
            time = st.time_input("New Appointment Time")
            if st.button("Update Appointment Time"):
                update_apttime(time, apt_id)
                st.success("Appointment updated successfully.")
                apt_id = 0
                time = None
        elif option == "Update Appointment Status":
            apt_id = st.number_input("Appointment ID", min_value=0)
            status = st.selectbox("New Appointment Status", ["Pending", "Completed"])
            if st.button("Update Appointment Status"):
                update_aptstatus(status, apt_id)
                st.success("Appointment status updated successfully.")
                apt_id = 0
                status = "Pending"
        elif option == "Delete Appointment":
            apt_id = st.number_input("Appointment ID", min_value=0)
            if st.button("Delete Appointment"):
                delete_apt(apt_id)
                st.success("Appointment deleted successfully.")
                apt_id = 0
        elif option == "Appointments List":
            appointments = get_all_apts()
            if st.button("Get Appointments"):
                df = pd.DataFrame(appointments)
                st.dataframe(df)

    with tab4:
        st.header("Bills")
        option = st.selectbox("Select an option", ["Create Bill", "Update Bill Amount", "Update Bill Status", "Get All Bills", "Get Total Amount"])
        if option == "Create Bill":
            create_patient_id = st.number_input("Patient ID", min_value=0, key="create_patient_id")
            bill_date = st.date_input("Bill Date")
            payment_status = st.selectbox("Payment Status", ["Unpaid","Partial", "Paid"])
            amount = st.number_input("Amount", min_value=0.0, key="create_amount")
            if st.button("Create Bill"):
                data = {
                    'patient_id': create_patient_id,
                    'bill_date': bill_date,
                    'payment_status': payment_status,
                    'amount': amount
                }
                create_bill(data)
                st.success("Bill created successfully.")
                create_patient_id = 0
                bill_date = None
                payment_status = "Unpaid"
                amount = 0.0
        elif option == "Update Bill Amount":
            update_bill_id = st.number_input("Bill ID", min_value=0, key="update_bill_id")
            new_amount = st.number_input("New Amount", min_value=0.0, key="update_amount")
            if st.button("Update Bill Amount"):
                update_amount(update_bill_id, new_amount)
                st.success("Bill amount updated successfully.")
                update_bill_id = 0
                new_amount = 0.0
        elif option == "Update Bill Status":
            update_status_bill_id = st.number_input("Bill ID", min_value=0, key="update_status_bill_id")
            status = st.selectbox("New Payment Status", ["Paid", "Unpaid"])
            if st.button("Update Bill Status"):
                update_status(update_status_bill_id, status)
                st.success("Bill status updated successfully.")
                update_status_bill_id = 0
                status = "Unpaid"
        elif option == "Get All Bills":
            if st.button("Get All Bills"):
                bills = get_all_bills()
                if bills:
                    df = pd.DataFrame(bills)
                    st.dataframe(df)
        elif option == "Get Total Amount":
            total_patient_id = st.number_input("Patient_ID", min_value=0, key="total_patient_id")
            if st.button("Get Total Amount"):
                total = get_totals(total_patient_id)
                st.write("Total amount:"f"{total}")

    with tab5:
        st.header("Medications")
        meds = get_medicines()
        if meds:
            df = pd.DataFrame(meds)
            st.dataframe(df)
        st.subheader("Add a new medicine")
        name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        price = st.number_input("Price", min_value=0.0)
        if st.button("Add Medicine"):
            data = {
                'name': name,
                'dosage': dosage,
                'price': price
            }
            add_medicine(data)
            st.success("Medicine added successfully.")
            name = ""
            dosage = ""
            price = 0.0
        st.subheader("Update medicine price")
        med_id = st.number_input("Medicine ID", min_value=0)
        new_price = st.number_input("New Price", min_value=0.0)
        if st.button("Update Price"):
            update_price(med_id, new_price)
            st.success("Medicine price updated successfully.")
            med_id = 0
            new_price = 0.0
        st.subheader("Delete a medicine")
        med_id = st.number_input("MEDICINE ID", min_value=0)
        if st.button("Delete Medicine"):
            delete_medicine(med_id)
            st.success("Medicine deleted successfully.")
            med_id = 0
        st.subheader("Update medicine dosage")
        med_id = st.number_input("Medicine id", min_value=0)
        new_dosage = st.text_input("New Dosage")
        if st.button("Update Dosage"):
            update_dosage(med_id, new_dosage)
            st.success("Medicine dosage updated successfully.")
            med_id = 0
            new_dosage = ""

    with tab6:
        st.header("Prescriptions")
        functionality = st.selectbox("Select a functionality", ["Create Prescription", "Get Prescription", "Update Quantity", "Update End Date"])
        if functionality == "Create Prescription":
            st.subheader("Create a new prescription")
            record_id = st.number_input("Medical Record ID", min_value=0)
            medicine_id = st.number_input("medicine id", min_value=0)
            quantity = st.number_input("Quantity", min_value=0)
            frequency = st.text_input("Frequency")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            prescription_ID = st.number_input("Prescription ID", min_value=0)
            if st.button("Create Prescription"):
                data = {
                    'record_id': record_id,
                    'medicine_id': medicine_id,
                    'quantity': quantity,
                    'frequency': frequency,
                    'start_date': start_date,
                    'end_date': end_date,
                    'prescription_ID': prescription_ID
                }
                create_prescription(data)
                st.success("Prescription created successfully.")
                record_id = 0
                medicine_id = 0
                quantity = 0
                frequency = None
                start_date = None
                end_date = None
                prescription_ID = 0
        elif functionality == "Get Prescription":
            st.subheader("Get a prescription")
            record_id = st.number_input("Medical Record ID", min_value=0)
            medicine_id = st.number_input("MEDICINE Id", min_value=0)
            if st.button("Get Prescription"):
               p = get_prescription(record_id, medicine_id)
               if p:
                df = pd.DataFrame(p)
                st.dataframe(df)
        elif functionality == "Update Quantity":
            st.subheader("Update medicine quantity")
            record_id = st.number_input("Medical Record Id", min_value=0)
            medicine_id = st.number_input("Medicine Id", min_value=0)
            quantity = st.number_input("New Quantity", min_value=0)
            if st.button("Update Quantity"):
                update_quantity(record_id, medicine_id, quantity)
                st.success("Medicine quantity updated successfully.")
                record_id = 0
                medicine_id = 0
                quantity = 0
        elif functionality == "Update End Date":
            st.subheader("Update end date")
            record_id = st.number_input("Medical Record id", min_value=0)
            medicine_id = st.number_input("MEDICINe id", min_value=0)
            end_date = st.date_input("New End Date")
            if st.button("Update End Date"):
                update_end_date(record_id, medicine_id, end_date)
                st.success("End date updated successfully.")
                record_id = 0
                medicine_id = 0
                end_date = None

    with tab7:
        st.header("Medical Records")
        records = get_all_records()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.write("No medical records found.")
        st.subheader("Create a new medical record")
        patient_id = st.number_input("Patient_ID", min_value=0)
        doctor_id = st.number_input("Doctor_ID", min_value=0)
        date = st.date_input("Record Date")
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")
        if st.button("Create Record"):
            data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'date': date,
                'diagnosis': diagnosis,
                'treatment': treatment
            }
            create_record(data)
            st.success("Record created successfully.")
            patient_id = 0
            doctor_id = 0
            date = None
            diagnosis = ""
            treatment = ""
        st.subheader("Update diagnosis")
        record_id = st.number_input("Record ID", min_value=0)
        diagnosis = st.text_area("New Diagnosis")
        if st.button("Update Diagnosis"):
            update_diagnosis(record_id, diagnosis)
            st.success("Diagnosis updated successfully.")
            record_id = 0
            diagnosis = ""
        st.subheader("Update treatment")
        record_id = st.number_input("Record_ID", min_value=0)
        treatment = st.text_area("New Treatment")
        if st.button("Update Treatment"):
            update_treatment(record_id, treatment)
            st.success("Treatment updated successfully.")
            record_id = 0
            treatment = ""

def show_doctor_interface(doctor_id):
    tab1, tab2, tab3 = st.tabs(["My Appointments", "Patient Records", "Prescriptions"])

    with tab1:
        st.header("My Appointments")
        appointments = get_doctor_appointments(doctor_id)
        if appointments:
            df = pd.DataFrame(appointments)
            st.dataframe(df)

    with tab2:
        st.header("Patient Records")
        patient_id = st.number_input("Enter Patient ID", min_value=1)
        if st.button("View Records"):
            records = get_patient_records_for_doctor(doctor_id, patient_id)
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df)

    with tab3:
        st.header("Prescriptions")
        functionality = st.selectbox("Select a functionality", ["Create Prescription", "Get Prescription", "Update Quantity", "Update End Date"])
        if functionality == "Create Prescription":
            st.subheader("Create a new prescription")
            record_id = st.number_input("Medical Record ID", min_value=0)
            medicine_id = st.number_input("medicine id", min_value=0)
            quantity = st.number_input("Quantity", min_value=0)
            frequency = st.text_input("Frequency")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            prescription_ID = st.number_input("Prescription ID", min_value=0)
            if st.button("Create Prescription"):
                data = {
                    'record_id': record_id,
                    'medicine_id': medicine_id,
                    'quantity': quantity,
                    'frequency': frequency,
                    'start_date': start_date,
                    'end_date': end_date,
                    'prescription_ID': prescription_ID
                }
                create_prescription(data)
                st.success("Prescription created successfully.")
                record_id = 0
                medicine_id = 0
                quantity = 0
                frequency = None
                start_date = None
                end_date = None
                prescription_ID = 0

def show_patient_interface(patient_id):
    tab1, tab2, tab3 = st.tabs(["My Appointments", "Medical Records", "Bills"])

    with tab1:
        st.header("My Appointments")
        appointments = get_patient_appointments(patient_id)
        if appointments:
            df = pd.DataFrame(appointments)
            st.dataframe(df)

        st.subheader("Book New Appointment")
        with st.form("book_appointment"):
            doctor_id = st.number_input("Doctor ID", min_value=1)
            date = st.date_input("Appointment Date")
            time = st.time_input("Appointment Time")
            if st.form_submit_button("Book Appointment"):
                create_apt({
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'date': date,
                    'time': time
                })
                st.success("Appointment booked successfully!")

    with tab2:
        st.header("My Medical Records")
        records = get_medical_records(patient_id)
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)

    with tab3:
        st.header("My Bills")
        bills = get_bills(patient_id)
        if bills:
            df = pd.DataFrame(bills)
            st.dataframe(df)

        total = get_totals(patient_id)
        st.info(f"Total outstanding amount: ${total}")

main()
