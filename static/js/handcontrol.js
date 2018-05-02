var paddleMap = new Map();
var maxNumberPaddles = 10;
var socketurl = "ws://" + "127.0.0.1:5006";
console.log(" socket url ...", socketurl);

var ws;
windowHeight = window.innerHeight
windowWidth = window.innerWidth

var bounceClip = new Audio('static/sound/bounce.wav');
var enableAudio = false;
var pauseGame = false;

var pauseGame = false;
var pauseGameAnimationDuration = 500;

$("input#sound").click(function () {
    enableAudio = $(this).is(':checked')
    soundtext = enableAudio ? "sound on" : "sound off";
    $(".soundofftext").text(soundtext)
});

planck.testbed(function (testbed) {
    var pl = planck,
        Vec2 = pl.Vec2;

    var world = pl.World(Vec2(0, -30));
    var BEAD = 4
    var PADDLE = 5


    var beadFixedDef = {
        density: 1.0,
        restitution: BEAD_RESTITUTION,
        userData: {
            name: "bead",
            points: 3
        }
    };
    var paddleFixedDef = {
        // density : 1.0,
        // restitution : BEAD_RESTITUTION,
        userData: {
            name: "paddle"
        }
    };

    var self;

    testbed.step = tick;
    testbed.width = SPACE_WIDTH;
    testbed.height = SPACE_HEIGHT;

    var playerScore = 0;

    var windowWidth = window.innerWidth
    var windowXRange = [0, windowWidth]
    var worldXRange = [-(SPACE_WIDTH / 2), SPACE_WIDTH / 2]

    var box, paddle
    var characterBodies = [];
    var paddleBodies = new Map();

    var globalTime = 0;
    var CHARACTER_LIFETIME = 6000

    start()

    $(function () {
        console.log("ready!");
        scoreDiv = document.createElement('div');
        $(scoreDiv).addClass("classname")
            .text("bingo")
            .appendTo($("body")) //main div
    });

    function start() {
        addUI()
        connectSocket();
    }


    //getXCord(sampleHandData.data)
    function getXCord(data) {

        pointindex = 0;
        var currentMap = new Map()
        data.forEach(function (point) {
            currentMap.set(point.id_label, {
                timestamp: Date.now()
            })
            if (!paddleBodies.has(point.id_label)) {
                //paddleMap.set(point.id, point)
                addPaddle(point.id_label)
            }
            box = point.box;
            top = box[0] * windowHeight;
            left = (box[1]) * windowWidth;
            width = Math.abs(box[3] - box[1]) * windowWidth;
            height = Math.abs(box[2] - (box[0])) * windowHeight;

            midx = left + (width / 2)
            paddle = paddleBodies.get(point.id_label).paddle

            mouseX = convertToRange(midx, windowXRange, worldXRange);
            lineaVeloctiy = Vec2((mouseX - paddle.getPosition().x) * accelFactor, 0)
            paddle.setLinearVelocity(lineaVeloctiy)
        })
        refreshMap(currentMap)
    }

    // Remove paddles that are no longer in frame.
    function refreshMap(currentMap) {
        paddleBodies.forEach(function (item, key, mapObj) {
            if (!currentMap.has(key)) {

                world.destroyBody(paddleBodies.get(key).paddle);
                paddleBodies.delete(key)
            }
        });
    }

    function connectSocket() {
        ws = new WebSocket(socketurl);
        console.log("attemptino socket connection ");

        ws.onopen = function () {
            $(".disableoverlay").hide();
            $("button").prop("disabled", false)
            console.log("Connection opened");
        };

        ws.onmessage = function (evt) {
            data = JSON.parse(evt.data);
            // console.log("recevied:", evt.data);
            if (!pauseGame) {
                getXCord(data.data)
            }
        };

        ws.onclose = function () {
            console.log("Connection is closed...");
            $(".disableoverlay").show();
            $("button").prop("disabled", true)

            setTimeout(function () {
                connectSocket();
                console.log("lengthof of paddleBodiesHoder", paddleBodies.length);
            }, 3000)
        };
    }

    world.on('pre-solve', function (contact) {

        var fixtureA = contact.getFixtureA();
        var fixtureB = contact.getFixtureB();

        var bodyA = contact.getFixtureA().getBody();
        var bodyB = contact.getFixtureB().getBody();

        var apaddle = bpaddle = false
        if (fixtureA.getUserData()) {
            apaddle = fixtureA.getUserData().name == paddleFixedDef.userData.name;
        }

        if (fixtureB.getUserData()) {
            bpaddle = fixtureB.getUserData().name == paddleFixedDef.userData.name;
        }
        if (apaddle || bpaddle) {
            // Paddle collided with something
            var paddle = apaddle ? fixtureA : fixtureB;
            var bead = !apaddle ? fixtureA : fixtureB;

            // console.log(paddle, bead);

            setTimeout(function () {
                paddleBeadHit(paddle, bead);
            }, 1);
        }

    })

    function paddleBeadHit(paddle, bead) {
        // console.log("attempting stroke change", bead.getUserData());
        //console.log("bead points ",bead.getUserData().points);
        playClip(bounceClip)
        updateScoreBox(bead.getUserData().points);

    }

    function playClip(clip) {
        if (enableAudio) {
            clip.play()
        }
    }

    function updateScoreBox(points) {
        if (!pauseGame) {
            playerScore += points;
            $(".scorevalue").text(playerScore)
            pointsAdded = points > 0 ? "+" + points : points
            $(".scoreadded").text(pointsAdded)
            $(".scoreadded").show().animate({
                opacity: 0,
                fontSize: "4vw",
                color: "#ff8800"
            }, 500, function () {
                $(this).css({
                    fontSize: "2vw",
                    opacity: 1
                }).hide()
            });
        }
    }

    function pauseGamePlay() {
        pauseGame = !pauseGame
        if (pauseGame) {
            // paddle.setLinearVelocity(Vec2(0, 0))
            $(".pauseoverlay").show()
            $(".overlaycenter").animate({
                opacity: 1,
                fontSize: "4vw"
            }, pauseGameAnimationDuration, function () {});
        } else {
            // paddle.setLinearVelocity(Vec2(3, 0))

            $(".overlaycenter").animate({
                opacity: 0,
                fontSize: "0vw"
            }, pauseGameAnimationDuration, function () {
                $(".pauseoverlay").hide()
            });
        }

    }

    function addUI() {

        // Add keypress event listener to pause game
        document.onkeyup = function (e) {
            var key = e.keyCode ? e.keyCode : e.which;
            if (key == 32) {
                console.log("spacebar pressed")
                pauseGamePlay()
            }
            if (key == 83) {
                $("input#sound").click()
            }
        }

        var ground = world.createBody();
        var groundY = -(0.3 * SPACE_HEIGHT)
        // ground.createFixture(pl.Edge(Vec2(-(0.95 * SPACE_WIDTH / 2), groundY), Vec2((0.95 * SPACE_WIDTH / 2), groundY)), 0.0);
    }

    function addPaddle(id) {
        var paddleBody = world.createBody({
            type: "kinematic",
            filterCategoryBits: PADDLE,
            filterMaskBits: BEAD,
            position: Vec2(-(0.4 * SPACE_WIDTH / 2) + (Math.random() * 50.2), -(0.25 * SPACE_HEIGHT))
        })

        paddleBody.timestampe = Date.now


        paddleBodies.set(id, {
            paddle: paddleBody,
            timestamp: Date.now()
        })
        paddleLines = [
            [1.8, -0.1],
            [1.8, 0.1],
            [1.2, 0.4],
            [0.4, 0.6],
            [-2.4, 0.6],
            [-3.2, 0.4],
            [-3.8, 0.1],
            [-3.8, -0.1]
        ]

        n = 10, radius = SPACE_WIDTH * 0.03, paddlePath = [], paddlePath = []

        paddleLines.forEach(function (each) {
            paddlePath.push(Vec2(radius * each[0], radius * each[1]))
        })

        paddleBody.createFixture(pl.Polygon(paddlePath), paddleFixedDef)
        paddleBody.render = {
            fill: colors[Math.ceil(Math.random() * colors.length)],
            stroke: '#000000'
        }
        //colorindex++ ;
    }

    // Generate Beeds falling from sky
    function generateBeads(numCharacters) {


        var beadWidthFactor = 0.005
        var beadColor = {
            fill: '#fff',
            stroke: '#000000'
        };



        for (var i = 0; i < numCharacters; ++i) {
            var characterBody = world.createBody({
                type: 'dynamic',
                filterCategoryBits: BEAD,
                filterMaskBits: PADDLE,
                position: Vec2(pl.Math.random(-(SPACE_WIDTH / 2), (SPACE_WIDTH / 2)), pl.Math.random((0.5 * SPACE_HEIGHT), 0.9 * SPACE_HEIGHT))
            });



            var fd = {
                density: beadFixedDef.density,
                restitution: BEAD_RESTITUTION,
                userData: {
                    name: beadFixedDef.userData.name,
                    points: 3
                }
            };

            var randVal = Math.random();


            if (randVal > 0.8) {
                beadColor.fill = '#32CD32'
                beadWidthFactor = 0.007
                fd.userData.points = 10;
            } else if (randVal < 0.2) {
                beadWidthFactor = 0.005
                beadColor.fill = '#ff0000'
                fd.userData.points = -10;
            } else {
                beadColor.fill = '#fff'
                beadWidthFactor = 0.005
                fd.userData.points = 3;
            }


            var shape = pl.Circle(SPACE_WIDTH * beadWidthFactor);
            characterBody.createFixture(shape, fd);

            characterBody.render = beadColor

            characterBody.dieTime = globalTime + CHARACTER_LIFETIME

            characterBodies.push(characterBody);

        }

    }

    function tick(dt) {

        globalTime += dt;
        if (world.m_stepCount % 80 == 0) {

            if (!pauseGame) {
                generateBeads(NUM_BEADS);

                for (var i = 0; i !== characterBodies.length; i++) {
                    var characterBody = characterBodies[i];
                    //If the character is old, delete it
                    if (characterBody.dieTime <= globalTime) {
                        characterBodies.splice(i, 1);
                        world.destroyBody(characterBody);
                        i--;
                        continue;
                    }

                }
            }
        }
        paddleBodies.forEach(function (item, key, mapObj) {
            stayPaddle(item.paddle)
        });


    }

    function stayPaddle(paddle) {
        var p = paddle.getPosition()

        if (p.x < -SPACE_WIDTH / 2) {
            p.x = -SPACE_WIDTH / 2
            paddle.setPosition(p)
        } else if (p.x > SPACE_WIDTH / 2) {
            p.x = SPACE_WIDTH / 2
            paddle.setPosition(p)
        }
    }

    // Returns a random number between -0.5 and 0.5
    function rand(value) {
        return (Math.random() - 0.5) * (value || 1);
    }

    // If the body is out of space bounds, wrap it to the other side
    function wrap(body) {
        var p = body.getPosition();
        p.x = wrapNumber(p.x, -SPACE_WIDTH / 2, SPACE_WIDTH / 2);
        p.y = wrapNumber(p.y, -SPACE_HEIGHT / 2, SPACE_HEIGHT / 2);
        body.setPosition(p);
    }


    function wrapNumber(num, min, max) {
        if (typeof min === 'undefined') {
            max = 1, min = 0;
        } else if (typeof max === 'undefined') {
            max = min, min = 0;
        }
        if (max > min) {
            num = (num - min) % (max - min);
            return num + (num < 0 ? max : min);
        } else {
            num = (num - max) % (min - max);
            return num + (num <= 0 ? min : max);
        }
    }

    // rest of your code
    return world; // make sure you return the world
});


function convertToRange(value, srcRange, dstRange) {
    // value is outside source range return
    if (value < srcRange[0] || value > srcRange[1]) {
        return NaN;
    }

    var srcMax = srcRange[1] - srcRange[0],
        dstMax = dstRange[1] - dstRange[0],
        adjValue = value - srcRange[0];

    return (adjValue * dstMax / srcMax) + dstRange[0];

}