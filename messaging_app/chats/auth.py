from rest_framework_simplejwt.tokens import RefreshToken

# Function to generate tokens with custom claims
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Add custom claims
    refresh['user_id'] = str(user.user_id)
    refresh['email'] = user.email
    refresh['role'] = user.role
    return refresh
