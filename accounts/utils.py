import re

import requests


def send_otp_via_textlk(phone_number, otp):
    url = "https://app.text.lk/api/v3/sms/send"  # Replace with the correct Text.lk API URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 97|zm0F4SdIfFMQ9Y0P5WtM0L7DjiQMEjeihvW1mmzxf68f7177 ",  # Replace with your API key
    }
    payload = {
        "recipient": phone_number,
        "message": f"Your OTP is {otp}",
        "sender_id": "TEXTLK",  # Replace with your sender ID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None


def nest_member_data(request_data, request_files):
    return {
        "user": {
            "first_name": request_data.get("first_name"),
            "last_name": request_data.get("last_name"),
            "email": request_data.get("email"),
            "date_of_birth": request_data.get("date_of_birth"),
            "password": request_data.get("password"),
        },
        "position_in_party": request_data.get("position_in_party"),  # Using .get() here
        "Nic": request_data.get("Nic"),
        "phone": request_data.get("phone"),
        "gender": request_data.get("gender"),
        "district": request_data.get("district"),
        "constituency": request_data.get("constituency"),
        "image": request_files.get("image"),  # This will remain the same
    }


def flatten_member_data(member):
    """Flatten member data for response."""
    user = member.user
    print("member", member)
    print("member", member.image.url)
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "position_in_party": member.position_in_party,
        "Nic": member.Nic,
        "phone": member.phone,
        "gender": member.gender,
        "district": member.district,
        "constituency": member.constituency,
        "image": member.image.url if member.image else None,
    }


def flatten_candidate_data(request_data):
    """Flatten candidate data for processing."""
    return {
        "user": {
            "first_name": request_data["first_name"],
            "last_name": request_data["last_name"],
            "email": request_data["email"],
            "password": request_data.get("password"),
        },
        "constituency": request_data["constituency"],
        "age": request_data["age"],
        "party": request_data.get("party"),
        "district": request_data.get("district"),
        "image": request_data.get("image"),
        "election_status": request_data.get(
            "election_status", "nominated"
        ),  # Default status
    }


def validate_nic(user_details):
    nic = str(user_details.get("Nic")).strip()  # Ensure to strip whitespace
    date_of_birth = user_details.get("date_of_birth")
    gender = user_details.get("gender").lower()

    # print(f"Original NIC: '{nic}'")  # Debugging line

    # Check for 'V' at the end and process accordingly
    if nic.endswith("V") or nic.endswith("v"):
        nic = nic[:-1]  # Remove 'V'

    # Validate NIC length and format
    if len(nic) == 9:
        if not re.match(r"^\d{9}$", nic):  # Old NIC format should be digits only
            return False, "Old NIC format is incorrect"
    elif len(nic) == 12:
        if not re.match(r"^\d{12}$", nic):  # New NIC format should be digits only
            return False, "New NIC format is incorrect"
    else:
        return False, "Invalid NIC length"

    # Extract year and day code from NIC
    year_prefix = 1900 if len(nic) == 9 else None
    if not year_prefix:
        year = int(nic[:4])
    else:
        year = int(nic[:2]) + year_prefix
    day_code = int(nic[2:5]) if len(nic) == 9 else int(nic[4:7])

    # Adjust for gender: Female if day_code > 500
    detected_gender = "female" if day_code > 500 else "male"
    if day_code > 500:
        day_code -= 500

    # Check if day_code is within the range we assume (1-366)
    if day_code < 1 or day_code > 366:
        return False, "Invalid day code in NIC"

    # Define the days in each month, assuming February has 29 days for all years
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month, day = 1, day_code

    # Calculate month and day by iterating through days_in_month
    for days in days_in_month:
        if day <= days:
            break
        day -= days
        month += 1

    # print(f"Extracted Date from NIC: {day} {month} {year}")

    # Compare date of birth
    try:
        dob_year, dob_month, dob_day = map(int, date_of_birth.split("-"))
        # print(f"Provided Date of Birth: {dob_day}-{dob_month}-{dob_year}")

        # Check if the year and day/month extracted from NIC matches the provided date of birth
        if (year != dob_year) or (month != dob_month) or (day != dob_day):
            return False, "Date of birth does not match NIC"
    except ValueError:
        return False, "Date of birth format is incorrect"

    # Compare gender
    if detected_gender != gender:
        return False, "Gender does not match NIC information"

    return True, "NIC and user details are valid"


# # Example usage
# Testing the function
# l = [("922852270v", "1992-10-11"), ("972491160v", "1997-09-05"), ("198831704968", "1988-11-12"),("923662270v","1992-12-31"), ("920102270v","1992-01-10"), ]

# # Example usage
# user_details = {
#     "first_name": "Madhav",
#     "last_name": "M",
#     "email": "madhav@sample.com",
#     "date_of_birth": "1988-11-12",  # YYYY-MM-DD format
#     "position_in_party": "leader",
#     "region": "Malva",
#     "Nic": "198831704968",  # Old NIC format, valid
#     "phone": 7412589123,
#     "gender": "male",
#     "district": "district1",
#     "constituency": "constituency1",
#     "image": None
# }

# for i in l:
#     user_details['Nic'] = i[0]
#     user_details['date_of_birth'] = i[1]
#     is_valid, message = validate_nic(user_details)
#     print(f"The NIC is valid: {is_valid}. Message: {message}")
#     print()
