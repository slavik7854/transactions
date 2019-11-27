from rest_framework import serializers

from .models import Account, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    A serializer for a Payment objects.
    """
    class Meta:
        model = Payment
        fields = ['account', 'amount', 'to_account', 'from_account', 'direction']
        read_only_fields = ('account', 'from_account', 'direction')

    def validate(self, attrs):
        '''
        Validation by currency wallet and balance of account
        '''
        if attrs.get('to_account').currency not in self.context['request'].user.account_set.values_list('currency',
                                                                                                        flat=True):
            raise serializers.ValidationError('You can made transfer only to next wallets: {}.'.format(
                list(self.context['request'].user.account_set.values_list('currency', flat=True))))

        if attrs.get('amount') > self.context['request'].user.account_set.get(
                currency=attrs.get('to_account').currency).balance:
            raise serializers.ValidationError('Maximum amount, that you can to transfer is {}{}.'.format(
                self.context['request'].user.account_set.get(
                    currency=attrs.get('to_account').currency).balance, attrs.get('to_account').currency))

        if attrs.get('to_account').user == self.context['request'].user:
            raise serializers.ValidationError('You can\'t to transfer to yourself account.')

        return attrs


class AccountSerializer(serializers.ModelSerializer):
    """
    A serializer for a Account objects.
    """
    class Meta:
        model = Account
        fields = ['user', 'balance', 'currency']
