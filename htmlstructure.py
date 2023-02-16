
from bs4 import BeautifulSoup


class HTML(BeautifulSoup):

    def __contains__(self, login_form):
        for form in self.find_all('form'):
            if form.find('input', attrs={'id': login_form['usr_field']}) and form.find('input', attrs={'id': login_form['pwd_field']}):
                return True
        return False

    def get_login_forms(self):
        results = []

        forms = self.find_all('form')
        for form in forms:
            for inp in form.find_all('input', {'type': False}):
                inp.attrs['type'] = 'text'

            txt_fields = form.find_all('input', attrs={'id': True, 'type': 'text'})
            pwd_fields = form.find_all('input', attrs={'id': True, 'type': 'password'})

            if len(txt_fields) != 1 or len(pwd_fields) != 1:
                continue

            usr_field = txt_fields[0]
            pwd_field = pwd_fields[0]

            json_form = {'usr_field': usr_field.attrs['id'], 'pwd_field': pwd_field.attrs['id'], 'fields': {}}

            for inp in form.find_all('input', attrs={'id': True, 'value': True}):
                json_form['fields'][inp.attrs['id']] = inp.attrs['value']

            json_form['index'] = len(results)
            results.append(json_form)
        return results
