from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() #create an instance of FastAPI

# The app instance is the main component of our FastAPI application. 
# It is used to configure the application.

class Custom(BaseModel):
    name: str
    age: int

@app.get('/ping') # here we have the decorator of app instance allowing to access the get http method and define the route on which it will recieve the request.
async def root(): # and this is like the controller method that we pass as a callback in the node js routes definition
    return { "message": "Server is alive" } # here we are returning a dictionary, but in node js we return a json object using the res parameter of callback method. 
# here fastify automatically serializes the returned value of controller method into json object and sends it over the network.

@app.get('/blogs/{blog_id}') # here we have defined the route with URL params, which we define in node js as :blog_id
async def read_blog(blog_id: int): # here the URL param that we define in route, is directly accessible in the controller method, but in node js we used to access it on req.params.blog_id 
    return { "blog_id": blog_id } # and the best part is the data validation and conversion is also done by fastify as we have kept the data type for blog_id as int, it will throw error if some other type data is passed in the URL params

@app.get('/comments/{comment_id}')
async def read_comment(comment_id: int, q: str = None, name: str = None): # here any extra parameters passed apart from those mentioned in the route, it will take them as query params.
    print(q, name)
    return { "comment_id": comment_id } 

# now how can we recieve data from client through request body i.e json object format in fastapi ?
# for that we need to define the request body types about what actually are we expecting in the request.
# And to define these types we use pydantic, it is library which helps us define the request body types and helps us
# validating the request body as well.
# here we have defined a Custom class for the defining request body type and since it takes the BaseModel from pydantic
# as its parent class, fastapi acknowledges it as request body type and does validation on that.

@app.post('/users')
async def create_user(user: Custom): # if you send some extra properties in the request body, then fastapi does not bother about it, but if any parameter is missing, then it will throw an error.
    print(user)
    return { "User created": user }