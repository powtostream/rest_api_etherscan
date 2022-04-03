import random
import json
import string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Token
from . import serializers

from web3 import Web3
from web3.middleware import geth_poa_middleware
from decouple import config


infura_url = config('INFURA_URL')
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = json.loads(config('ABI'))
contract_address = config('CONTRACT_ADDRESS')
myContract = w3.eth.contract(address=contract_address, abi=abi)
myAddress = config('PUBLIC_ADDRESS')
myPrivateKey = config('PRIVATE_KEY')


class Create(APIView):

    serializer_class = serializers.PostSerializer

    def post(self, request):
        serializer = serializers.PostSerializer(data=request.data)

        if serializer.is_valid() and w3.isAddress(w3.toChecksumAddress(serializer.data.get('owner'))):

            media_url = serializer.data.get('media_url')
            owner = w3.toChecksumAddress(serializer.data.get('owner'))

            unique_hash = ''.join(
                random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))

            nonce = w3.eth.getTransactionCount(myAddress, 'latest')

            txn = myContract.functions.mint(owner, unique_hash, media_url).buildTransaction({"nonce": nonce})
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=myPrivateKey)
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            new = Token(owner=owner, media_url=media_url,
                        tx_hash=txn_hash.hex(), unique_hash=unique_hash)
            new.save()

            serialized_response = serializers.TokenSerializer(new)

            return Response(serialized_response.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TotalSupply(APIView):
    def get(self, request):
        total = myContract.functions.totalSupply().call()
        return Response({'result': total})


class TokenList(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = serializers.TokenSerializer
