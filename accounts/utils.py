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
