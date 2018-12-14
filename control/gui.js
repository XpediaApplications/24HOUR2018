function full_screen() {
    if ('fullscreenEnabled' in document || 'webkitFullscreenEnabled' in document || 'mozFullScreenEnabled' in document || 'msFullscreenEnabled' in document) {
        if (document.fullscreenEnabled || document.webkitFullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled) {
            var element = document.getElementsByTagName('body')[0];
            if ('requestFullscreen' in element) {
                element.requestFullscreen();
            }
            else if ('webkitRequestFullscreen' in element) {
                element.webkitRequestFullscreen();
            }
            else if ('mozRequestFullScreen' in element) {
                element.mozRequestFullScreen();
            }
            else if ('msRequestFullscreen' in element) {
                element.msRequestFullscreen();
            }
        }
    }
}

function screen_change() {
    if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
    }
    else {
        if ('exitFullscreen' in document) {
            document.exitFullscreen();
        }
        else if ('webkitExitFullscreen' in document) {
            document.webkitExitFullscreen();
        }
        else if ('mozCancelFullScreen' in document) {
            document.mozCancelFullScreen();
        }
        else if ('msExitFullscreen' in document) {
            document.msExitFullscreen();
        }
    }
}

function initGUI(controller) {

    // GUI Controllers

    var gui = new dat.GUI();

    //Fullscreen
    var settingsFolder = gui.addFolder('Settings');

    settingsFolder.add({fullScreen: false}, 'fullScreen').onFinishChange(function (value) {
        if (value) {
            full_screen();
        } else {
            screen_change();
        }
    });

    var parametersFolder = gui.addFolder('Parameters');

    parametersFolder.add(controller, 'throttle', 0, 100);
    parametersFolder.add(controller, 'rudder', -90, 90);
    parametersFolder.add(controller, 'rudderTrim', -90, 90);

    parametersFolder.open();

    //called when an event goes full screen and vice-versa.
    document.addEventListener('fullscreenchange', screen_change);
    document.addEventListener('webkitfullscreenchange', screen_change);
    document.addEventListener('mozfullscreenchange', screen_change);
    document.addEventListener('MSFullscreenChange', screen_change);

    //called when requestFullscreen(); fails. it may fail if iframe don't have allowfullscreen attribute enabled or for something else.
    document.addEventListener('fullscreenerror', function () {
        console.log('Full screen failed');
    });
    document.addEventListener('webkitfullscreenerror', function () {
        console.log('Full screen failed');
    });
    document.addEventListener('mozfullscreenerror', function () {
        console.log('Full screen failed');
    });
    document.addEventListener('MSFullscreenError', function () {
        console.log('Full screen failed');
    });
}
