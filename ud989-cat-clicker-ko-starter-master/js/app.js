var cats =  [
        {
            clickCount : 0,
            name : 'Tabby',
            imgSrc : 'img/434164568_fea0ad4013_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/bigtallguy/434164568',
			nickNames: ['Nick1','Nick2']
        },
        {
            clickCount : 0,
            name : 'Tiger',
            imgSrc : 'img/4154543904_6e2428c421_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/xshamx/4154543904',
			nickNames: ['Nick4','Nick3']
        },
        {
            clickCount : 0,
            name : 'Scaredy',
            imgSrc : 'img/22252709_010df3379e_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/kpjas/22252709',
			nickNames: ['Nick6']
        },
        {
            clickCount : 0,
            name : 'Shadow',
            imgSrc : 'img/1413379559_412a540d29_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/malfet/1413379559',
			nickNames: ['Nick11','Nick12']
        },
        {
            clickCount : 0,
            name : 'Sleepy',
            imgSrc : 'img/9648464288_2516b35537_z.jpg',
            imgAttribution : 'https://www.flickr.com/photos/onesharp/9648464288',
			nickNames: ['Nick21','Nick22']
        }
    ]

var Cat = function(data) {
	this.clickCount = ko.observable(data.clickCount);
	this.name = ko.observable(data.name);
	this.imgSrc = ko.observable(data.imgSrc);
	this.imgArribution = ko.observable(data.imgArribution);	
	this.nickNames = ko.observableArray(data.nickNames);	
	
	this.level = ko.computed(function(){
		var level;
		var clicks = this.clickCount();
		
		if (clicks < 10){
			level = 'NewBorn'
		} else if (clicks < 50){
			level = 'Inflant'
		} else if (clicks < 100){
			level = 'Child'
		} else if (clicks < 200){
			level = 'Teen'
		} else if (clicks < 500){
			level = 'Adult'
		} else {
			level = 'Ninja'
		}  
		return level;
		},this);			
}

var viewModel = function(){
	var self = this;	
	this.catList = ko.observableArray([]);
	
	cats.forEach(function(catItem){
		self.catList.push(new Cat(catItem));
	})
	
	this.currentCat = ko.observable(this.catList()[0]);
	
	this.incrementCounter = function () {
		self.currentCat().clickCount(self.currentCat().clickCount() + 1);
		//this.clickCount(this.clickCount() + 1); // bu da doðru
	}
	this.setCat = function(clickedCat){
		self.currentCat(clickedCat);
	}
}

ko.applyBindings(new viewModel());