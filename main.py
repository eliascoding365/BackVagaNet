from fastapi import FastAPI
from db.supabase import create_supabase_client
from app.models import Vaga
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize supabase client
supabase = create_supabase_client()

#Path father
@app.get("/")
async def get():
    return {"Elias":"Montan"}


#NAME exists
def name_exists(key: str = "name", value: str = None):
    user = supabase.from_("vaga").select("*").eq(key, value).execute()
    return len(user.data) > 0




# OUTPUT THE TABLE
@app.get("/user")
def get_user(id: Union[str, None] = None):
    try:
        if id:
            user = supabase.from_("vaga")\
            .select("id", "name", "description")\
            .eq("id",id)\
            .execute()

            if user:
                return user
        else:
            name = supabase.from_("vaga")\
            .select("id", "name", "description")\
            .execute()

        if name:
            return name
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User not found"}
    
#create new NAME
@app.post("/user")
def post_user(vaga:Vaga):

        

    try:           
        #Check if user exists
        if name_exists(value=vaga.name):
            return {"message": "Name already exists"}
        
        #Add User to table
        vaga = supabase.from_("vaga")\
        .insert ({"name": vaga.name ,"description": vaga.description })\
        .execute()  

    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}

# DELETE A NAME
@app.delete("/user")
def delete_name(id:str):
    try:
        if name_exists("id", id):
            #delete name
            supabase.from_("vaga")\
                .delete().eq("id", id)\
                .execute()
            return {"message": "Name deleted successfully"}

        else:
            return {"message": "User deletion failed"}
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User deletion failed"}