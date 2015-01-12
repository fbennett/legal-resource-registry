var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();

var citation_segments = [
    "case_name",
    "docket_number",
    "federal_cite_one",
    "federal_cite_three",
    "federal_cite_two",
    "lexis_cite",
    "neutral_cite",
    "resource_uri",
    "scotus_early_cite",
    "specialty_cite_one",
    "state_cite_one",
    "state_cite_regional",
    "state_cite_three",
    "state_cite_two",
    "westlaw_cite"
]

// Okay. Get all short titles. Can we do that?

var citation_string = citation_segments.join('__')

//var url = "/api/rest/v2/document/2766124/?fields=citation,docket,court,date_filed,date_modified"
//var url = "/api/rest/v2/document/138330/?fields=citation,docket,court,date_filed,date_modified"
//var url = "/api/rest/v2/document/138330/?fields=citation__" + citation_string;

//var url = "/api/rest/v2/document/138330/?fields=date_filed,citation__resource_uri";
var url = "/api/rest/v2/document/138330/";

function getAPI (key) {
    var url = 'https://www.courtlistener.com' + key;
    console.log("\nCalling ... " + url);
    xhr.open('GET', url, false);
    authstr = 'Basic ' + new Buffer('fbennett:Lnosiatl').toString('base64');
    //console.log("authstr: " + authstr);
    xhr.setRequestHeader('Authorization', authstr);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(null);
    console.log('Status: ' + xhr.status)
    return xhr.responseText;
}

var txt = getAPI(url);
var obj = JSON.parse(txt)
console.log(JSON.stringify(obj, null, 2))

var citation = obj.citation.resource_uri;
txt = getAPI(citation)
obj = JSON.parse(txt)
console.log(JSON.stringify(obj, null, 2))



/*
var court = obj.court;
var docket = obj.docket;

txt = getAPI(court)
obj = JSON.parse(txt)
console.log(JSON.stringify(obj, null, 2))

txt = getAPI(docket)
obj = JSON.parse(txt)
console.log(JSON.stringify(obj, null, 2))
*/
