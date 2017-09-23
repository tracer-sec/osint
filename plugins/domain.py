import model

SUBDOMAINS = [
    'www',
    'web'
    'static',
    'images',
    'img',
    'cdn',
    'content',

    'mail',
    'pop3',
    'imap',
    'smtp',
    'exchange',

    'db',
    'db0',
    'db1',
    'db2',
    'db3',
    'db4',
    'db5',
    'sql',
    'mysql',
    'mssql',
    'sqlserver',
    'postgres',
    'mongo',
    'couchbase',
    'couch',
    'redis',
    'memcache',
    'elasticsearch',
    'elastic',

    'ftp',
    'sftp',
    'ftps',
    'fs',
    'file',
    'files',

    'ldap',
    'snmp',
    'backup',

    'logging',
    'logs',
    'syslog',
    'snort',
    'logstash',

    'dc',
    'dc0',
    'dc1',
    'dc2',
    'dc3',
    'dc4',
    'dc5',
    'pdc',
    'bdc',

    'ns',
    'ns0',
    'ns1',
    'ns2',
    'ns3',
    'ns4',
    'ns5',
    'ns6',
    'ns7',
    'ns8',
    'ns9',

    'cvs',
    'svn',
    'git',
    'mercurial',

    'staging',
    'dev',
    'development',
    'prod',
    'production',
    'test',
    'uat',
    'deploy',

    'ci',
    'jenkins',
    'teamcity',
    'gocd',

    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z'
]

client = None

def guess_subdomains(node):
    results = []
    for subdomain in SUBDOMAINS:
        test_domain = subdomain + '.' + node.name
        if client.domain_exists(test_domain):
            results.append(model.Node('domain', test_domain, None))

    return results

def get(config, c):
    global client
    client = c

    return [
        {
            'func': guess_subdomains,
            'name': 'Test for common subdomains',
            'acts_on': ['domain']
        }
    ]

