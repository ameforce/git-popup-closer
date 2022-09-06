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
        self.rand_range = 128
        self.account_data = ''

    def encryption_data(self, resource: str = None):
        encrypted_resource = []
        id_resource, pw_resource = resource.split('@Account Separator#')

        for char in id_resource:
            char = char + '@enm#'
            encrypted_char = []
            rand_num = random.randint(1, self.rand_range)
            for semi_char in char:
                semi_char = chr(ord(semi_char) + rand_num)
                encrypted_char.append(semi_char)
            encrypted_resource.append(''.join(encrypted_char))

        encrypted_resource.append('@Account Separator#')

        for char in pw_resource:
            char = char + '@enm#'
            encrypted_char = []
            rand_num = random.randint(1, self.rand_range)
            for semi_char in char:
                semi_char = chr(ord(semi_char) + rand_num)
                encrypted_char.append(semi_char)
            encrypted_resource.append(''.join(encrypted_char))
        self.account_data = ''.join(encrypted_resource)

    def decryption_data(self):
        decrypted_account = []
        for resource in self.account_data.split('@Account Separator#'):
            new_resource = []
            for i in range(len(resource) // 6):
                split_data = []
                for j in range(6):
                    split_data.append(resource[i*6+j])
                new_resource.append(split_data)

            for raw_data in new_resource:
                max_range = self.rand_range
                raw_data_min_num = min(ord(raw_char) for raw_char in raw_data[0:6])
                if raw_data_min_num < self.rand_range:
                    max_range = raw_data_min_num
                for i in range(max_range):
                    decrypting_data = []
                    for raw_char in raw_data:
                        decrypting_data.append(chr(ord(raw_char) - i))
                    if ''.join(decrypting_data[1:6]) == '@enm#':
                        decrypted_account.append(decrypting_data[0])
                        break
            if '@Account Separator#' not in decrypted_account:
                decrypted_account.append('@Account Separator#')
        return ''.join(decrypted_account)

    def check_validity(self, resource: str = None):
        for char in resource:
            if ord(char) >= self.ascii_check_range:
                return False
        return True

    def input_account_data(self):
        id_resource, pw_resource = '', ''
        while True:
            id_resource = input('Enter ID to use for automatic login: ')
            if not self.check_validity(id_resource):
                print('\nOnly English, numbers, and special characters are allowed. Please re-enter.')
                continue
            break

        while True:
            pw_resource = input('Enter PW to use for automatic login: ')
            if not self.check_validity(pw_resource):
                print('\nOnly English, numbers, and special characters are allowed. Please re-enter.')
                continue
            break

        self.encryption_data(f'{id_resource}@Account Separator#{pw_resource}')
        self.save_account()

    def read_account(self):
        reg_handle = winreg.ConnectRegistry(None, self.hkey_type)
        try:
            reg_key = winreg.OpenKey(reg_handle, self.path, 0, winreg.KEY_READ)
            value = winreg.QueryValueEx(reg_key, self.account_key_name)
            winreg.CloseKey(reg_key)
            self.account_data = value[0]
            return True
        except WindowsError:
            return False

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
    if not am.read_account():
        am.input_account_data()
    print(am.decryption_data())


if __name__ == '__main__':
    main()
