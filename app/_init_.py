from app import db
from models import Role, Rank, Category

# ===== Creating tables ===== #

db.create_all()
db.session.commit()

# === Role === #

role = []

role.append(Role(name='admin', description='Permissions:/admin'))
role.append(Role(name='user', description='Permissions:/view/create/delete/edit/comment'))

# === Rank === #

rank = []

rank.append(Rank(name='anonymus', description=''))
rank.append(Rank(name='newbie', description=''))

# === Category === #

category = []

category.append(Category(name='Leisure',       about='Info about Leisure'))       
category.append(Category(name='Math',          about='Info about Math'))       
category.append(Category(name='Art',           about='Info about Art'))         
category.append(Category(name='Cars',          about='Info about Cars'))        
category.append(Category(name='Health',        about='Info about Health'))        
category.append(Category(name='Physics',       about='Info about Physics'))     
category.append(Category(name='Beauty',        about='Info about Beauty'))         
category.append(Category(name='Travel',        about='Info about Travel'))        
category.append(Category(name='Games',         about='Info about Games'))         
category.append(Category(name='Science',       about='Info about Science'))        
category.append(Category(name='Music',         about='Info about Music'))          
category.append(Category(name='Lifestyle',     about='Info about Lifestyle'))      
category.append(Category(name='Movies',        about='Info about Movies'))        
category.append(Category(name='Technologies',  about='Info about Technologies'))  
category.append(Category(name='Clothing',      about='Info about Clothing'))      
category.append(Category(name='Shopping',      about='Info about Shopping'))      
category.append(Category(name='Nature',        about='Info about Nature'))         
category.append(Category(name='Programming',   about='Info about Programming'))   
category.append(Category(name='Design',        about='Info about Design'))        
category.append(Category(name='Food',          about='Info about Food'))           
category.append(Category(name='Animals',       about='Info about Animals'))        
category.append(Category(name='Gardens',       about='Info about Gardens'))        
category.append(Category(name='Photographing', about='Info about Photographing')) 
category.append(Category(name='Drinks',        about='Info about Drinks'))       
category.append(Category(name='Space',         about='Info about Space'))        
category.append(Category(name='Law',           about='Info about Law'))          
category.append(Category(name='Sport',         about='Info about Sport'))        
category.append(Category(name='Finance',       about='Info about Finance'))      
category.append(Category(name='Education',     about='Info about Education'))    
category.append(Category(name='Marketing',     about='Info about Marketing'))    
category.append(Category(name='History',       about='Info about History'))      
category.append(Category(name='Business',      about='Info about Business'))      
category.append(Category(name='Books',         about='Info about Books'))        
category.append(Category(name='Cartoons',      about='Info about Cartoons'))     
category.append(Category(name='Wildlife',      about='Info about Wildlife'))     
category.append(Category(name='Fashion',       about='Info about Fashion'))        
category.append(Category(name='Fitness',       about='Info about Fitness'))       
# category.append(Category(name='', about=''))

# === Add === #

for i in role:
    db.session.add(i)

for i in rank:
    db.session.add(i)

for i in category:
    db.session.add(i)

# === Commit === #

db.session.commit()
