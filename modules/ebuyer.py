import requests
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed

def ppCheckout():

    site = str(input('SITE: '))
    s = requests.session()

    r = s.get(site)

    if r.status_code == 200:
        print("Page successfully loaded!")
        soup = BeautifulSoup(r.text, 'html.parser')
        print("Searching for Paypal link!")
        paypalLink = soup.find('a', {'id': 'paypalButton'})
        if paypalLink:
            print("Paypal link found!")
            url = Webhook('https://discord.com/api/webhooks/847193363811270697/ss6t--DVQDjfrPuLwZxNnPHiEE2FCF2rzB_Kw2iY-i_5ecV4YlmAhbKWcEiCfzlnvIMj')
            embed = Embed(
                title = 'PayPal Checkout!',
                timestamp ='now'
            )
            embed.set_author(name='Ebuyer - New Paypal Checkout!', url='https://www.ebuyer.com')
            embed.set_title(title=soup.find('h1', class_='product-hero__title').string, url=site)
            embed.add_field(name='**Price**', value=soup.find('p', class_='price').text.replace("\n", "").replace(" ", "").replace("inc.vat",""))
            embed.add_field(name='**Checkout URL**', value=paypalLink['href'])
            embed.set_footer(text='Unite')

            url.send(username='UniteAIO', embed=embed)
            print("Paypal link sent. Check your discord webhook!")
        else:
            print('Paypal link not found!')

    else:
        print(r.status_code)

if __name__ == '__main__':
    ppCheckout()