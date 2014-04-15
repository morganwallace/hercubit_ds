$(document).ready(function(){
    // var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');


    // How these websockets work: 
    // 1. Start button clicked triggers the bluetooth_conn function on app.py 
    $('#startbtn').click(function(event) {
        if ($('#startbtn').html()=='Done'){
            // console.log($("#chosen-goal .goal_count").text());
            // console.log($("#count_denomenator").html());
            $("#connection_status").text("Searching for Hercubit device on bluetooth");
            $("#count_denomenator").text("/"+$("#chosen-goal .goal_count").text());
            $.ajax({
                url:'./bluetooth_conn',
                success: function(msg){
                    //Device is connected now so request data from server at the sample rate
                    // socket.on('connection established', function(msg) {
                    if (msg.connected==true){
                        $("#connection_status").text("Problem with Connection. Turn Hercubit off and on and restart application.");
                        return
                    }
                    $('#log').append('<p>Bluetooth Connection Established</p>');
                    $("#connection_status").text("Connected. Start Exercising!");
                    fetch_data = setInterval( function() { 
                        // socket.emit('get_sample');
                        $.ajax({
                            url: './getsample',
                            success: function(msg){
                                $("#count_numerator").html(msg.count)
                                goal_completed()
                            }
                        })
                        if ($('#startbtn').html()=='Start'){
                            clearInterval(fetch_data);
                            finished_exercising()
                        }
                    }, msg.sample_rate);

                }
            })
            // socket.emit('bluetooth_conn');
        }
        return false;
    });

    
    var goal_completed = function(){
        var goal_num=$("#chosen-goal .goal_count").text()*1;
        var count= $("#count_numerator").html()*1;
        if (count>=goal_num){
            $("#count_numerator").css("color",'green');
            $("#connection_status").text("You rock! You reached your goal.")
        }
    }
    // Show output of device in DOM
    // socket.on('device response', function(msg) {
    //     $("#count_numerator").html(msg.data)
    //     goal_completed()
    // });

    // socket.on('graph', function(msg){
    //     $("#graph").html(msg.graph)
    // });


    // socket.on('Bluetooth Connection Stopped', function(msg) {
    //     $('#log').append('<p>Bluetooth connection Stopped</p>');
    // });

    //
    //Triggers for Web Socket
    //
    var finished_exercising= function(){
        // socket.emit('stop');
        $.ajax('./stop');
        determineActivity();
        getNewBadge(2);
        getNewBadge(3);
        getNewBadge(4);
        getNewBadge(5);

        //Gather data about exercise session for insertion into database
        var thisgoal=$("#chosen-goal span").html();
        var type=$("#chosen-goal .exercise_type").text();
        var weight=$("#chosen-goal .goal_weight").text();
        var goal_num=$("#chosen-goal .goal_count").text()*1;
        var count= $("#count_numerator").html()*1;
        var goal_complete= "0";
        if (count>=goal_num){
            console.log('goal completed');
            goal_complete="1";
        }
        var username= $("#username").text();
        // var exercise_data=;
        // socket.emit('addexercise',exercise_data);
        




        $.post("/addexercise",
            {'username':username,count:count,"type":type,"weight":weight,"goal_complete":goal_complete},
            function(data){
                console.log(data);
            });

        $("#count_numerator").text(0);
        $("#count_numerator").css("color",'black');

        
    }
    //

    $("#quit").click(function(){
        // socket.emit('quit');
        $.ajax('./quit');
        console.log('quiting')
        window.onbeforeunload = function(){}
        window.open('','_self').close();
    })

    // setInterval(function(){
    //     $.ajax({
    //       type: "POST",
    //       url: "./test_connection",
    //       data: "test",
    //       success: function(msg){
    //             console.log('connected to server');
    //       },
    //       error: function(XMLHttpRequest, textStatus, errorThrown) {
    //          window.onbeforeunload = function(){}
    //         window.open('','_self').close();
    //       }
    //     });
        
    // },15000);
        
    
});
