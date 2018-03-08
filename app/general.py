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


def thirty_days_chg():
    btc_url = 'http://coincap.io/history/30day/BTC'
    btc_data = requests.get(btc_url).json()
    nano_url = 'http://coincap.io/history/30day/NANO'
    nano_data = requests.get(nano_url).json()
    eth_url = 'http://coincap.io/history/30day/ETH'
    eth_data = requests.get(eth_url).json()

    img = io.BytesIO()

    btc_price_list = []
    btc_time_list = []
    btc_df_price = {}
    for values in btc_data['price']:
        time = values[0]
        time = int(str(time)[:10])
        converted_time = datetime.datetime.utcfromtimestamp(time).strftime(
            '%Y-%m-%d %H:%M:%S')

        btc_df_price.setdefault('Datetime', [])
        btc_df_price['Datetime'].append(converted_time)
        btc_df_price.setdefault('Price', [])
        btc_df_price['Price'].append(str(values[1]))

        btc_df = pd.DataFrame(btc_df_price, columns=['Datetime', 'Price'])

        btc_price_list.append(str(values[1]))
        btc_time_list.append(converted_time)

    btc_df.to_csv('btc_30d_chg.csv')

    nano_price_list = []
    nano_time_list = []
    nano_df_price = {}
    for values in nano_data['price']:
        time = values[0]
        time = int(str(time)[:10])
        converted_time = datetime.datetime.utcfromtimestamp(time).strftime(
            '%Y-%m-%d %H:%M:%S')

        nano_df_price.setdefault('Datetime', [])
        nano_df_price['Datetime'].append(converted_time)
        nano_df_price.setdefault('Price', [])
        nano_df_price['Price'].append(str(values[1]))

        nano_df = pd.DataFrame(nano_df_price, columns=['Datetime', 'Price'])

        nano_price_list.append(str(values[1]))
        nano_time_list.append(converted_time)

    nano_df.to_csv('nano_30d_chg.csv')

    eth_price_list = []
    eth_time_list = []
    eth_df_price = {}

    for values in eth_data['price']:
        time = values[0]
        time = int(str(time)[:10])
        converted_time = datetime.datetime.utcfromtimestamp(time).strftime(
            '%Y-%m-%d %H:%M:%S')

        eth_df_price.setdefault('Datetime', [])
        eth_df_price['Datetime'].append(converted_time)
        eth_df_price.setdefault('Price', [])
        eth_df_price['Price'].append(str(values[1]))

        eth_df = pd.DataFrame(eth_df_price, columns=['Datetime', 'Price'])

        eth_price_list.append(str(values[1]))
        eth_time_list.append(converted_time)

    eth_df.to_csv('eth_30d_chg.csv')

    btc_graph = pd.read_csv('btc_30d_chg.csv', parse_dates=True, index_col=1)
    nano_graph = pd.read_csv('nano_30d_chg.csv', parse_dates=True, index_col=1)
    eth_graph = pd.read_csv('eth_30d_chg.csv', parse_dates=True, index_col=1)

    x = btc_graph['Price']
    y = eth_graph['Price']
    z = nano_graph['Price']

    f, axarr = plt.subplots(3, sharex=True, figsize=(8, 12))
    # f.suptitle('Bitcoin and NANO changes (30d)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    axarr[0].plot(x)
    axarr[0].set_title('Bitcoin')
    axarr[1].plot(y)
    axarr[1].set_title('Ethereum')
    axarr[2].plot(z)
    axarr[2].set_title('NANO')

    f.set_facecolor('#F2F2F2')

    plt.gca().set_aspect('equal', adjustable='datalim')

    f.subplots_adjust(hspace=0.3)

    # plt.show()
    plt.savefig(img, format='png', facecolor=f.get_facecolor())
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


@app.route('/')
def index():
    top5_percent = get_top5_inc()
    top5_mktcap = get_top5_mktcap()
    top5_volume = get_top5_volume()
    graphs = thirty_days_chg()
    return render_template('index.html', tables=[top5_percent, top5_mktcap, top5_volume],
                           graphs=graphs,
                           titles=['coins', 'Top 5 by percent increase in the last 24 hours.',
                                   'Top 5 by Market Capitalization.', 'Top 5 by 24h Trade Volume.'])


if __name__ == '__main__':
    app.run(debug=True)
