import re

import requests


def send_otp_via_textlk(phone_number, otp):
    url = "https://app.text.lk/api/v3/sms/send"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 97|zm0F4SdIfFMQ9Y0P5WtM0L7DjiQMEjeihvW1mmzxf68f7177 ",
    }
    payload = {
        "recipient": phone_number,
        "message": f"Your OTP is {otp}",
        "sender_id": "TEXTLK",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
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
        "position_in_party": request_data.get("position_in_party"),
        "Nic": request_data.get("Nic"),
        "phone": request_data.get("phone"),
        "gender": request_data.get("gender"),
        "district": request_data.get("district"),
        "constituency": request_data.get("constituency"),
        "image": request_files.get("image"),
    }


def flatten_member_data(member):
    """Flatten member data for response."""
    user = member.user
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
        "election_status": request_data.get("election_status", "nominated"),
    }


def validate_nic(user_details):
    nic = str(user_details.get("Nic")).strip()
    date_of_birth = user_details.get("date_of_birth")
    gender = user_details.get("gender").lower()

    if nic.endswith("V") or nic.endswith("v"):
        nic = nic[:-1]

    if len(nic) == 9:
        if not re.match(r"^\d{9}$", nic):
            return False, "Old NIC format is incorrect"
    elif len(nic) == 12:
        if not re.match(r"^\d{12}$", nic):
            return False, "New NIC format is incorrect"
    else:
        return False, "Invalid NIC length"

    year_prefix = 1900 if len(nic) == 9 else None
    if not year_prefix:
        year = int(nic[:4])
    else:
        year = int(nic[:2]) + year_prefix
    day_code = int(nic[2:5]) if len(nic) == 9 else int(nic[4:7])

    detected_gender = "female" if day_code > 500 else "male"
    if day_code > 500:
        day_code -= 500

    if day_code < 1 or day_code > 366:
        return False, "Invalid day code in NIC"

    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month, day = 1, day_code

    for days in days_in_month:
        if day <= days:
            break
        day -= days
        month += 1
    try:
        dob_year, dob_month, dob_day = map(int, date_of_birth.split("-"))

        if (year != dob_year) or (month != dob_month) or (day != dob_day):
            return False, "Date of birth does not match NIC"
    except ValueError:
        return False, "Date of birth format is incorrect"

    if detected_gender != gender:
        return False, "Gender does not match NIC information"

    return True, "NIC and user details are valid"
