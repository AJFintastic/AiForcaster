# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:02:20 2024

@author: user
"""

from supabase import create_client, Client

# Replace these with your actual project URL and API Key
SUPABASE_URL = "https://bqvxvlsxbumchobifewl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxdnh2bHN4YnVtY2hvYmlmZXdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkyMzc3NzgsImV4cCI6MjA0NDgxMzc3OH0.dnZyICdudVlCqRW5W_O_Z57kP2z1nkUDYB2ObZgD6Vk"


# Function to get the Supabase client
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
