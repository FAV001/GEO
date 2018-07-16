from configobj import ConfigObj
import requests
import csv
import bs4

run = True

def get_geo(url, address):
    link = url + '?geocode=' + address
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    if use_proxy == True:
        r = requests.get(link, proxies=proxy, verify=False, headers = headers)
        pass
    else:
        r = requests.get(link, headers = headers)
        pass
    main_soap = bs4.BeautifulSoup(r.text, 'lxml')
    return main_soap

def get_featuremember(text):
    featuremember_soap = text.find_all('featuremember')
    for row in featuremember_soap:
        comp = get_component(row)
        write_row(comp)
    return

def get_component(text):
    ret = dict()
    ret['source'] = in_query
    ret['latitude'] = (text.find_all('pos')[0].text).split(' ')[1]
    ret['longitude'] = (text.find_all('pos')[0].text).split(' ')[0]
    a = ''
    temp_soap = text.find_all('component')
    for n in temp_soap:
        a += n.next.next.next.next.next.next
        if temp_soap.index(n) != (len(temp_soap) - 1):
                a += ', '
    ret['name'] = a
    return ret

def write_row(item):
    global run
    if run == True:
        with open('out.csv', "w") as output:
            writer = csv.writer(output, lineterminator='\n', delimiter=';')
            writer.writerow([item['source'],item['name'],item['latitude'],item['longitude']])
        run = False
    else:
        with open('out.csv', "a") as output:
            writer = csv.writer(output, lineterminator='\n', delimiter=';')
            writer.writerow([item['source'],item['name'],item['latitude'],item['longitude']])
    pass

def main():
    config = ConfigObj('geo.cfg')
    geo_url = config['GEOCoder']['url']
    #получили ссылку на геокодер Яндекса

    global use_proxy
    use_proxy = config.get('Proxy').as_bool('use_proxy')
    proxy_list = config['Proxy']['Proxy']
    global proxy
    proxy = {
        'http': 'http://' + proxy_list,
        'https': 'http://' + proxy_list
    }
    global in_query
    with open('in.csv','r') as f:
        in_list = list(csv.reader(f))
    for row in in_list:
        s = ''
        for r in row:
            s += r
            if row.index(r) != (len(row) - 1):
                s += ', '
        #print(s)
        in_query = s
        soap = get_geo(geo_url, s)
        get_featuremember(soap)
    #     out_list.append(get_geo(geo_url, s))

    pass

if __name__ == '__main__':
    main()


    # found = int(main_soap.find_all('found')[0].text)
    # print(main_soap.find_all('found'))
    # ret['source'] = address
    # ret['latitude'] = (main_soap.find_all('pos')[0].text).split(' ')[1]
    # ret['longitude'] = (main_soap.find_all('pos')[0].text).split(' ')[0]
    # a = ''
    # temp_soap = main_soap.find_all('component')
    # for n in temp_soap:
    #     a += n.next.next.next.next.next.next
    #     if temp_soap.index(n) != (len(temp_soap) - 1):
    #             a += ', '
    # ret['name'] = a
