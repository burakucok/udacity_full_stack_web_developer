var locations = [{
        title: 'Blue Mosque',
        location: {
            lat: 41.005410,
            lng: 28.976814
        },
		fs_id: '4b753a2af964a520d4012ee3'
    },
    {
        title: 'Hagia Sophia',
        location: {
            lat: 41.008583,
            lng: 28.980175
        },
		fs_id: '4bc8088f15a7ef3b6b857ada'
    },
    {
        title: 'Topkapi Palace',
        location: {
            lat: 41.011519,
            lng: 28.983379
        },
		fs_id: '4b824a4bf964a5202dcf30e3'
    },
    {
        title: 'Taksim Square',
        location: {
            lat: 41.037002,
            lng: 28.985092
        },
		fs_id: '4cd103d96449a0936af0cdcf'
    },
    {
        title: 'Galata Tower',
        location: {
            lat: 41.025840,
            lng: 28.974458
        },
		fs_id: '4b732d5bf964a52011a02de3'
    },
	 {
        title: 'Galata Bridge',
        location: {
            lat: 41.020240,
            lng: 28.973214
        },
		fs_id: '4ba1fb68f964a520c4d437e3'
    },
    {
        title: 'Rahmi Koc Museum',
        location: {
            lat: 41.042273,
            lng: 28.948547
        },
		fs_id: '4bae0155f964a5202a7a3be3'
    },
    {
        title: 'Grand Bazaar',
        location: {
            lat: 41.010685,
            lng: 28.968068
        },
		fs_id: '4c09fd76009a0f476ac2e8bf'
    },
];

var styles = [
    {
        "featureType": "water",
        "stylers": [
            {
                "saturation": 43
            },
            {
                "lightness": -11
            },
            {
                "hue": "#0088ff"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "hue": "#ff0000"
            },
            {
                "saturation": -100
            },
            {
                "lightness": 99
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#808080"
            },
            {
                "lightness": 54
            }
        ]
    },
    {
        "featureType": "landscape.man_made",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#ece2d9"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#ccdca1"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#767676"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#b8cb93"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi.sports_complex",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi.medical",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi.business",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    }
];

var map, infowindow, bounds, defaultIcon, highlightedIcon;

var markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 41.008238,
            lng: 28.978359
        },
        zoom: 13,
		styles : styles
    });


    infowindow = new google.maps.InfoWindow();
    bounds = new google.maps.LatLngBounds();

    defaultIcon = makeMarkerIcon('FF0000');
    highlightedIcon = makeMarkerIcon('FFFF00');
    for (var i = 0; i < locations.length; i++) {
        var position = locations[i].location;
        var title = locations[i].title;
				
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            icon: defaultIcon,
            id: locations[i].fs_id,
			content: ""
        });
	setMarkerContent(marker);
	addMarkerClickEvent(marker);
        markers.push(marker);	    
        bounds.extend(markers[i].position);
    }
    map.fitBounds(bounds);

    window.onresize = function() {
        map.fitBounds(bounds);
    };

    function addMarkerClickEvent(marker) {
        marker.addListener('click', function() {
            markerClicked(this);
        });
    }
	
    function markerClicked(marker) {
        populateInfoWindow(marker, infowindow);
        makeHighlightedSelectedIcon(marker, highlightedIcon, defaultIcon);
    }


	function makeAllIconDefault() {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setIcon(defaultIcon);
        }
    }
	
    function makeHighlightedSelectedIcon(selectedIcon) {
        makeAllIconDefault();
        selectedIcon.setIcon(highlightedIcon);
    }


    function makeMarkerIcon(markerColor) {
        var markerImage = new google.maps.MarkerImage(
            'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|' + markerColor +
            '|40|_|%E2%80%A2',
            new google.maps.Size(21, 34),
            new google.maps.Point(0, 0),
            new google.maps.Point(10, 34),
            new google.maps.Size(21, 34));
        return markerImage;
    }


    function populateInfoWindow(marker, infowindow) {
        if (infowindow.marker != marker) {			
            infowindow.marker = marker;
	    infowindow.setContent(marker.content);					
            infowindow.open(map, marker);

            infowindow.addListener('closeclick', function() {
		infowindow.close(infowindow);
		makeAllIconDefault();
            });
        }
    }

	function setMarkerContent(marker){		
		var clinet_info = "client_id=HSLG1DFKVUHTDBFDW3EWBJ3BPTJC23VDNGNZXQVJW20Z15OK&client_secret=DC43EYNQNYHCLTKF5SVJ0SKFFIBLNZB1EXQQIWCWHJMWOHS2&v=20161016";
		// AJAX call to Foursquare
		$.ajax({
		  type: "GET",
		  url: "https://api.foursquare.com/v2/venues/" + locations[i].fs_id + "/?" + clinet_info,
		  dataType: "json",
		  cache: false,
		  success: function(data) {
			if (data.response){						
				var photoUrl = data.response.venue.bestPhoto.prefix + "height150" + data.response.venue.bestPhoto.suffix;
				marker.content = "<h3>" + marker.title + "</h3><br>" +
								'<a href="' + data.response.venue.shortUrl + '"target="_blank">' +  
								"<div style='height:150'><img src=" + '"' +
								photoUrl + '"></div></a>';								
			} 
		  },
		  error: function(jqXHR, exception) {
			var msg = '';
			if (jqXHR.status === 0) {
			    msg = 'Not connect. Verify Network.';
			} else if (jqXHR.status == 404) {
			    msg = 'Requested page not found. [404]';
			} else if (jqXHR.status == 500) {
			    msg = 'Internal Server Error [500].';
			} else if (exception === 'parsererror') {
			    msg = 'Requested JSON parse failed.';
			} else if (exception === 'timeout') {
			    msg = 'Time out error.';
			} else if (exception === 'abort') {
			    msg = 'Ajax request aborted.';
			} else {
			    msg = 'Uncaught Error.' + jqXHR.responseText;
			}	  
			  
			marker.content = "<h3>" + marker.title + "</h3><br>" +
					 "<p>Oppss,Could not load data from Foursquare!!<br>" + msg + "</p>";                             
		  }  	
		});			
		
	}
	
	// Close infowindow when clicked elsewhere on the map
	map.addListener("click", function(){
		infowindow.close(infowindow);
		makeAllIconDefault();
	});
	  
    var viewModel = function() {
        var self = this;

        this.filter = ko.observable("");

        this.filteredMarkers = ko.dependentObservable(function() {
            var query = this.filter().toUpperCase();
            return ko.utils.arrayFilter(markers, function(item) {
                if (query && item.title.toUpperCase().indexOf(query) < 0) {
                    item.setMap(null);
                    return false;
                } else {
                    item.setMap(map);
                    return true;
                }
            });
        }, this);			
		
        this.markerClicked = function(marker) {
            markerClicked(marker);
        };
    };


    ko.applyBindings(new viewModel());
}


var onMapError = function() {
    document.getElementById("map").innerHTML = "<h2> Sorry, something went wrong. Please try again later. </h2>";
};
