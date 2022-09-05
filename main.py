from win32gui import GetWindowText, GetForegroundWindow
import random
import winreg
import time


class AccountManagement:
    def __init__(self):
        self.hkey_type = winreg.HKEY_CURRENT_USER
        self.path = r'SOFTWARE\ENMSoft\GPC'
        self.account_key_name = 'account_data'
        self.ascii_check_range = 126
        self.account_data = ''

    def encryption_data(self, resource: str = None):
        encrypted_resource = []
        for char in resource:
            char = char + '@enm#'
            encrypted_char = []
            for semi_char in char:
                semi_char = chr(ord(semi_char) + random.randint(1, 128))
                encrypted_char.append(semi_char)
            encrypted_resource.append(''.join(encrypted_char))
        self.account_data = ''.join(encrypted_resource)

    def decryption_data(self):

        for char in self.account_data:


    def check_validity(self, resource: str = None):
        for char in resource:
            if ord(char) >= self.ascii_check_range:
                return False
        return True

    def input_account_data(self, fall_back_state: bool = False):
        if not fall_back_state:
            id_resource = input('Enter ID to use for automatic login: ')
            if self.check_validity(id_resource):
                pw_resource = input('Enter PW to use for automatic login: ')
                if self.check_validity(pw_resource):
                    self.encryption_data(f'@id_start#{id_resource}@id_end#@pw_start#{pw_resource}@pw_end#')
                    return True
                else:
                    self.input_account_data(True)
        else:
            print('Only English, numbers, and special characters are allowed. Please re-enter.')
            pw_resource = input('Enter PW to use for automatic login: ')
            return self.check_validity(pw_resource)

    def read_account(self):
        reg_handle = winreg.ConnectRegistry(None, self.hkey_type)
        try:
            reg_key = winreg.OpenKey(reg_handle, self.path, 0, winreg.KEY_READ)
            value = winreg.QueryValueEx(reg_key, self.account_key_name)
            winreg.CloseKey(reg_key)
            return True, value
        except WindowsError:
            return False, None

    def save_account(self, fall_back_state: bool = False):
        reg_handle = winreg.ConnectRegistry(None, self.hkey_type)
        try:
            reg_key = winreg.OpenKey(reg_handle, self.path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, self.account_key_name, 0, winreg.REG_SZ, self.account_data)
            winreg.CloseKey(reg_key)
            return True
        except WindowsError:
            if fall_back_state:
                return False
            else:
                winreg.CreateKey(self.hkey_type, self.path)
                return self.save_account(True)


def main():
    am = AccountManagement()
    am.input_account_data()
    print(am.account_data)
    # print(am.account_data)


if __name__ == '__main__':
    main()
