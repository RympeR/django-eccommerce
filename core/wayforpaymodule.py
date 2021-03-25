import requests
import hashlib
import hmac
from datetime import date

API_URL = "https://api.wayforpay.com/api"
PURCHASE_URL = "https://secure.wayforpay.com/pay"
API_VERSION = 1
today = date.today()

class WayForPayAPI:
    __signature__keys = [
        'merchantAccount',
        'merchantDomainName',
        'orderReference',
        'orderDate',
        'amount',
        'currency',
        'productName',
        'productCount',
        'productPrice'
    ]
    __ORDER_APPROVED = 'Approved'
    __ORDER_REFUNDED = 'Refunded'
    __SIGNATURE_SEPARATOR = ';'
    __ORDER_SEPARATOR = ":"

    def __init__(self, merchant_account, merchant_key, merchant_domain):
        self.id = 'wayforpay'
        self.method_title = 'WayForPay'
        self.merchant_account = merchant_account
        self.merchant_key = merchant_key
        self.merchant_domain = merchant_domain
        self.options = {
            'merchantAccount':self.merchant_account,
            'merchantAuthType':'simpleSignature',
            'merchantDomainName':self.merchant_domain,
            'merchantTransactionSecureType':'AUTO',
        }
        

    def generate_widget(self, data, return_url=""):
        self.merchantSignature = self.get_request_signature({**self.options, **data})
        request_form = r"""function pay(){
                var payment = new Wayforpay();
                    payment.run({""" + f"""
                        merchantAccount: \'{self.merchant_account}\',
                        merchantDomainName: '{self.merchant_domain}',
                        merchantAuthType: 'SimpleSignature ',
                        merchantTransactionType: 'AUTO',
                        merchantTransactionSecureType: 'AUTO',
                        orderReference: '{data['orderReference']}',
                        orderDate: '{data['orderDate']}',
                        amount: '{data["amount"]}',
                        authorizationType: 'SimpleSignature',
                        currency: 'UAH',
                        productName:   {data['productName']} ,
                        productPrice:  {data['productPrice']},
                        productCount:  {data['productCount']},		
                        merchantSignature: '{self.merchantSignature}',
                        language: 'UA',
                        straightWidget: true
                    """ + r"""},
                    function (response) {
                        window.location.href='';		
                    } , 			
                    function (response) {
                        console.log('dude');			
                    },
                    function (response) {
                        console.log(response)
                        window.location.href='';		
                    } 
                );
            }
            
        """
        return request_form

    def generate_payment_form(self, data, return_url=""):
        ...

    def get_signature(self, options, keys):
        hash_str = list()
        for datakey in keys:
            if not options.get(datakey, None):
                continue

            if isinstance(options[datakey], list):
                for _ in options[datakey]:
                    hash_str.append(str(_))
            else:
                hash_str.append(str(options[datakey]))
        hash_str = ';'.join(hash_str)
        print(hash_str)
        print(hmac.new(self.merchant_key.encode(), hash_str.encode(), hashlib.md5).hexdigest())
        return hmac.new(self.merchant_key.encode(), hash_str.encode(), hashlib.md5).hexdigest()

    def get_request_signature(self, options):
        return self.get_signature(options, self.__signature__keys)

    def generate_form(self, order_data):
        ...
