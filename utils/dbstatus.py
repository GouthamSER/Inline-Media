import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
  
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.ucol = self.db["USERS"]
  
    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.ucol.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.ucol.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.ucol.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.ucol.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.ucol.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
    
    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.ucol.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.ucol.find({})
    

    async def delete_user(self, user_id):
        await self.ucol.delete_many({'id': int(user_id)})
      
    async def get_banned(self):
        users = self.ucol.find({'ban_status.is_banned': True})
        b_users = [user['id'] async for user in users]
        return b_users

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

db = Database(DATABASE_URI, DATABASE_NAME)

