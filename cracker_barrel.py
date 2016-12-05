#-*-coding:utf8;-*-
#qpy:3
#qpy:console

from collections import namedtuple

Move = namedtuple('Move', 'r c d')
class Dir:
    def __init__(s,x,y, name=''):
        s.x=x
        s.y=y
        s.name=name
        
    def __mul__(s,rhs): 
        return Dir(s.x*rhs,s.y*rhs)
        
    def __str__(s):
        return s.name or 'Dir(x='+str(s.x)+', y='+str(s.y)+')'
        
    def __repr__(s):
        return str(s)
u = Dir(0, -1, 'u')
d = Dir(0, 1, 'd')
ur = Dir(1, -1, 'ur') 
dl = Dir(-1, 1, 'dl')
l = Dir(-1, 0, 'l')
r = Dir(1, 0, 'r')
zero=Dir(0,0, 'zero')

dirs=[u,d,l,r,ur,dl]

class Puzzle:
    def __str__(s):
        return '\n'.join(str(r) for r in s.b) + '\n'

    def get(s, m, d):
        if m.r +d.y < 0 or m.c + d.x < 0:
            raise IndexError
        return s.b[m.r+d.y][m.c+d.x]
    
    def set(s,m, d, val):
        if m.r +d.y < 0 or m.c + d.x < 0:
            raise IndexError
        s.b[m.r+d.y][m.c+d.x]=val

    def __init__(self, b=None, moves=None):
        self.b = b or [
        [1,1,1,1,1],
        [1,1,1,1],
        [1,0,1],
        [1,1],
        [1]]
        self.moves = (moves or
         self.allMoves()
        )
        self.sol=[]
        
    def solve(self,move=None):
        I=0
        if move:
            nm = self.hop(move)
            if nm:
                if nm != [zero]:
                    
                
                    for m in nm:
                  #  print(len(self.moves))
                   # print(I)
                #    I +=1
                        p = Puzzle(list(list(r) for r in self.b), list(nm))
                        p.solve(m)
                        if p.sol:
                            self.sol = [move] + p.sol
                            break
               #     else:
                    #    print('no solution')
           
                
        else:
            
            for move in self.moves:
                if not self.sol:
                    p = Puzzle(list(list(r) for r in self.b),
                 	list(self.moves))
                    p.solve(move)
                    if p.sol:
                        self.sol = [move] + p.sol
                        break
                    
                
    def hop(s, m):
        if not (s.get(m, m.d) == s.get(m, m.d*2) == 1
               	and s.get(m,zero)==0):
            #print(s, m)
            return [zero]
      #  print(s, '\ngonna try',m)
        s.set(m, zero, 1)
        s.set(m, m.d, 0)
        s.set(m,m.d*2, 0)
        
        left = 0
        for r in s.b:
            for c in r:
                left += c
        if left == 1:
            s.sol=[m]
          #  print('found a solution at',s)
            return []
        return list(s.moves)
        nm=list(s.moves)
        I=0
        return nm
        """
        while I < len(nm):
            if nm[I].r==m.r and nm[I].c==m.c:
                print('removing',nm[I])
                del nm[I]
                
            else: I +=1
        nm.extend(s.getMoves(m))
        
        return nm
        """
        
        
    def getMoves(s,mv):
        res=[]
        for d in dirs:
            for I in [1,2]:
                m=Move(mv.r+I*mv.d.y, 
                	mv.c+I*mv.d.x, d)
                try:
                   s.get(m,m.d)
                   s.get(m,m.d*2)
                   res.append(m)
                   print('adding',m)
                except IndexError:
                   pass
        return res
        
    def allMoves(s):
        res=[]
        for d in dirs:
            for r in range(5):
                for c in range(5-r):
                    m=Move(r,c,d)
                    try:
                       s.get(m,m.d)
                       s.get(m,m.d*2)
                       res.append(m)
                    except IndexError:
                       pass
        return res

p = Puzzle()
p.solve()
Q = Puzzle()

print('solution:')
for m in p.sol:
    print(Q, m)
    Q.hop(m)