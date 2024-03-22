
import re
from oss.file_operation.json_file_operations import JsonFileOperations
from oss.content_analyzer.spdx_license_provider import SpdxLicenseProvider
from oss.types.spdx_files import SpdxFiles


class SpdxFileReaderException(Exception):
    pass


class UnknownSpdxFileNameException(SpdxFileReaderException):
    pass


class MissingInputFileListException(SpdxFileReaderException):
    pass


class MissingInputlicenseListException(SpdxFileReaderException):
    pass


class SpdxFileReader():

    def __init__(self, file_list: list):
        self.spdx_files_map = {}
        self.create_spdx_file_name(file_list)

    def create_spdx_file_name(self, file_list):
        if not file_list:
            raise MissingInputFileListException("File_list is empty!")
        for el in file_list:
            name = ""
            for spdx_file in SpdxFiles:
                spdx_name = (spdx_file.value)
                if re.search(spdx_name, str(el)):
                    name = spdx_name
            if not name:
                raise UnknownSpdxFileNameException("{el} is unknown")
            print (">>>>>>>>>>>>>>>>>>>>>>>>>   ", (name))
            print (">>>>>>>>>>>>>>>>>>>>>>>>> el  ", (el))
            json_file_operations =  JsonFileOperations(el)
            self.spdx_files_map[name] = SpdxLicenseProvider(json_file_operations, name)

    def check_licenses_exit(self, license_list):
        if not license_list:
            raise MissingInputlicenseListException("The input License_list is empty!")
        self.missing_license_map = {}
        licenses_file = str(SpdxFiles.licenses)
        exceptions_file = str(SpdxFiles.exceptions)
        for license in license_list:
            # First look for the license among the spdx licenses file
            if license not in self.spdx_files_map[licenses_file].names_list:
                self.set_missing_licenses_names(licenses_file, license)
                # In case it was not found in licenses, search spdx exceptions file
                if license not in self.spdx_files_map[exceptions_file].names_list:
                    self.set_missing_licenses_names(exceptions_file, license)
                
    def get_missing_licenses_names(self):
        return self.missing_license_map

    def set_missing_licenses_names(self, name: str, license:str):
        if name in self.missing_license_map:
            self.missing_license_map[name].append(license)
        else:
            self.missing_license_map[name] = [license]
    
    missing_licenses = property(get_missing_licenses_names, set_missing_licenses_names)