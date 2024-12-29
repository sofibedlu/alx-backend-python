from rest_framework_simplejwt.tokens import RefreshToken

# for A custom login endpoint or Token generation for admin-created users we need to override the default token generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Add custom claims
    refresh['email'] = user.email
    refresh['role'] = user.role
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
