def safe_user_details(strategy, details, user=None, *args, **kwargs):
    """
    Update first/last name ONLY if they are currently blank.
    Never overwrite existing names.
    """
    if not user:
        return
    changed = False
    if not user.first_name and details.get('first_name'):
        user.first_name = details['first_name']; changed = True
    if not user.last_name and details.get('last_name'):
        user.last_name = details['last_name']; changed = True
    if changed:
        user.save()
