# Banano Blockchain Visualisation Tool

## What is the Banano Visualisation Tool
This tool was initially created as part of an honours project for the University of Abertay Dundee.
It is a Python 3.7 application designed to help make understanding the transactions on the Banano Blockchain easier to
follow. It was written in Python in order allow it to be run on any OS however it has only been tested on Windows 10 and 
Windows 7. 

## Running the Application
### Dependencies
The application requires Python 3.7 to be installed and the following libraries to be installed.
```
pyqt5
matplotlib
networkx
requests
aiohttp
scipy
```
On Windows these can be easily installed by running setup.bat.

### Requirements
In order to access blockchain data, the tool needs to retrieve data from a Banano node. By default the tool requests 
data from a personal node hosted at "http://206.189.120.80:7072". On first run of gui.py, config.cfg is created
and the node that is used can be changed should you wish to change it in case of preference or the node is no longer
online. The default contents of the configutation file are as follows:
```json
[{"host": "http://206.189.120.80:7072", "default address": "ban_1tc93no6sebhpbh69b877wy3hhhxriqoj5cneq3qbfg9skw63o9wbezrjmka"}]
```
In order to run your own Banano node, instructions for running it using Docker can be found [HERE](https://github.com/BananoCoin/banano/wiki/Running-a-Docker-Bananode)
and instructions for building it from source can be found [HERE](https://github.com/BananoCoin/banano/wiki/Building-a-Bananode-from-sources)
. The default ports for a Banano Node are 7071 and 7072.

### Using the application
Once all dependencies have been installed and a node is online and synced with the Banano network, the application is
ready to be used. It can be executed by running gui.py with Python 3. The following features are available within the 
application.

1. Setting an address to perform a visualisation of. A default address can be set in config.cfg
2. Setting how many transactions wide to search. This starts from the most recent transaction down to the transaction 
specified
3. Setting the depth of the search allows you to limit whether your relationship search goes beyond the initial address
4. Importing a list of addresses separated by colons. This can be useful for highlighting known addresses that may be of
interest such as exchanges. The shortest path to known addresses it output in the console
5. A Banano only feature* is the highlighting of addresses owned by the BananoBet gambling site (displayed in cyan) and 
Discord Tipping bot (displayed in yellow)
6. Upon each history search, the graph is also saved as a .gefx format in the execution directory which can be opened 
with [Gephi](https://gephi.org)

\*While this application is written specifically for Banano, if the target data node is configured to be that of a Nano
node or other fork of Nano it should work as the nodes run the same protocols however this has not been tested. 

##Useful resources
List of exchanges and their related addresses:
```
ban_31dhbgirwzd3ce7naor6o94woefws9hpxu4q8uxm1bz98w89zqpfks5rk3ad:Mercatox
ban_3k76rawffjm79qedoc54nhk3edkq5makoyp73b1t6q6j9yjeq633q1xck9g8:Mercatox Withdraw
ban_1gtkt1ekpazojhxwnym9ur61cz4w7n8yez5yq81id6cb8k63bhwx7axhtsxx:Bitmesh
ban_3x1o69xsppjb1d9owsn8x6uqr8a1ttpitsu3yya7iyimaboqhb9urb8x61y8:Txbit
ban_3wwd51yoxeafubpn84gy7tje7yw6ccqcach9m4yfn46sf15itnysap9dd1xc:Citex
ban_3w6yatruhkxgu4bhx1d8zggpwafrq3z7xyrqchuw8h5xa9aqhnrj7mi79mtu:QBTC
ban_3yafcjcq79cjfm4wio5db6drffmf61jh8cosoijmg3eppzmbxb4kej8t3dze:QTrade
ban_16bfuppfebtmgh1t8ktpk4eq4dyz5m1ztxesznagd916jzk8b87qity3habz:Unnamed
ban_1bujgzb69qr4owkcm3qu35mb843qtwnx4zf8q3myjw1dui7br5k87k84e54d:ViteX
ban_1gooj14qko1u6md87aga9c53nf4iphyt1ua7x3kq1wnkdh49u5mndqygbr1q:Ataix
ban_1fxc48dynhbjb69uuyue4bsfuymxick8js14synwznduy61g6i9esdeasmem:GJ
ban_36e1qnwo5faf7uapp6gbzzmzt3bgz6a93txuukmr45pmodcy4q7pwaray1u9:Atomars
ban_1oaocnrcaystcdtaae6woh381wftyg4k7bespu19m5w18ze699refhyzu6bo:nano.trade
ban_1ddaz5y8jk47hkicpi1kc38kg359r74y38gmmq6moiki11gx1g4a9qb4r7c6:moon.banano.trade
ban_16c58nu7kmays7bmfaq7u4zpf8oady9ydgwkb6pcxegyx3n1nxygix5r4hpi:Altilly
```
List of Banano distribution addresses:
```
ban_3he11oi45zcfe3i65wogyikf1569mu1jcf9kj4o7jojpebmmkbhrpf38qrqx:WeChat/Reddit
ban_1wha1enz8k8r65k6nb89cxqh6cq534zpixmuzqwbifpnqrsycuegbmh54au6:Banano Jumper
ban_1crane864e1cn1g3p9mrduf49hp86gfgfosp8rib43smxxuqp3phq1yiu58k:Crane
ban_1mine1fnjzz84gwapyqhfw1d115zst859pf1u5rzge8hehzjg9ztchokmghb:Miner
ban_3pp1antnfudas6ad44kwpad4jb376cihftskq9ne76hazosi654gjdohriai:MinerV2
ban_3fo1d1ng6mfqumfoojqby13nahaugqbe5n6n3trof4q8kg5amo9mribg4muo:Folding
ban_3faucb1o9ifundznqw6xn1xkybztz4zfbn4fw95ujfy48ds1ebayzycfsspk:Meme Faucet
ban_3temho9bnim1acqzwwa673yeggeudzo6y857y4t38pmu6jx79amtku8szp3s:Black Monkey 1
ban_1b1ack1188caohzjdj65uarnk4kobzrnr3q3oc3bew5rfkyqxzu81zhjgp1e:Black Monkey 2
ban_3runnerrxm74165sfmystpktzsyp7eurixwpk59tejnn8xamn8zog18abrda:Banano Runner
ban_3matchhw9ksc9xfqdhedfn34n8kw6woxr36gnyoop7jc14j7unw9uknhjk8h:Monkey Match 1
ban_1no4g7k51giqnhscpqm153hamoe956958yrr79sggzgy8wriiemx7owh89ka:Monkey Match Nov1
ban_1no3g6ho99zjfgujgkyqmmedi4k9u46yxwnf8bchxs4sof1yg334u8yrt4h5:Monkey Match Nov2
ban_1no1g31yq9ne9b1uhzge7co6af34qot37ydifagy13cb53ki7dor1yeceg8f:Monkey Match Nov3
ban_3jan54btk13gsutxw6brj1i7e31zip4zj43u4jde7qad3hchx8u1gc6jwxd9:Monkey Match Jan
ban_1mar4j94wjqnkourdfw1jwqzsn4a9p6fqfjzrjsyjiym4zixm1ek3bkqk1r7:Monkey Match Mar
ban_3craftbqpyfbr4gdjhdwnrsd4zwr73wg6xojnr61nres8mnbz5x1o6563qxc:BananoCraft
ban_1monkeyt1x77a1rp9bwtthajb8odapbmnzpyt8357ac8a1bcron34i3r9y66:Monkey Talks
ban_1boompow14irck1yauquqypt7afqrh8b6bbu5r93pc6hgbqs7z6o99frcuym:BoomPoW
ban_3disc5557sb9ri99h7czmn6ms5kcfsafnsxekarg1pp9f3a1ik4ndjcb9cod:Discord Beta
ban_3j67xu1yuhfbezm7myw7bhzekj1mdzjkhhtctrqz5d9sanar8wt6hkgexzwn:Volcano
ban_1santayq7qgtoar9s9kx9ur5jw6ustty741bxnidanf8miuakju7kqb8imwo:Santa Discord Bot
ban_1treatf1gc4acpgjqzg9jxthwqnew7gef5wf7mru4ffyeb9ayj61rejzs5st:Trick or Treat Bot
ban_1ce1ery6hqwyqqyh15m4atcoaywd8rycyapjjooqeg7gi149kmatjbb3wiwx:Celery/Salary
ban_1zookix8zpo13go1xrbwcmodjfsr8xw5e18smbmz8mh4orkmd33t8zmescpo:Distribution Allowances
ban_1nice4sy9fgcb8qxbx7nkj9ajc79aapqnayrfk4gow184mgnfm49ncstg36w:NiceBanano
``` 
List of Banano gambling services:
```
ban_3iejwmk1n3fqdntwcgudhmddo9bpwa8jzx6g361iq6rzbsrzonekmdus9yj5:Banano Royale
ban_1w5q77ocgfrjn6sqwudfuygtomwyij8ijes3y5g8kaydxsf8f4jpz4n9q9a3:Nanogames.io
ban_1banbet955hwemgsqrb8afycd3nykaqaxsn7iaydcctfrwi3rbb36y17fbcb:BanBet
ban_1kwin96znfqopi7be3shxcxn8qeruirob885oaya4ix5pkrnpsou4u5qbeaa:BanSlots
ban_16tduo1cu9ydp8ris3o5w4rm96myqics5o8tjw8s13ja8owba6xfpwc8399r:BanRoulette
ban_1p3oxrfuqddcb4r7ercjwdnxiyn1bwqspzettum7c8x1awsnd5zqtj5f1d6m:BC.Game
```
List of suspicious addresses:
```
ban_19i3rxxmdtxa7zsxoroygx38xpcad4gp7ouwf9bn5raum1d3mc4b5w7proxy:Banano Runner botter
ban_14bbb43paw4gtkc69j445e6ogxytns35ks9qk8pe7g37qyc7as63tipfz6gp:Seed wiper
ban_3ri6hkmndz8aehqjhuru1s5ozcb14ifzyqbax8p8arm9u7pykz6qoaj8rimz:bonus-program phish
```
Other:
```
ban_3imophzbk9ruq3ju18jyw37376h3wdeon15asw4yj3kfgxs6m1eg7784a4im:Tip.cc
```

The Banano Runner botter botted the Banano Runner faucet and took $15,000 worth of Banano. The seed wiper accessed logs
which were not meant to be visible and found publicly posted seeds.




