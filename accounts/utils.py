import re
from datetime import datetime


def nest_member_data(request_data):
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
        "image": request_data["image"],
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
        "image": member.image,
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
    md = month_and_date(day_code)
    if md.day == -1:
        return False, "Invalid day code in NIC"

    # Debugging output for the date extracted from NIC
    print(f"Extracted Date from NIC: {md.day} {md.month} {year}")

    # Compare date of birth
    try:
        dob_year, dob_month, dob_day = map(int, date_of_birth.split("-"))
        print(
            f"Provided Date of Birth: {dob_day}-{dob_month}-{dob_year}"
        )  # Debugging line

        # Check if the year and day/month extracted from NIC matches the provided date of birth
        if (
            (year != dob_year)
            or (md.month != datetime(dob_year, dob_month, dob_day).strftime("%B"))
            or (md.day != dob_day)
        ):
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
#     "date_of_birth": "1998-02-02",  # YYYY-MM-DD format
#     "position_in_party": "leader",
#     "region": "Malva",
#     "Nic": "980330330V",  # Old NIC format, valid (February 3, 1998)
#     "phone": 7412589123,
#     "gender": "male",
#     "district": "district1",
#     "constituency": "constituency1",
#     "image": None
# }

# is_valid, message = validate_nic(user_details)