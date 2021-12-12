import os


def delete_file(filename:str):
    """
        This function deletes all files related to the current user

        :param filename: str - user id
    """
    if f"{filename}.csv" not in os.listdir("files/"):
        return False
    os.remove(f"files/{filename}.csv")
    os.remove(f"files/{filename}.png")
    return True
