from configobj import ConfigObj
import requests

def main():
    config = ConfigObj('geo.cfg')
    geo_url = config['GEOCoder']['url']
    #получили ссылку на геокодер Яндекса
    print(geo_url)
    pass

if __name__ == '__main__':
    main()
