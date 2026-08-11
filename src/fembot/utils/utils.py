# should NOT require any fembot module


def check_string(string: str, pattern: str) -> bool:
    pattern = pattern.lower()
    mode = ""
    if len(pattern.split("/")) > 1:
        mode = pattern.split("/")[0]
        pattern = "/".join(pattern.split("/")[1:])
    match mode:
        case "startswith":
            for i in pattern.split(":"):
                if string.startswith(i):
                    return True
        case "endswith":
            for i in pattern.split(":"):
                if string.endswith(i):
                    return True
        case "is":
            for i in pattern.split(":"):
                if i == string:
                    return True
        case "all":
            check = True
            for i in pattern.split(":"):
                if i not in string:
                    check = False
            return check
        case "any":
            for i in pattern.split(":"):
                if i in string:
                    return True
        case _:
            for i in pattern.split(":"):
                if i in string:
                    return True
    return False
