

function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}

function openWs(host, tid) {
    tid = tid
    var terminalContainer = document.getElementById('terminal-container'),
        protocols = ["tty"],
        autoReconnect = -1,
        term, pingTimer, wsError;

    wid = "wid" + guid();

    console.log('openWs to ')
    console.log(host)
    var ws = new WebSocket("ws://" + host + "/ws");
    var unloadCallback = function(event) {
        var message = 'Close terminal? this will also terminate the command.';
        (event || window.event).returnValue = message;
        return message;
    };

    ws.onopen = function(event) {

        //reg to webserver
        ws.send(btoa(JSON.stringify({"cmd": "reg", "tid":tid, "wid": wid})));
        console.log("Websocket connection opened");
        wsError = false;

        pingTimer = setInterval(sendPing, 30 * 1000, ws);

        if (typeof term !== 'undefined') {
            term.destroy();
        }

        term = new Terminal();

        term.on('resize', function(size) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(btoa(JSON.stringify({"cmd":"pty_resize","tid":tid, "wid": wid, "param":{columns: size.cols, rows: size.rows}})));
            }
            setTimeout(function() {
                term.showOverlay(size.cols + 'x' + size.rows);
            }, 500);
        });

        term.on("data", function(data) {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(btoa(JSON.stringify({"cmd":"pty_input","tid":tid, "wid": wid, "param":data})));
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
        var obj = JSON.parse(atob(msg))
        console.log('received base64 decode msg:')
        console.log(obj)
        var data = obj["param"]

        switch(obj.cmd) {
            case 'pty_resp':
                term.writeUTF8(data);
                break;
            case 'pty_pong': // pong
                break;
            case 'pty_set_title':
                document.title = data;
                break;
            case 'pty_option':
                var preferences = JSON.parse(data);
                Object.keys(preferences).forEach(function(key) {
                    console.log("Setting " + key + ": " +  preferences[key]);
                    term.setOption(key, preferences[key]);
                });
                break;
            case 'pty_reconn':
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

