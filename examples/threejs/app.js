var __assignement = [undefined, undefined, undefined];
camera = __assignement[0];
scene = __assignement[1];
renderer = __assignement[2];
var __assignement = [undefined, undefined, undefined];
geometry = __assignement[0];
material = __assignement[1];
mesh = __assignement[2];
var init = function() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 10000);
    camera.position.z = 500;
    scene.add(camera);
    geometry = new THREE.CubeGeometry(200, 200, 200);
    material = new THREE.MeshNormalMaterial();
    mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
    renderer = new THREE.CanvasRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
};
var animate = function() {
    requestAnimationFrame(animate);
    render();
};
var render = function() {
    mesh.rotation.x = mesh.rotation.x + 0.01;
    mesh.rotation.y = mesh.rotation.y + 0.02;
    renderer.render(scene, camera);
};
init();
animate();
