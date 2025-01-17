from supabase_client import get_supabase_client

supabase = get_supabase_client()

def register_user(email, password, role="user"):
    try:
        # Sign up the user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        user = response.user

        if user:
            # Insert user details into the users table
            user_id = user.id
            insert_response = supabase.table('users').insert({
                "id": user_id,
                "email": email,
                "role": role
            }).execute()

            # Check if the insert operation was successful by verifying the `data` attribute
            if insert_response and hasattr(insert_response, 'data') and insert_response.data:
                # Automatically log in the user
                return {
                    "success": True,
                    "message": "User registered and logged in successfully!",
                    "user": user,
                    "role": role
                }
            else:
                print(f"User insertion failed: {insert_response}")
                return {"success": False, "message": "Failed to register user in database."}

        return {"success": False, "message": "Failed to register user."}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": str(e)}





def login_user(email, password):
    try:
        # Sign in the user using email and password
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # Extract the user information from the response
        user = response.user
        
        if user:
            user_id = user.id  # This will be the UUID
            # Fetch user role from the database using the UUID `id`
            user_data = supabase.table('users').select('role').eq('id', user_id).execute()
            if user_data.data:
                return {"response": response, "role": user_data.data[0]['role']}
            else:
                return {"response": response, "role": "user"}
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None




