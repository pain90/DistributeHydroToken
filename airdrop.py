import json
import web3
import requests
import time
import math
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

from web3 import Web3, IPCProvider, TestRPCProvider, middleware
from web3.contract import ConciseContract
# from web3.gas_strategies.time_based import medium_gas_price_strategy

# Loading the Hydro Smart Contract ABI
# Note this is the testnet ABI which is slightly different than the mainnet version
with open('airdropAbi.json') as abi_json:
  airdropABI = json.load(abi_json)

# with open('accounts.json') as accounts_json:
#   accounts = json.load(accounts_json)
#   print(len(accounts))

# This will need to point to your geth node
w3 = Web3(IPCProvider('/Users/andychorlian/Library/Ethereum/testnet/geth.ipc'))
print(w3.eth.gasPrice)

contract_address = '0x5765dc88a1b88220b31d3b7b3701a9aed6432d63'
airdropContract = w3.eth.contract(airdropABI, contract_address, ContractFactoryClass=ConciseContract)

address_list = []
balance_list = []

w3.personal.unlockAccount(w3.eth.accounts[0], '$Hedgeable4124$')

for x in range(1, 227):

    q = Request("http://etherscan.io/token/generic-tokenholders2?a=0x12fb5d5802c3b284761d76c3e723ea913877afba&s=1.1111111111E%2b28&p=" + str(x))
    q.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    q.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    q.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
    q.add_header('Accept-Encoding', 'none')
    q.add_header('Accept-Language', 'en-US,en;q=0.8')
    q.add_header('Connection', 'keep-alive')

    with urlopen(q) as a:

        soup = BeautifulSoup(a, "lxml")

        table = soup.table

        table_rows = table.find_all('tr')

        for row in table_rows:
            balance_test = row.find_all('td')
            if balance_test == []:
                continue;
            address_to_balance = {}
            address_list.append(str(balance_test[1].contents[0].contents[0].contents[0]))
            balance_list.append(math.ceil(float(balance_test[2].contents[0])))

        print("finished page " + str(x))

    if (x % 30 == 1):
        time.sleep(15)

print(len(balance_list))
print(len(address_list))

with open("balances_final.json", 'w') as f:
    f.write(str(balance_list))

with open("address_final.json", 'w') as f:
    f.write(str(address_list))
#
# balance_batch = []
# address_batch = []
#
# for y in range(0, len(balance_list)):
#     balance_batch.append(balance_list[y])
#     address_batch.append(address_list[y])
#     if ((y % 100 == 0) and (y != 0)):
#         print("Sending tokens " + str(y))
#         # print(address_batch)
#         trxHash = airdropContract.setBalances(address_batch, balance_batch, transact={'from':w3.eth.accounts[0], 'gasPrice':3000000000, 'gasLimit':3000000})
#         address_batch = []
#         balance_batch = []
#         time.sleep(8)
#
# trxHash = airdropContract.setBalances(address_batch, balance_batch, transact={'from':w3.eth.accounts[0], 'gasPrice':3000000000, 'gasLimit':3000000})
#

# print(balance_list)

#
# recipients = []
#
# for i in range(0, len(accounts)):
# 	if (w3.isAddress(accounts[i])):
# 		recipients.append(accounts[i])
# 	if ((i+1) % 80 == 0):
# 		trxHash = airdropContract.airdropTokensBulk(recipients, 10000000000000000000, transact={'from':w3.eth.accounts[0], 'gasPrice':1000000000})
# 		recipients = []
# 		# # Wait for the transaction to be mined
# 		# while (w3.eth.getTransactionReceipt(trxHash) == None):
# 		# 	print("Waiting for transaction to be mined")
# 		# 	time.sleep(5)
# 		print("-----------------------------------------")
# 		print("Batch " + str((i + 1) // 80) + " of " + str(len(accounts) // 80) + " complete")
# 		print("-----------------------------------------")
#
# if len(recipients) > 0:
# 	trxHash = airdropContract.airdropTokensBulk(recipients, 10000000000000000000, transact={'from':w3.eth.accounts[0], 'gasPrice':1000000000})
# 	recipients = []
# 	# Wait for the transaction to be mined
# 	# while (w3.eth.getTransactionReceipt(trxHash) == None):
# 	# 	print("Waiting for transaction to be mined")
# 	# 	time.sleep(5)
# 	print("-----------------------------------------")
# 	print("Final leftover batch comlete")
# 	print("-----------------------------------------")
