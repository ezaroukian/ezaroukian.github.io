
var reserved = ["break","default","function","return","var","case","delete","if","switch","void","catch","do","in","this","while","const","else","instanceof","throw","with","continue","finally","let","try","debugger","for","new","typeof"];//reserved words cannot be used for property names

//Make a dictionary from text
function popDictJS(txt){
	//Takes a String, builds dictionary of all words in the file mapped to their counts. Returns dictionary.
	var user = {};
	var words = txt.split(/\s/);
	console.log(words);
	//remove any reserved words (I could remove the frequent words here too)
	var finalWords = [];
	var finalWordsTemp = [];
	for (i=0; i<words.length; i++){
		var safeWord = true; 
		for (j=0; j<reserved.length; j++){
			if (words[i]==reserved[j]){
				safeWord = false;
				break;
			}
		}
		if (safeWord){
			finalWords.push(words[i]);
		}
	}
	//remove . , ? ! : ; ) (  and  eol  and  make lowercase 
	for (i=0; i<finalWords.length; i++){
		var word = finalWords[i];
		//word = word.replace(/(\r\n|\n|\S|\r)/gm,"");
		word = word.replace(/\s/g,"");//remove white space
		console.log(word);
		if (word.length>1){
			if (word.charAt(word.length-1) == "." || word.charAt(word.length-1) == "," || word.charAt(word.length-1) == "!" || word.charAt(word.length-1) == "?" || word.charAt(word.length-1) == ":" || word.charAt(word.length-1) == ";" || word.charAt(word.length-1) == ")"){
				//console.log("Found . , ? ! : ; in "+word);
				finalWords[i] = word.substr(0,word.length-1);
			}
			if(word.charAt(0) == "("){
				finalWords[i] = word.substr(1,word.length);
			}
		}
		finalWords[i] = finalWords[i].toLowerCase();
		if(finalWords[i].length>0 &&  finalWords[i]!="-"){
			finalWordsTemp.push(finalWords[i]);
		}
		else{
			console.log("ZERO LENGTH");
		}
		
	}
	finalWords = finalWordsTemp;
	//console.log(finalWords);
	
	//put counts in dict
	for (i=0; i<finalWords.length; i++){
		var hf = false;
		for (w=0;w<highFreq.length;w++){
			if (highFreq[w] == finalWords[i]){
				hf=true;
				}
			}
		if (hf==false){
			if (user[finalWords[i]] == undefined){
				user[finalWords[i]] = 1;
			}
			else{
				user[finalWords[i]] += 1;
			}
		}
	}
	//divide counts by total
	var total = 0;
	for (var word in user) {
		total += user[word];
	}
	for (var word in user){
		user[word] = user[word]/total;
	}
	
	return user;
}


//Make a version of the input with the unused parts in gray
var grayOutIgnored = function(userText,userDict){
	RegExp.quote = function(str) {
		 return str.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
	 };
	RegExp.unquote = function(str) {
		 return str.replace(/\\([.?*+^$[\]\\(){}|-])/g, "$1");
	 };
	var userText = RegExp.quote(userText.toLowerCase());
	for(var key in userDict){
		var regex = new RegExp(key, "g");
		userText=userText.replace(regex, "<span style='color:black'>"+key+"</span>");
	}
 
	return "<span style='color:#FFCC99'>"+RegExp.unquote(userText)+"</span>";
} 
 
 
 

//compare vector with python-generated dictionaries in supplements.js
function categorize(input, option1, option2){
	//Find all the words in all the dictionaries, so each dict can be filled out for all words
	var allWords = $.extend({},input, option1, option2);
	//console.log("input: "+Object.keys(input).length);
	//console.log("option1: "+Object.keys(option1).length);
	//console.log("option2: "+Object.keys(option2).length);
	//console.log("allWords: "+Object.keys(allWords).length);
	//console.log("---");
	
	//make vectors with counts for all words`
	var vectorInput = [];
	var vectorOption1 = [];
	var vectorOption2 = [];
	for(var key in allWords) {
		//console.log("input key-val: "+key+"-"+input[key]);
		//console.log("option1 key-val: "+key+"-"+option1[key]);
		//console.log("option2 key-val: "+key+"-"+option2[key]);
		if (input[key]>=0){
			vectorInput.push(input[key]);
		}
		else if (input[key]==undefined){
			vectorInput.push(0);
		}
		if (option1[key]>=0){
			vectorOption1.push(option1[key]);
		}
		else if (option1[key]==undefined){
			vectorOption1.push(0);
		}		
		if (option2[key]>=0){
			vectorOption2.push(option2[key]);
		}
		else if (option2[key]==undefined){
			vectorOption2.push(0);
		}		
	}
	//console.log("input: "+vectorInput.length);
	//console.log("       "+vectorInput);
	//console.log("Option1: "+vectorOption1.length);
	//console.log("         "+vectorOption1);
	//console.log("Option2: "+vectorOption2.length);
	//console.log("         "+vectorOption2);
	
	//calculate cos
	var cos1 = math.dot(vectorOption1,vectorInput)/(math.norm(vectorOption1)*math.norm(vectorInput));
    var cos2 = math.dot(vectorOption2,vectorInput)/(math.norm(vectorOption2)*math.norm(vectorInput));
	
	
   //make output
	var winnerString = "";
    if (cos1 > cos2){
		winnerString += "<p><b>Your text most matches Kirk!</b></p>";
	}
	else if(cos1 < cos2){
		winnerString += "<p><b>Your text most matches Spock!</b></p>";
	}
	else{
		winnerString += "<p><b>It's a tie!</b></p>";
	}

	winnerString += "<p>Kirk's cos = "+cos1+"<p>";
	winnerString += "<p>Spock's cos = "+cos2+"<p>";
	winnerString += "<p>Biggest cosine / smallest angle wins<p><br/>";
	
	var counter = 0;
	winnerString +="<table>";//add borders to hd, td...
	winnerString +="<tr><th>Word</th><th>Kirk</th><th>you</th><th>Spock</th></tr>";
	for (var word in allWords){
		winnerString +="<tr>";
		winnerString += "<td >"+word+"</td>";
		winnerString += "<td style='padding:5px;text-align:center;'>"+Math.round(vectorOption1[counter]*10000)/10000+"</td>";
		winnerString += "<td style='padding:5px;text-align:center;'>"+Math.round(vectorInput[counter]*10000)/10000+"</td>";
		winnerString += "<td style='padding:5px;text-align:center;'>"+Math.round(vectorOption2[counter]*10000)/10000+"</td>";
		winnerString +="</tr>";
		counter +=1;
	}
	winnerString +="</table>";
	
	//make output div visible
	document.getElementById("inoutput").style.visibility = "visible";
	
	return winnerString; 
}


//Give results
function returnResults(){
	var userTxt = document.getElementById("input").value;
	var input = popDictJS(userTxt);
	document.getElementById("output").innerHTML = categorize(input, dictKirk, dictSpock);
	//document.getElementById("output").innerHTML = categorize(input, dictTest1, dictTest2);
	document.getElementById("inputAgain").innerHTML = userTxt;//grayOutIgnored(userTxt,input);
}
