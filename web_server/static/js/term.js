

function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}

function openWs(host, tid, session_id) {
    tid = tid
    session_id = session_id
    var terminalContainer = document.getElementById('terminal-container'),
        protocols = ["tty"],
        autoReconnect = -1,
        term, pingTimer, wsError;


    console.log('openWs to ')
    console.log(host)
    var ws = new WebSocket("ws://" + host + "/pty_ws");
    var unloadCallback = function(event) {
        var message = 'Close terminal? this will also terminate the command.';
        (event || window.event).returnValue = message;
        return message;
    };
    var b = new Base64();
    ws.onopen = function(event) {

        //reg to webserver
        ws.send("w"+session_id+"&&"+tid);
        console.log("Websocket connection opened");
        wsError = false;

        pingTimer = setInterval(sendPing, 30 * 1000, ws);

        if (typeof term !== 'undefined') {
            term.destroy();
        }

        term = new Terminal();

        term.on('resize', function(size) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send("s"+ size.cols+','+size.rows);
            }
            setTimeout(function() {
                term.showOverlay(size.cols + 'x' + size.rows);
            }, 500);
        });

        term.on("data", function(data) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send("i"+data);
            }
        });

        term.on('open', function() {
            window.addEventListener('resize', function(event) {
                term.fit();
            });
            window.addEventListener('beforeunload', unloadCallback);
            term.fit();
            term.focus();
        });

        while (terminalContainer.firstChild) {
            terminalContainer.removeChild(terminalContainer.firstChild);
        }

        term.open(terminalContainer);
    };

    ws.onmessage = function(evt) {
        var msg = evt.data;
        console.log('received ws msg:')

        console.log(msg)
        var cmd = msg.substring(0,1);

        switch(cmd) {
            case 'p': //response
                term.write(b.decode(msg.substring(1)));
                break;
            case 'n': // pong
                break;
            case 't': //title
                document.title = data;
                break;
            case 'o': //option
                var preferences = JSON.parse(data);
                Object.keys(preferences).forEach(function(key) {
                    console.log("Setting " + key + ": " +  preferences[key]);
                    term.setOption(key, preferences[key]);
                });
                break;
            case 'c': //reconnection
                autoReconnect = JSON.parse(data);
                console.log("Enabling reconnect: " + autoReconnect + " seconds");
                break;
        }
    };

    ws.onclose = function(event) {
        console.log("Websocket connection closed with code: " + event.code);
        if (term) {
            term.off('data');
            term.off('resize');
            if (!wsError) {
                term.showOverlay("Connection Closed", null);
            }
        }
        window.removeEventListener('beforeunload', unloadCallback);
        clearInterval(pingTimer);
        if (autoReconnect > 0) {
            setTimeout(openWs, autoReconnect * 1000);
        }
    };
};

var sendPing = function(ws) {
    ws.send(btoa(JSON.stringify({"cmd":"pty_ping","tid":tid, "wid": wid})));
};

