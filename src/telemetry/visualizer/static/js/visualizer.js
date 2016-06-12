var last_kp = {'x': 0, 'y':0, 'theta': 0};
var current_scale = 1.0
var ANCHORBOUND = 1000000000;

function encoder_to_velocity(encoder, delta_t)
{
    var ENCODER_DISTANCE_FACTOR = 1.0;
    return (encoder * ENCODER_DISTANCE_FACTOR) / delta_t;
}

function kinematics_velocity(encoder_dl, encoder_dr, delta_t)
{
    var ROOMBA_L = 35.0;
    var vr = encoder_to_velocity(encoder_dr, delta_t);
    var vl = encoder_to_velocity(encoder_dl, delta_t);
    var R = 0.0;
    var omega = (vr-vl)/ROOMBA_L;
    if(vr == vl)
        R = Infinity;
    else
        R = (0.5 * ROOMBA_L) * (vr+vl) / (vr-vl);
    return {'R': R, 'omega': omega, 'vr':vr, 'vl':vl};
}

function kinematics_position(x, y, theta, encoder_dl, encoder_dr, delta_t)
{
    var kv = kinematics_velocity(encoder_dr, encoder_dl, delta_t);
    var x_p = x;
    var y_p = y;
    var theta_p = theta;
    var linear = true;
    if(kv.R != Infinity)
    {
        var odt = kv.omega * delta_t;
        var sth = Math.sin(theta);
        var cth = Math.cos(theta);
        var icc_x = x - kv.R * Math.sin(theta);
        var icc_y = y + kv.R * Math.cos(theta);
        var pcos = Math.cos(odt);
        var psin = Math.sin(odt);
    
        theta_p = theta + odt;
        x_p = pcos * (x-icc_x) - psin * (y-icc_y) + (icc_x);
        y_p = (psin * (x-icc_x) + pcos * (y-icc_y) + (icc_y));
        linear = false;
    }
    else
    {
        theta_p = theta;
        x_p = x + kv.vr * Math.cos(theta) * delta_t;
        y_p = (y + kv.vr * Math.sin(theta) * delta_t);
        linear = true;
    }
    return {'x': x_p, 'y': y_p, 'theta': theta_p, 'linear': linear};
}

function direction_ind(pt, theta)
{
    var d = new paper.Point(pt.x + 20*Math.cos(theta), pt.y + 20*Math.sin(theta));
    var ind = new paper.Path.Line(pt, d);
    ind.strokeColor = "#000";
    return ind;
}

function save_pos()
{
    lyr_roomba.scale(1/current_scale, 1/current_scale);
    abs_init_loc = lyr_roomba.bounds;
    lyr_roomba.bounds = new paper.Rectangle(-ANCHORBOUND,-ANCHORBOUND, abs_init_loc.width, abs_init_loc.height);
}

function restore_pos()
{
    lyr_roomba.bounds = new paper.Rectangle(abs_init_loc.x, abs_init_loc.y, lyr_roomba.bounds.width, lyr_roomba.bounds.height);
    lyr_roomba.scale(current_scale, current_scale);
}



function draw_path(x, y, theta, encoder_dl, encoder_dr, delta_t)
{
    save_pos();

    var from = new paper.Point(x,y);
    var kp_final = kinematics_position(x,y,theta,encoder_dr,encoder_dl,delta_t);
    var final = new paper.Point(kp_final.x, kp_final.y);
    if(kp_final.linear != true)
    {
        var kp_mid = kinematics_position(x,y,theta,encoder_dr/2.0, encoder_dl/2.0, delta_t/2.0);
        var mid = new paper.Point(kp_mid.x, kp_mid.y);
        var path = new paper.Path.Arc(from, mid, final);
        path.strokeColor = "#000";
        //var circl = new paper.Path.Circle(mid, 5);
        //circl.strokeColor = "#00f";
    }
    else
    {
        var path = new paper.Path.Line(from, final);
        path.strokeColor = "#000";
    }
    current_location.position = final;

    restore_pos();
    return kp_final;
}


function change_zoom_centered(delta, pos)
{
    var SCALE_RATE = 1.5
    var scaling = delta > 0 ? SCALE_RATE : 1/SCALE_RATE;
    current_scale *= scaling
    lyr_roomba.scale(scaling,scaling);
    paper.view.draw();
}

function load_ws()
{
    var ws = new WebSocket("ws://192.168.1.71:9998/live");

    ws.onopen = function()
    {
        ws.send("go");
    }

    ws.onmessage = function(evt)
    {
        var msg = evt.data;
        obj = JSON.parse(msg);
        last_kp = draw_path(last_kp.x, last_kp.y, last_kp.theta, obj.encoder_left, obj.encoder_right, obj.delta_t);
        ws.send("go");
    }
    ws.onclose = function()
    {
        alert("End of data");
    }
}

window.onload = function() {

    var canvas = document.getElementById("myCanvas");
    paper.setup(canvas);
    lyr_roomba = new paper.Layer();

    var scaling = new paper.Point(1,1);

    var anchor = new paper.Path.Circle(-ANCHORBOUND,-ANCHORBOUND,2);
    anchor.strokeColor = "#000";
    var anchor2 = new paper.Path.Circle(ANCHORBOUND,ANCHORBOUND,2);
    anchor2.strokeColor = "#000";

    current_location = new paper.Path.Circle(new paper.Point(0,0), 5);
    current_location.strokeColor = "#f00"
    current_location.fillColor = "#f00"

    
    draw_path(0,0,0,100,100,1);
    draw_path(0,0,0,100,150,1);


    //lyr_roomba.scale(1, -1);
    //lyr_roomba.position.y += lyr_roomba.bounds.height;
    //lyr_roomba.position.x += lyr_roomba.bounds.width;

    tool = new paper.Tool();
    tool.onMouseDrag= function(event)
    {
        var init = event.point;
        var delta = event.delta;
        lyr_roomba.position = lyr_roomba.position.add(delta);
        //paper.view.draw();
    };

    paper.view.draw();

    ($("#myCanvas")).mousewheel((event) => {
      const mousePosition = new paper.Point(event.offsetX, event.offsetY);
      change_zoom_centered(event.deltaY, mousePosition);
    });
};
