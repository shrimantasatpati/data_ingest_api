import redis
 
 
def main():
    r  = redis.Redis(host="20.41.249.147", port=6379, username="default", password="admin", db=0)
    print(r.ping())
 
 
if __name__ == "__main__":
    main()