camera, scene, renderer = None, None, None
geometry, material, mesh = None, None, None

def init():
    global camera, scene, renderer, geometry, material, mesh
    scene = JS('new THREE.Scene()')

    camera = JS('new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 10000)')
    camera.position.z = 500
    scene.add(camera)

    geometry = JS('new THREE.CubeGeometry(200, 200, 200)')
    material = JS('new THREE.MeshNormalMaterial()')

    mesh = JS('new THREE.Mesh(geometry, material)')
    scene.add(mesh)

    renderer = JS('new THREE.CanvasRenderer()')
    renderer.setSize(window.innerWidth, window.innerHeight)

    document.body.appendChild(renderer.domElement);


def animate():
    global camera, scene, renderer, geometry, material, mesh
    requestAnimationFrame(animate);
    render()

def render():
    global camera, scene, renderer, geometry, material, mesh
    mesh.rotation.x += 0.01
    mesh.rotation.y += 0.02

    renderer.render(scene, camera)

init()
animate()

