
import uvicorn 

def main():
    config = uvicorn.Config("csat.server.app:app")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    main()