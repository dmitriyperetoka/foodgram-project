def user_purchases_count(request):
    count = (
        request.user.purchases.count()
        if request.user.is_authenticated
        else None
    )
    return {'user_purchases_count': count}
