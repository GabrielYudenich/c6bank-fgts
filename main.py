import requests, json

# Criação do objeto para chamada da api e contrução entre SENHA e EMAIL

class PRATA_DIGITAL(object):

    # Inicializador de objeto para armazenar o email e senha

    def __init__(self, email, senha):
        self.email_conta = email
        self.senha_conta = senha

    # Obter token da API de logins para identificar a validade do usuário conectado

    def get_token(self):
        link = 'https://api.bancoprata.com.br/v1/users/login'

        json_data = {
            "email":self.email_conta,
            "password":self.senha_conta
            }

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'
            }

        res = requests.post(link, json=json_data, headers=headers)

        return json.loads(res.text)['data']['token']
    
    # Função para obter os dados de FGTS da pessoa

    def get_fgts(self, cpf:str):
        
        link = f'https://pratadigital.com.br/sistema-cb/v1/qitech/fgts/balance?document={cpf}&rate_id=7'

        headers = {
            'Authorization':f'Bearer {self.get_token()}',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'
            }

        res = requests.get(link, headers=headers)

        if res.status_code == 400:

            link_wait = 'https://pratadigital.com.br/sistema-cb/v1/qitech/fgts/balance-wait-list'

            res_wait = requests.get(link_wait, headers=headers)

            json_data = json.loads(res_wait.text)

            for x in json_data['data']:

                cpf_formated = f'{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}'
                
                if x['document'] == cpf_formated:
                    return {'Status:':'OK', 'Resultado':x}
        else:
            return {'Status:':'PENDENTE', 'Resultado':'CPF ainda pendente'}