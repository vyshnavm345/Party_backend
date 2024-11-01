import re
from datetime import datetime, timedelta

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
            "first_name": request_data["first_name"],
            "last_name": request_data["last_name"],
            "email": request_data["email"],
            "date_of_birth": request_data["date_of_birth"],
            "password": request_data.get("password"),
        },
        "position_in_party": request_data["position_in_party"],
        "Nic": request_data["Nic"],
        "phone": request_data["phone"],
        "gender": request_data["gender"],
        "district": request_data["district"],
        "constituency": request_data["constituency"],
        "image": request_files.get("image"),  # Access image from request_files
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


class MD:
    def __init__(self, month="", day=0):
        self.month = month
        self.day = day


def month_and_date(val):
    # Ensure the day codes correspond correctly to the actual month-day structure.
    if val <= 31:
        return MD("January", val)
    elif val <= 59:  # February in non-leap year has 28 days, hence 59
        return MD("February", val - 31)
    elif val <= 90:  # March has 31 days
        return MD("March", val - 59)
    elif val <= 120:  # April has 30 days
        return MD("April", val - 90)
    elif val <= 151:  # May has 31 days
        return MD("May", val - 120)
    elif val <= 181:  # June has 30 days
        return MD("June", val - 151)
    elif val <= 212:  # July has 31 days
        return MD("July", val - 181)
    elif val <= 243:  # August has 31 days
        return MD("August", val - 212)
    elif val <= 273:  # September has 30 days
        return MD("September", val - 243)
    elif val <= 304:  # October has 31 days
        return MD("October", val - 273)
    elif val <= 334:  # November has 30 days
        return MD("November", val - 304)
    elif val <= 365:  # December has 31 days
        return MD("December", val - 334)
    else:
        return MD("Invalid Month", -1)


def validate_nic(user_details):
    nic = str(user_details.get("Nic")).strip()  # Ensure to strip whitespace
    date_of_birth = user_details.get("date_of_birth")
    gender = user_details.get("gender").lower()

    print(f"Original NIC: '{nic}'")  # Debugging line

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
    year_prefix = 1900 if len(nic) == 9 else 2000
    year = int(nic[:2]) + year_prefix
    day_code = int(nic[2:5]) if len(nic) == 9 else int(nic[4:7])

    # Adjust for gender: Female if day_code > 500
    detected_gender = "female" if day_code > 500 else "male"
    if day_code > 500:
        day_code -= 500

    # Convert day_code to month and day
    if day_code < 1 or day_code > 365:  # Check if the day_code is valid
        return False, "Invalid day code in NIC"

    # Calculate the actual date
    date = datetime(year, 1, 1) + timedelta(days=day_code - 1)
    print(f"Extracted Date from NIC: {date.day} {date.month} {year}")

    # Compare date of birth
    try:
        dob_year, dob_month, dob_day = map(int, date_of_birth.split("-"))
        print(
            f"Provided Date of Birth: {dob_day}-{dob_month}-{dob_year}"
        )  # Debugging line

        # Check if the year and day/month extracted from NIC matches the provided date of birth
        if (year != dob_year) or (date.month != dob_month) or (date.day != dob_day):
            return False, "Date of birth does not match NIC"
    except ValueError:
        return False, "Date of birth format is incorrect"

    # Compare gender
    if detected_gender != gender:
        return False, "Gender does not match NIC information"

    return True, "NIC and user details are valid"


# # Example usage
# user_details = {
#     "first_name": "Madhav",
#     "last_name": "M",
#     "email": "madhav@sample.com",
#     "date_of_birth": "1992-10-11",  # YYYY-MM-DD format
#     "position_in_party": "leader",
#     "region": "Malva",
#     "Nic": "922852270v",  # Old NIC format, valid
#     "phone": 7412589123,
#     "gender": "male",
#     "district": "district1",
#     "constituency": "constituency1",
#     "image": None
# }

# is_valid, message = validate_nic(user_details)
# print(f"The NIC is valid: {is_valid}. Message: {message}")
