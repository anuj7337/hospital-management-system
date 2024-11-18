import pymysql
import bcrypt

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Ajwin2008',
        database='hdb',
        cursorclass=pymysql.cursors.DictCursor
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)

def verify_user(email, password):
    connection = get_connection()
    if email == "Admin" and password == "Admin":
        return "admin", 0
    try:
        with connection.cursor() as cursor:
            query = "SELECT password, role, user_id FROM Users WHERE username = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result and verify_password(password, result['password']):
                return result['role'], result['user_id']
            return None
    finally:
        connection.close()

def delete_user(email):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Users WHERE username = %s"
            cursor.execute(sql, (email,))
            connection.commit()
            print("User deleted successfully.")
    finally:
        connection.close()

def create_apt(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO appointments (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (data['patient_id'], data['doctor_id'], data['date'], data['time']))
            connection.commit()
            print("Appointment created successfully.")
    finally:
        connection.close()

def update_aptdate(date, apt_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE appointments
                SET Appointment_Date = %s
                WHERE Appointment_ID = %s
            """
            cursor.execute(sql, (date,  apt_id))
            connection.commit()
            print("Appointment updated successfully.")
    finally:
        connection.close()

def update_apttime(time, apt_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE appointments
                SET Appointment_Time = %s
                WHERE Appointment_ID = %s
            """
            cursor.execute(sql, (time,  apt_id))
            connection.commit()
            print("Appointment updated successfully.")
    finally:
        connection.close()

def update_aptstatus(status, apt_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE appointments
                SET Appointment_Status = %s
                WHERE Appointment_ID = %s
            """
            cursor.execute(sql, (status,  apt_id))
            connection.commit()
            print("Appointment completed.")
    finally:
        connection.close()

def delete_apt(apt_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                DELETE FROM appointments
                WHERE Appointment_ID = %s
            """
            cursor.execute(sql, (apt_id))
            connection.commit()
            print("Appointment deleted successfully.")
    finally:
        connection.close()

def create_bill(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Bills (Patient_ID, Bill_Date, Payment_Status, Amount) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['patient_id'],data['bill_date'],data['payment_status'],data['amount'],))
            connection.commit()
            print("Bill created successfully.")
    finally:
        connection.close()

def get_all_bills():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Bills"
            cursor.execute(sql)
            bills = cursor.fetchall()
            return bills
    finally:
        connection.close()

def get_bills(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Bills WHERE Patient_ID = %s"
            cursor.execute(sql, (data,))
            bill = cursor.fetchone()
            if not bill:
                print("Bill not found.")
            else:
                print(bill)
    finally:
        connection.close()

def update_amount(bill_id, amount):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Bills SET Amount = %s WHERE Bill_ID = %s"
            cursor.execute(sql, (amount, bill_id))
            connection.commit()
        print("Bill amount updated successfully.")
    finally:
        connection.close()

def update_status(bill_id, status):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Bills SET Payment_Status = %s WHERE Bill_ID = %s"
            cursor.execute(sql, (status, bill_id))
            connection.commit()
            print("Bill status updated successfully.")
    finally:
        connection.close()

def get_totals(total_patient_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT SUM(Amount) AS Total
                FROM bills
                WHERE Patient_ID = %s
            """
            cursor.execute(sql, (total_patient_id,))
            res = cursor.fetchone()
            
            # Check if res is None or res[0] is None
            if res is None or res[0] is None:
                total = 0.00
            else:
                total = res[0]
                
            return total
    finally:
        conn.close()


def get_medicines():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM medications')
            medicines = cursor.fetchall()
            return medicines
    finally:
        conn.close()

def add_medicine(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO medications (medicine_name, dosage, price) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'],data['dosage'],data['price']))
    conn.commit()
    conn.close()

def update_price(med_id, new_price):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE medications SET price = %s WHERE medicine_id = %s"
    cursor.execute(sql, (new_price, med_id))
    conn.commit()
    conn.close()

def delete_medicine(med_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM medications WHERE medicine_id = %s"
    cursor.execute(sql, med_id)
    conn.commit()
    conn.close()

def update_dosage(med_id, new_dosage):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE medications SET dosage = %s WHERE medicine_id = %s"
    cursor.execute(sql, (new_dosage, med_id))
    conn.commit()
    conn.close()

def create_prescription(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO prescriptions (Record_ID, Medicine_ID, Quantity, Start_Date, End_Date) VALUES (%s, %s, %s, %s, %s)"
            sql2= "INSERT INTO prescription_frequencies (prescription_ID, frequency) VALUES (%s, %s)"
            cursor.execute(sql, (data['record_id'],data['medicine_id'],data['quantity'], data['start_date'],data['end_date']))
            cursor.execute(sql2, (data['record_id'],data['frequency']))
            connection.commit()
            print("Prescription created successfully.")
    finally:
        connection.close()

def get_all_prescriptions():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Prescriptions"
            cursor.execute(sql)
            prescriptions = cursor.fetchall()
            if not prescriptions:
                print("No prescriptions found.")
            else:
                for prescription in prescriptions:
                    print(prescription)
    finally:
        connection.close()

def get_prescription(record, medicine):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Prescriptions WHERE Record_ID = %s AND Medicine_ID = %s"
            cursor.execute(sql, (record, medicine))
            prescription = cursor.fetchall()
            return prescription
    finally:
        connection.close()

def update_quantity(record_id, medicine_id, quantity):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                    UPDATE Prescriptions
                    SET Quantity = %s
                    WHERE Record_ID = %s AND Medicine_ID = %s
                  """
            cursor.execute(sql, (quantity, record_id, medicine_id))
            connection.commit()
        print("Medicine quantity updated successfully.")
    finally:
        connection.close()

def update_end_date(record_id, medicine_id, end_date):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                    UPDATE Prescriptions
                    SET End_Date = %s
                    WHERE Record_ID = %s AND Medicine_ID = %s
                  """
            cursor.execute(sql, (end_date, record_id, medicine_id))
            connection.commit()
        print("End date updated successfully.")
    finally:
        connection.close()

def update_frequency(record_id, new_frequency):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Prescriptions SET frequency = %s WHERE medicine_id = %s"
    cursor.execute(sql, (new_frequency, record_id))
    conn.commit()
    conn.close()

def create_record(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO medical_record (Patient_ID, Doctor_ID, Record_Date, Diagnosis, Treatment)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['patient_id'], data['doctor_id'], data['date'],
                data['diagnosis'], data['treatment']
            ))
            connection.commit()
            print("Record created successfully.")
    finally:
        connection.close()

def update_diagnosis(record_id, diagnosis):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE medical_record SET Diagnosis = %s WHERE Record_ID = %s"
            cursor.execute(sql, (diagnosis, record_id))
            connection.commit()
            print("Diagnosis updated successfully.")
    finally:
        connection.close()

def update_treatment(record_id, treatment):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE medical_record SET Treatment = %s WHERE Record_ID = %s"
            cursor.execute(sql, (treatment, record_id))
            connection.commit()
            print("Treatment updated successfully.")
    finally:
        connection.close()

def register_patient(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Start transaction
            connection.begin()
            
            try:
                # Hash password
                hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
                
                # Insert into patients table
                sql_patient = """
                    INSERT INTO patients (First_Name, Last_Name, Date_of_Birth, Gender, Email, Address, Password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_patient, (
                    data['first_name'], data['last_name'], data['dob'], data['gender'],
                    data['email'], data['address'], hashed_password
                ))
                
                # Get the patient ID immediately after insertion
                patient_id = cursor.lastrowid
                
                # Insert into users table
                sql_user = """
                    INSERT INTO users (username, password, role)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_user, (
                    data['email'], hashed_password, "patient"
                ))
                
                # Insert phone number
                sql_phone = """
                    INSERT INTO patient_phone_numbers (Patient_ID, Phone_Number)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_phone, (patient_id, data['phone_number']))
                
                # If everything is successful, commit the transaction
                connection.commit()
                print("Patient registered successfully.")
                return patient_id
                
            except Exception as e:
                # If any error occurs, rollback all changes
                connection.rollback()
                print(f"Error during registration: {str(e)}")
                raise
                
    finally:
        connection.close()

def register_doctor(data):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            sql = """
                INSERT INTO doctors (First_Name, Last_Name, Phone_Number, Email, Dept_ID, Password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            sql_user1 = """
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                data['first_name'], data['last_name'], data['phone_number'],
                data['email'], data['dept_id'], hashed_password
            ))
            cursor.execute(sql_user1, (
                data['email'], hashed_password, "doctor"
            ))
            connection.commit()
            print("Doctor registered successfully.")
    finally:
        connection.close()

def delete_patient(patient_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM patients WHERE patient_id = %s"
            cursor.execute(sql, (patient_id,))
            connection.commit()
        print("Patient deleted successfully.")
    finally:
        connection.close()

def delete_doctor(doctor_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM doctors WHERE doctor_id = %s"
            cursor.execute(sql, (doctor_id,))
            connection.commit()
        print("Doctor deleted successfully.")
    finally:
        connection.close()

def get_all_patients():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT
                p.Patient_ID,
                CONCAT(p.First_Name, " ", p.Last_Name) AS Patient_Name,
                p.Date_of_birth,
                p.gender,
                p.Email,
                ph.Phone_Number,
                p.address
                FROM
                    patients AS p
                INNER JOIN
                    patient_phone_numbers AS ph ON p.Patient_ID = ph.Patient_ID;
            """
            cursor.execute(sql)
            patients = cursor.fetchall()
            print(patients)
            return patients
    finally:
        connection.close()

def get_all_doctors():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT
                d.Doctor_ID,
                CONCAT(d.First_Name, " ", d.Last_Name) AS Doctor_Name,
                d.Phone_Number,
                d.Email,
                d.Dept_ID,
                dept.Department_Name
                FROM
                    doctors AS d
                INNER JOIN
                    departments AS dept ON d.Dept_ID = dept.Dept_ID;
            """
            cursor.execute(sql)
            doctors = cursor.fetchall()
            print(doctors)
            return doctors
    finally:
        connection.close()

def get_all_apts():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql =  """
                SELECT
                a.appointment_id,
                CONCAT(p.First_Name, " ", p.Last_Name) AS Patient_Name,
                CONCAT(d.First_Name, " ", d.Last_Name) AS Doctor_Name,
                a.appointment_time,
                a.appointment_date,
                a.appointment_status
                FROM
                    appointments AS a
                INNER JOIN
                    doctors AS d ON d.Doctor_ID = a.Doctor_ID
                INNER JOIN
                    patients AS p ON p.Patient_ID = a.Patient_ID;
            """
            cursor.execute(sql)
            apts = cursor.fetchall()
            return apts
    finally:
        connection.close()

def get_all_records():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "CALL rec_pre8();"
            cursor.execute(sql)
            records = cursor.fetchall()
            return records
    finally:
        connection.close()

def get_doctor_appointments(doctor_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Appointments WHERE doctor_id = %s"
            cursor.execute(query, (doctor_id,))
            appointments = cursor.fetchall()
            if not appointments:
                print("No appointments found for this doctor.")
            return appointments
    finally:
        connection.close()

def get_patient_records_for_doctor(doctor_id, patient_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM Medical_Record
                WHERE patient_id = %s
                AND EXISTS (
                    SELECT * FROM Doctors WHERE doctor_id = %s
                )
            """
            cursor.execute(query, (patient_id, doctor_id))
            records = cursor.fetchall()
            if not records:
                print("No medical records found for this patient.")
            return records
    finally:
        connection.close()

def get_patient_appointments(patient_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Appointments WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            appointments = cursor.fetchall()
            if not appointments:
                print("No appointments found for this patient.")
            return appointments
    finally:
        connection.close()

def get_medical_records(patient_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Medical_Record WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            records = cursor.fetchall()
            if not records:
                print("No medical records found for this patient.")
            return records
    finally:
        connection.close()
