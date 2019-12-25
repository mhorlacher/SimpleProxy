import configparser

import psycopg2

class ProxyDB():
    def __init__(self, db_cfg):
        config = configparser.ConfigParser()
        config.read(db_cfg)
        
        self.conn = psycopg2.connect(**config['CREDENTIALS'])
        self.cur = self.conn.cursor()

        # Set encoding
        self.conn.set_client_encoding('UTF8')

    def insert(self, proxy):
        columns = ['ip_v4', 'port', 'type', 'delay', 'anonymity', 'status']
        columns += ['up_since', 'down_since', 'first_received', 'last_checked']

        insert_string = 'INSERT INTO proxies (%s) ' % (', '.join(columns))
        insert_string += 'VALUES (%s) ' % (', '.join(['%s']*len(columns)))
        insert_string += 'ON CONFLICT DO NOTHING'

        try:
            d = proxy.__dict__
            insert_values = [d[column] for column in columns]
        except:
            raise

        try:
            self.cur.execute(insert_string, insert_values)
            self.conn.commit()
        except:
            raise

    def fetch_proxies(self):
        columns = ['ip_v4', 'port', 'type', 'status']
        select_string = "SELECT %s FROM proxies WHERE status != 'DEAD'" % (', '.join(columns))

        try:
            self.cur.execute(select_string)
            proxy_table = self.cur.fetchall()
        except:
            raise

        proxy_list = list()
        for row in proxy_table:
            proxy_dict = dict(zip(['proxy_' + column for column in columns], row))
            proxy = Proxy(**proxy_dict)
            proxy_list.append(proxy)

        return proxy_list

    def delete_proxy(self, proxy):
        pass

    def update_proxy(self, proxy, update_dict):
        update_string = 'UPDATE proxies '
        update_string += 'SET delay = %s, status = %s, up_since = %s, '
        update_string += 'down_since = %s, last_checked = %s '
        update_string += 'WHERE ip_v4 = %s AND port = %s AND type = %s'

        try:
            update_values = [proxy.delay, proxy.status, proxy.up_since]
            update_values += [proxy.down_since, proxy.last_checked]
            update_values += [proxy.ip_v4, proxy.port, proxy.type]
        except:
            raise

        try:
            self.cur.execute(update_string, update_values)
            self.conn.commit()
        except:
            raise

    def get_rand_proxy(self):
        pass

