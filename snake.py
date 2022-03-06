class Dot: 
    #x coordinate
    #y coordinate 
    #(R,G,B) value color
    def __init__(self, x, y, color):
        self.x = x 
        self.y = y
        self.color = color

class Snake: 
    #list of dots 
    def __init__(self, dots): 
        self.dots = dots 

def main(): 
    snakeDot = Dot(3,4,(0,0,0)) 
    print(snakeDot.x) 
    snakeDot.x = 33
    print(snakeDot.x) 

if __name__ == "__main__": 
    main()