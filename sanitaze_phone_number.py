def sanitaze_phone_number(phone: str) -> str:
    new_phone = (phone.strip()
                 .lstrip("+")
                 # .removeprefix('+')
                 .replace("(", "")
                 .replace(")", "")
                #  .replace(" ", "")
                 .replace("-", "")
                 )
    return new_phone


if __name__ == "__main__":  
    sanitaze_phone_number()