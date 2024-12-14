import schemdraw
import schemdraw.elements as e

# Create a new drawing
d = schemdraw.Drawing()

# Define power supply
d += e.SourceV().up().label('Vdd', loc='top')
d += e.Ground().down().label('Vss', loc='bottom')

# Define the differential amplifier inputs (Vp, Vn)
d += e.Line().right().label('Vp', loc='top')
d += e.Line().right().label('Vn', loc='bottom')

# Draw N-channel MOSFETs (XM1, XM2) - NFET
d += e.NFet().at((1, 0)).label('XM1').up().reverse()
d += e.NFet().at((2, 0)).label('XM2').down().reverse()

# Connect the gate terminals of the NMOS (NFET) devices
d += e.Line().right().at((1, 1)).to((2, 1))

# Define the P-channel MOSFETs (XM3, XM4) - PFET
d += e.PFet().at((3, 0)).label('XM3').up().reverse()
d += e.PFet().at((4, 0)).label('XM4').down().reverse()

# Connect the gates of the PMOS (PFET) transistors to the outputs
d += e.Line().right().at((3, 1)).to((4, 1))

# Define the output nodes (Vop, Von)
d += e.Line().right().at((5, 0)).label('Vop', loc='top')
d += e.Line().right().at((5, 0)).label('Von', loc='bottom')

# Draw the mid voltage (vmid) node between the differential pair
d += e.Line().right().at((3, 0)).to((5, 0)).label('vmid', loc='center')

# Save the drawing as a PNG file
d.draw()
d.save('trial2.png')
