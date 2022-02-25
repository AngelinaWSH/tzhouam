var address="";
let marker_list = []
var add_mark;
var insert_marker;
var delete_marker;
var set_zoom;
function initMap() {

    var latlng = new google.maps.LatLng(22.3363998, 114.2654655);
    var myOptions = {
        zoom: 16,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    //new map
    map = new google.maps.Map(document.getElementById("map"),
        myOptions);
    // add marker

    // var information= new google.maps.InfoWindow({content: '<h1> yyds </h1>>'});
    // marker.addListener('click', function () {
    //     information.open(map,marker);
    // });
    //Add marker func
    function addMarker(coords,input) {
        if(check_exist(coords.lat,coords.lng)===true){
            alert("Marker already exists!!!");
            return;
        }
        const marker= new google.maps.Marker({
            position: coords,
            map:map,

        });
        var id=0;
        if (marker_list.length===0){
            id=1;
        }
        else{
            id=marker_list[Math.max(marker_list.length-1,0)].id+1;
        }
        var marker_object={marker:marker,id:id,lat:coords.lat,lng:coords.lng, name:input}
        marker_list.push(marker_object);


        add_listener(marker);

        load_delete_list(marker_object,input)



        //add to marker
    }
    add_mark = addMarker;
    function Handle_address() {
        var address_input=document.getElementById("input_address").value;
        var modified_address_input="";
        for (var i=0;i<address_input.length;i++){
            if(address_input[i]===' '){
                modified_address_input+='+';
            }
            else {
                modified_address_input+=address_input[i];
            }
        }

        var request_address="https://maps.googleapis.com/maps/api/geocode/json?address="+modified_address_input+"&key=AIzaSyB5S6d6RpebI_Z5pjm_Rti2MX9xs93leyk";
        $.getJSON(request_address, function(data) {
            var address_lat=Number(data.results[0].geometry.location.lat);
            var address_lng=Number(data.results[0].geometry.location.lng);
            addMarker({lat:address_lat,lng:address_lng},address_input);


        });
    }
    insert_marker=Handle_address;
    function delete_markers(){
        var markers=document.getElementById("markers");
        var id=this.innerText;
        for (var i=0;i<marker_list.length;i++){
            if (marker_list[i].id==id){
                marker_list.splice(id-1,1)
            }
        }


    }
    function delete_marker_inner() {
        var value=Number(document.getElementById("markers").value);
        marker_list[value-1].marker.setMap(null);
        marker_list.splice(value-1,1);
        var ids="";
        for (var i=0;i<marker_list.length;i++){
            ids+=marker_list[i].id;
        }
        var lists=document.getElementById("markers");
        lists.innerHTML="";
        for(var i=0;i<marker_list.length;i++){
            var id=marker_list[i].id;
            var name=marker_list[i].name;
            lists.innerHTML+="<option value='"+id.toString()+"'> ID:"+id.toString()+" Name: "+name+"</option>";
        }


    }
    delete_marker=delete_marker_inner;
    function check_exist(lat,lng){
        for(var i=0;i<marker_list.length;i++){
            if(lat===marker_list[i].lat && lng===marker_list[i].lng){
                return true;
            }
        }
        return false;
    }
    function load_delete_list(marker_object,input) {
        var lists=document.getElementById("markers");
        var id=marker_object.id;
        var lat=marker_object.lat;
        var lng=marker_object.lng;
        // var request_address="https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat.toString()+","+lng.toString()+"&key=AIzaSyB5S6d6RpebI_Z5pjm_Rti2MX9xs93leyk";
        // var address="";
        // $.getJSON(request_address, function(data) {
        //     var address_list=data.results[0].address_components;
        //
        //     for (var i=0;i<6;i++){
        //         address+=address_list[i].longname+", ";
        //     }
        //
        // });
        lists.innerHTML+="<option value='"+id.toString()+"'> ID:"+id.toString()+" Name: "+input+"</option>";


    }
    function change_zoom(){

        map.setZoom(Number(document.getElementById("change_zoom").value));
        document.getElementById("zoom_value").innerText=document.getElementById("change_zoom").value;
    }
    set_zoom=change_zoom;
    function draw_line() {
        d3.select("#info1").data([1,2,3]);
    }
}
function add_listener(marker){
    marker.addListener("click", () => {
            alert("in");
            //document.getElementById("info1").innerHTML=id;
        })
}



