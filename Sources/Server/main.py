__author__ = 'Hari'
import settings
import lights


users = []

def main():
    lights.connect()
    lights.power("on")
    #lights.setLighting("Light0" ,settings.BLUE,)

if __name__=="__main__":
    main()

