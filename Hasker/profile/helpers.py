from Hasker.profile.forms import HaskerUserForm, HaskerUserSettingsForm


def save_haskeruser_by_form(request, context):
    user_form = HaskerUserForm(request.POST, request.FILES)

    context.update({'form': user_form})
    if user_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()
        context.update({'user': user})
        return user


def update_hasker_user_by_form(request, context):
    user = context['user']
    user_settings_form = HaskerUserSettingsForm(request.POST, request.FILES, instance=user)
    context.update({'form': user_settings_form})
    if user_settings_form.is_valid():
        user_update = user_settings_form.save(commit=False)
        user_update.set_password(user_update.password)
        user_update.save()
        context.update({'user': user_update})
        return user