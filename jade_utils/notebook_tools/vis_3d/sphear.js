requirejs.config({
    paths: {
        'T' : ['//cdnjs.cloudflare.com/ajax/libs/three.js/r83/three'],
    },
});
require(['T'], function(THREE) {
    console.log(THREE);
    var camera, scene, light, renderer;
    var geometry, material, mesh;
    var width = 600;
    var height = 400;
    var parentDiv = document.getElementById("%ELEMENT_ID%");
    var data = %DATA%;
    init();
    animate();

    function init(){
        scene = new THREE.Scene();
        light = new THREE.AmbientLight(0xffffff, 0.8); // soft white light
          scene.add(light);
        camera = new THREE.PerspectiveCamera( 75, width / height, 1, 1000 );
        camera.position.z = 500;
        var data_size = Math.sqrt(data)
        var ta = Uint8Array.from(data);
        console.log(ta)
        var texture = new THREE.DataTexture(ta, data_size, data_size, THREE.RGBAFormat  )
        texture.needsUpdate = true;
        geometry = new THREE.SphereGeometry(200, 64, 64);
        material =  new THREE.MeshLambertMaterial({
            map: texture
        })
        mesh = new THREE.Mesh(geometry, material);
        scene.add( mesh );

        renderer = new THREE.WebGLRenderer({antialias: true});
        renderer.setSize(width, height);
        renderer.setClearColor('white');
        while (parentDiv.firstChild) {
            parentDiv.removeChild(parentDiv.firstChild);
        }
        parentDiv.appendChild( renderer.domElement ) ;
    }

    function animate(){
        window.requestAnimationFrame( animate );
        mesh.rotation.x = Date.now() * 0.00005;
        mesh.rotation.y = Date.now() * 0.0001;
        renderer.render( scene, camera);
    }

});
