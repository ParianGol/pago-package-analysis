
class SpdxLicenseProvider:
    def __init__(self, file_operation, search_key):
        self.file_operation = file_operation
        self.spdx_file_content = self.file_operation.read_file()
        self.names = []
        self.read_all_names(search_key)
    
    def read_all_names(self, search_key):
        
        for item in self.spdx_file_content[search_key]:
            print (item["name"])
            self.set_names(item["name"])
    
    def get_names(self):
        return self.names

    def set_names(self, name: str):
        self.names.append(name)
    
    names_list = property(get_names, set_names)