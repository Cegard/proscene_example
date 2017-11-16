'''
    DOF.
    by Jean Pierre Charalambos.
    
    This example illustrates how to attach a PShape to an interactive frame.
    PShapes attached to interactive frames can then be automatically picked
    and easily drawn.
    
    Press 'h' to display the key shortcuts and mouse bindings in the console.
'''
add_library('proscene')


# PShader
depthShader, dofShader = None, None

# PGraphics
srcPGraphics, depthPGraphics, dofPGraphics = \
None, None, None

# Scene
scene = None

# float
posns = []

# InteractiveFrame[]
models = []

mode = 2


def setup():
    global posns, srcPGraphics, scene, models, depthShader, \
        dofShader, depthPGraphics, dofPGraphics
    
    size(900, 900, P3D);
    colorMode(HSB, 255);
    
    for i in xrange(0, 300, 3):
        posns.append(random(-1000, 1000))
        posns.append(random(-1000, 1000))
        posns.append(random(-1000, 1000))
    
    srcPGraphics = createGraphics(width, height, P3D)
    scene = Scene(this, srcPGraphics)
    print(this)
    
    for i in xrange(100):
        i_frame = InteractiveFrame(scene, boxShape())
        i_frame.translate(posns[3*i], posns[3*i+1], posns[3*i+2])
        models.append(i_frame)
    
    scene.setRadius(1000)
    scene.showAll()
    
    depthShader = loadShader("depth.glsl")
    depthShader.set("maxDepth", scene.radius()*2)
    depthPGraphics = createGraphics(width, height, P3D)
    depthPGraphics.shader(depthShader)
    
    dofShader = loadShader("dof.glsl")
    dofShader.set("aspect", width/height)
    dofShader.set("maxBlur", 0.015)
    dofShader.set("aperture", 0.02)
    dofPGraphics = createGraphics(width, height, P3D)
    dofPGraphics.shader(dofShader)
    
    frameRate(1000)


def draw():
    global scene, depthPGraphics, dofPGraphics, dofShader, models
    
    # 1. Draw into main buffer
    scene.beginDraw()
    scene.pg().background(0)
    scene.drawFrames()
    scene.endDraw()
    
    # 2. Draw into depth buffer
    depthPGraphics.beginDraw()
    depthPGraphics.background(0)
    scene.drawFrames(depthPGraphics)
    depthPGraphics.endDraw()
    
    # 3. Draw destination buffer
    dofPGraphics.beginDraw()
    dofShader.set("focus", map(mouseX, 0, width, -0.5, 1.5))
    dofShader.set("tDepth", depthPGraphics)
    dofPGraphics.image(scene.pg(), 0, 0)
    dofPGraphics.endDraw()
    
    # display one of the 3 buffers
    if mode == 0 :
        scene.display()
    
    elif mode == 1:
        scene.display(depthPGraphics)
    
    else:
        scene.display(dofPGraphics)


def boxShape():
    box = createShape(BOX, 60)
    box.setFill(color(random(0,255), random(0,255), random(0,255)))
    
    return box


def generator_point_line_distance(line_start, line_end):
    v0 = line_end - line_start
    denominator = v0.mag()
    
    def point_line_distance(position):
        point_in_space = PVector(position[0], position[1], 
                                 position[2])
        v1 = point_in_space - line_start
        v2 = point_in_space - line_end
        v3 = v1.cross(v2)
        numerator = v3.mag()
        result = numerator/denominator
        
        return result
    
    
    return point_line_distance


def keyPressed():
    global mode
    
    if key == '0':
        mode = 0
    
    elif key == '1':
        mode = 1  
    
    elif key == '2':
        mode = 2