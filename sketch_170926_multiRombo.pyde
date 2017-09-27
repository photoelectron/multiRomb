from Saver import saves
N_PHI = 60
N_save = N_PHI
fc = 2
wd = 1080/fc
ht = wd

maxRot = PI/8
dRot = PI/16
nS = 450.      # noise factor in space

def settings():
    size(wd,ht)

def setup():
    global rSys,saver
    background(0)
    saver = saves(N_PHI, N_save)
    blendMode(SUBTRACT)
    strokeWeight(2)
    noiseSeed(13323)
    rSys = rombSys(PVector(0,0),PVector(wd,ht),10,15)

def draw():
    background(255)
    rSys.show()
    saver.save_frame()

###
class rombus():
    def __init__(self,pos,dim):
        self.pos = pos
        self.dim = dim
        p1 = PVector(self.dim.x,0)
        p2 = PVector(0,self.dim.y)
        p3 = PVector(-self.dim.x,0)
        p4 = PVector(0,-self.dim.y)
        self.pts = [p1,p2,p3,p4]
        self.c = color(0)
        self.phi = 0
        self.theta = 0
    
    def show(self):
        noFill()
        stroke(self.c)
        with pushMatrix():
            translate(self.pos.x,self.pos.y)
            rotate(self.phi+self.theta)
            beginShape()
            for i in xrange(len(self.pts)):
                vertex(self.pts[i].x,self.pts[i].y)
            endShape(CLOSE)
#####
class multRomb():
    def __init__(self,pos,dim,n,theta):
        self.pos = pos
        self.dim = dim
        self.n = n
        self.theta = theta
        self.pts = []
        for i in xrange(n):
            dimn = PVector.mult(self.dim,1.*(i+1)/n)
            pr = rombus(self.pos,dimn)
            if i%3==0: c = color(0,0,255)
            elif i%3==1: c = color(255,0,0)
            else: c = color(0,255,0)
            pr.c = c
            pr.theta = self.theta
            self.pts.append(pr)
    
    def update(self):
        for i in xrange(len(self.pts)):
            self.pts[i].phi = maxRot*sin(TWO_PI*(1.*i/len(self.pts)+
                                         1.*frameCount/N_PHI)+self.theta)
            self.pts[i].theta = self.theta + maxRot*sin(TWO_PI*i/len(self.pts))
            self.pts[i].show()
    
    def show(self):
        for i in xrange(len(self.pts)):
            self.pts[i].show()
####
class rombSys():
    def __init__(self,posi,posf,nromb,npts):
        self.rombs = []
        dim = PVector.div(PVector.sub(posf,posi),2*nromb)
        for i in xrange(nromb):
            x = map(i,0,nromb,posi.x,posf.x) + dim.x
            for j in xrange(nromb):
                y = map(j,0,nromb,posi.y,posf.y) + dim.y
                th = noise(x/nS,y/nS)*TWO_PI
                pos = PVector(x,y)
                pr = multRomb(pos,dim,npts,th)
                self.rombs.append(pr)
    
    def show(self):
        for i in xrange(len(self.rombs)):
            self.rombs[i].update()

####
def mouseClicked():
    saver.onClick()
