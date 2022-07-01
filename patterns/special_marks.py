vultype_exclude = [set()] * 31
vultype_exclude[3] = {'oob', 'cross', 'buffer', 'format', 'inclus', 'signatur', 'bound', 'disclosur', 'travers', 'null'}
vultype_exclude[4] = {'leak', 'corrupt', 'use after', 'protect', 'access', 'exhaust', 'consumpt'}
vultype_exclude[6] = {'xml', 'credenti', 'memori', 'file', 'path', 'databas'}
vultype_exclude[11] = {'buffer', 'authent', 'bypass'}
vultype_exclude[16] = {'cross', 'xss'}
vultype_exclude[-5] = {'search', }

vul_type = [{'race', 'concurr', 'corruption/concurr'}, # CWE-362, 367
            {'rce'}, # 128
            {'dll preload', 'dll hijack', 'dll load', 'tty hijack', 'load dll', 'search ord hijack', 'file handler hijack'}, # 426, 427

            {'privileg', 'escal', 'permiss', 'access', 'bypass', 'authent',  'account', 'credenti',  'encrypt',  'unauthor' # 287, 264
                , 'reboot', 'admin', 'login', 'debug', 'interfac', 'breakout','download', 'flood', 'load', 'ssh', 'brute forc', 'bruteforc', 'brute'
             'authorization', 'hash', 'restart', 'process kil' ,'root', 'read', 'daemon', 'undocu commun string', 'snmp', 'administr', 'monitor',
             'chang'},

            {'heap', 'buffer', 'arrow', 'stack', 'floating point', 'oob', 'overrun', 'bound', 'overflow', 'underflow', 'integ', 'truncat', # 119
             'over read', 'clash', 'overflow/underflow', 'pri/oob', 'oom', 'overread', 'excess', 'stackoverflowerror',
             'jailbreak', 'jail', 'address derefer', 'array dereferenc', 'smb negoti processid function tabl derefer',
             'memori', 'memory', 'heart',},

            {'memori exhaust', 'memori consumpt'}, #674, 770
            {'leak', 'unsaf storag', 'exposur', 'password', 'disclosur', 'information', 'infoleak', 'leakag', 'view'}, # 200

            {'memori leak', 'memori leakag'}, # 399
            {'cwe'}, # \
            {'divide by zero', 'divid zero', 'divis zero'}, # 369, 189
            {'null byte', 'pointer', 'null pointer derefer', 'offset derefer', 'nullpoint derefer', 'doubl derefer', 'null derefer', 'invalid derefer'}, # 476
            {'session poison', 'session fixact', 'session fixat', 'session fix'}, # 384, 287
            {'unquot'}, # 428, 264
            {'format string', 'format str', 'string format'}, # 134
            {'cach pollut', 'cach poison'}, # 444
            {'failur', 'panic', 'kernel', 'consumpt', 'except handl', 'assert', 'denial', 'dos', 'crash', 'zip slip', 'hang', 'exhaust', # 730
             'shutdown', 'corrupt', 'disrupt', 'loop', 'fault'},
            {'code inject', 'script inject', 'remot file inclus'}, # 94, 74
            {'file upload'}, # 434
            {'command'}, # 77, 78, 74
            {'code execut'}, # \
            {'off by one', 'off by'}, # 193, 189, 119
            {'xss', 'css', 'cross sit script', 'obfusc', 'site script', 'temporari link', 'xss/sqli', 'csrf/xss', 'xss/csrf', 'linkjack', 'credenti disclosur'}, # 79
            {'redirect',}, # 601
            {'sql', 'databas'}, # 89
            {'free', 'use after fre', 'double', 'after fre', 'doube', 'use after destruct', 'use afte fre'}, # 825
            {'type confus'}, # 843
            {'directori', 'path', 'file creation', 'symbol', 'traves','travers', 'null', 'path disclosur', 'file disclosur', 'local file inclus'}, # 22
            {'csrf', 'cross sit request forgeri', 'forgeri', 'ssrf', 'xsrf','local socket hijack'}, # 352, 918
            {'input validation', 'valid'}, # 20
            {'xxe', 'xml', 'xxe/ssrf'}, # 611
            {'middle','middl',}] # \




impact_exclude =  vultype_exclude
impact_exclude[3] = impact_exclude[3].union({'steal victim cookie','jack', 'overwrite', 'execut arbitrari code system privileg victim'})
impact_exclude[6] = impact_exclude[6].union({'denial', 'privileg', 'sproof', })
impact_exclude[10] = impact_exclude[11]
impact_exclude[11] = set()
impact_exclude[13] = impact_exclude[16]
impact_exclude[16] = set()
impact_exclude[-4] = impact_exclude[-5]
impact_exclude[-5] = set()
impact_exclude[15] = impact_exclude[15].union({'command', })
impact_exclude[19] = impact_exclude[19].union({'download', 'obtain', 'bypass', 'overflow'})
impact_type = [{'race', 'concurr', 'corruption/concurr'}, # CWE-362, 367
            {'rce'}, # 128
            {'dll preload', 'dll hijack', 'dll load', 'tty hijack', 'load dll', 'search ord hijack', 'file handler hijack'}, # 426, 427

            {'privileg', 'escal', 'permiss', 'access', 'bypass', 'authent',  'account', 'credenti',  'encrypt',  'unauthor' # 287, 264
                , 'reboot', 'admin', 'login', 'debug', 'interfac', 'breakout','download', 'flood', 'load', 'ssh', 'brute forc', 'bruteforc', 'brute'
             'authorization', 'hash', 'restart', 'process kil' ,'root', 'read', 'daemon', 'undocu commun string', 'snmp','delete',
               'authent', 'creat', 'read', 'writ', 'overwrit', 'perform'},

            {'heap', 'buffer', 'arrow', 'stack', 'floating point', 'oob', 'overrun', 'bound', 'overflow', 'underflow', 'integ', 'truncat', # 119
             'over read', 'clash', 'overflow/underflow', 'pri/oob', 'oom', 'overread', 'excess', 'stackoverflowerror',
             'jailbreak', 'jail', 'address derefer', 'array dereferenc', 'smb negoti processid function tabl derefer',
             'heart','execut arbitrari code'},

            {'memori exhaust', 'memori consumpt', 'memori leak', 'memori leakag'}, # 399
            {'leak', 'unsaf storag', 'exposur', 'password', 'disclosur', 'information', 'infoleak', 'leakag', 'obtain', 'sensit', 'disclos',
             'inform', 'gain', 'password', 'chang', 'crypt', 'discov', 'memori', 'memory'}, # 200

            {'cwe'}, # \
            {'divide by zero', 'divid zero', 'divis zero'}, # 369, 189
            {'null pointer derefer',  'nullpoint derefer', 'null derefer'}, # 476
            {'session poison', 'session fixact', 'session fixat', 'session fix'}, # 384, 287
            {'unquot'}, # 428, 264
            {'format string', 'format str', 'string format'}, # 134

            {'code inject', 'script inject', 'remot file inclus'}, # 94, 74
            {'file upload', 'upload'}, # 434
            {'command',}, # 77, 78, 74

            {'xss', 'css', 'cross sit script', 'obfusc', 'site script', 'temporari link', 'xss/sqli', 'csrf/xss', 'xss/csrf', 'linkjack', 'credenti disclosur',
             'steal victim cookie'}, # 79
            {'redirect',}, # 601
            {'sql', 'databas'}, # 89
            {'free', 'use after fre', 'double', 'after fre', 'doube', 'use after destruct', 'use afte fre','caus pointer reus freed'}, # 825

            {'directori', 'file creation', 'symbol', 'traves','travers', 'null', 'path disclosur', 'file disclosur', 'local file inclus',
             'view arbitrari file', 'read arbitrari file', 'retriev arbitrari file', 'delet arbitrari file', 'creat arbitrari file', 'upload arbitrari file'}, # 22
            {'csrf', 'cross sit request forgeri', 'forgeri', 'ssrf', 'xsrf','local socket hijack', 'sproof', 'jack'}, # 352, 918, 611
            {'middle','middl',}] # \



root_type = [{'race', 'concurr', 'corruption/concurr'}, # CWE-362, 367

            {'privileg', 'escal', 'permiss', 'access', 'bypass', 'authent',  'account', 'credenti',  'encrypt',  'unauthor' # 287, 264
                , 'reboot', 'admin', 'login', 'debug', 'interfac', 'breakout','download', 'flood', 'load', 'ssh', 'brute forc', 'bruteforc', 'brute'
             'authorization', 'hash', 'restart', 'process kil' ,'root', 'read', 'daemon', 'undocu commun string', 'snmp', 'administr', 'monitor',
             'chang'},

            {'heap', 'buffer', 'arrow', 'stack', 'floating point', 'oob', 'overrun', 'bound', 'overflow', 'underflow', 'integ', 'truncat', # 119
             'over read', 'clash', 'overflow/underflow', 'pri/oob', 'oom', 'overread', 'excess', 'stackoverflowerror',
             'jailbreak', 'jail', 'address derefer', 'array dereferenc', 'smb negoti processid function tabl derefer',
             'memori', 'memory', 'heart',},

            {'memori exhaust', 'memori consumpt'}, #674, 770

            {'divide by zero', 'divid zero', 'divis zero'}, # 369, 189
            {'session poison', 'session fixact', 'session fixat', 'session fix'}, # 384, 287
            {'unquot'}, # 428, 264
            {'format string', 'format str', 'string format'}, # 134

            {'code inject', 'script inject', 'remot file inclus'}, # 94, 74
            {'file upload'}, # 434
            {'command'}, # 77, 78, 74

            {'off by one', 'off by'}, # 193, 189, 119
            {'xss', 'css', 'cross sit script', 'obfusc', 'site script', 'temporari link', 'xss/sqli', 'csrf/xss', 'xss/csrf', 'linkjack', 'credenti disclosur'}, # 79
            {'redirect',}, # 601
            {'sql', 'databas'}, # 89
            {'free', 'use after fre', 'double', 'after fre', 'doube', 'use after destruct', 'use afte fre'}, # 825
            {'type confus'}, # 843
            {'directori', 'path', 'file creation', 'symbol', 'traves','travers', 'null', 'path disclosur', 'file disclosur', 'local file inclus'}, # 22
            {'csrf', 'cross sit request forgeri', 'forgeri', 'ssrf', 'xsrf','local socket hijack'}, # 352, 918
            {'xxe', 'xml', 'xxe/ssrf'}] # 611

root_exclude = [set()] * 31
root_exclude[1] = {'oob', 'cross', 'buffer', 'format', 'inclus', 'signatur', 'bound', 'disclosur', 'travers',
                           'null', 'memori', 'array', }
root_exclude[2] = {'leak', 'corrupt', 'use after', 'protect', 'access', 'exhaust', 'consumpt'}
root_exclude[5] = {'buffer', 'authent', 'bypass'}
root_exclude[8] = {'cross', 'xss'}
root_exclude[10] = {'sever', 'improp input valid command argument', 'pointer', 'invalid', 'argument'}
root_exclude[-3] = {'search', 'access', 'permiss'}



