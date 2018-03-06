from flask import Flask, render_template
from app import app
import pandas as pd
import requests
import datetime
import io
import base64
import matplotlib.pyplot as plt


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


def get_top5_mktcap():
    url = 'http://coincap.io/front'
    data = requests.get(url).json()
    top100_data = sorted(data, key=lambda k: (float(k['mktcap'])), reverse=True)[:100]
    ordered_data = sorted(top100_data, key=lambda k: (float(k['mktcap'])),
                          reverse=True)[:5]
    raw_data_increase = {}
    for currency in ordered_data:
        name = currency['long']
        market_cap = float(currency['mktcap'])
        market_cap_rounded = '$' + f'{market_cap:,.2f}'
        price = float(currency['price'])
        price_rounded = '$' + f'{price:.2f}'

        raw_data_increase.setdefault('Name', [])
        raw_data_increase['Name'].append(name)
        raw_data_increase.setdefault('Market Cap', [])
        raw_data_increase['Market Cap'].append(market_cap_rounded)
        raw_data_increase.setdefault('Price', [])
        raw_data_increase['Price'].append(price_rounded)

    df = pd.DataFrame(raw_data_increase,
                      columns=['Name', 'Market Cap', 'Price'])
    df.to_csv('top5_mktcap.csv', index=False)
    data_read = pd.read_csv('top5_mktcap.csv')
    data_read.set_index(['Name'], inplace=True)
    data_read.index.name = None
    html_data = data_read.to_html()
    return html_data


def get_top5_volume():
    url = 'http://coincap.io/front'
    data = requests.get(url).json()
    top100_data = sorted(data, key=lambda k: (float(k['mktcap'])), reverse=True)[:100]
    ordered_data = sorted(top100_data, key=lambda k: (float(k['usdVolume'])),
                          reverse=True)[:5]
    raw_data_increase = {}
    for currency in ordered_data:
        name = currency['long']
        usd_volume = float(currency['usdVolume'])
        usd_volume_rounded = '$' + f'{usd_volume:,.2f}'
        price = float(currency['price'])
        price_rounded = '$' + f'{price:.2f}'

        raw_data_increase.setdefault('Name', [])
        raw_data_increase['Name'].append(name)
        raw_data_increase.setdefault('24h Trade Volume', [])
        raw_data_increase['24h Trade Volume'].append(usd_volume_rounded)
        raw_data_increase.setdefault('Price', [])
        raw_data_increase['Price'].append(price_rounded)

    df = pd.DataFrame(raw_data_increase,
                      columns=['Name', '24h Trade Volume', 'Price'])
    df.to_csv('top5_volume.csv', index=False)
    data_read = pd.read_csv('top5_volume.csv')
    data_read.set_index(['Name'], inplace=True)
    data_read.index.name = None
    html_data = data_read.to_html()
    return html_data


def btc_chg():
    btc_url = 'http://coincap.io/history/30day/BTC'
    btc_data = requests.get(btc_url).json()
    price_list = []
    time_list = []
    df_price = {}
    img = io.BytesIO()

    for values in btc_data['price']:
        time = values[0]
        time = int(str(time)[:10])
        converted_time = datetime.datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

        df_price.setdefault('Datetime', [])
        df_price['Datetime'].append(converted_time)
        df_price.setdefault('Price', [])
        df_price['Price'].append(str(values[1]))

        df = pd.DataFrame(df_price, columns=['Datetime', 'Price'])

        price_list.append(str(values[1]))
        time_list.append(converted_time)

    df.to_csv('btc_30d_chg.csv')
    graph = pd.read_csv('btc_30d_chg.csv', parse_dates=True, index_col=1)
    graph['Price'].plot()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Bitcoin changes (30d)')
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


@app.route('/')
def index():
    top5_percent = get_top5_inc()
    top5_mktcap = get_top5_mktcap()
    top5_volume = get_top5_volume()
    btc_graph = btc_chg()
    return render_template('index.html', tables=[top5_percent, top5_mktcap, top5_volume],
                           graph=btc_graph,
                           titles=['coins', 'Top 5 by percent increase in the last 24 hours.',
                                   'Top 5 by Market Capitalization.', 'Top 5 by 24h Trade Volume.'])


if __name__ == '__main__':
    app.run(debug=True)
