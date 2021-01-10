from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime, timedelta

BASEURL = 'http://157.90.24.177:3000/'
PARAMS = {}

def index(request):

    # Total Supply
    totalSupplyView = 'total_supply'
    totalSupplyUrl = BASEURL + totalSupplyView
    totalSupplyResponse = requests.get(totalSupplyUrl).json()[0]
    totalSupply = totalSupplyResponse['current_supply']
    totalSupply = round(totalSupply, 2)

    # Active Stake
    activeStakeView = 'active_stake'
    activeStakeUrl = BASEURL + activeStakeView
    activeStakeResponse = requests.get(activeStakeUrl).json()[0]
    activeStake = activeStakeResponse['active_stake']
    activeStake = round(activeStake, 2)

    # Transactions
    totalTransactionsView = 'total_transactions'
    totalTransactionsUrl = BASEURL + totalTransactionsView
    totalTransactionsResponse = requests.get(totalTransactionsUrl).json()[0]
    totalTransactionsCount = totalTransactionsResponse['total_count']
    totalTransactionsAmount = round(totalTransactionsResponse['total_amount'], 2)

    # Current Epoch
    currentEpochView = 'epoch'
    currentEpochUrl = BASEURL + currentEpochView
    PARAMS = {
        'order': 'no.desc',
        'limit': 1
    }
    currentEpochResponse = requests.get(currentEpochUrl, PARAMS).json()[0]
    currentEpochBlocks = currentEpochResponse['blk_count']
    currentEpochTransactions = currentEpochResponse['tx_count']
    currentEpochFees = round(currentEpochResponse['fees'] / 1000000, 2)
    currentEpoch = currentEpochResponse['no']

    # Epoch Progress
    currentEpochStart = currentEpochResponse['start_time']
    currentEpochStartDatetime = datetime.strptime(currentEpochStart, '%Y-%m-%dT%H:%M:%S')
    currentEpochEndDatetime = currentEpochStartDatetime + timedelta(days = 5)
    startTimestamp = datetime.timestamp(currentEpochStartDatetime)
    endTimestamp = datetime.timestamp(currentEpochEndDatetime)
    nowTimestamp = datetime.now().timestamp()
    distance = endTimestamp - startTimestamp
    distanceLeft = endTimestamp - nowTimestamp
    epochProgress = round(100 - (distanceLeft / distance * 100), 1)
    currentEpochSlot = distance - distanceLeft

    # Latest Blocks
    latestBlocksView = 'latest_blocks'
    latestBlocksUrl = BASEURL + latestBlocksView
    latestBlocksResponse = requests.get(latestBlocksUrl).json()
    latestBlocks = []
    i = 0
    for block in latestBlocksResponse:
        i += 1
        tempBlock = {}
        tempBlock['size'] = f"{block['size']} B"
        time = datetime.strptime(block['time'], '%Y-%m-%dT%H:%M:%S')
        tempBlock['time'] = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
        tempBlock['hash'] = block['block_hash'][3:]
        tempBlock['tx_count'] = block['tx_count']
        tempBlock['block_no'] = block['block_no']

        try:
            metadataResponse = requests.get(block['metadata_url']).json()
            tempBlock['ticker'] = metadataResponse['ticker']
            tempBlock['name'] = metadataResponse['name']
            tempBlock['homepage'] = metadataResponse['homepage']
        except:
            pass

        tempBlock['identifier'] = i
        latestBlocks.append(tempBlock)


    # Richest Wallets
    richestWalletsView = 'richest_wallets'
    richestWalletsUrl = BASEURL + richestWalletsView
    richestWalletsResponse = requests.get(richestWalletsUrl).json()
    richestWallets = richestWalletsResponse



    return render(request, 'cardanodash/index.html', {
        'totalSupply': f"{totalSupply:,}",
        'totalSupplyBillions': round(totalSupply / 1000000000, 1),
        'activeStake': f"{activeStake:,}",
        'activeStakeBillions': round(activeStake / 1000000000, 1),
        'totalTransactionsCount': f"{totalTransactionsCount:,}",
        'totalTransactionsAmount': f"{totalTransactionsAmount:,}",
        'currentEpochBlocks': f"{currentEpochBlocks:,}",
        'currentEpochTransactions': f"{currentEpochTransactions:,}",
        'currentEpochFees': f"{currentEpochFees:,}",
        'currentEpoch': currentEpoch,
        'epochProgress': epochProgress,
        'currentEpochSlot': int(currentEpochSlot),
        'epochSlots': int(distance),
        'latestBlocks': latestBlocks,
        'richestWallets': richestWallets
    })