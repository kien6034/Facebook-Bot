import gspread 
import json 
from gspread.spreadsheet import Spreadsheet
import pandas as pd 

class Sheet:
    def __init__(self) -> None:
        self.sa = gspread.service_account()
      
        self.type = 0 
        self.sh = None 
        self.wks = None 

        self.data = self.read_data_from_csv("data.csv")
        self.new = self.read_data_from_csv("new.csv")
     
    
    def read_data_from_csv(self, file_name) -> pd.DataFrame:
        return pd.read_csv(file_name)  

    
 

    def set_sheet(self, sheet_name):
        self.sh = self.sa.open(sheet_name)
        print(f"using sheet {sheet_name} ...")

    def set_wks(self, wks_name):
        self.wks = self.sh.worksheet(wks_name)
        print(f"using workingsheet {wks_name} ...")
    
    def get_data(self):
        print(self.wks.get('A1'))
    
    def uplopad(self):
        self.import_csv(f"test01", "./data.csv")
    
    def import_csv(self, sheet_name, csv_dir):
        sh = self.get_spreadsheet(sheet_name)

        self.update_permission(sh)
       
        with open(csv_dir, 'r', encoding='UTF8') as f:
            content = f.read()
            content = content.encode('utf-8')
            self.sa.import_csv(sh.id, data= content)

        #get worksheet 
        worksheet = sh.get_worksheet(0)

        #formart header 
        worksheet.format("A1:J1", {
            "backgroundColor": {
                "red": 10,
                "green": 20,
                "blue": 50
            },
            "textFormat": {
                "fontSize": 12,
                "bold": True
            }
        })

        worksheet.format("A1:J100", {
          "horizontalAlignment": "CENTER",
        })
    
    def get_spreadsheet(self, name) -> Spreadsheet:
        spreadsheet = None 
        try:
            spreadsheet = self.sa.open(name)
           
        except:
            spreadsheet = self.sa.create(name)
        
        return spreadsheet 

    def update_permission(self, spreadsheet: Spreadsheet):
        permissions = spreadsheet.list_permissions()
        
        updated_permissions = {}

         #share worksheet to the needed accounts 
        f = open('email.json')
        data = json.load(f)
        for permission in permissions:
            updated_permissions[permission["emailAddress"]] = permission["role"]

        for new_permission in data:
            email = new_permission["email"]
            role = new_permission["role"]

            if updated_permissions[f"{email}"] == role:
                continue

            spreadsheet.share(email, perm_type='user', role = role)

            print(f"\n\n --------------------------")
            print(f"Update permission for user: {email} => Role: {role}")

sheet = Sheet()
sheet.set_sheet("Seeder")
sheet.set_wks("Data")
sheet.uplopad()