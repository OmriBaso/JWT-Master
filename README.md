# JWT-Master
JWT Token Decoder - Forger - And Secret Key Brute Forcer  

**Must Download:**    
`pip3 install pyjwt`

**About The Tool**    
The JWT-Master can decode a JWT token and show you it's values  
it can also forge a custom JWT Token with custom data in it provided  
and it can also Brute Force and search for the secret key that was used to create  
the JWT Token Provided in the `-d` flag.  
The Tool had Threading implemented which makes it super fast.  


**Example**  
`python3 jwt_forger.py -d eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoiMCJ9.YuclVhzA4BX66YjyXtdo3RmgnJYWbJdDGEaSWb_Hq3w`  
_____________________________________________________________________________________
This JWT Token secret key is `omri` - add the word `omri` inside your wordlist  
and check how it is decoding it and brute forcing it.  
**Example2**  
`python3 jwt_forger.py -f "{'username':'admin','iat':'0'}" -s omri -a HS256`  
In That example we forge our own JWT token.  

**What Can it Be Used For?**  
If you have the secret key you can use it to forge your own token 
and authenticate as someone else!

**Credits**  
Created and Written by j3wker AKA "Omri Baso"

