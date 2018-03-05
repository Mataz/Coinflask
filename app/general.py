from flask import Flask, render_template
from app import app
import pandas as pd
import requests


def get_top5_inc():
    url = 'http://coincap.io/front'
    data = requests.get(url).json()
    top100_data = sorted(data, key=lambda k: (float(k['mktcap'])), reverse=True)[:100]
    ordered_data = sorted(top100_data, key=lambda k: (float(k['cap24hrChange'])),
                          reverse=True)[:5]
    raw_data_increase = {}

    for currency in ordered_data:
        name = currency['long']
        market_cap = float(currency['mktcap'])
        market_cap_rounded = f'{market_cap:,.2f}'
        percent_change_24 = currency['cap24hrChange']
        price = float(currency['price'])
        price_rounded = f'{price:.2f}'

        raw_data_increase.setdefault('Name', [])
        raw_data_increase['Name'].append(name)
        raw_data_increase.setdefault('Market Cap(USD)', [])
        raw_data_increase['Market Cap(USD)'].append(market_cap_rounded)
        raw_data_increase.setdefault('%24hr', [])
        raw_data_increase['%24hr'].append(percent_change_24)
        raw_data_increase.setdefault('Price(USD)', [])
        raw_data_increase['Price(USD)'].append(price_rounded)

    df = pd.DataFrame(raw_data_increase,
                      columns=['Name', 'Market Cap(USD)', '%24hr', 'Price(USD)'])

    df.to_csv('top5_table.csv', index=False)
    data_read = pd.read_csv('top5_table.csv')
    data_read.set_index(['Name'], inplace=True)
    data_read.index.name = None
    data_html = data_read.to_html()
    return data_html



@app.route('/')
def index():
    return render_template('index.html', table=html_data)


if __name__ == '__main__':
    app.run(debug=True)
