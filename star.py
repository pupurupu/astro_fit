import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
x=1091
y=1036
hdulist = pyfits.open("v523cas60s-001(1).fit")
hdulist. info() #получение информ о файле
axis = hdulist[0].header['naxis2']
value=hdulist[0].data
#print(value)
#print(value[y][x])
cx = []
cy = []
vx = []
vy = []
for i in range(-15, 15):
    xx=x+i
    v= value[y][xx]
    cx.append(int(xx))
    vx.append(v)
for i in range(-15, 15):
    yy=y+i
    v= value[yy][x]
    cy.append(int(yy))
    vy.append(v)
#print(cx)
#print(vx)
#print(cy)
#print(vy)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(cx,vx)
plt.xlabel('x')
plt.ylabel('value')
plt.subplot(2, 1, 2)
plt.plot(cy,vy)
plt.xlabel('y')
plt.ylabel('value')
plt.show()
hdulist. close()